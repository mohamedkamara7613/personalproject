# -*- coding: utf-8 -*-
"""
    KAMARA Mohamed

        pre-processing.py 21/10/24

    Descripition : CONTIENT TOUTES LES FONCTIONS NECESSAIRES POUR L'ANALYSE DES CODES BARRES

    Ce programme est utilisé pour lire un code barre et afficher le résultat
"""

import cv2
import numpy as np



# ###########################################################################################################
# ETAPE 3 : Analyse des codes barres
# ###########################################################################################################
"""
    Mesure des barres et des espaces a partir de l'image "propre" :
    

"""

def measure_bars_in_window(window):
    print(" --------- BARS MEASURE ---------")
    # Étape 1 : Calcul de la moyenne d'intensité pour chaque colonne de la fenêtre
    profile = np.mean(window, axis=0)  # Projection horizontale moyenne

    # Étape 2 : Binarisation du profil (e.g., par méthode de Otsu)
    _, binary_profile = cv2.threshold(profile.astype(np.uint8), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Étape 3 : Calcul des largeurs des barres et des espaces
    bar_widths = []  # Liste pour stocker les largeurs des barres et espaces
    current_width = 1
    for i in range(1, len(binary_profile)):
        # Si une transition est détectée (de 0 à 255 ou de 255 à 0)
        if binary_profile[i] != binary_profile[i - 1]:
            bar_widths.append(current_width)
            current_width = 1  # Réinitialiser la largeur pour la prochaine barre/zone
        else:
            current_width += 1  # Incrémenter la largeur de la barre/zone en cours

    # Ajouter la dernière largeur mesurée
    bar_widths.append(current_width)
    print("--------- NORMALIZATION ---------")
    # normalize_bar_widths(bar_widths)
    # Trouver l'unité de base comme le plus petit élément non nul
    unit_base = min([w for w in bar_widths if w > 0])
    
    # Normaliser chaque largeur en arrondissant au multiple le plus proche de l'unité de base
    normalized_widths = [round(width / unit_base) for width in bar_widths]
    
    # Retourner les largeurs des barres et espaces
    return normalized_widths

def decode_ean13_barcode(widths):
    pass


def analyse_code_barre(bars_zones_images):
    def detect_contours(img):
        # Détection des contours
        # RETR_EXTERNAL, RETR_LIST, RETR_CCOMP, RETR_TREE
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

        pass

    def detect_codes_barres(img):
        pass
"""

"""