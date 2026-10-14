import pandas as pd
import numpy as np
import math
import folium
import sys
sys.path.append("/home/mkamara/Bureau/repos/pi_itineraire_26_28/code/Code_fusion")
from core.gps_utils import gps_to_local_meters, local_meters_to_gps

# --- Mathématiques des Quaternions ---
def quat_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

def quat_conjugate(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])

def rotate_vector(v, q):
    """Tourne un vecteur 3D v par le quaternion q"""
    q_v = np.array([0, v[0], v[1], v[2]])
    q_res = quat_mult(quat_mult(q, q_v), quat_conjugate(q))
    return q_res[1:4]

# --- Filtre Mahony (Orientation 3D) ---
class MahonyFilter:
    def __init__(self, kp=2.0, ki=0.0):
        self.q = np.array([1.0, 0.0, 0.0, 0.0]) # [w, x, y, z]
        self.kp = kp
        self.ki = ki
        self.eInt = np.array([0.0, 0.0, 0.0])
        
    def update(self, a, w, dt):
        """ a: accel [x, y, z], w: gyro [x, y, z] en rad/s """
        # Normalisation de l'accélération
        a_norm = np.linalg.norm(a)
        if a_norm == 0: return self.q
        a = a / a_norm

        # Direction estimée de la gravité (basée sur le quaternion actuel)
        # La gravité terrestre dans le repère global ENU est [0, 0, 1] (vers le haut en accélération)
        # Dans le repère capteur, c'est la rotation inverse de [0, 0, 1]
        v = np.array([
            2.0 * (self.q[1]*self.q[3] - self.q[0]*self.q[2]),
            2.0 * (self.q[0]*self.q[1] + self.q[2]*self.q[3]),
            self.q[0]**2 - self.q[1]**2 - self.q[2]**2 + self.q[3]**2
        ])
        
        # Erreur : produit vectoriel entre la gravité estimée et l'accélération mesurée
        e = np.cross(a, v)
        
        if self.ki > 0:
            self.eInt += e * dt
        else:
            self.eInt = np.array([0.0, 0.0, 0.0])
            
        # Correction du gyroscope
        w = w + self.kp * e + self.ki * self.eInt
        
        # Intégration du quaternion (dérivée q_dot = 0.5 * q * w)
        q_dot = 0.5 * quat_mult(self.q, np.array([0, w[0], w[1], w[2]]))
        self.q += q_dot * dt
        self.q /= np.linalg.norm(self.q)
        return self.q

# --- Filtre de Kalman Linéaire (Position 2D) ---
class LinearKalmanFilter:
    def __init__(self, x0, y0):
        # État : [x, y, vx, vy]
        self.X = np.array([[x0], [y0], [0.0], [0.0]])
        self.P = np.eye(4) * 100.0 # Incertitude initiale plus forte
        self.H = np.eye(4) # On observe tout : x, y, vx, vy
        
        # Bruit de mesure GPS (R)
        self.R = np.array([
            [2.0**2, 0, 0, 0],
            [0, 2.0**2, 0, 0],
            [0, 0, 1.0**2, 0], # Bruit sur la vitesse GPS
            [0, 0, 0, 1.0**2]
        ])
        self.var_a = 5.0**2 # Bruit de modèle énorme pour forcer la confiance au GPS

    def predict(self, a_x, a_y, dt):
        # Matrices F et B
        F = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1, 0 ],
            [0, 0, 0, 1 ]
        ])
        B = np.array([
            [0.5 * dt**2, 0],
            [0, 0.5 * dt**2],
            [dt, 0],
            [0, dt]
        ])
        U = np.array([[a_x], [a_y]])
        
        # Q matrix
        Q = self.var_a * (B @ B.T)
        
        self.X = F @ self.X + B @ U
        self.P = F @ self.P @ F.T + Q

    def update(self, gps_x, gps_y, gps_vx, gps_vy):
        Z = np.array([[gps_x], [gps_y], [gps_vx], [gps_vy]])
        Y = Z - (self.H @ self.X)
        S = self.H @ self.P @ self.H.T + self.R
            
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.X = self.X + K @ Y
        self.P = (np.eye(4) - K @ self.H) @ self.P
        return True


def main():
    base_dir = "/home/mkamara/Bureau/INSA_ROUEN_Noramandie/PI/Iteneraire/Acquisition1_20_05/Acquisition_Code_fusion/"
    print("Chargement des données...")
    df_gps = pd.read_csv(base_dir + 'gps_data.csv')
    df_imu = pd.read_csv(base_dir + 'imu_data.csv')

    # Filtrage et tri
    df_gps = df_gps[(df_gps['Latitude'] >= -90) & (df_gps['Latitude'] <= 90)]
    df_gps['Type'] = 'GPS'
    df_imu['Type'] = 'IMU'
    
    df_all = pd.concat([df_gps, df_imu]).sort_values('Timestamp').reset_index(drop=True)

    origin_lat = df_gps['Latitude'].iloc[0]
    origin_lon = df_gps['Longitude'].iloc[0]

    mahony = MahonyFilter(kp=2.0)
    ekf = LinearKalmanFilter(0.0, 0.0)

    last_imu_time = None
    last_gps_time = None
    last_gps_pos = None
    trajectoire_ekf = []
    points_rejetes = []
    
    # Compteur pour laisser le filtre Mahony converger
    imu_count = 0
    
    print("Début de la fusion 3D...")
    for idx, row in df_all.iterrows():
        t = row['Timestamp']
        
        if row['Type'] == 'IMU':
            if last_imu_time is None:
                last_imu_time = t
                continue
                
            dt = t - last_imu_time
            last_imu_time = t
            
            # Lecture (g à l'accéléromètre correspond à environ 1g ~ 9.81 m/s²)
            # Nos données d'accélération semblent être en g (car Accel X ~ 1.0 au repos)
            # On les convertit en m/s²
            g = 9.80665
            a_raw = np.array([row['Accel X']*g, row['Accel Y']*g, row['Accel Z']*g])
            w_raw = np.array([row['Gyro X'], row['Gyro Y'], row['Gyro Z']]) # en rad/s
            
            # Mise à jour de l'orientation 3D
            q = mahony.update(a_raw, w_raw, dt)
            
            imu_count += 1
            if imu_count < 200:
                # On attend 2 secondes pour que le filtre d'orientation converge vers la verticale
                continue
            
            # Rotation de l'accélération dans le repère global ENU
            a_global = rotate_vector(a_raw, q)
            
            # Soustraction de la gravité (qui pointe vers +Z dans ce repère)
            a_global[2] -= g
            
            # Projection 2D et prédiction EKF
            # Note: Si le capteur a son axe X vers l'avant et Y vers la gauche (repère classique)
            # a_global[0] = North, a_global[1] = East
            a_est = a_global[1]
            a_nord = a_global[0]
            
            ekf.predict(a_est, a_nord, dt)
            
            # Sauvegarde périodique
            if np.random.rand() < 0.05: # Sauvegarder ~5 points par seconde
                lat, lon = local_meters_to_gps(ekf.X[0,0], ekf.X[1,0], origin_lat, origin_lon)
                trajectoire_ekf.append([lat, lon])

        elif row['Type'] == 'GPS':
            gps_x, gps_y = gps_to_local_meters(row['Latitude'], row['Longitude'], origin_lat, origin_lon)
            
            # Calcul de la vitesse GPS
            if last_gps_pos is None:
                gps_vx, gps_vy = 0.0, 0.0
            else:
                dt_gps = t - last_gps_time
                if dt_gps > 0:
                    gps_vx = (gps_x - last_gps_pos[0]) / dt_gps
                    gps_vy = (gps_y - last_gps_pos[1]) / dt_gps
                else:
                    gps_vx, gps_vy = 0.0, 0.0
                    
            last_gps_pos = (gps_x, gps_y)
            last_gps_time = t

            accepted = ekf.update(gps_x, gps_y, gps_vx, gps_vy)
            if not accepted:
                points_rejetes.append([row['Latitude'], row['Longitude']])

    print(f"Fusion terminée. {len(points_rejetes)} points GPS rejetés.")
    
    # --- Affichage ---
    print("Génération de la carte map_3d.html...")
    m = folium.Map(location=[origin_lat, origin_lon], zoom_start=18)
    
    # Légende
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 250px; height: auto; 
                border:2px solid grey; z-index:9999; font-size:14px; background-color: white; padding: 10px;">
        <b>EKF 3D (Quaternions)</b><br>
        <i style="color:red;">●</i> GPS Brut<br>
        <i style="color:orange;">●</i> GPS Rejeté<br>
        <i style="color:purple;">▬</i> Trajectoire EKF 3D
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # GPS Brut
    for idx, row in df_gps.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=2, color='red', fill=True
        ).add_to(m)
        
    # Rejetés
    for pt in points_rejetes:
        folium.CircleMarker(
            location=[pt[0], pt[1]],
            radius=4, color='orange', fill=True
        ).add_to(m)

    # Ligne EKF
    folium.PolyLine(
        trajectoire_ekf, color='purple', weight=4, opacity=0.8
    ).add_to(m)

    m.save(base_dir + 'map_3d.html')
    print("Carte enregistrée avec succès !")

if __name__ == '__main__':
    main()
