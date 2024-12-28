import cv2
import numpy as np

image = cv2.cvtColor(cv2.imread("img/img2.jpg", 1), cv2.COLOR_BGR2GRAY)

def add_salt_and_pepper_noise(image, salt_prob=0.05, pepper_prob=0.05):
    noisy_image = image.copy()
    # Ajouter des pixels blancs (sel)
    num_salt = np.ceil(salt_prob * image.size)
    coords = tuple([np.random.randint(0, i - 1, int(num_salt)) for i in image.shape])
    noisy_image[coords] = 255

    # Ajouter des pixels noirs (poivre)
    num_pepper = np.ceil(pepper_prob * image.size)
    coords = tuple([np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape])
    noisy_image[coords] = 0

    return noisy_image

# modele pour la binarisation
gradient = np.linspace(0, 255, 256).astype(np.uint8)
gradient_image = np.tile(gradient, (256, 1))

noisy_image = add_salt_and_pepper_noise(image)
cv2.imwrite("img/noisy_img.jpg", noisy_image)
cv2.imwrite("img/model_binarisation.jpg", gradient_image)
