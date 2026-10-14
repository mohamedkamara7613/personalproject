import sys
import numpy as np
import pandas as pd
import folium
import xml.etree.ElementTree as ET
from pathlib import Path

# Importer le kalman linéaire existant
from kalman import KalmanFilter

G = 9.80665

def latlon_to_m(lat, lon, ref_lat, ref_lon):
    north = (lat - ref_lat) * 111_320
    east  = (lon - ref_lon) * 111_320 * np.cos(np.radians(ref_lat))
    return north, east

def m_to_latlon(north, east, ref_lat, ref_lon):
    lat = ref_lat + north / 111_320
    lon = ref_lon + east / (111_320 * np.cos(np.radians(ref_lat)))
    return lat, lon

# Mathématiques des Quaternions
def quat_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

def quat_inv(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])

def rotate_vector(q, v):
    q_v = np.array([0, v[0], v[1], v[2]])
    res = quat_mult(quat_mult(q, q_v), quat_inv(q))
    return res[1:]

def initial_quaternion_from_accel(accel_mean):
    """Calcule un quaternion initial tel que l'axe accel_mean devienne [0, 0, 1]"""
    a = accel_mean / np.linalg.norm(accel_mean)
    up = np.array([0, 0, 1])
    axis = np.cross(a, up)
    sin_theta = np.linalg.norm(axis)
    cos_theta = np.dot(a, up)
    
    if sin_theta < 1e-6:
        if cos_theta > 0: return np.array([1, 0, 0, 0])
        else: return np.array([0, 1, 0, 0]) # 180 deg rot
    
    axis = axis / sin_theta
    theta = np.arctan2(sin_theta, cos_theta)
    
    q = np.array([
        np.cos(theta / 2.0),
        axis[0] * np.sin(theta / 2.0),
        axis[1] * np.sin(theta / 2.0),
        axis[2] * np.sin(theta / 2.0)
    ])
    return q / np.linalg.norm(q)

def integrate_gyro(q, gyro, dt):
    """gyro en rad/s"""
    norm_w = np.linalg.norm(gyro)
    if norm_w < 1e-6:
        return q
    theta = norm_w * dt
    axis = gyro / norm_w
    dq = np.array([
        np.cos(theta / 2.0),
        axis[0] * np.sin(theta / 2.0),
        axis[1] * np.sin(theta / 2.0),
        axis[2] * np.sin(theta / 2.0)
    ])
    new_q = quat_mult(q, dq)
    return new_q / np.linalg.norm(new_q)

def parse_gpx(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    # Espace de nom GPX
    ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}
    points = []
    for trkpt in root.findall('.//gpx:trkpt', ns):
        lat = float(trkpt.get('lat'))
        lon = float(trkpt.get('lon'))
        points.append((lat, lon))
    return points

def main():
    print("--- Démarrage Méthode 1 (Pré-Rotation + Kalman Linéaire) ---")
    
    # 1. Chargement
    gps = pd.read_csv("gps_data.csv")
    imu = pd.read_csv("imu_data.csv")
    
    # Filtre de base GPS (comme l'équipe)
    gps = gps[(gps.Latitude < 90) & (gps.Longitude < 180)].copy()
    for col in ["Latitude", "Longitude"]:
        Q1, Q3 = gps[col].quantile(0.25), gps[col].quantile(0.75)
        iqr = Q3 - Q1
        gps = gps[(gps[col] >= Q1 - 1.5*iqr) & (gps[col] <= Q3 + 1.5*iqr)]
    gps = gps[gps.Timestamp > gps.Timestamp.iloc[0] + 15].reset_index(drop=True)
    
    # Restreindre l'IMU à la période GPS
    t_start = gps.Timestamp.iloc[0]
    t_end = gps.Timestamp.iloc[-1]
    imu = imu[(imu.Timestamp >= t_start) & (imu.Timestamp <= t_end)].reset_index(drop=True)
    
    ref_lat = gps.Latitude.iloc[0]
    ref_lon = gps.Longitude.iloc[0]
    
    # 2. Initialisation Attitude
    # Prendre les 50 premiers points IMU pour l'accel initiale
    accel_init = imu[['Accel X', 'Accel Y', 'Accel Z']].iloc[:50].mean().values
    q_attitude = initial_quaternion_from_accel(accel_init)
    
    # Biais Gyro (calcul sur les 50 premiers points si on suppose qu'il est statique)
    gyro_bias = imu[['Gyro X', 'Gyro Y', 'Gyro Z']].iloc[:50].mean().values
    
    # 3. Initialisation Kalman
    # On utilise var_accel faible car on injecte a_lin pure
    kf = KalmanFilter(initial_x=0.0, initial_y=0.0, var_accel=0.1, var_gps=1.20)
    
    t_imu = imu.Timestamp.values
    accels = imu[['Accel X', 'Accel Y', 'Accel Z']].values
    gyros = imu[['Gyro X', 'Gyro Y', 'Gyro Z']].values
    
    t_gps = gps.Timestamp.values
    gps_lat = gps.Latitude.values
    gps_lon = gps.Longitude.values
    
    kalman_coords = []
    gps_idx = 1 # GPS 0 utilisé pour init
    
    for i in range(1, len(imu)):
        dt = t_imu[i] - t_imu[i-1]
        if dt <= 0: continue
            
        # Conversion gyro en rad/s (apparemment en deg/s dans le CSV)
        w = np.radians(gyros[i] - gyro_bias)
        
        # Mise à jour orientation
        q_attitude = integrate_gyro(q_attitude, w, dt)
        
        # Rotation de l'accélération
        a_body = accels[i] # en g
        a_nav = rotate_vector(q_attitude, a_body)
        
        # Soustraction gravité (a_nav doit être [0, 0, 1] si au repos)
        a_lin = a_nav - np.array([0.0, 0.0, 1.0])
        a_lin_ms2 = a_lin * G
        
        # Prédiction Kalman (East = X, North = Y)
        # On peut assigner arbitrairement X_nav à East et Y_nav à North
        ax_east = a_lin_ms2[0]
        ay_north = a_lin_ms2[1]
        
        kf.predict(ax_east, ay_north, dt)
        
        # Vérifier si on a un GPS à intégrer
        while gps_idx < len(gps) and t_gps[gps_idx] <= t_imu[i]:
            n, e = latlon_to_m(gps_lat[gps_idx], gps_lon[gps_idx], ref_lat, ref_lon)
            # update kalman (x=East, y=North)
            kf.update(e, n)
            gps_idx += 1
            
        # Stockage de la position (tous les 10 points IMU pour alléger)
        if i % 10 == 0:
            state = kf.get_state()
            lat_k, lon_k = m_to_latlon(state["y"], state["x"], ref_lat, ref_lon)
            kalman_coords.append((lat_k, lon_k))

    print("Trajectoire Méthode 1 calculée.")
    
    # 4. Traçage Folium
    m = folium.Map(location=[ref_lat, ref_lon], zoom_start=18, tiles="OpenStreetMap")
    
    # Strava (Vérité terrain)
    strava_path = "strava_ground_truth.gpx"
    if Path(strava_path).exists():
        try:
            strava_pts = parse_gpx(strava_path)
            folium.PolyLine(strava_pts, color="black", weight=4, opacity=0.8, tooltip="Strava (Vérité Terrain)").add_to(m)
        except Exception as e:
            print(f"Erreur GPX: {e}")
    else:
        print("Fichier Strava non trouvé.")
        
    # GPS filtré
    gps_pts = list(zip(gps.Latitude, gps.Longitude))
    folium.PolyLine(gps_pts, color="red", weight=2, opacity=0.6, tooltip="GPS Filtré").add_to(m)
    
    # Kalman Méthode 1
    folium.PolyLine(kalman_coords, color="blue", weight=3, opacity=1.0, tooltip="Kalman Méthode 1 (Pré-Rot)").add_to(m)
    
    out_map = "methode1_map.html"
    m.save(out_map)
    print(f"Carte générée : {out_map}")

if __name__ == "__main__":
    main()
