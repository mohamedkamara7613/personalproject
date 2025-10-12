import cv2
import mediapipe as mp




cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7) as hands:
    while True:
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_RGB)
        
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)
        
        
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()