"""
Kalman filter — GPS smoothing avec Q adaptive depuis l'IMU

State: x = [North_m, vNorth, East_m, vEast]
- Modèle cinématique vitesse constante (prédiction)
- Mesure GPS (correction)
- Q adaptive : sigma_a recalculé à chaque intervalle GPS depuis le RMS
  de l'accélération horizontale IMU (axes Y et Z, X étant l'axe gravité)
- Gate de Mahalanobis rejette les outliers GPS (multipath, trame corrompue)
"""

import sys
import numpy as np
import pandas as pd
import folium
from pathlib import Path

# ── Kalman parameters ─────────────────────────────────────────────────────────
SIGMA_A     = 0.8596   # m/s²  — σ_a de fallback (utilisé si pas d'IMU dans l'intervalle)
SIGMA_A_MIN = 0.10     # m/s²  — plancher (quasi-stationnaire)
SIGMA_A_MAX = 5.00     # m/s²  — plafond  (très dynamique)
R_GPS       = np.diag([0.07, 1.20])   # m²    — bruit GPS stationnaire
MAHA_THR    = 9.21                    # chi² 2 ddl, 99 %
G           = 9.80665                 # m/s²
N_STATIC    = 200                     # nb d'échantillons IMU pour le biais statique

REF_LAT = None
REF_LON = None


# ── helpers ───────────────────────────────────────────────────────────────────

def latlon_to_m(lat, lon):
    north = (lat - REF_LAT) * 111_320
    east  = (lon - REF_LON) * 111_320 * np.cos(np.radians(REF_LAT))
    return north, east


def m_to_latlon(north, east):
    lat = REF_LAT + north / 111_320
    lon = REF_LON + east / (111_320 * np.cos(np.radians(REF_LAT)))
    return lat, lon


def build_Q(dt, sigma_a=SIGMA_A):
    s = sigma_a ** 2
    return s * np.array([
        [dt**4/4,  dt**3/2, 0,        0       ],
        [dt**3/2,  dt**2,   0,        0       ],
        [0,        0,       dt**4/4,  dt**3/2 ],
        [0,        0,       dt**3/2,  dt**2   ],
    ])


# ── GPS cleaning ──────────────────────────────────────────────────────────────

def clean_gps(gps: pd.DataFrame) -> pd.DataFrame:
    # filtre 1 — trames NMEA corrompues (0xFF → 262.046)
    gps = gps[(gps.Latitude < 90) & (gps.Longitude < 180)].copy()
    # filtre 2 — outliers géographiques (mauvais lock satellite)
    for col in ["Latitude", "Longitude"]:
        Q1, Q3 = gps[col].quantile(0.25), gps[col].quantile(0.75)
        iqr = Q3 - Q1
        gps = gps[(gps[col] >= Q1 - 1.5*iqr) & (gps[col] <= Q3 + 1.5*iqr)]
    # filtre 3 — début instable (~15 premières secondes)
    gps = gps[gps.Timestamp > gps.Timestamp.iloc[0] + 15].reset_index(drop=True)
    return gps


# ── IMU — biais et sigma_a adaptatif ─────────────────────────────────────────

def load_imu(path: Path, t_start: float, t_end: float):
    """Charge l'IMU, calcule le biais (N_STATIC premières trames), filtre sur [t_start, t_end]."""
    imu = pd.read_csv(path)
    bias_Y = imu['Accel Y'].iloc[:N_STATIC].mean()
    bias_Z = imu['Accel Z'].iloc[:N_STATIC].mean()
    imu = imu[(imu.Timestamp >= t_start) & (imu.Timestamp <= t_end)].reset_index(drop=True)
    return imu, bias_Y, bias_Z


def compute_sigma_a(imu: pd.DataFrame, gps_timestamps: np.ndarray,
                    bias_Y: float, bias_Z: float) -> np.ndarray:
    """
    Pour chaque intervalle [t[k-1], t[k]] entre fixes GPS, calcule le RMS
    de l'accélération horizontale IMU (axes Y et Z, X étant l'axe gravité).
    Retourne un tableau de len(gps_timestamps)-1 valeurs de sigma_a.
    """
    t_imu  = imu.Timestamp.values
    aY     = (imu['Accel Y'].values - bias_Y) * G
    aZ     = (imu['Accel Z'].values - bias_Z) * G
    a_horiz = np.hypot(aY, aZ)

    sigma_arr = np.empty(len(gps_timestamps) - 1)
    for k in range(len(gps_timestamps) - 1):
        mask = (t_imu >= gps_timestamps[k]) & (t_imu < gps_timestamps[k + 1])
        samples = a_horiz[mask]
        if len(samples) == 0:
            sigma_arr[k] = SIGMA_A   # fallback si aucun échantillon IMU
        else:
            sigma_arr[k] = np.clip(np.sqrt(np.mean(samples ** 2)),
                                   SIGMA_A_MIN, SIGMA_A_MAX)
    return sigma_arr


# ── Kalman filter ─────────────────────────────────────────────────────────────

def run_kalman(gps: pd.DataFrame, sigma_a_arr: np.ndarray):
    """GPS-only Kalman avec Q adaptive (sigma_a par intervalle) et gate de Mahalanobis."""
    gps_n, gps_e = latlon_to_m(gps.Latitude.values, gps.Longitude.values)

    H = np.array([[1, 0, 0, 0],
                  [0, 0, 1, 0]])

    x = np.array([gps_n[0], 0.0, gps_e[0], 0.0])
    P = np.diag([R_GPS[0, 0], 1.0, R_GPS[1, 1], 1.0])

    estimates = [(gps_n[0], gps_e[0])]
    accepted  = [True]
    t = gps.Timestamp.values

    for k in range(1, len(gps)):
        dt = t[k] - t[k-1]

        # ── prédiction ────────────────────────────────────────────────────────
        F = np.array([[1, dt, 0, 0 ],
                      [0, 1,  0, 0 ],
                      [0, 0,  1, dt],
                      [0, 0,  0, 1 ]])
        x_pred = F @ x
        P_pred = F @ P @ F.T + build_Q(dt, sigma_a_arr[k - 1])

        # ── mesure GPS ────────────────────────────────────────────────────────
        z     = np.array([gps_n[k], gps_e[k]])
        innov = z - H @ x_pred
        S     = H @ P_pred @ H.T + R_GPS
        maha  = innov @ np.linalg.inv(S) @ innov

        if maha < MAHA_THR:
            K = P_pred @ H.T @ np.linalg.inv(S)
            x = x_pred + K @ innov
            P = (np.eye(4) - K @ H) @ P_pred
            accepted.append(True)
        else:
            # GPS rejeté → on garde la prédiction
            x = x_pred
            P = P_pred
            accepted.append(False)

        estimates.append((x[0], x[2]))

    est = np.array(estimates)
    return est[:, 0], est[:, 1], np.array(accepted)


# ── carte Folium ──────────────────────────────────────────────────────────────

def make_map(gps_raw, gps_clean, kf_n, kf_e, accepted, out_path):
    center = [gps_clean.Latitude.mean(), gps_clean.Longitude.mean()]
    m = folium.Map(location=center, zoom_start=18, tiles="CartoDB voyager")

    # GPS brut (rouge)
    for _, row in gps_raw.iterrows():
        folium.CircleMarker(
            [row.Latitude, row.Longitude],
            radius=3, color="red", fill=True, fill_opacity=0.5,
            tooltip="GPS brut"
        ).add_to(m)
    folium.PolyLine(
        list(zip(gps_raw.Latitude, gps_raw.Longitude)),
        color="red", weight=1.5, opacity=0.4, tooltip="GPS brut"
    ).add_to(m)

    # GPS propre (gris) — après filtrage pré-Kalman
    folium.PolyLine(
        list(zip(gps_clean.Latitude, gps_clean.Longitude)),
        color="gray", weight=1.5, opacity=0.6, tooltip="GPS filtré (pré-Kalman)"
    ).add_to(m)

    # Points GPS rejetés par le gate (orange)
    for i, (acc, row) in enumerate(zip(accepted, gps_clean.itertuples())):
        if not acc:
            folium.CircleMarker(
                [row.Latitude, row.Longitude],
                radius=6, color="orange", fill=True,
                tooltip=f"Rejeté Mahalanobis — point {i}"
            ).add_to(m)

    # Trajectoire Kalman (bleu)
    kf_lat, kf_lon = m_to_latlon(kf_n, kf_e)
    folium.PolyLine(
        list(zip(kf_lat, kf_lon)),
        color="blue", weight=3, opacity=0.9, tooltip="Kalman (Q depuis IMU)"
    ).add_to(m)

    folium.Marker(
        [kf_lat[0], kf_lon[0]], popup="Départ",
        icon=folium.Icon(color="green")
    ).add_to(m)
    folium.Marker(
        [kf_lat[-1], kf_lon[-1]], popup="Arrivée",
        icon=folium.Icon(color="red")
    ).add_to(m)

    m.save(str(out_path))
    print(f"Carte → {out_path}")


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    global REF_LAT, REF_LON

    if len(sys.argv) > 1:
        data_dir = Path(sys.argv[1])
    else:
        data_dir = Path(__file__).parent.parent / "IMU_ET_GPS"

    gps_raw   = pd.read_csv(data_dir / "gps_data.csv")
    gps_clean = clean_gps(gps_raw)
    print(f"GPS : {len(gps_raw)} brut → {len(gps_clean)} propres")

    REF_LAT = gps_clean.Latitude.iloc[0]
    REF_LON = gps_clean.Longitude.iloc[0]

    imu, bias_Y, bias_Z = load_imu(data_dir / "imu_data.csv",
                                    gps_clean.Timestamp.iloc[0],
                                    gps_clean.Timestamp.iloc[-1])
    print(f"IMU : {len(imu)} échantillons  |  biais Y={bias_Y:.4f}g  Z={bias_Z:.4f}g")

    sigma_a_arr = compute_sigma_a(imu, gps_clean.Timestamp.values, bias_Y, bias_Z)
    print(f"sigma_a : min={sigma_a_arr.min():.3f}  moy={sigma_a_arr.mean():.3f}  max={sigma_a_arr.max():.3f}  m/s²")

    kf_n, kf_e, accepted = run_kalman(gps_clean, sigma_a_arr)

    n_rej = (~accepted).sum()
    print(f"Rejetés par Mahalanobis : {n_rej}/{len(gps_clean)}")

    make_map(gps_raw, gps_clean, kf_n, kf_e, accepted,
             data_dir / "kalman_fusion.html")


if __name__ == "__main__":
    main()
