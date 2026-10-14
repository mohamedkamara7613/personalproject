import argparse
import threading
import os
import queue
import time
import csv
import numpy as np

from config import (
    LSM6DSO_ADDR, ACCEL_RANGE, ACCEL_FREQ,
    GYRO_RANGE, GYRO_FREQ)
    
from config import (
    GNSS_MODES, MODE_GNSS)

from core.imu_acquisition import get_imu_data
from core.gnss_position import gnss_position

# Modules Temps Réel (Kalman & GPS Utils)
from core.kalman import KalmanFilter
from core.gps_utils import gps_to_local_meters, local_meters_to_gps


def run_imu(save_path, q):
    get_imu_data(
        LSM6DSO_ADDR,
        ACCEL_RANGE,
        ACCEL_FREQ,
        GYRO_RANGE,
        GYRO_FREQ,
        save_path,
        data_queue=q
    )


def run_gps(mode, save_path, display_lcd, q):
    gnss_position(
        mode=GNSS_MODES[mode],
        csv_out=save_path,
        display_LCD=display_lcd,
        data_queue=q
    )

def run_kalman(q, save_path):
    """
    Thread de fusion temps réel : écoute la queue, instancie le Kalman, 
    calcule la fusion et exporte le résultat.
    """
    print("[KALMAN] Thread démarré. Attente du premier point GPS pour l'initialisation...")
    
    kf = None
    lat_origin = None
    lon_origin = None
    last_time = None
    
    record_path = os.path.join(save_path, "kalman_realtime.csv")
    with open(record_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Position_X_m", "Position_Y_m", "Latitude", "Longitude"])
        
        while True:
            # On attend un événement de la queue (bloquant)
            event = q.get()
            event_type = event[0]
            
            if event_type == 'GPS':
                _, current_time, lat, lon = event
                
                # Ignorer les points hors limites
                if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                    continue
                
                # 1. Initialisation sur le premier point GPS valide
                if kf is None:
                    lat_origin = lat
                    lon_origin = lon
                    last_time = current_time
                    
                    # --- Matrices Calibrées ---
                    var_accel = 0.8596 ** 2 
                    R_calibree = np.diag([1.20, 0.07])  # [x=Est, y=Nord] en m²
                    
                    kf = KalmanFilter(initial_x=0.0, initial_y=0.0, var_accel=var_accel, var_gps=0, R=R_calibree, dt_imu=0.01)
                    print(f"[KALMAN] Initialisé à l'origine GPS: Lat={lat_origin}, Lon={lon_origin}")
                    continue
                
                # 2. Mise à jour (Update)
                x, y = gps_to_local_meters(lat, lon, lat_origin, lon_origin)
                
                # Filtre anti-téléportation
                if abs(x) > 1000 or abs(y) > 1000:
                    continue
                    
                _, accepted = kf.update(x, y)
                
                if not accepted:
                    print("[KALMAN] Anomalie GPS ignorée (Rejet par Mahalanobis)")
                
                # Sauvegarde temps réel
                state = kf.get_state()
                fusion_lat, fusion_lon = local_meters_to_gps(state['x'], state['y'], lat_origin, lon_origin)
                writer.writerow([f"{current_time:.3f}", f"{state['x']:.4f}", f"{state['y']:.4f}", f"{fusion_lat:.8f}", f"{fusion_lon:.8f}"])
                f.flush() # Force l'écriture sur le disque
                print(f"[KALMAN] Mise à jour GPS traitée.")

            elif event_type == 'IMU':
                _, current_time, ax, ay = event
                
                if kf is not None:
                    dt = current_time - last_time
                    if dt <= 0.0001:
                        dt = 0.0001
                        
                    kf.predict(ax, ay, dt)
                    last_time = current_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode", "-m",
        type=str,
        choices=GNSS_MODES.keys(),
        default=MODE_GNSS,
        help="Mode GNSS à utiliser"
    )

    parser.add_argument(
        "--save-path", "-s",
        type=str,
        default="data",
        help="Dossier de sauvegarde (les fichiers seront séparés)"
    )

    parser.add_argument(
        "--display-LCD",
        action="store_true",
        help="Affiche la position sur le LCD"
    )

    args = parser.parse_args()

    # Création du dossier si nécessaire
    os.makedirs(args.save_path, exist_ok=True)

    imu_file = os.path.join(args.save_path, "imu_data.csv")
    gps_file = os.path.join(args.save_path, "gps_data.csv")

    # File d'attente (Queue) partagée pour la fusion temps réel
    sensor_queue = queue.Queue()

    # Création des threads
    imu_thread = threading.Thread(target=run_imu, args=(imu_file, sensor_queue))
    gps_thread = threading.Thread(target=run_gps, args=(args.mode, gps_file, args.display_LCD, sensor_queue))
    kalman_thread = threading.Thread(target=run_kalman, args=(sensor_queue, args.save_path))
    
    kalman_thread.daemon = True # Pour qu'il s'arrête si le Main Thread s'arrête

    # Lancement
    imu_thread.start()
    gps_thread.start()
    kalman_thread.start()

    # Attente de fin
    imu_thread.join()
    gps_thread.join()
