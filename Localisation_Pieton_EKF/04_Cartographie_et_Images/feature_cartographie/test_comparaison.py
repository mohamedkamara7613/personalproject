#!/usr/bin/env python3
"""
test_comparaison.py — Test de Comparaison d'Images avec ORB (OpenCV)
-----------------------------------------------------------------------
Usage : python3 test_comparaison.py

  C       → Capturer l'image de référence (ou la remplacer)
  Q       → Quitter

L'algorithme ORB est invariant à la rotation et partiellement aux 
changements d'échelle et de lumière. Il compte les "points d'intérêts" 
communs entre la caméra en direct et l'image de référence.
"""

import cv2
import numpy as np
import os

# ── Configuration ──────────────────────────────────────────────────────────────
REF_IMAGE_PATH = "reference.jpg"
MIN_MATCH_COUNT = 30     # Nombre de correspondances requises pour valider
ORB_FEATURES = 1000      # Nombre max de points détectés par ORB
MAX_DISTANCE = 50        # Distance de Hamming max pour qu'un "Match" soit bon

def main():
    cap = cv2.VideoCapture(0)
    
    # Création du détecteur ORB
    orb = cv2.ORB_create(nfeatures=ORB_FEATURES)
    # Matcher Brute-Force adapté aux descripteurs binaires comme ORB
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    img_ref = None
    kp_ref = None
    des_ref = None
    
    # Chargement de la référence si elle existe déjà
    if os.path.exists(REF_IMAGE_PATH):
        img_ref = cv2.imread(REF_IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
        kp_ref, des_ref = orb.detectAndCompute(img_ref, None)
        print(f"[✓] Image de référence chargée avec {len(kp_ref)} points-clés.")
    
    print("\n╔══════════════════════════════════════════╗")
    print("║   Test OpenCV — Comparaison d'images    ║")
    print("╠══════════════════════════════════════════╣")
    print("║  C      → capturer une REFERENCE         ║")
    print("║  Q      → quitter                        ║")
    print("╚══════════════════════════════════════════╝\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[✗] Erreur de lecture webcam.")
            break
            
        display = frame.copy()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # --- UI Instructions ---
        cv2.putText(display, "C: Capturer Ref  |  Q: Quitter", (10, 25), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        if img_ref is None:
            cv2.putText(display, "Aucune reference. Appuyez sur 'C' !", (10, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            # 1. Calcul des points de la webcam en direct
            kp_frame, des_frame = orb.detectAndCompute(gray_frame, None)
            
            # 2. Comparaison (Matching)
            if des_frame is not None and len(des_frame) > 0 and des_ref is not None and len(des_ref) > 0:
                matches = bf.match(des_ref, des_frame)
                
                # Filtrer pour ne garder que les très bonnes correspondances
                good_matches = [m for m in matches if m.distance < MAX_DISTANCE]
                match_count = len(good_matches)
                
                # 3. Affichage du résultat
                color = (0, 255, 0) if match_count >= MIN_MATCH_COUNT else (0, 0, 255)
                text = f"Points communs : {match_count} / {MIN_MATCH_COUNT}"
                cv2.putText(display, text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                if match_count >= MIN_MATCH_COUNT:
                    cv2.putText(display, "MATCH REUSSI !", (10, 100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                                
                    # Dessiner les cadres de quelques points qui matchent pour effet visuel
                    for m in good_matches[:10]:
                        pt = kp_frame[m.trainIdx].pt
                        cv2.circle(display, (int(pt[0]), int(pt[1])), 4, (0, 255, 0), 1)

        cv2.imshow("Test Comparaison ORB", display)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("[…] Fermeture.")
            break
        elif key == ord('c'):
            print("\n─── Nouvelle Référence Capturée ───")
            cv2.imwrite(REF_IMAGE_PATH, gray_frame)
            img_ref = gray_frame
            kp_ref, des_ref = orb.detectAndCompute(img_ref, None)
            print(f"Points-clés détectés sur la référence : {len(kp_ref)}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
