"""
get_IMU_GPS.py — Version EKF Piéton (Fusion GPS + Gyroscope)
=============================================================
Remplace l'ancienne version qui utilisait ax, ay bruts dans predict()
(ce qui intégrait la gravité et causait une dérive en t²).

Modèle utilisé : Cinématique plan — cours CM6 INSA, slide 66-67
  État : [x_est (m), y_nord (m), theta (rad)]
  - v   (m/s)   : calculé depuis les positions GPS consécutives
  - omega (rad/s): Gyro_X (axe vertical du capteur) avec biais soustrait

PRÉREQUIS : modifier core/imu_acquisition.py, ligne 47 :
  AVANT : data_queue.put(('IMU', time.time(), accel_x, accel_y))
  APRÈS : data_queue.put(('IMU', time.time(), accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z))

Matrices calibrées (source: calibration statique) :
  R_GPS    = diag([1.20, 0.07])  m²   [x=Est, y=Nord]
  sigma_a  = 0.8596 m/s²  (fallback pour Q adaptive)
"""

import argparse
import threading
import os
import queue
import time
import csv
import numpy as np
import sys

# Ajout des chemins de l'équipe pour récupérer la bibliothèque
sys.path.append("/home/mkamara/Bureau/repos/pi_itineraire_26_28/code/Code_fusion")
from core.kalman import EKFSansMagneto

from config import (
    LSM6DSO_ADDR, ACCEL_RANGE, ACCEL_FREQ,
    GYRO_RANGE, GYRO_FREQ)

from config import (
    GNSS_MODES, MODE_GNSS)

from core.imu_acquisition import get_imu_data
from core.gnss_position import gnss_position
from core.gps_utils import gps_to_local_meters, local_meters_to_gps


# Paramètres calibrés

# R : bruit de mesure GPS [x=Est, y=Nord] en m² — calibré sur données statiques
R_GPS = np.diag([1.20, 0.07])

# sigma_a : écart-type de l'accélération horizontale — valeur de fallback
SIGMA_A_DEFAULT = 0.8596     # m/s²
SIGMA_A_MIN     = 0.10       # m/s² — plancher (piéton quasi-immobile)
SIGMA_A_MAX     = 5.00       # m/s² — plafond (mouvement très dynamique)

# Nombre d'échantillons IMU pour calibrer le biais statique au démarrage
N_STATIC = 200

# Gate de Mahalanobis : seuil chi² 2 ddl à 99% (rejet des outliers GPS)
MAHA_THR = 9.21

G = 9.80665

# ══════════════════════════════════════════════════════════════════════════════Threads de capture

def run_imu(save_path, q):
    get_imu_data(
        LSM6DSO_ADDR, ACCEL_RANGE, ACCEL_FREQ,
        GYRO_RANGE, GYRO_FREQ,
        save_path, data_queue=q
    )


def run_gps(mode, save_path, display_lcd, q):
    gnss_position(
        mode=GNSS_MODES[mode],
        csv_out=save_path,
        display_LCD=display_lcd,
        data_queue=q
    )


# Thread EKF (fusion temps réel)

def run_kalman(q, save_path, stop_signal=None):
    """
    Thread de fusion EKF temps réel.

    Protocole d'initialisation :
      1. Les N_STATIC premières trames IMU calibrent le biais du Gyro X
         (piéton supposé immobile au démarrage — attendre ~2s avant de marcher).
      2. Le premier point GPS valide initialise la position et le cap.
      3. À partir du 2ème point GPS valide, le filtre tourne normalement.

    Flux de données :
      IMU (100 Hz) → predict(v_dernier, omega=Gyro_X, dt)
      GPS  (1 Hz)  → compute v depuis delta-position → update(east, nord)
    """
    print("[EKF] Thread démarré. Calibration du biais gyroscope...")

    ekf            = None
    lat_origin     = None
    lon_origin     = None

    # Biais IMU (calculé sur N_STATIC premières trames immobiles)
    gyro_x_buf     = []      # buffer biais Gyro X (rad/s)
    accel_yz_buf   = []      # buffer accel horizontale pour sigma_a
    gyro_x_bias    = None    # biais en deg/s
    sigma_omega    = np.radians(5.0)  # valeur par défaut ~5°/s
    imu_count      = 0

    # État inter-GPS
    last_v         = 0.0     # m/s  — vitesse scalaire issue du dernier intervalle GPS
    last_east      = None
    last_nord      = None
    last_gps_time  = None
    last_imu_time  = None
    theta_mag      = 0.0

    # Sigma_a courant (mis à jour à chaque nouveau GPS depuis le buffer accel)
    sigma_a_current = SIGMA_A_DEFAULT

    record_path = os.path.join(save_path, "kalman_realtime.csv")
    with open(record_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Position_X_m", "Position_Y_m",
                         "Latitude", "Longitude", "Theta_deg", "GPS_accepted", "Speed_m_s"])
        f.flush()

        while stop_signal is None or not stop_signal.is_set() or not q.empty():
            event      = q.get()
            event_type = event[0]

            if event_type == 'IMU':
                # Format attendu (après modification de imu_acquisition.py) :
                #   ('IMU', timestamp, ax, ay, az, gx, gy, gz)
                # Rétrocompatibilité si l'ancien format (4 éléments) est encore utilisé :
                if len(event) >= 8:
                    _, current_time, ax, ay, az, gx, gy, gz = event
                    has_gyro = True
                else:
                    _, current_time, ax, ay = event
                    gz = gx = gy = 0.0
                    has_gyro = False

                # Phase 1 : calibration du biais (N_STATIC premières trames)
                if imu_count < N_STATIC:
                    if has_gyro:
                        gyro_x_buf.append(gx)
                    imu_count += 1
                    if imu_count == N_STATIC:
                        if has_gyro and gyro_x_buf:
                            gyro_x_bias = np.mean(gyro_x_buf)
                            sigma_omega  = np.radians(np.std(gyro_x_buf))
                            sigma_omega  = max(sigma_omega, np.radians(1.0))
                            print(f"[EKF] Biais Gyro X calibré : {gyro_x_bias:.2f} °/s")
                        else:
                            gyro_x_bias = 0.0
                            print("[EKF] ⚠️  Pas de gyroscope — cap intégré depuis GPS uniquement")
                        gyro_x_buf = []  # libère la mémoire de calibration
                    last_imu_time = current_time
                    continue

                # Phase 2 : EKF actif — prédiction à chaque trame IMU
                if ekf is not None and last_imu_time is not None:
                    dt_imu = current_time - last_imu_time
                    if 0 < dt_imu < 0.5:   # protection contre les grandes discontinuités
                        # Omega : Gyro X (axe vertical) corrigé du biais, en rad/s
                        omega = np.radians(gx - gyro_x_bias) if has_gyro else 0.0

                        # Buffer accel horizontale pour sigma_a adaptatif
                        accel_yz_buf.append(np.hypot(ay, az) * G)

                        ekf.predict(last_v, omega, dt_imu, sigma_a_current)

                last_imu_time = current_time


            elif event_type == 'GPS':
                speed = None
                if len(event) >= 6:
                    _, current_time, lat, lon, speed, n_sats, *rest = event
                elif len(event) == 5:
                    _, current_time, lat, lon, n_sats, *rest = event
                else:
                    _, current_time, lat, lon = event
                    n_sats = 99  # Rétrocompatibilité si non fourni par l'équipe

                # Rejet des trames corrompues ou signal trop faible (< 4 satellites)
                if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                    continue
                if n_sats < 4:
                    print(f"[EKF] GPS ignoré (signal faible : {n_sats} satellites)")
                    continue

                # Initialisation sur le premier point GPS valide
                if lat_origin is None:
                    if imu_count < N_STATIC:
                        # Attendre la fin de la calibration IMU
                        continue
                    lat_origin    = lat
                    lon_origin    = lon
                    last_east, last_nord = gps_to_local_meters(lat, lon, lat_origin, lon_origin)
                    last_gps_time = current_time
                    print(f"[EKF] Origine GPS : Lat={lat_origin:.6f}, Lon={lon_origin:.6f}")
                    print("[EKF] En attente d'un 2ème point GPS pour calculer le cap initial...")
                    continue

                # Calcul position locale
                east, nord = gps_to_local_meters(lat, lon, lat_origin, lon_origin)

                # Anti-téléportation (>500m entre deux fixes = aberrant)
                if np.hypot(east, nord) > 500:
                    continue

                dt_gps = current_time - last_gps_time
                if dt_gps <= 0:
                    last_gps_time = current_time
                    continue

                if ekf is None:
                    dx, dy = east - last_east, nord - last_nord
                    dist   = np.hypot(dx, dy)
                    # Cap initial depuis le vecteur GPS (si déplacement suffisant)
                    if dist >= 1.0:
                        theta0 = np.arctan2(dy, dx)
                    else:
                        theta0 = 0.0
                    ekf = EKFSansMagneto(last_east, last_nord, theta0, sigma_omega)
                    last_v = dist / dt_gps
                    print(f"[EKF] Initialisé — Cap={np.degrees(theta0):.1f}°, v={last_v:.2f} m/s")

                if accel_yz_buf:
                    rms = np.sqrt(np.mean(np.array(accel_yz_buf)**2))
                    sigma_a_current = float(np.clip(rms, SIGMA_A_MIN, SIGMA_A_MAX))
                    accel_yz_buf = []

                #  Vitesse scalaire depuis le GPS (SOG ou delta-position) ─
                dx, dy = east - last_east, nord - last_nord
                if speed is not None and speed > 0.1: # On fait confiance au SOG s'il > 0.1 m/s
                    last_v = speed
                else:
                    dist   = np.hypot(dx, dy)
                    last_v = dist / dt_gps   # m/s (fallback)

                accepted = ekf.update(east, nord)
                if not accepted:
                    print("[EKF]   GPS rejeté (Mahalanobis)")

                # Sauvegarde
                fus_lat, fus_lon = local_meters_to_gps(
                    ekf.x[0], ekf.x[1], lat_origin, lon_origin)
                writer.writerow([
                    f"{current_time:.3f}",
                    f"{ekf.x[0]:.4f}",
                    f"{ekf.x[1]:.4f}",
                    f"{fus_lat:.8f}",
                    f"{fus_lon:.8f}",
                    f"{np.degrees(ekf.x[2]):.2f}",
                    1 if accepted else 0,
                    f"{last_v:.3f}"
                ])
                f.flush()

                last_east, last_nord = east, nord
                last_gps_time = current_time


# Main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", "-m", type=str,
                        choices=GNSS_MODES.keys(), default=MODE_GNSS)
    parser.add_argument("--save-path", "-s", type=str, default="data")
    parser.add_argument("--display-LCD", action="store_true")
    args = parser.parse_args()

    os.makedirs(args.save_path, exist_ok=True)
    imu_file = os.path.join(args.save_path, "imu_data.csv")
    gps_file = os.path.join(args.save_path, "gps_data.csv")

    sensor_queue = queue.Queue()
    stop_signal  = threading.Event()

    imu_thread    = threading.Thread(target=run_imu,
                                     args=(imu_file, sensor_queue),
                                     daemon=True)
    gps_thread    = threading.Thread(target=run_gps,
                                     args=(args.mode, gps_file,
                                           args.display_LCD, sensor_queue),
                                     daemon=True)
    kalman_thread = threading.Thread(target=run_kalman,
                                     args=(sensor_queue, args.save_path,
                                           stop_signal),
                                     daemon=True)

    imu_thread.start()
    gps_thread.start()
    kalman_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[EKF] Arrêt demandé — fermeture propre...")
        stop_signal.set()
        imu_thread.join(timeout=5)
        gps_thread.join(timeout=5)
        kalman_thread.join(timeout=5)
        print("[EKF] Arrêt complet.")

