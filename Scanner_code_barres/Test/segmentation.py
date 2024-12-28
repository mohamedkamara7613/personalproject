import cv2
import numpy as np
import sys
import os

# Ajouter le dossier parent au chemin d'importation
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import pre_processing # module externe


original_img_path = "img/temp_result.jpg" #original_oblic_resized

    
def detect_barcode_texture(gray_img, sign, factor, offset_1, offset_2, offset_3, offset_4):
    # Convertir l'image en niveaux de gris
    #gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    
    

    #print(f"-- sign: {sign} --- factor: {factor} --- offset_1: {offset_1} --- offset_2: {offset_2} --- offset_3: {offset_3} --- offset_4: {offset_4}")
    
    # Appliquer la transformée de Fourier
    f = np.fft.fft2(gray_img)
    fshift = np.fft.fftshift(f)
    
    # Calculer le spectre de fréquence
    magnitude_spectrum = sign * np.log(np.abs(fshift)) # Application d'un filtre passe haut

    # Calculer la moyenne du spectre de fréquence
    mean_magnitude = np.mean(magnitude_spectrum)
    
    # Définir le seuil comme un multiple de la moyenne
    threshold = mean_magnitude * factor  # Ajuste le facteur selon les résultats observés

    
    # Localiser des pics de fréquence caractéristiques des codes-barres
    # (paramètres à ajuster selon les caractéristiques de l'image)
    rows, cols = magnitude_spectrum.shape
    center_row, center_col = rows // 2, cols // 2
    freq_zone = magnitude_spectrum[center_row-offset_1:center_row+offset_2, center_col-offset_3:center_col+offset_4]  
    
    # Vérification si les pics sont présents dans la zone d'intérêt
    if np.mean(freq_zone) > threshold:  # Définir un seuil approprié
        return True
    else:
        print("Aucune zone de code-barres détectée")
        return False
    
def segmentation5(straightened_img):
    # Paramètres de la fenêtre
    window_height = 50  # Hauteur de la fenêtre mobile

    # Parametres #-2 1 30 30 10 10
    sign = -20
    factor = 1
    offset_1 = 30
    offset_2 = 30 # offset_2 doit etre >= offset_1
    offset_3 = 10
    offset_4 = 10

    # Obtenir les dimensions de l'image
    image_height, image_width = straightened_img.shape[:2]

    # Balayage vertical de l'image
    print(f"-- sign: {sign} --- factor: {factor} --- offset_1: {offset_1} --- offset_2: {offset_2} --- offset_3: {offset_3} --- offset_4: {offset_4}")
 
    for y in range(0, image_height - window_height, window_height): # 3eme position remplacer window_height par window_height // 2 pour le chevauchement
        # Définir la fenêtre de balayage
        window = straightened_img[y:y + window_height, 0:image_width]
        
        if detect_barcode_texture(window,  sign, factor, offset_1, offset_2, offset_3, offset_4):
            print(f"Zone contenant des barres détectée à partir de y = {y}")
            cv2.imwrite(f"img/window/ft_segment_{y}.jpg", window)
    return None


def segmentation4(straightened_img):
    print(" ------------------ SEGMENTATION TECHNIQUE 4")
    """
    Technique de segmentation avec échantillonnage multi-échelle.
    Objectif : réduire l'image par échelles successives et analyser les zones d'intérêt détectées.
    """
    # Paramètres de détection
    seuil_nombre_lignes = 2
    delta_angle = 60
    contrast_threshold = 100

    def calculate_contrast(window):
        min_val, max_val, _, _ = cv2.minMaxLoc(window)
        return max_val - min_val

    # Créer une pyramide d'image pour l'analyse multi-échelle
    pyramid_images = [straightened_img]
    for i in range(1, 4):  # Par exemple, 4 niveaux dans la pyramide
        reduced_img = cv2.pyrDown(pyramid_images[-1])
        pyramid_images.append(reduced_img)

    # Analyser chaque niveau de la pyramide
    for level, img in enumerate(pyramid_images[::-1]):  # Commence du plus bas vers le plus haut
        scale_factor = 2 ** (len(pyramid_images) - 1 - level)  # Facteur d'échelle pour chaque niveau
        image_height, image_width = img.shape[:2]
        window_height = max(20, 50 // scale_factor)  # Ajuster la hauteur de la fenêtre selon l'échelle

        for y in range(0, image_height - window_height, window_height):
            window = img[y:y + window_height, 0:image_width]
            output_img = np.zeros_like(window)
            contrast = calculate_contrast(window)

            # Détecteur de segments de ligne LSD
            lsd = cv2.createLineSegmentDetector(0)
            lines = lsd.detect(window)[0]
            vertical_lines = []

            if lines is not None:
                for line in lines:
                    angle = line[0][1] * 180 / np.pi
                    if abs(angle - 90) < delta_angle:
                        vertical_lines.append(line)

            # Condition pour marquer une zone comme code-barres potentielle
            if len(vertical_lines) > seuil_nombre_lignes and contrast > contrast_threshold:
                print(f"Zone contenant des barres détectée à échelle {scale_factor} au niveau y = {y * scale_factor}")
                
                # Reconstruire les coordonnées sur l'image d'origine
                scaled_window = cv2.resize(window, (image_width * scale_factor, window_height * scale_factor))
                output_img = lsd.drawSegments(scaled_window, np.array(vertical_lines))
                cv2.imwrite(f"img/window/scale_{scale_factor}_segments_{y}.jpg", output_img)
                
                # Optionnel : Arrêter l'analyse si une zone est confirmée pour réduire les calculs
                break


    # --------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------

def segmentation3(straightened_img):
    print(" ------------------ SEGMENTATION TECHNIQUE 3")
    """
        Technique 3 personalisée utilisée pour la segmentation
        
        - meme technique que la 1ere suaf pour l'echantillonange qui se fait par l'algorithme de dichotomie 
        sur la hauteur de l'image d'entrée
    
    """


    # Paramètres de détection
    seuil_nombre_lignes = 2
    delta_angle = 57  # Plage d'angle plus stricte pour identifier les lignes quasi-verticales
    contrast_threshold = 100
    window_height = 50  # Hauteur de la fenêtre mobile pour le balayage

    def calculate_contrast(window):
        min_val, max_val, _, _ = cv2.minMaxLoc(window)
        return max_val - min_val

    # Obtenir les dimensions de l'image
    image_height, image_width = straightened_img.shape[:2]

    # Fonction de segmentation par dichotomie
    def dichotomic_search(start_y, end_y):
        if start_y >= end_y:
            return
        
        # Déterminer le point médian
        mid_y = (start_y + end_y) // 2
        window = straightened_img[mid_y:mid_y + window_height, 0:image_width]
        output_img = np.zeros_like(window)
        contrast = calculate_contrast(window)

        # Détecteur de segments de ligne LSD
        lsd = cv2.createLineSegmentDetector(0)
        lines = lsd.detect(window)[0]
        vertical_lines = []

        if lines is not None:
            for line in lines:
                angle = line[0][1] * 180 / np.pi
                if abs(angle - 90) < delta_angle:
                    vertical_lines.append(line)

        # Vérification de la zone de code-barres
        if len(vertical_lines) > seuil_nombre_lignes and contrast > contrast_threshold:
            print(f"Zone contenant des barres détectée à partir de y = {mid_y}")
            output_img = lsd.drawSegments(output_img, np.array(vertical_lines))
            cv2.imwrite(f"img/window/dichotomic_search/dichotomic_segments_{mid_y}.jpg", output_img)

            # Appliquer la recherche dans les deux sous-segments autour de la détection
            dichotomic_search(start_y, mid_y)
            dichotomic_search(mid_y + window_height, end_y)
        else:
            print(f"Aucune zone détectée dans l'intervalle y = {start_y} à y = {end_y}")

    # Lancer la recherche dichotomique sur toute la hauteur de l'image
    dichotomic_search(0, image_height)

    # --------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------



def segmentation2(straightened_img):
    print(" ------------------ SEGMENTATION TECHNIQUE 2")
    """
        Technique 2  personalisée utilisée pour la segmentation
        Objectif : Determiner une zone probable de code barre

        - prend un echantillon au centre et de la largeur de l'image
    """

    # Obtenir les dimensions de l'image
    image_height, image_width = straightened_img.shape[:2]

    # Calcul des Dimensions de l'echantillon
    window_height = 50
    sample_top = (abs(image_height // 2) - (window_height // 2))
    sample_bottom = sample_top + window_height

    # Creation de l'echantillon
    window = straightened_img[sample_top:sample_bottom, 0:image_width]

    cv2.imwrite("img/window/V2_segments.jpg", window)


    # --------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------


def segmentation1(straightened_img):
    print(" ------------------ SEGMENTATION TECHNIQUE 1")
    """
        Technique 1 personalisée utilisé pour la segmentation
        Objectif : determiner les differentes zones potentielles de codes barres
        - Utilisation d'une fenetre de largeur la largeur de l'image d'entrée et de hauteur arbitraire
        - qui va balyer l'image de haut en bas
        - pour chaque fenetre on applique un detecteur de segment LSD (LineSegmentDetector)
        - on recupere les lignes detecter et par une condition suffisante on determine s'ils sont verticales
        - s'il y a assez de ligne verticales et que le contraste est assez elevé on suppose que cette 
            zone contient des codes barres
    
    """
    # PARAMETRE TRES IMPORTANTES INFLUENT GRANDEMENT SUR LA DETECTION DES LIGNES DROITES
    seuil_nombre_lignes = 2
    delta_angle = 60

    def calculate_contrast(window):
        # Calculer le contraste dans la fenêtre (différence entre le maximum et le minimum d'intensité)
        min_val, max_val, _, _ = cv2.minMaxLoc(window)
        contrast = max_val - min_val
        return contrast
    
    # Seuil de contraste à ajuster pour déterminer si une zone a un fort contraste
    contrast_threshold = 100  

    # Paramètres de la fenêtre
    window_height = 50  # Hauteur de la fenêtre mobile

    # Obtenir les dimensions de l'image
    image_height, image_width = straightened_img.shape[:2]

    # Balayage vertical de l'image
    for y in range(0, image_height - window_height, window_height):
        # Définir la fenêtre de balayage
        window = straightened_img[y:y + window_height, 0:image_width]
        output_img = np.zeros_like(window)

        # Calculer le contraste dans la fenêtre
        contrast = calculate_contrast(window)

        # Détecteur de segments de ligne LSD
        lsd = cv2.createLineSegmentDetector(0)
        lines = lsd.detect(window)[0]  # Renvoie les lignes détectées
        vertical_lines = []
        
        # Recuperation des lignes veriticales
        if lines is not None:
            # Vérifier si les lignes sont quasi-verticales
            for line in lines:
                angle = line[0][1] * 180 / np.pi
                if abs(angle - 90) < delta_angle:
                    vertical_lines.append(line)
        
        # Vérifier si la fenêtre contient à la fois des lignes verticales et un fort contraste
        if len(vertical_lines) > seuil_nombre_lignes and contrast > contrast_threshold:
            print(f"Zone contenant des barres détectée à partir de y = {y}")
            
            output_img = lsd.drawSegments(output_img, np.array(vertical_lines))
      
            # Enregistrer la fenetre (zone potentielle de code barre)
            cv2.imwrite(f"img/window/segments_{y}.jpg", output_img)

        else:
            print(f"Aucune zone détectée à y = {y}")



segmentation5(pre_processing.import_image(original_img_path))





"""
# VERIFICATION DE L'ESPACEMENT REGULIER DES LIGNES
distances = []
for i in range(1, len(vertical_lines)):
    # Distance horizontale entre les lignes (en pixels)
    rho1 = vertical_lines[i-1][0][0]
    rho2 = vertical_lines[i][0][0]
    distances.append(abs(rho2 - rho1))

# Vérifier si les écarts sont réguliers
if np.std(distances) < seuil_ecart:
    # Zone probablement contenant des codes-barres



"""