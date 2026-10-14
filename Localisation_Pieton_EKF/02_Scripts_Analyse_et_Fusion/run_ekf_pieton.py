"""
EKF Piéton — Fusion GPS/IMU
============================
Modèle cinématique plan (cours CM6 INSA, slide 66-67) :
  État : x = [x_est, y_nord, theta]    (m, m, rad)
  Commande : u = [v, omega]             (m/s, rad/s)
  Mesure : GPS = [x_est, y_nord]

  f(x, u) = [x + v*cos(theta)*dt,
             y + v*sin(theta)*dt,
             theta + omega*dt]

  Jacobienne F analytique :
  F = [[1, 0, -v*sin(theta)*dt],
       [0, 1,  v*cos(theta)*dt],
       [0, 0,  1              ]]

Paramètres calibrés :
  R_GPS = diag([1.20, 0.07])  m²  (Est, Nord — source: get_IMU_GPS.py ligne 81)
  sigma_a = 0.8596 m/s²  (source: get_IMU_GPS.py ligne 80, Q adaptive)
  Maha threshold = 9.21  (chi² 2 ddl, 99% — source: kalman_gps_imu.py)

Axes IMU (d'après l'analyse des données) :
  Accel X moyen ≈ +1g → axe X = Up (vertical)
  Gyro X = vitesse angulaire autour de l'axe vertical = omega (Yaw rate)
"""

import numpy as np
import pandas as pd
import folium
import xml.etree.ElementTree as ET
from pathlib import Path

# ── Paramètres calibrés ──────────────────────────────────────────────────────
# R: matrice de bruit de mesure GPS [Est, Nord] en m²
# Source: get_IMU_GPS.py ligne 81, R_calibree = np.diag([1.20, 0.07])
# Note: dans notre convention (x=Est, y=Nord) → R = diag([1.20, 0.07])
R_GPS = np.diag([1.20, 0.07])

SIGMA_A      = 0.8596   # m/s² — σ_a fallback (source: get_IMU_GPS.py ligne 80)
SIGMA_A_MIN  = 0.10     # m/s² — plancher (quasi-stationnaire)
SIGMA_A_MAX  = 5.00     # m/s² — plafond (très dynamique)
MAHA_THR     = 9.21     # chi² 2 ddl, 99% (source: kalman_gps_imu.py)
N_STATIC     = 200      # nb échantillons IMU pour calibrer le biais statique
G            = 9.80665

# ── Helpers géodésiques ──────────────────────────────────────────────────────
def latlon_to_m(lat, lon, ref_lat, ref_lon):
    """Conversion GPS → (East m, Nord m) depuis une origine."""
    north = (lat - ref_lat) * 111_320
    east  = (lon - ref_lon) * 111_320 * np.cos(np.radians(ref_lat))
    return east, north   # (x=Est, y=Nord) — convention get_IMU_GPS.py

def m_to_latlon(east, north, ref_lat, ref_lon):
    lat = ref_lat + north / 111_320
    lon = ref_lon + east  / (111_320 * np.cos(np.radians(ref_lat)))
    return lat, lon

# ── Nettoyage GPS ─────────────────────────────────────────────────────────────
def clean_gps(gps: pd.DataFrame) -> pd.DataFrame:
    """
    Même logique que kalman_gps_imu.py :
      1. Trames corrompues (coordonnées hors plage physique)
      2. Outliers géographiques (IQR ×1.5)
      3. Début instable (≈15 premières secondes, cold start GPS)
    """
    gps = gps[(gps.Latitude < 90) & (gps.Longitude < 180)].copy()
    for col in ["Latitude", "Longitude"]:
        Q1, Q3 = gps[col].quantile(0.25), gps[col].quantile(0.75)
        iqr    = Q3 - Q1
        gps    = gps[(gps[col] >= Q1 - 1.5*iqr) & (gps[col] <= Q3 + 1.5*iqr)]
    gps = gps[gps.Timestamp > gps.Timestamp.iloc[0] + 15].reset_index(drop=True)
    return gps

# ── Traitement IMU ─────────────────────────────────────────────────────────────
def load_imu(path, t_start, t_end):
    """
    Charge l'IMU, calcule le biais gyro sur les N_STATIC premières trames
    (supposées statiques avant que la personne commence à marcher),
    puis filtre sur la fenêtre temporelle GPS.
    """
    imu = pd.read_csv(path)

    # Biais gyroscope : moyenne sur les premières trames (piéton immobile)
    # Axe X = axe vertical → omega = Gyro_X
    gyro_x_bias = imu['Gyro X'].iloc[:N_STATIC].mean()

    # Biais accéléromètre horizontal pour Q adaptive
    # Axes Y et Z = horizontaux (cf. accel_mean Y≈0, Z≈0)
    bias_Y = imu['Accel Y'].iloc[:N_STATIC].mean()
    bias_Z = imu['Accel Z'].iloc[:N_STATIC].mean()

    imu = imu[(imu.Timestamp >= t_start) & (imu.Timestamp <= t_end)].reset_index(drop=True)
    return imu, gyro_x_bias, bias_Y, bias_Z

def compute_sigma_a(imu, gps_timestamps, bias_Y, bias_Z):
    """
    Calcule le sigma_a adaptatif pour chaque intervalle GPS.
    (Identique à kalman_gps_imu.py — réutilisation directe)
    On utilise les axes Y et Z de l'accél (horizontaux dans notre configuration).
    """
    t_imu   = imu.Timestamp.values
    aY      = (imu['Accel Y'].values - bias_Y) * G
    aZ      = (imu['Accel Z'].values - bias_Z) * G
    a_horiz = np.hypot(aY, aZ)

    sigma_arr = np.empty(len(gps_timestamps) - 1)
    for k in range(len(gps_timestamps) - 1):
        mask    = (t_imu >= gps_timestamps[k]) & (t_imu < gps_timestamps[k + 1])
        samples = a_horiz[mask]
        if len(samples) == 0:
            sigma_arr[k] = SIGMA_A
        else:
            sigma_arr[k] = np.clip(np.sqrt(np.mean(samples**2)), SIGMA_A_MIN, SIGMA_A_MAX)
    return sigma_arr

def compute_omega(imu, gps_timestamps, gyro_x_bias):
    """
    Calcule omega moyen (rad/s) pour chaque intervalle GPS.
    omega = Gyro_X - biais, converti de deg/s en rad/s.
    """
    t_imu = imu.Timestamp.values
    gx    = np.radians(imu['Gyro X'].values - gyro_x_bias)

    omega_arr = np.empty(len(gps_timestamps) - 1)
    for k in range(len(gps_timestamps) - 1):
        mask    = (t_imu >= gps_timestamps[k]) & (t_imu < gps_timestamps[k + 1])
        samples = gx[mask]
        omega_arr[k] = np.mean(samples) if len(samples) > 0 else 0.0
    return omega_arr

def build_Q(dt, sigma_a, sigma_omega):
    """
    Matrice de bruit de processus Q (3×3) pour l'état [x, y, theta].
    Inspirée de kalman_gps_imu.py mais adaptée à l'état étendu.
    """
    sa2 = sigma_a**2
    so2 = sigma_omega**2
    return np.array([
        [sa2 * dt**4/4,  0,              0             ],
        [0,              sa2 * dt**4/4,  0             ],
        [0,              0,              so2 * dt**2   ],
    ])

# ── EKF Piéton ────────────────────────────────────────────────────────────────
class EKFPieton:
    """
    EKF (Extended Kalman Filter) cinématique plan — piéton.
    État : [x_est (m), y_nord (m), theta (rad)]
    Modèle d'après le cours CM6 INSA, slide 66-67.
    """

    H = np.array([[1, 0, 0],
                  [0, 1, 0]])   # On mesure seulement x et y (pas theta)

    def __init__(self, x0, y0, theta0):
        self.x = np.array([x0, y0, theta0], dtype=float)
        # P initiale : confiance modérée sur position (≈ R_GPS), forte incertitude sur theta
        self.P = np.diag([R_GPS[0,0], R_GPS[1,1], (np.pi)**2])
        self.accepted_last = True

    def predict(self, v, omega, dt, sigma_a, sigma_omega):
        """
        Prédiction EKF — Slide 62 du cours.
        x̂k⁻ = f(x̂k-1, u)
        Pk⁻  = Fk * Pk-1 * Fk' + Q
        """
        x_, y_, th = self.x
        # ── Équations d'état non-linéaires (f) ──────────────────────────────
        self.x = np.array([
            x_ + v * np.cos(th) * dt,
            y_ + v * np.sin(th) * dt,
            th + omega * dt
        ])
        # Normalisation de theta dans [-pi, pi]
        self.x[2] = (self.x[2] + np.pi) % (2 * np.pi) - np.pi

        # ── Jacobienne analytique Fk ─────────────────────────────────────────
        # dervation partielle de f par rapport à x, évaluée en (x̂k-1, uk-1)
        Fk = np.array([
            [1, 0, -v * np.sin(th) * dt],
            [0, 1,  v * np.cos(th) * dt],
            [0, 0,  1                  ]
        ])

        # ── Propagation de la covariance ────────────────────────────────────
        Q = build_Q(dt, sigma_a, sigma_omega)
        self.P = Fk @ self.P @ Fk.T + Q

    def update(self, gps_x, gps_y):
        """
        Correction EKF depuis le GPS — Slide 62 du cours.
        Gate de Mahalanobis avant d'accepter la mesure.
        """
        z    = np.array([gps_x, gps_y])
        innov = z - (self.H @ self.x)          # Innovation (surprise)
        S    = self.H @ self.P @ self.H.T + R_GPS  # Covariance innovation

        # ── Gate de Mahalanobis ──────────────────────────────────────────────
        maha = innov @ np.linalg.inv(S) @ innov
        if maha > MAHA_THR:
            self.accepted_last = False
            return False   # GPS rejeté, on garde la prédiction

        # ── Gain de Kalman ───────────────────────────────────────────────────
        K = self.P @ self.H.T @ np.linalg.inv(S)

        # ── Mise à jour état et covariance ──────────────────────────────────
        self.x = self.x + K @ innov
        self.x[2] = (self.x[2] + np.pi) % (2 * np.pi) - np.pi   # Normalisation theta
        self.P = (np.eye(3) - K @ self.H) @ self.P

        self.accepted_last = True
        return True

# ── GPX Parser ────────────────────────────────────────────────────────────────
def parse_gpx(path):
    tree = ET.parse(path)
    root = tree.getroot()
    ns   = {'gpx': 'http://www.topografix.com/GPX/1/1'}
    return [(float(t.get('lat')), float(t.get('lon')))
            for t in root.findall('.//gpx:trkpt', ns)]

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("EKF PIÉTON — Fusion GPS/IMU (modèle cinématique plan)")
    print("=" * 60)

    gps_raw = pd.read_csv("gps_data.csv")
    gps     = clean_gps(gps_raw)
    print(f"GPS : {len(gps_raw)} brut → {len(gps)} après nettoyage")

    ref_lat = gps.Latitude.iloc[0]
    ref_lon = gps.Longitude.iloc[0]

    imu, gyro_x_bias, bias_Y, bias_Z = load_imu(
        "imu_data.csv",
        gps.Timestamp.iloc[0],
        gps.Timestamp.iloc[-1]
    )
    print(f"IMU : {len(imu)} échantillons | biais Gyro_X={gyro_x_bias:.2f} °/s")

    t_gps = gps.Timestamp.values
    lats  = gps.Latitude.values
    lons  = gps.Longitude.values

    # ── Vitesse scalaire (v) depuis le GPS ──────────────────────────────────
    # v = |delta_position| / delta_t   (pas d'intégration d'accéléromètre)
    x_gps, y_gps = latlon_to_m(lats, lons, ref_lat, ref_lon)
    v_arr = np.zeros(len(gps))
    for k in range(1, len(gps)):
        dt_k     = t_gps[k] - t_gps[k-1]
        dx, dy   = x_gps[k] - x_gps[k-1], y_gps[k] - y_gps[k-1]
        v_arr[k] = np.hypot(dx, dy) / dt_k if dt_k > 0 else 0.0

    # ── sigma_a et omega adaptatifs ──────────────────────────────────────────
    sigma_arr = compute_sigma_a(imu, t_gps, bias_Y, bias_Z)
    omega_arr = compute_omega(imu, t_gps, gyro_x_bias)
    sigma_omega = np.radians(imu['Gyro X'].std())  # écart-type global du Gyro_X
    print(f"sigma_a : min={sigma_arr.min():.3f} moy={sigma_arr.mean():.3f} max={sigma_arr.max():.3f} m/s²")
    print(f"omega_arr (rad/s) : moy={omega_arr.mean():.4f} std={omega_arr.std():.4f}")

    # ── Initialisation du cap θ₀ depuis le premier vrai déplacement GPS ─────
    # On cherche le premier couple de points où le piéton a réellement bougé
    # (distance > 1m), pour éviter que le GPS statique au démarrage donne yaw=0
    theta0 = 0.0
    MIN_DIST_INIT = 1.5   # m — seuil de déplacement minimum pour calculer un cap fiable
    for k in range(1, min(30, len(gps))):   # on regarde les 30 premiers points max
        dx_init = x_gps[k] - x_gps[0]
        dy_init = y_gps[k] - y_gps[0]
        if np.hypot(dx_init, dy_init) >= MIN_DIST_INIT:
            theta0 = np.arctan2(dy_init, dx_init)
            print(f"Cap initial calculé depuis GPS[0→{k}] (dist={np.hypot(dx_init,dy_init):.1f}m)")
            break
    else:
        print("⚠️  Pas de déplacement initial détecté sur 30 pts — cap forcé à 0°")

    ekf       = EKFPieton(x0=x_gps[0], y0=y_gps[0], theta0=theta0)
    estimates = [(x_gps[0], y_gps[0])]
    accepted  = [True]

    # ── Boucle EKF ──────────────────────────────────────────────────────────
    for k in range(1, len(gps)):
        dt = t_gps[k] - t_gps[k-1]
        if dt <= 0:
            continue

        # Prédiction (IMU → omega, GPS → v)
        ekf.predict(
            v        = v_arr[k],
            omega    = omega_arr[k - 1],
            dt       = dt,
            sigma_a  = sigma_arr[k - 1],
            sigma_omega = sigma_omega
        )

        # Correction GPS avec gate de Mahalanobis
        acc = ekf.update(x_gps[k], y_gps[k])
        accepted.append(acc)
        estimates.append((ekf.x[0], ekf.x[1]))

    n_rej = sum(1 for a in accepted if not a)
    print(f"Points GPS rejetés (Mahalanobis) : {n_rej}/{len(gps)}")

    # ── Carte Folium ─────────────────────────────────────────────────────────
    center = [ref_lat, ref_lon]
    m = folium.Map(location=center, zoom_start=18, tiles="OpenStreetMap")

    # Strava (vérité terrain — noir)
    strava_path = "strava_ground_truth.gpx"
    if Path(strava_path).exists():
        strava = parse_gpx(strava_path)
        folium.PolyLine(strava, color="black", weight=4, opacity=0.8,
                        tooltip="Strava (Vérité Terrain)").add_to(m)
        folium.CircleMarker(strava[0], radius=8, color="black", fill=True,
                            popup="Début Strava").add_to(m)

    # GPS totalement brut (avant nettoyage IQR) - Petits points gris
    for lat, lon in zip(gps_raw.Latitude, gps_raw.Longitude):
        folium.CircleMarker([lat, lon], radius=2, color="gray", fill=True,
                            opacity=0.5, tooltip="GPS BRUT (avant nettoyage)").add_to(m)

    # GPS nettoyé (rouge) - Ligne solide
    folium.PolyLine(list(zip(lats, lons)), color="red", weight=2,
                    opacity=0.8, tooltip="GPS nettoyé (utilisé par EKF)").add_to(m)

    # Points GPS rejetés (orange)
    for k, (acc, row) in enumerate(zip(accepted, gps.itertuples())):
        if not acc:
            folium.CircleMarker(
                [row.Latitude, row.Longitude], radius=7,
                color="orange", fill=True,
                tooltip=f"Rejeté Mahalanobis — point {k}"
            ).add_to(m)

    # Trajectoire EKF (bleu)
    ekf_coords = [m_to_latlon(e, n, ref_lat, ref_lon) for e, n in estimates]
    folium.PolyLine(ekf_coords, color="blue", weight=3, opacity=1.0,
                    tooltip="EKF Piéton (GPS+Gyro)").add_to(m)
    folium.Marker(ekf_coords[0],  popup="Départ EKF",
                  icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(ekf_coords[-1], popup="Arrivée EKF",
                  icon=folium.Icon(color="red")).add_to(m)

    out = "ekf_pieton_map.html"
    m.save(out)
    print(f"\nCarte générée → {out}")
    print("Légende : Noir=Strava | Rouge=GPS filtré | Orange=Rejetés | Bleu=EKF")

if __name__ == "__main__":
    main()
