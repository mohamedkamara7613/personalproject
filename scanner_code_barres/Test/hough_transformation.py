import cv2
import numpy as np
import sys
import os

# Ajouter le dossier parent au chemin d'importation
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)




original_img_path = "img/window/window_400.jpg" #original_oblic_resized

edges = cv2.cvtColor(cv2.imread(original_img_path, 1), cv2.COLOR_BGR2GRAY)
cv2.imwrite("img1.jpg", edges)


edges = cv2.Canny(edges, 100, 200)
cv2.imwrite("img2.jpg", edges)

#_, black_and_white_img = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
negative = cv2.bitwise_not(edges)
cv2.imwrite("img3.jpg", negative)



lines = cv2.HoughLines(negative, 1, np.pi / 180, 200)
#lines = cv2.HoughLinesP(negative, 1, np.pi / 180, threshold=200, minLineLength=100, maxLineGap=10)

output_image = np.zeros_like(edges)
if lines is not None:
    for line in lines:
        for rho, theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * a)
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * a)
            cv2.line(output_image, (x1, y1), (x2, y2), (255, 255, 255), 2)
else:
    print("Pas de lignes trouvées")
    
# Enregistrer la fenetre la fenêtre
cv2.imwrite("img/hough_img.jpg", output_image)


