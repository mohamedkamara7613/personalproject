import argparse
import os
import numpy as np
import pandas as pd
import folium
import xml.etree.ElementTree as ET
import csv
from pathlib import Path
import sys

# Ajout du chemin pour importer utils (kalman, gps_utils)
sys.path.append("/home/mkamara/Bureau/INSA_ROUEN_Noramandie/PI/Iteneraire/02_Scripts_Analyse_et_Fusion")
try:
    from kalman import EKFSansMagneto
    from gps_utils import gps_to_local_meters, local_meters_to_gps
except ImportError:
    # Si exécuté depuis Final_Test
    sys.path.append("/home/mkamara/Bureau/INSA_ROUEN_Noramandie/PI/Iteneraire/Final_Test")
    from utils.kalman import EKFSansMagneto
    from utils.gps_utils import gps_to_local_meters, local_meters_to_gps

# -- Paramètres calibrés ------------------------------------------------------
SIGMA_A      = 0.8596   # m/s²
SIGMA_A_MIN  = 0.10     # m/s²
SIGMA_A_MAX  = 5.00     # m/s²
N_STATIC     = 200
G            = 9.80665

# -- Helpers ------------------------------------------------------------------
def parse_gpx(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        ns   = {'gpx': 'http://www.topografix.com/GPX/1/1'}
        return [(float(t.get('lat')), float(t.get('lon')))
                for t in root.findall('.//gpx:trkpt', ns)]
    except Exception as e:
        print(f"[Erreur lecture GPX] {e}")
        return []

def clean_gps(gps: pd.DataFrame) -> pd.DataFrame:
    if 'Latitude' not in gps.columns or 'Longitude' not in gps.columns:
        raise ValueError("Le fichier GPS doit contenir les colonnes 'Latitude' et 'Longitude'")
        
    gps = gps[(gps.Latitude >= -90) & (gps.Latitude <= 90) & 
              (gps.Longitude >= -180) & (gps.Longitude <= 180)].copy()
    for col in ["Latitude", "Longitude"]:
        Q1, Q3 = gps[col].quantile(0.25), gps[col].quantile(0.75)
        iqr    = Q3 - Q1
        gps    = gps[(gps[col] >= Q1 - 1.5*iqr) & (gps[col] <= Q3 + 1.5*iqr)]
    if len(gps) > 0:
        gps = gps[gps.Timestamp > gps.Timestamp.iloc[0] + 15].reset_index(drop=True)
    return gps

def load_imu(path, t_start, t_end):
    imu = pd.read_csv(path)
    if 'Gyro X' not in imu.columns or 'Accel Y' not in imu.columns or 'Accel Z' not in imu.columns:
        raise ValueError("Le fichier IMU doit contenir 'Gyro X', 'Accel Y', 'Accel Z'")
        
    gyro_x_bias = imu['Gyro X'].iloc[:N_STATIC].mean() if len(imu) > N_STATIC else 0.0
    bias_Y = imu['Accel Y'].iloc[:N_STATIC].mean() if len(imu) > N_STATIC else 0.0
    bias_Z = imu['Accel Z'].iloc[:N_STATIC].mean() if len(imu) > N_STATIC else 0.0

    imu = imu[(imu.Timestamp >= t_start) & (imu.Timestamp <= t_end)].reset_index(drop=True)
    return imu, gyro_x_bias, bias_Y, bias_Z

def compute_sigma_a(imu, gps_timestamps, bias_Y, bias_Z):
    t_imu   = imu.Timestamp.values
    aY      = (imu['Accel Y'].values - bias_Y) * G
    aZ      = (imu['Accel Z'].values - bias_Z) * G
    a_horiz = np.hypot(aY, aZ)

    sigma_arr = np.empty(len(gps_timestamps) - 1)
    for k in range(len(gps_timestamps) - 1):
        mask    = (t_imu >= gps_timestamps[k]) & (t_imu < gps_timestamps[k + 1])
        samples = a_horiz[mask]
        sigma_arr[k] = np.clip(np.sqrt(np.mean(samples**2)), SIGMA_A_MIN, SIGMA_A_MAX) if len(samples) > 0 else SIGMA_A
    return sigma_arr

def compute_omega(imu, gps_timestamps, gyro_x_bias):
    t_imu = imu.Timestamp.values
    gx    = np.radians(imu['Gyro X'].values - gyro_x_bias)
    omega_arr = np.empty(len(gps_timestamps) - 1)
    for k in range(len(gps_timestamps) - 1):
        mask    = (t_imu >= gps_timestamps[k]) & (t_imu < gps_timestamps[k + 1])
        samples = gx[mask]
        omega_arr[k] = np.mean(samples) if len(samples) > 0 else 0.0
    return omega_arr

# -- Main -------------------------------------------------------------------- -
def main():
    parser = argparse.ArgumentParser(description="Post-traitement EKF Piéton (V2: Gyro+GPS)")
    parser.add_argument(
        "--gps", 
        type=str,
        required=True, 
        help="Chemin vers le fichier contenant les données GPS (ex: gps_data.csv)"
    )
    parser.add_argument(
        "--imu", 
        type=str,
        required=True, 
        help="Chemin vers le fichier contenant les données IMU (ex: imu_data.csv)"
    )
    parser.add_argument(
        "--out-csv", 
        type=str,
        required=True, 
        help="Chemin de destination pour le CSV de fusion en sortie"
    )
    parser.add_argument(
        "--out-html", 
        type=str,
        required=True, 
        help="Chemin de destination pour la carte HTML générée"
    )
    parser.add_argument(
        "--strava", 
        type=str,
        help="Chemin (optionnel) vers le fichier strava_ground_truth.gpx pour afficher la vérité terrain", 
        default=None
    )
    args = parser.parse_args()

    if not args.out_csv.endswith('.csv'):
        args.out_csv += '.csv'
    if not args.out_html.endswith('.html'):
        args.out_html += '.html'

    print(f"[*] Chargement du GPS: {args.gps}")
    gps_raw = pd.read_csv(args.gps)
    gps = clean_gps(gps_raw)
    
    if len(gps) < 10:
        print("[-] Pas assez de points GPS valides après nettoyage.")
        return

    ref_lat = gps.Latitude.iloc[0]
    ref_lon = gps.Longitude.iloc[0]

    print(f"[*] Chargement de l'IMU: {args.imu}")
    imu, gyro_x_bias, bias_Y, bias_Z = load_imu(args.imu, gps.Timestamp.iloc[0], gps.Timestamp.iloc[-1])
    
    if len(imu) == 0:
        print("[-] Pas de données IMU synchronisées avec la fenêtre temporelle du GPS.")
        return

    t_gps = gps.Timestamp.values
    lats  = gps.Latitude.values
    lons  = gps.Longitude.values

    # Convert coordinates
    x_gps, y_gps = gps_to_local_meters(lats, lons, ref_lat, ref_lon)
    x_gps, y_gps = np.array(x_gps) if isinstance(x_gps, list) else x_gps, np.array(y_gps) if isinstance(y_gps, list) else y_gps
    
    # Calculate velocity
    v_arr = np.zeros(len(gps))
    for k in range(1, len(gps)):
        dt_k = t_gps[k] - t_gps[k-1]
        v_arr[k] = np.hypot(x_gps[k] - x_gps[k-1], y_gps[k] - y_gps[k-1]) / dt_k if dt_k > 0 else 0.0

    sigma_arr = compute_sigma_a(imu, t_gps, bias_Y, bias_Z)
    omega_arr = compute_omega(imu, t_gps, gyro_x_bias)
    sigma_omega = np.radians(imu['Gyro X'].std())

    # Init theta0
    theta0 = 0.0
    for k in range(1, min(30, len(gps))):
        dx_init = x_gps[k] - x_gps[0]
        dy_init = y_gps[k] - y_gps[0]
        if np.hypot(dx_init, dy_init) >= 1.5:
            theta0 = np.arctan2(dy_init, dx_init)
            break

    ekf = EKFSansMagneto(x0=x_gps[0], y0=y_gps[0], theta0=theta0, sigma_omega=sigma_omega)
    
    estimates = [(x_gps[0], y_gps[0])]
    accepted  = [True]
    thetas    = [theta0]

    print("[*] Lancement du filtre EKF...")
    for k in range(1, len(gps)):
        dt = t_gps[k] - t_gps[k-1]
        if dt <= 0: 
            estimates.append(estimates[-1])
            accepted.append(False)
            thetas.append(thetas[-1])
            continue
            
        ekf.predict(v_arr[k], omega_arr[k - 1], dt, sigma_arr[k - 1])
        acc = ekf.update(x_gps[k], y_gps[k])
        
        accepted.append(acc)
        estimates.append((ekf.x[0], ekf.x[1]))
        thetas.append(ekf.x[2])

    n_rej = sum(1 for a in accepted if not a)
    print(f"[+] Fusion terminée. {n_rej} points GPS rejetés.")

    # Generate CSV Output
    print(f"[*] Génération du CSV: {args.out_csv}")
    os.makedirs(os.path.dirname(os.path.abspath(args.out_csv)), exist_ok=True)
    with open(args.out_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Position_X_m", "Position_Y_m", "Latitude", "Longitude", "Theta_deg", "GPS_accepted", "Speed_m_s"])
        for k in range(len(gps)):
            fus_lat, fus_lon = local_meters_to_gps(estimates[k][0], estimates[k][1], ref_lat, ref_lon)
            writer.writerow([
                f"{t_gps[k]:.3f}",
                f"{estimates[k][0]:.4f}", f"{estimates[k][1]:.4f}",
                f"{fus_lat:.8f}", f"{fus_lon:.8f}",
                f"{np.degrees(thetas[k]):.2f}",
                1 if accepted[k] else 0,
                f"{v_arr[k]:.3f}"
            ])

    # Generate HTML Map
    print(f"[*] Génération de la carte: {args.out_html}")
    os.makedirs(os.path.dirname(os.path.abspath(args.out_html)), exist_ok=True)
    m = folium.Map(location=[ref_lat, ref_lon], zoom_start=18)
    
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 220px; height: auto; 
                border:2px solid grey; z-index:9999; font-size:14px; background-color: white; padding: 10px;">
        <b>EKF Cinématique (V2)</b><br>
        <i style="color:black;">▬</i> Vérité Terrain (Strava)<br>
        <i style="color:gray;">●</i> GPS Brut (avant filtre IQR)<br>
        <i style="color:red;">▬</i> GPS Nettoyé (utilisé)<br>
        <i style="color:orange;">●</i> GPS Rejeté (Mahalanobis)<br>
        <i style="color:blue;">▬</i> Trajectoire EKF<br>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    if args.strava and os.path.exists(args.strava):
        strava = parse_gpx(args.strava)
        if strava:
            folium.PolyLine(strava, color="black", weight=4, opacity=0.8, tooltip="Strava (Vérité Terrain)").add_to(m)

    for lat, lon in zip(gps_raw.Latitude, gps_raw.Longitude):
        folium.CircleMarker([lat, lon], radius=2, color="gray", fill=True, opacity=0.5).add_to(m)

    folium.PolyLine(list(zip(lats, lons)), color="red", weight=2, opacity=0.8).add_to(m)

    for k, (acc, row) in enumerate(zip(accepted, gps.itertuples())):
        if not acc:
            folium.CircleMarker([row.Latitude, row.Longitude], radius=7, color="orange", fill=True).add_to(m)

    ekf_coords = [local_meters_to_gps(e, n, ref_lat, ref_lon) for e, n in estimates]
    folium.PolyLine(ekf_coords, color="blue", weight=3, opacity=1.0).add_to(m)

    m.save(args.out_html)
    print(f"[+] Succès !")

if __name__ == "__main__":
    main()
