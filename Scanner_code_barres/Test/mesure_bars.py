import numpy as np
import cv2

original_img_path = "img/window/ft_segment_100.jpg" #original_oblic_resized


window = cv2.cvtColor(cv2.imread(original_img_path, 1), cv2.COLOR_BGR2GRAY)


def measure_bars_in_window(window):
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

    # Retourner les largeurs des barres et espaces
    return bar_widths


def normalize_bar_widths(bar_widths):
    # Trouver l'unité de base comme le plus petit élément non nul
    unit_base = min([w for w in bar_widths if w > 0])
    
    # Normaliser chaque largeur en arrondissant au multiple le plus proche de l'unité de base
    normalized_widths = [round(width / unit_base) for width in bar_widths]
    
    return normalized_widths



# Mesurer les barres dans la fenêtre
bar_widths = measure_bars_in_window(window)
print("Largeurs des barres et espaces : ", bar_widths)  


normalized_widths = normalize_bar_widths(bar_widths)
print("Largeurs normalisées :", normalized_widths)