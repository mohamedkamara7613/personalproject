
import cv2
import numpy as np

original_img_path = "img/temp_result.jpg" #original_oblic_resized


gray_img = cv2.cvtColor(cv2.imread(original_img_path, 1), cv2.COLOR_BGR2GRAY)




# Détecteur de segments de ligne LSD
lsd = cv2.createLineSegmentDetector(0)
lines = lsd.detect(gray_img)[0]  # Renvoie les lignes détectées

# Dessiner les lignes détectées
output_img = np.zeros_like(gray_img)
output_img = lsd.drawSegments(output_img, lines)

cv2.imwrite("img/lsd_img.jpg", output_img)