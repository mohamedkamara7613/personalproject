"""
Script de capture photo déclenchée par détection de main (Mediapipe) ou bouton.
Tourne en tâche de fond sur le Raspberry Pi.
"""

import cv2
import time
import os
import csv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import math

# --- Configuration ---
ENABLE_DISPLAY = True   # Mettre à False sur le Raspberry Pi en marche (Headless)
COOLDOWN_SECONDS = 3.0  # Délai minimum entre deux photos
BUTTON_PIN = 2          # Pin GPIO du bouton poussoir
PINCH_THRESHOLD = 0.05  # Seuil de distance pour valider le pincement (entre 0.02 et 0.08)

# --- Initialisation du bouton GPIO (sécurisée pour test sur PC) ---
try:
    from gpiozero import Button
    button = Button(BUTTON_PIN)
    BUTTON_ENABLED = True
    print("Bouton physique détecté.")
except Exception as e:
    print("Avertissement : Librairie gpiozero non disponible (normal si vous êtes sur un PC). Le bouton physique est désactivé.")
    BUTTON_ENABLED = False
    button = None


def loop_capture():
    # 1. Initialisation Mediapipe (Nouvelle API Tasks compatible Python 3.12)
    model_path = os.path.join(os.path.dirname(__file__), 'hand_landmarker.task')
    if not os.path.exists(model_path):
        print(f"Erreur: Le modèle IA '{model_path}' est introuvable.")
        print("Veuillez le télécharger avec la commande :")
        print("wget -qO feature_cartographie/hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")
        return

    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
    detector = vision.HandLandmarker.create_from_options(options)
    
    # 2. Initialisation Caméra
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la caméra.")
        return
        
    # 3. Préparation des dossiers et fichiers
    os.makedirs("photos", exist_ok=True)
    csv_file = "photos_log.csv"
    
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Filename"])
            
    last_capture_time = 0
    timer_started = False
    timer_start_time = 0
    print("Prêt. En attente d'une main ou du bouton...")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # --- Correction de l'effet miroir ---
            frame = cv2.flip(frame, 1)
                
            current_time = time.time()
            trigger_intent = False
            
            # --- Test 1 : Le Bouton Poussoir ---
            if BUTTON_ENABLED and button.is_pressed:
                trigger_intent = True
                
            # --- Test 2 : Intelligence Artificielle (Mediapipe Tasks API) ---
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
            detection_result = detector.detect(mp_image)
            
            if detection_result.hand_landmarks:
                for hand_landmarks in detection_result.hand_landmarks:
                    thumb_tip = hand_landmarks[4]
                    index_tip = hand_landmarks[8]
                    
                    # Calcul de la distance 3D euclidienne entre les deux bouts de doigts
                    dist = math.sqrt((thumb_tip.x - index_tip.x)**2 + 
                                     (thumb_tip.y - index_tip.y)**2 + 
                                     (thumb_tip.z - index_tip.z)**2)
                                     
                    if dist < PINCH_THRESHOLD:
                        trigger_intent = True
                        break
                        
            # --- Gestion du Décompte de 2 secondes ---
            if trigger_intent and not timer_started and (current_time - last_capture_time > COOLDOWN_SECONDS):
                timer_started = True
                timer_start_time = current_time
                print("[TIMER] Déclencheur activé ! Photo dans 2 secondes...")
                
            take_photo_now = False
            if timer_started:
                time_elapsed = current_time - timer_start_time
                if time_elapsed >= 2.0:
                    take_photo_now = True
                    timer_started = False  # Reset
                elif ENABLE_DISPLAY:
                    # Affichage visuel du décompte
                    countdown = int(math.ceil(2.0 - time_elapsed))
                    cv2.putText(frame, f"Photo dans {countdown}s", (20, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3, cv2.LINE_AA)

            # --- Sauvegarde de la Photo ---
            if take_photo_now:
                timestamp_str = f"{current_time:.3f}"
                filename = f"photos/photo_{timestamp_str}.jpg"
                
                # Sauvegarde de l'image sur la carte SD
                cv2.imwrite(filename, frame)
                
                # Inscription dans le journal
                with open(csv_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp_str, filename])
                    
                print(f"[{timestamp_str}] [CAPTURE] Clic ! Photo sauvegardée : {filename}")
                last_capture_time = current_time
                
            # --- Affichage GUI (si activé) ---
            if ENABLE_DISPLAY:
                # Dessiner le squelette de la main pour le fun/debug
                if detection_result.hand_landmarks:
                    for hand_landmarks in detection_result.hand_landmarks:
                        for landmark in hand_landmarks:
                            x = int(landmark.x * frame.shape[1])
                            y = int(landmark.y * frame.shape[0])
                            cv2.circle(frame, (x, y), 3, (255, 0, 255), -1)
                            
                cv2.imshow("Camera IA - Appuyez sur 'q' pour quitter", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
    finally:
        # Libération propre du matériel
        cap.release()
        if ENABLE_DISPLAY:
            cv2.destroyAllWindows()

if __name__ == "__main__":
    loop_capture()
