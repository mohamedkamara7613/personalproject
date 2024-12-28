# -*- coding: utf-8 -*-
"""
    KAMARA Mohamed

        lecteur_code_barre_VO.py 09/10/24

    Descripition : VERSION DU PROGRAMME SUR UN CAS DE BASE SANS TROP DE PROBLEME

    Ce programme est utilisé pour lire un code barre et afficher le résultat
"""

# Import
import pre_processing # module externe
import analyse_decode_bars # module externe
import cv2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

original_img_path = "test0.jpg" # original_oblic_resized

img = pre_processing.import_image(original_img_path)

#processed_img = pre_processing.image_preprocessing(img)

bars_zones_images = pre_processing.image_preprocessing(img)

for bars_zone_img in bars_zones_images:
    # le retour de l'analyse
    normalized_bars_widths =  analyse_decode_bars.measure_bars_in_window(bars_zones_images) # liste de la dimension des barres detectés

    # le retour de la conversion
    code_barre = analyse_decode_bars.decode_ean13_barcode(normalized_bars_widths)

    # verification du resultat, le retour de la fonction qui va verifier si le code est bon
    code_valid = False 

# TEMP
#cv2.imwrite("temp_result.jpg", bars_zones_images)


