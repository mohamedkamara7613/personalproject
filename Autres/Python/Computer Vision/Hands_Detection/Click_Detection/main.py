# -*- coding: utf-8 -*-

import cv2
import mediapipe as mp

# -----------------------------------------------------------
def get_coord_px_tip_and_circle(code_tip, hand, w, h, color=(0,255,0), radius=10):
    hand_tip = hand.landmark[code_tip]
    x_px = int(hand_tip.x * w)
    y_px = int(hand_tip.y * h)

    cv2.circle(frame, (x_px, y_px), radius, color, -1)
    return x_px, y_px


# ---------------------------------------------------------------
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

seuil = 40  # seuil de distance pour détecter le "pinch"


with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while True:
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        w, h, c = frame.shape
        
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_RGB)
        
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            # on s'interrese a 8 et 4
            # recuperation des coordonnées
            index_x_px, index_y_px = get_coord_px_tip_and_circle(8, hand, h, w, color=(0,0,255), radius=15)
            thumb_x_px, thumb_y_px = get_coord_px_tip_and_circle(4, hand, h, w, color=(255,0,0), radius=15)
            
            # Calcul de la distance entre les deux points (euclidienne)
            distance = ((index_x_px - thumb_x_px) ** 2 + (index_y_px - thumb_y_px) ** 2) ** 0.5
            cv2.putText(frame, f"Distance: {int(distance)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # si la distance est inferieure a un certain seuil, on affiche "Pinch"
            if distance < seuil:
                cv2.putText(frame, "Pinch", (index_x_px, index_y_px - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Display the frame
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()