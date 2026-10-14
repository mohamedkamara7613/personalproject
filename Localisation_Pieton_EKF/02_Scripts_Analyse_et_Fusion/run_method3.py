import sys
import numpy as np
import pandas as pd
import folium
import xml.etree.ElementTree as ET
from pathlib import Path

from ekf import EKF

G = 9.80665

def latlon_to_m(lat, lon, ref_lat, ref_lon):
    north = (lat - ref_lat) * 111_320
    east  = (lon - ref_lon) * 111_320 * np.cos(np.radians(ref_lat))
    return north, east

def m_to_latlon(north, east, ref_lat, ref_lon):
    lat = ref_lat + north / 111_320
    lon = ref_lon + east / (111_320 * np.cos(np.radians(ref_lat)))
    return lat, lon

def parse_gpx(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}
    points = []
    for trkpt in root.findall('.//gpx:trkpt', ns):
        lat = float(trkpt.get('lat'))
        lon = float(trkpt.get('lon'))
        points.append((lat, lon))
    return points

def main():
    print("--- Démarrage Méthode 3 (EKF Standard avec Init Yaw) ---")
    
    gps = pd.read_csv("gps_data.csv")
    imu = pd.read_csv("imu_data.csv")
    
    # Nettoyage
    gps = gps[(gps.Latitude < 90) & (gps.Longitude < 180)].copy()
    for col in ["Latitude", "Longitude"]:
        Q1, Q3 = gps[col].quantile(0.25), gps[col].quantile(0.75)
        iqr = Q3 - Q1
        gps = gps[(gps[col] >= Q1 - 1.5*iqr) & (gps[col] <= Q3 + 1.5*iqr)]
    gps = gps[gps.Timestamp > gps.Timestamp.iloc[0] + 15].reset_index(drop=True)
    
    t_start = gps.Timestamp.iloc[0]
    t_end = gps.Timestamp.iloc[-1]
    imu = imu[(imu.Timestamp >= t_start) & (imu.Timestamp <= t_end)].reset_index(drop=True)
    
    ref_lat = gps.Latitude.iloc[0]
    ref_lon = gps.Longitude.iloc[0]
    
    # Init Roulis (Roll) et Tangage (Pitch) avec l'accéléromètre
    accel_init = imu[['Accel X', 'Accel Y', 'Accel Z']].iloc[:50].mean().values * G
    ax, ay, az = accel_init
    
    # Calcul de phi (Roulis) et theta (Tangage)
    theta_init = np.arcsin(np.clip(-ax / G, -1.0, 1.0))
    phi_init = np.arctan2(ay, az)
    
    # Init Lacet (Yaw) avec le GPS (On prend les points 0 et 2 par exemple pour avoir un bon vecteur)
    if len(gps) > 2:
        n0, e0 = latlon_to_m(gps.Latitude.iloc[0], gps.Longitude.iloc[0], ref_lat, ref_lon)
        n2, e2 = latlon_to_m(gps.Latitude.iloc[2], gps.Longitude.iloc[2], ref_lat, ref_lon)
        dy = n2 - n0
        dx = e2 - e0
        psi_init = np.arctan2(dy, dx)
    else:
        psi_init = 0.0
        
    print(f"Init Angles (deg) -> Roll: {np.degrees(phi_init):.1f}, Pitch: {np.degrees(theta_init):.1f}, Yaw: {np.degrees(psi_init):.1f}")
    
    # Biais Gyroscope (calibration initiale)
    gyro_bias = imu[['Gyro X', 'Gyro Y', 'Gyro Z']].iloc[:50].mean().values
    
    # Vecteur d'état X = [x, y, vx, vy, phi, theta, psi]
    init_X = [0.0, 0.0, 0.0, 0.0, phi_init, theta_init, psi_init]
    
    # Instance EKF
    ekf = EKF(
        init_X=init_X,
        var_acc=0.5,     # Bruit accélération
        var_gyro=0.1,    # Bruit gyro
        var_gps=1.20     # Bruit GPS
    )
    
    t_imu = imu.Timestamp.values
    accels = imu[['Accel X', 'Accel Y', 'Accel Z']].values
    gyros = imu[['Gyro X', 'Gyro Y', 'Gyro Z']].values
    
    t_gps = gps.Timestamp.values
    gps_lat = gps.Latitude.values
    gps_lon = gps.Longitude.values
    
    kalman_coords = []
    gps_idx = 1
    
    for i in range(1, len(imu)):
        dt = t_imu[i] - t_imu[i-1]
        if dt <= 0: continue
            
        acc_ms2 = accels[i] * G
        w_rads = np.radians(gyros[i] - gyro_bias)
        u = np.concatenate([acc_ms2, w_rads])
        
        # 1. Prediction EKF
        ekf.predict(u, dt)
        
        # 2. Correction GPS
        while gps_idx < len(gps) and t_gps[gps_idx] <= t_imu[i]:
            n, e = latlon_to_m(gps_lat[gps_idx], gps_lon[gps_idx], ref_lat, ref_lon)
            ekf.update_gps([e, n]) # e=x, n=y
            gps_idx += 1
            
        if i % 10 == 0:
            lat_k, lon_k = m_to_latlon(ekf.X[1], ekf.X[0], ref_lat, ref_lon)
            kalman_coords.append((lat_k, lon_k))

    print("Trajectoire Méthode 3 calculée.")
    
    m = folium.Map(location=[ref_lat, ref_lon], zoom_start=18, tiles="OpenStreetMap")
    
    strava_path = "strava_ground_truth.gpx"
    if Path(strava_path).exists():
        try:
            strava_pts = parse_gpx(strava_path)
            folium.PolyLine(strava_pts, color="black", weight=4, opacity=0.8, tooltip="Strava (Vérité Terrain)").add_to(m)
        except Exception as e:
            print(f"Erreur GPX: {e}")
            
    gps_pts = list(zip(gps.Latitude, gps.Longitude))
    folium.PolyLine(gps_pts, color="red", weight=2, opacity=0.6, tooltip="GPS Filtré").add_to(m)
    folium.PolyLine(kalman_coords, color="orange", weight=3, opacity=1.0, tooltip="EKF (Méthode 3)").add_to(m)
    
    out_map = "methode3_map.html"
    m.save(out_map)
    print(f"Carte générée : {out_map}")

if __name__ == "__main__":
    main()
