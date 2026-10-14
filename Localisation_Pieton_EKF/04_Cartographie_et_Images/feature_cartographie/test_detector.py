#!/usr/bin/env python3
"""
test_detector.py — Test MediaPipe Object Detection avec webcam laptop
-----------------------------------------------------------------------
Usage : python3 test_detector.py

  ESPACE  → capture le frame actuel et lance la détection
  Q       → quitter

Le modèle EfficientDet Lite0 (~5 Mo) est téléchargé automatiquement
au premier lancement.

Install :
    pip install mediapipe opencv-python
"""

import cv2
import os
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

# ── Configuration ──────────────────────────────────────────────────────────────

MODEL_PATH  = "efficientdet_lite0.tflite"
MODEL_URL   = (
    "https://storage.googleapis.com/mediapipe-models/"
    "object_detector/efficientdet_lite0/float32/1/efficientdet_lite0.tflite"
)
SCORE_THRESHOLD = 0.40   # seuil de confiance minimum
MAX_RESULTS     = 5      # nb max d'objets retournés par frame

# ── Utilitaires ────────────────────────────────────────────────────────────────

def download_model() -> None:
    if os.path.exists(MODEL_PATH):
        print(f"[✓] Modèle trouvé : {MODEL_PATH}")
        return
    print("[…] Téléchargement du modèle EfficientDet Lite0 (~5 Mo)…")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print(f"[✓] Modèle téléchargé : {MODEL_PATH}")


def draw_detections(frame, result) -> None:
    """Dessine les bounding boxes + labels directement sur frame (in-place)."""
    for det in result.detections:
        bb    = det.bounding_box
        x, y  = int(bb.origin_x), int(bb.origin_y)
        w, h  = int(bb.width),    int(bb.height)
        cat   = det.categories[0]
        label = f"{cat.category_name}  {cat.score:.0%}"

        # Bounding box verte
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 220, 0), 2)

        # Fond du label
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
        cv2.rectangle(frame, (x, y - th - 8), (x + tw + 6, y), (0, 220, 0), -1)

        # Texte du label
        cv2.putText(frame, label, (x + 3, y - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 1, cv2.LINE_AA)


def print_detections(result) -> None:
    """Affiche les détections dans le terminal."""
    if not result.detections:
        print("  ⚠  Aucun objet détecté — essaie de mieux cadrer l'objet.")
        return
    print(f"  {len(result.detections)} objet(s) détecté(s) :")
    for det in result.detections:
        cat = det.categories[0]
        print(f"    → {cat.category_name:<22s}  score = {cat.score:.1%}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    download_model()

    # Initialisation du détecteur MediaPipe
    options = vision.ObjectDetectorOptions(
        base_options=mp_python.BaseOptions(model_asset_path=MODEL_PATH),
        score_threshold=SCORE_THRESHOLD,
        max_results=MAX_RESULTS,
    )
    detector = vision.ObjectDetector.create_from_options(options)

    # Ouverture webcam (backend V4L2 explicite pour Linux)
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    if not cap.isOpened():
        print("[✗] Impossible d'ouvrir la webcam (index 0).")
        return

    # Chauffe la caméra — les premières frames sont noires
    print("[…] Initialisation caméra…")
    for _ in range(15):
        cap.read()
    print("[✓] Caméra prête")

    print("\n╔══════════════════════════════════════════╗")
    print("║   Test MediaPipe — Détection d'objets   ║")
    print("╠══════════════════════════════════════════╣")
    print("║  ESPACE → capturer & détecter            ║")
    print("║  Q      → quitter                        ║")
    print("╚══════════════════════════════════════════╝\n")

    last_result = None   # garde le dernier résultat pour l'affichage continu

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[✗] Erreur de lecture webcam.")
            break

        display = frame.copy()

        # Superpose les dernières détections sur le flux vidéo
        if last_result:
            draw_detections(display, last_result)

        # Overlay d'instructions
        cv2.putText(display, "ESPACE: detecter  |  Q: quitter",
                    (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                    (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Test MediaPipe — Object Detection", display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("[…] Fermeture.")
            break

        elif key == ord(' '):
            print("\n─── Détection sur capture ───")
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            last_result = detector.detect(mp_img)
            print_detections(last_result)

            # ── Conseil chasse au trésor ────────────────────────────────────
            # Note les noms exacts affichés : ce sont les classes COCO que tu
            # devras mettre dans objects.json pour la chasse.
            # Classes faciles à trouver à l'INSA :
            #   bottle, backpack, chair, laptop, bicycle, bench,
            #   cell phone, book, cup, fire hydrant, clock
            # ───────────────────────────────────────────────────────────────

    cap.release()
    cv2.destroyAllWindows()
    detector.close()


if __name__ == "__main__":
    main()