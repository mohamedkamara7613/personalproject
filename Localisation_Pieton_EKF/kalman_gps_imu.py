"""
Kalman filter — GPS smoothing avec bruit IMU calibré

State: x = [North_m, vNorth, East_m, vEast]
- Modèle cinématique vitesse constante (prédiction)
- Mesure GPS (correction)
- Q calibrée depuis IMU en mouvement (sigma_a = 0.8596 m/s²)
- Gate de Mahalanobis rejette les outliers GPS (multipath, trame corrompue)
"""

import numpy as np
import pandas as pd
import folium
from pathlib import Path

# ── Kalman parameters ─────────────────────────────────────────────────────────
SIGMA_A  = 0.8596                     # m/s²  — σ_a IMU en mouvement
R_GPS    = np.diag([0.07, 1.20])      # m²    — bruit GPS stationnaire
MAHA_THR = 9.21                       # chi² 2 ddl, 99 %

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


def build_Q(dt):
    s = SIGMA_A ** 2
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


# ── Kalman filter ─────────────────────────────────────────────────────────────

def run_kalman(gps: pd.DataFrame):
    """GPS-only Kalman avec gate de Mahalanobis."""
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
        P_pred = F @ P @ F.T + build_Q(dt)

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
    m = folium.Map(location=center, zoom_start=18, tiles="OpenStreetMap")

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

    data_dir = Path(__file__).parent.parent / "IMU_ET_GPS"

    gps_raw   = pd.read_csv(data_dir / "gps_data.csv")
    gps_clean = clean_gps(gps_raw)
    print(f"GPS : {len(gps_raw)} brut → {len(gps_clean)} propres")

    REF_LAT = gps_clean.Latitude.iloc[0]
    REF_LON = gps_clean.Longitude.iloc[0]

    kf_n, kf_e, accepted = run_kalman(gps_clean)

    n_rej = (~accepted).sum()
    print(f"Rejetés par Mahalanobis : {n_rej}/{len(gps_clean)}")

    make_map(gps_raw, gps_clean, kf_n, kf_e, accepted,
             data_dir / "kalman_fusion.html")


if __name__ == "__main__":
    main()
