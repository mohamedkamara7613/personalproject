import sys
import numpy as np
import pandas as pd
import folium
import xml.etree.ElementTree as ET
from pathlib import Path

from eskf import ESKF

# Redéfinition car pas mise dans eskf.py
def matrix_to_quat(R):
    m00, m01, m02 = R[0,0], R[0,1], R[0,2]
    m10, m11, m12 = R[1,0], R[1,1], R[1,2]
    m20, m21, m22 = R[2,0], R[2,1], R[2,2]
    tr = m00 + m11 + m22
    if tr > 0:
        S = np.sqrt(tr + 1.0) * 2
        w = 0.25 * S
        x = (m21 - m12) / S
        y = (m02 - m20) / S
        z = (m10 - m01) / S
    elif (m00 > m11) and (m00 > m22):
        S = np.sqrt(1.0 + m00 - m11 - m22) * 2
        w = (m21 - m12) / S
        x = 0.25 * S
        y = (m01 + m10) / S
        z = (m02 + m20) / S
    elif m11 > m22:
        S = np.sqrt(1.0 + m11 - m00 - m22) * 2
        w = (m02 - m20) / S
        x = (m01 + m10) / S
        y = 0.25 * S
        z = (m12 + m21) / S
    else:
        S = np.sqrt(1.0 + m22 - m00 - m11) * 2
        w = (m10 - m01) / S
        x = (m02 + m20) / S
        y = (m12 + m21) / S
        z = 0.25 * S
    q = np.array([w, x, y, z])
    return q / np.linalg.norm(q)

def initial_quaternion(accel_mean, yaw_gps):
    """
    On sait que l'axe X de l'IMU vaut ~1g, donc X pointe vers le HAUT (Up).
    On sait que l'axe Y a la plus grande variance, donc Y pointe vers l'AVANT (Forward).
    """
    # X_body pointe vers UP
    U = accel_mean / np.linalg.norm(accel_mean)
    
    # Le vecteur Forward (Y_body) doit pointer vers yaw_gps dans le plan horizontal
    F = np.array([np.cos(yaw_gps), np.sin(yaw_gps), 0.0])
    
    # Projeter F pour qu'il soit orthogonal à U (Up)
    Y_body = F - np.dot(F, U) * U
    if np.linalg.norm(Y_body) < 1e-6:
        Y_body = np.array([0.0, 1.0, 0.0]) # fallback
    Y_body = Y_body / np.linalg.norm(Y_body)
    
    # Z_body doit être orthogonal à X et Y (Z = X cross Y)
    Z_body = np.cross(U, Y_body)
    Z_body = Z_body / np.linalg.norm(Z_body)
    
    # La matrice de rotation R a pour colonnes X_body, Y_body, Z_body exprimés dans le repère Nav
    R = np.column_stack((U, Y_body, Z_body))
    return matrix_to_quat(R)


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
    print("--- Démarrage Méthode 2 (ESKF - Error State Kalman Filter) ---")
    
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
    
    # Init
    # Init Yaw avec le GPS
    yaw_gps = 0.0
    if len(gps) > 2:
        n0, e0 = latlon_to_m(gps.Latitude.iloc[0], gps.Longitude.iloc[0], ref_lat, ref_lon)
        n2, e2 = latlon_to_m(gps.Latitude.iloc[2], gps.Longitude.iloc[2], ref_lat, ref_lon)
        yaw_gps = np.arctan2(n2 - n0, e2 - e0)
        
    accel_init = imu[['Accel X', 'Accel Y', 'Accel Z']].iloc[:50].mean().values
    q_init = initial_quaternion(accel_init, yaw_gps)
    gyro_bias = imu[['Gyro X', 'Gyro Y', 'Gyro Z']].iloc[:50].mean().values
    
    # Instance ESKF
    eskf = ESKF(
        init_p=[0.0, 0.0, 0.0],
        init_v=[0.0, 0.0, 0.0],
        init_q=q_init,
        var_acc=0.5,     # Bruit accéléromètre
        var_gyro=0.1,    # Bruit gyroscope
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
        
        # 1. Prediction ESKF
        eskf.predict(acc_ms2, w_rads, dt)
        
        # 2. Correction GPS
        while gps_idx < len(gps) and t_gps[gps_idx] <= t_imu[i]:
            n, e = latlon_to_m(gps_lat[gps_idx], gps_lon[gps_idx], ref_lat, ref_lon)
            eskf.update_gps([e, n])
            gps_idx += 1
            
        if i % 10 == 0:
            lat_k, lon_k = m_to_latlon(eskf.p[1], eskf.p[0], ref_lat, ref_lon)
            kalman_coords.append((lat_k, lon_k))

    print("Trajectoire Méthode 2 calculée.")
    
    m = folium.Map(location=[ref_lat, ref_lon], zoom_start=18, tiles="CartoDB voyager")
    
    strava_path = "strava_ground_truth.gpx"
    if Path(strava_path).exists():
        try:
            strava_pts = parse_gpx(strava_path)
            folium.PolyLine(strava_pts, color="black", weight=4, opacity=0.8, tooltip="Strava (Vérité Terrain)").add_to(m)
        except Exception as e:
            print(f"Erreur GPX: {e}")
            
    gps_pts = list(zip(gps.Latitude, gps.Longitude))
    folium.PolyLine(gps_pts, color="red", weight=2, opacity=0.6, tooltip="GPS Filtré").add_to(m)
    folium.PolyLine(kalman_coords, color="green", weight=3, opacity=1.0, tooltip="ESKF (Méthode 2)").add_to(m)
    
    out_map = "methode2_map.html"
    m.save(out_map)
    print(f"Carte générée : {out_map}")

if __name__ == "__main__":
    main()
