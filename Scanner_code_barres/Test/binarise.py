import cv2
import sys
import os

# Ajouter le dossier parent au chemin d'importation
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import pre_processing # module externe




original_img_path = "img/model_binarisation.jpg" #original_oblic


def binarise(gray_img):
    """ Applique une conversion en noir et blanc et une binarisation de l'image"""

    seuil = 127 # 255/2
    valeur_max = 255

    # Application du seuil fixé à 255/2 = 127
    #_, black_and_white_img = cv2.threshold(gray_img, seuil, valeur_max, cv2.THRESH_BINARY) 
    #black_and_white_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #filtered_img = cv2.bilateralFilter(gray_img, 9, 75, 75)
    #_, black_and_white_img = cv2.threshold(filtered_img, seuil, valeur_max, cv2.THRESH_BINARY)
    _, black_and_white_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return black_and_white_img


img_result = binarise(pre_processing.import_image(original_img_path))

cv2.imwrite("img/black_and_white_img.jpg", img_result)