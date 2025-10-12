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


with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while True:
        success, frame = cap.read()
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
            distance_index = distance((index_x_px, index_y_px), (thumb_x_px, thumb_y_px))
            distance_middle = distance((middle_x_px, middle_y_px), (thumb_x_px, thumb_y_px))
            distance_ring = distance((ring_x_px, ring_y_px), (thumb_x_px, thumb_y_px))
            distance_pinky = distance((pinky_x_px, pinky_y_px), (thumb_x_px, thumb_y_px))

            # si la distance est inferieure a un certain seuil, on affiche "Pinch"
            if distance_index < seuil:
                # Appliquer le filtre Canny au frame
                frame = apply_canny(frame)
                
            if distance_middle < seuil:
                # filtre negatif
                frame = apply_negatif(frame)

            if distance_ring < seuil:
                # filtre sepia
                frame = apply_cartoon(frame)
                
            if distance_pinky < seuil:
                # Gaussian Blur
                frame = apply_blur(frame)

                
        # Display the frame
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()


# -----------------------------------------------------------
