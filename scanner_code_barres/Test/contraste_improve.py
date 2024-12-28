import cv2
import numpy as np
import sys
import os

# Ajouter le dossier parent au chemin d'importation
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import pre_processing # module externe


original_img_path = "img/img2.jpg" #original_oblic_resized


def contrast_improve(gray_img):
    """
        Par la technique de normalisation de l'histogramme
    """

    normalized_img = cv2.equalizeHist(gray_img)

    return normalized_img


result_img = contrast_improve(pre_processing.import_image(original_img_path))

cv2.imwrite("img/contrasted_img.jpg", result_img)