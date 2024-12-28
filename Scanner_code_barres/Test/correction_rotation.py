import cv2
import numpy as np
import sys
import os

# Ajouter le dossier parent au chemin d'importation
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import pre_processing # module externe




original_img_path = "img/original_oblic_resized.jpg" #original_oblic_resized


def correction_rotation(gray_img):
    """
    NOTION CLE : filtre CANNY et TRANSFORMÉE DE HOUGH
    Correction de la rotation de l'image
        - filtre canny
        - detection de ligne avec hough
        - calcul de l'angle de rotation
        - appliquer la correction a l'image originale
    """
    # Filtre Canny
    canny_img = cv2.Canny(gray_img, 100, 200)

    # Detection avec HOUGH
    lines = cv2.HoughLines(canny_img, 1, np.pi / 180, 200)

    if lines is None:
        # Si aucune ligne n'est détectée, retourne l'image d'origine
        return gray_img

    # Calculer l'angle moyen des lignes détectées
    angle_sum = 0
    count = 0
    for line in lines:
        # rho : La distance entre l'origine de l'image (le point (0,0)) et la ligne.
        # theta : L'angle entre l'axe horizontal (l'axe des x) et la ligne.
        for rho, theta in line:  
            angle = (theta * 180 / np.pi)  # Convertir l'angle en degrés
            # Ignorer les lignes quasi-verticales pour éviter de fausser l'angle moyen
            if -85 < angle < 85:
                angle_sum += angle
                count += 1

    if count > 0:
        average_angle = angle_sum / count
    else:
        # Si toutes les lignes détectées étaient quasi-verticales, ignorer la rotation
        average_angle = 0

    # Redresser l'image en fonction de l'angle moyen
    (h, w) = gray_img.shape[:2]
    center = (w // 2, h // 2)

    # Création de la matrice de rotation
    rotation_matrix = cv2.getRotationMatrix2D(center, average_angle, 1.0)

    # Application de la convolution (rotation)
    straightened_img = cv2.warpAffine(gray_img, rotation_matrix, (w, h))

    return straightened_img



img_result = correction_rotation(pre_processing.import_image(original_img_path))

#edges = cv2.cvtColor(cv2.imread(original_img_path, 1), cv2.COLOR_BGR2GRAY)

#img_result = correction_rotation(edges)

cv2.imwrite("img/rotated_img.jpg", img_result)