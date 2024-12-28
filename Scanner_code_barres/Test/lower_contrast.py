import cv2


# Charger l'image en niveaux de gris
image = cv2.imread("img/img2.jpg", cv2.IMREAD_GRAYSCALE)

# Diminuer le contraste
alpha = 0.5  # Facteur de contraste (entre 0 et 1 pour diminuer)
beta = 128 * (1 - alpha)  # Pour centrer les valeurs autour de 128

low_contrast_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

cv2.imwrite("img/low_contrast_img.jpg", low_contrast_image)