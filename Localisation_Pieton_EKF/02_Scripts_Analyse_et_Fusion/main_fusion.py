import numpy as np
import os
import folium
from kalman import KalmanFilter
from gps_utils import read_gps_csv, local_meters_to_gps

def read_imu_csv(file_path):
    """
    Lit le fichier IMU.
    Retourne une liste de tuples: (timestamp, ax, ay)
    """
    import csv
    data = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if not row: continue
            data.append((float(row[0]), float(row[1]), float(row[2])))
    return data

def generate_mock_imu(gps_data):
    """
    Génère de fausses données IMU (accélération = 0) entre les points GPS,
    uniquement pour tester l'algorithme en attendant les vraies données.
    Fréquence simulée : 100 Hz.
    """
    print("---> Fichier IMU introuvable. Génération de données IMU simulées (accélérations nulles) à 100Hz...")
    mock_imu = []
    t_start = gps_data[0][0]
    t_end = gps_data[-1][0]
    
    t = t_start
    while t <= t_end:
        # Bruit très léger pour l'accélération
        ax = np.random.normal(0, 0.05)
        ay = np.random.normal(0, 0.05)
        mock_imu.append((t, ax, ay))
        t += 0.01 # 100 Hz
        
    return mock_imu

def main():
    gps_file = "calibrationGPS_beitou.csv"
    imu_file = "imu.csv"

    # Réglages pour Q et R
    var_accel = 0.1 # Incertitude IMU (Q
    var_gps = 5.0   # Incertitude GPS
    
    print("Chargement des données GPS...")
    gps_data, lat_origin, lon_origin = read_gps_csv(gps_file)
    
    if os.path.exists(imu_file):
        print("Chargement des données IMU...")
        imu_data = read_imu_csv(imu_file)
    else:
        imu_data = generate_mock_imu(gps_data)
        
    print("Synchronisation temporelle des capteurs...")
    events = []
    for d in gps_data:
        events.append({'time': d[0], 'type': 'GPS', 'x': d[1], 'y': d[2]})
        
    for d in imu_data:
        events.append({'time': d[0], 'type': 'IMU', 'ax': d[1], 'ay': d[2]})
        
    # On trie tous les événements chronologiquement, Priorité IMU
    events.sort(key=lambda e: (e['time'], 0 if e['type'] == 'IMU' else 1))
    
    # 3. Initialisation du Filtre de Kalman
    initial_x = gps_data[0][1]
    initial_y = gps_data[0][2]
    
    kf = KalmanFilter(initial_x, initial_y,  var_accel=var_accel, var_gps=var_gps, dt_imu=0.01)
    
    # Pour l'affichage final et l'export CSV
    kalman_trajectory_time = []
    kalman_trajectory_x = []
    kalman_trajectory_y = []
    
    gps_trajectory_x = [d[1] for d in gps_data]
    gps_trajectory_y = [d[2] for d in gps_data]
    
    # 4. BOUCLE PRINCIPALE
    print("Démarrage du Filtre de Kalman...")
    last_time = events[0]['time']
    
    for event in events:
        current_time = event['time']
        dt = current_time - last_time
        
        # dt > 0
        if dt <= 0.0001 and current_time != last_time: 
            dt = 0.0001
            
        if event['type'] == 'IMU':
            # Étape 1 : Prédiction
            if dt > 0:
                kf.predict(event['ax'], event['ay'], dt)
                last_time = current_time
                
        elif event['type'] == 'GPS':
            # Étape 2 : Mise à jour
            kf.update(event['x'], event['y'])
            # on va sauvegarde r la position estimée
            state = kf.get_state()
            kalman_trajectory_time.append(current_time)
            kalman_trajectory_x.append(state['x'])
            kalman_trajectory_y.append(state['y'])
            
            
    # 5. Sauvegarde des résultats en CSV (avec Lat/Lon en plus)
    import csv
    
    # Conversion des coordonnées Kalman (Mètres) en Lat/Lon mondiales
    kalman_trajectory_latlon = [
        local_meters_to_gps(x, y, lat_origin, lon_origin)
        for x, y in zip(kalman_trajectory_x, kalman_trajectory_y)
    ]
    
    output_csv = "trajectoire_fusionnee.csv"
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Position_X_m", "Position_Y_m", "Latitude", "Longitude"])
        for t, x, y, (lat, lon) in zip(kalman_trajectory_time, kalman_trajectory_x, kalman_trajectory_y, kalman_trajectory_latlon):
            writer.writerow([f"{t:.3f}", f"{x:.4f}", f"{y:.4f}", f"{lat:.8f}", f"{lon:.8f}"])
    print(f"Trajectoire fusionnée sauvegardée dans : {output_csv}")

    # 6. Affichage des résultats avec Folium (OpenStreetMap)
    print("Génération de la carte interactive Folium...")
    
    # Création de la carte centrée sur le point de départ
    m = folium.Map(location=[lat_origin, lon_origin], zoom_start=18)
    
    # Tracé des mesures GPS brutes (en rouge)
    # Les données GPS brutes sont reconverties pour l'affichage (ou on pourrait repasser le CSV brut)
    gps_trajectory_latlon = [
        local_meters_to_gps(x, y, lat_origin, lon_origin)
        for x, y in zip(gps_trajectory_x, gps_trajectory_y)
    ]
    folium.PolyLine(gps_trajectory_latlon, color="red", weight=2, opacity=0.5, tooltip="GPS Brut").add_to(m)
    
    # Tracé de l'estimation Kalman (en bleu)
    folium.PolyLine(kalman_trajectory_latlon, color="blue", weight=3, opacity=1.0, tooltip="Fusion Kalman").add_to(m)
    
    # Sauvegarde
    output_html = "trajectoire_fusionnee.html"
    m.save(output_html)
    print(f"Carte générée et sauvegardée dans : {output_html}")

if __name__ == "__main__":
    main()
