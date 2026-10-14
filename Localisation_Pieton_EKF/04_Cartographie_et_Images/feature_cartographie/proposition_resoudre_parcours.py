import folium
import queue
import threading
import numpy as np
import time
import os
import subprocess

from geopy.distance import geodesic

from config.constants import GNSS_MODES, PORT_BUTTON, LSM6DSO_ADDR
from config.parameters import MODE_GNSS, ACCEL_FREQ, ACCEL_RANGE, GYRO_RANGE, GYRO_FREQ
from core.gnss_position import gnss_position
from core.kalman import KalmanFilter
from core.gps_utils import gps_to_local_meters, local_meters_to_gps
from core.imu_acquisition import get_imu_data
from utils.Button import Button
import webbrowser

# --- NOUVEAU : Import de ton comparateur d'image ---
# En supposant que le collègue mette ton image_comparator.py dans le dossier "core"
from core.image_comparator import ImageComparator

R_matrix = np.array([
    [0.00799, -0.00226],
    [-0.00226, 0.00343]
])

last_kalman_pos = {"lat": None, "lon": None}
origin = {"lat": None, "lon": None}
shared_queue = queue.Queue()

# --- NOUVEAU : Initialisation de ton comparateur ---
comparateur = ImageComparator()

def charger_parcours(fichier):
    checkpoints = []
    with open(fichier,"r") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            image, lat, lon = ligne.strip().split(";")
            checkpoints.append({
                "image":image,
                "lat":float(lat),
                "lon":float(lon),
                "validé":False
            })
    return checkpoints

def generer_carte(checkpoints, fichier_html="parcours_map.html"):
    carte = folium.Map(location=[checkpoints[0]["lat"],checkpoints[0]["lon"]], zoom_start=18)
    for i, cp in enumerate(checkpoints):
        popup_html = f'<img src="{cp["image"]}" width="200px"><br>Checkpoint {i+1}'
        folium.Marker(
            location=[cp["lat"],cp["lon"]],
            popup=folium.Popup(popup_html,max_width=250),
            tooltip=f"Checkpoint {i+1}"
        ).add_to(carte)
    carte.save(fichier_html)
    print(f"Carte dispo ici : {fichier_html}")

def run_fusion(shared_queue):
    global last_kalman_pos, origin
    kf = None
    while True:
        try:
            msg = shared_queue.get(timeout=0.1)
            sensor_type = msg[0]

            if sensor_type == 'GPS':
                lat, lon = msg[2], msg[3]
                if origin["lat"] is None:
                    origin["lat"] = lat
                    origin["lon"] = lon
                    kf = KalmanFilter(
                        initial_x=0.0, initial_y=0.0,
                        dt_imu=1.0/ACCEL_FREQ,
                        var_accel=0.5,
                        var_gps=0.00779,
                        R=R_matrix
                    )
                    print("[FUSION] Origine fixée, Kalman initialisé.")
                    continue

                x, y = gps_to_local_meters(lat, lon, origin["lat"], origin["lon"])
                kf.update(x, y)

            elif sensor_type == 'IMU' and kf is not None:
                ax, ay = msg[2], msg[3]
                kf.predict(ax, ay)

            if kf is not None:
                state = kf.get_state()
                lat_est, lon_est = local_meters_to_gps(
                    state["x"], state["y"],
                    origin["lat"], origin["lon"]
                )
                last_kalman_pos["lat"] = lat_est
                last_kalman_pos["lon"] = lon_est

        except queue.Empty:
            continue

# --- NOUVEAU : Fonction pour prendre la photo ---
def prendre_photo(filepath):
    print("📸 Capture en cours...")
    try:
        subprocess.run(["libcamera-still", "-o", filepath, "--immediate", "--nopreview"], check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"❌ Erreur caméra : {e}")
        return False

def verifier_checkpoint(checkpoints):
    if last_kalman_pos["lat"] is None:
        print("❌ Pas de position disponible.")
        return

    for i, cp in enumerate(checkpoints):
        if cp["validé"]:
            continue

        distance = geodesic(
            (last_kalman_pos["lat"], last_kalman_pos["lon"]),
            (cp["lat"], cp["lon"])
        ).meters

        if distance < 10:
            print(f"📍 Position validée (distance: {distance:.1f}m) ! Prise de photo...")
            
            # --- NOUVEAU : L'intégration de ton code ORB ---
            photo_temp = "photo_verif_temp.jpg"
            if prendre_photo(photo_temp):
                print("🔍 Analyse de l'image (ORB)...")
                resultat = comparateur.compare(ref_image_input=cp["image"], test_image_input=photo_temp)
                
                if resultat["match"]:
                    cp["validé"] = True
                    print(f"✅ Checkpoint {i+1} validé ! (Match visuel parfait, Score: {resultat['score']})")
                    
                    restants = sum(1 for cp in checkpoints if not cp["validé"])
                    if restants == 0:
                        print("🎉 Tous les checkpoints validés ! Tu as gagné !")
                    else:
                        print(f"Il reste {restants} checkpoint(s).")
                else:
                    print(f"❌ Ce n'est pas le bon objet (Score: {resultat['score']}). Retentez !")
            return

    print(f"❌ Aucun checkpoint à proximité (vous êtes trop loin).")


if __name__ == "__main__":
    checkpoints = charger_parcours("parcours.txt")
    generer_carte(checkpoints)
    webbrowser.open("parcours_map.html")

    t_gnss = threading.Thread(
        target=gnss_position,
        kwargs={"mode": GNSS_MODES[MODE_GNSS], "data_queue": shared_queue},
        daemon=True
    )

    t_imu = threading.Thread(
        target=get_imu_data,
        args=(LSM6DSO_ADDR, ACCEL_RANGE, ACCEL_FREQ, GYRO_RANGE, GYRO_FREQ),
        kwargs={"data_queue": shared_queue},
        daemon=True
    )

    t_fusion = threading.Thread(target=run_fusion, args=(shared_queue,), daemon=True)

    t_gnss.start()
    t_imu.start()
    t_fusion.start()

    button = Button(PORT_BUTTON)
    button.on_press(lambda: verifier_checkpoint(checkpoints))

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nArrêt du script.")
    finally:
        button.cleanup()
