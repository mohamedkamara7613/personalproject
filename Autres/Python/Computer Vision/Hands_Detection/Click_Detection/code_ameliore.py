# -*- coding: utf-8 -*-

import cv2
import mediapipe as mp
import numpy as np

# Couleurs
VERT = (0, 255, 0)
ROUGE = (0, 0, 255)
BLEU = (255, 0, 0)
JAUNE = (0, 255, 255)
MAGENTA = (255, 0, 255)
CYAN = (255, 255, 0)
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)


# -----------------------------------------------------------
def get_coord_px_tip_and_circle(code_tip, hand, h, w, color=(0,255,0), radius=10):
    hand_tip = hand.landmark[code_tip]
    x_px = int(hand_tip.x * w)
    y_px = int(hand_tip.y * h)

    cv2.circle(frame, (x_px, y_px), radius, color, -1)
    #cv2.putText(frame, f"Distance Index: {int(distance_index)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    return x_px, y_px

def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def apply_canny(frame):
    return cv2.Canny(frame, 100, 200)

def apply_negatif(frame):
    return cv2.bitwise_not(frame)

def apply_sepia(frame):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    frame_sepia = cv2.transform(frame, kernel)
    return np.clip(frame_sepia, 0, 255).astype(np.uint8)

def apply_blur(frame):
    return cv2.GaussianBlur(frame, (41, 41), 0)

def apply_cartoon(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(frame, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

# ---------------------------------------------------------------
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

seuil = 40  # seuil de distance pour détecter le "pinch"

# Initialisation des distances
distance_index, distance_middle, distance_ring, distance_pinky = 1000, 1000, 1000, 1000
distances = {
    'index': distance_index,
    'middle': distance_middle,
    'ring': distance_ring,
    'pinky': distance_pinky
}

# ordre de priorité
priorite = ['index', 'middle', 'ring', 'pinky']

# filtre correspondant à chaque doigt
filtres = {
    'index': apply_canny,
    'middle': apply_negatif,
    'ring': apply_sepia,
    'pinky': apply_cartoon
}

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while True:
        success, frame = cap.read()
        if success and frame is None:
            print("Ignoring empty camera frame.")
            continue
        
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_RGB)
        
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            # on s'interrese a 4, 8, 12, 16, 20 (thumb, index, middle, ring, pinky)
            # recuperation des coordonnées
            index_x_px, index_y_px = get_coord_px_tip_and_circle(8, hand, h, w, color=ROUGE, radius=15)
            thumb_x_px, thumb_y_px = get_coord_px_tip_and_circle(4, hand, h, w, color=BLEU, radius=15)
            middle_x_px, middle_y_px = get_coord_px_tip_and_circle(12, hand, h, w, color=VERT, radius=15)
            ring_x_px, ring_y_px = get_coord_px_tip_and_circle(16, hand, h, w, color=JAUNE, radius=15)
            pinky_x_px, pinky_y_px = get_coord_px_tip_and_circle(20, hand, h, w, color=MAGENTA, radius=15)

            # Calcul des distances entre chaque doigt et le pouce (euclidienne)
            distances["index"] = distance((index_x_px, index_y_px), (thumb_x_px, thumb_y_px))
            distances["middle"] = distance((middle_x_px, middle_y_px), (thumb_x_px, thumb_y_px))
            distances["ring"] = distance((ring_x_px, ring_y_px), (thumb_x_px, thumb_y_px))
            distances["pinky"] = distance((pinky_x_px, pinky_y_px), (thumb_x_px, thumb_y_px))

            # si la distance est inferieure a un certain seuil, on affiche "Pinch"
            for doigt in priorite:
                if distances[doigt] < seuil:
                    # application du filtre correspondant
                    frame = filtres[doigt](frame)
                    break  # pour ne traiter qu'un seul doigt à la fois

                
        # Display the frame
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()


# -----------------------------------------------------------
