import os
import glob
import numpy as np
import pandas as pd
import folium
import xml.etree.ElementTree as ET
from pathlib import Path
from utils.kalman import EKFSansMagneto
from utils.gps_utils import gps_to_local_meters, local_meters_to_gps

# ── Paramètres calibrés ──────────────────────────────────────────────────────
SIGMA_A      = 0.8596   # m/s²
SIGMA_A_MIN  = 0.10     # m/s²
SIGMA_A_MAX  = 5.00     # m/s²
N_STATIC     = 200
G            = 9.80665

# ── Helpers ──────────────────────────────────────────────────────────────────
def parse_gpx(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        ns   = {'gpx': 'http://www.topografix.com/GPX/1/1'}
        return [(float(t.get('lat')), float(t.get('lon')))
                for t in root.findall('.//gpx:trkpt', ns)]
    except Exception as e:
        print(f"    [Erreur lecture GPX] {e}")
        return []

def clean_gps(gps: pd.DataFrame) -> pd.DataFrame:
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

# ── Main Processing Loop ─────────────────────────────────────────────────────
def process_dataset(data_dir, output_dir):
    dataset_name = os.path.basename(os.path.normpath(data_dir))
    gps_file = os.path.join(data_dir, "gps_data.csv")
    imu_file = os.path.join(data_dir, "imu_data.csv")
    
    if not os.path.exists(gps_file) or not os.path.exists(imu_file):
        print(f"[-] Ignoré : {dataset_name} (fichiers CSV manquants)")
        return
        
    print(f"[*] Traitement de : {dataset_name}")
    
    gps_raw = pd.read_csv(gps_file)
    if 'Latitude' not in gps_raw.columns:
        print(f"    [-] Erreur: Colonne Latitude absente dans {gps_file}")
        return
        
    gps = clean_gps(gps_raw)
    if len(gps) < 10:
        print(f"    [-] Pas assez de points GPS valides.")
        return

    ref_lat = gps.Latitude.iloc[0]
    ref_lon = gps.Longitude.iloc[0]

    # Load IMU
    try:
        imu, gyro_x_bias, bias_Y, bias_Z = load_imu(imu_file, gps.Timestamp.iloc[0], gps.Timestamp.iloc[-1])
    except Exception as e:
        print(f"    [-] Erreur IMU: {e}. Ce jeu de données n'a peut-être pas les bonnes colonnes.")
        return
        
    if len(imu) == 0:
        print(f"    [-] Pas de données IMU synchronisées.")
        return

    # Compute speeds and stats
    t_gps = gps.Timestamp.values
    lats  = gps.Latitude.values
    lons  = gps.Longitude.values

    x_gps, y_gps = gps_to_local_meters(lats, lons, ref_lat, ref_lon)
    x_gps, y_gps = np.array(x_gps) if isinstance(x_gps, list) else x_gps, np.array(y_gps) if isinstance(y_gps, list) else y_gps
    
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

    # Run EKF
    ekf = EKFSansMagneto(x0=x_gps[0], y0=y_gps[0], theta0=theta0, sigma_omega=sigma_omega)
    estimates = [(x_gps[0], y_gps[0])]
    accepted  = [True]

    for k in range(1, len(gps)):
        dt = t_gps[k] - t_gps[k-1]
        if dt <= 0: continue
        
        # Le EKF cinématique attend (v, omega, dt, sigma_a)
        ekf.predict(v_arr[k], omega_arr[k - 1], dt, sigma_arr[k - 1])
        acc = ekf.update(x_gps[k], y_gps[k])
        accepted.append(acc)
        estimates.append((ekf.x[0], ekf.x[1]))

    n_rej = sum(1 for a in accepted if not a)
    print(f"    [+] Terminé. {n_rej} points rejetés.")

    # Generate Map
    m = folium.Map(location=[ref_lat, ref_lon], zoom_start=18)
    
    # Légende HTML
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 220px; height: auto; 
                border:2px solid grey; z-index:9999; font-size:14px; background-color: white; padding: 10px;">
        <b>EKF Cinématique (V2)</b><br>
        <i style="color:black;">▬</i> Vérité Terrain (Strava)<br>
        <i style="color:gray;">●</i> GPS Brut (avant filtre IQR)<br>
        <i style="color:red;">▬</i> GPS Nettoyé (utilisé)<br>
        <i style="color:orange;">●</i> GPS Rejeté (Mahalanobis)<br>
        <i style="color:blue;">▬</i> Trajectoire EKF (Gyro+Vitesse)<br>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Strava Ground Truth
    gpx_files = glob.glob(os.path.join(data_dir, "*.gpx"))
    if gpx_files:
        strava = parse_gpx(gpx_files[0])
        if strava:
            folium.PolyLine(strava, color="black", weight=4, opacity=0.8, tooltip="Strava (Vérité Terrain)").add_to(m)

    # Raw GPS
    for lat, lon in zip(gps_raw.Latitude, gps_raw.Longitude):
        folium.CircleMarker([lat, lon], radius=2, color="gray", fill=True, opacity=0.5).add_to(m)

    # Clean GPS
    folium.PolyLine(list(zip(lats, lons)), color="red", weight=2, opacity=0.8).add_to(m)

    # Rejected GPS
    for k, (acc, row) in enumerate(zip(accepted, gps.itertuples())):
        if not acc:
            folium.CircleMarker([row.Latitude, row.Longitude], radius=7, color="orange", fill=True).add_to(m)

    # EKF Path
    ekf_coords = [local_meters_to_gps(e, n, ref_lat, ref_lon) for e, n in estimates]
    folium.PolyLine(ekf_coords, color="blue", weight=3, opacity=1.0).add_to(m)

    out_file = os.path.join(output_dir, f"MAP_{dataset_name}.html")
    m.save(out_file)
    print(f"    [+] Carte générée : {out_file}\n")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_parent = os.path.join(base_dir, "Donnees")
    output_parent = os.path.join(base_dir, "Resultats_HTML")
    
    print("==================================================")
    print(" DÉBUT DU TRAITEMENT PAR LOT (FINAL TEST EKF V2) ")
    print("==================================================")
    
    dirs = [os.path.join(data_parent, d) for d in os.listdir(data_parent) if os.path.isdir(os.path.join(data_parent, d))]
    
    for d in sorted(dirs):
        process_dataset(d, output_parent)
        
    print("==================================================")
    print(f" TOUT EST TERMINÉ ! Cartes dans : {output_parent}")
    print("==================================================")
