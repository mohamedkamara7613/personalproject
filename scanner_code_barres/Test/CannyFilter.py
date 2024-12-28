# -*- coding: utf-8 -*-


import cv2

img = cv2.imread("img/original_oblic_resized.jpg", 1) # Lecture en BGR not in GBR

# resize image fois 10, ne garde pas une bonne qualité de l'image
#img = cv2.resize(img, (0,0), fx=10, fy=10)

# resize image fois 10, gardant une bonne qualité de l'image
#img = cv2.resize(img, (0,0), fx=10, fy=10, interpolation=cv2.INTER_CUBIC)



# Appliquer le filtre canny
canny = cv2.Canny(img, 100, 200) # min, max

cv2.imwrite("img_canny.jpg", canny)


