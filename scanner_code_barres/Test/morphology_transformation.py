import cv2
import numpy as np


# charger l'image
black_and_white_img = cv2.imread("img/black_and_white_img2.jpg")

# Opérations morphologiques (dilatation et érosion)
kernel = np.ones((3, 3), np.uint8)
dilated = cv2.dilate(black_and_white_img, kernel, iterations=1)
eroded = cv2.erode(dilated, kernel, iterations=1)