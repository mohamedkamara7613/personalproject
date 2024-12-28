import PIL.Image as pili
import numpy as np

def overlay_images(background_array, overlay_array):
    # Extract the alpha channel (transparency) from the overlay image
    alpha_channel = overlay_array[:, :, 3]  # Assuming the image has an alpha channel

    # Create an alpha mask based on the transparency values
    alpha_mask = alpha_channel > 0

    # Create a copy of the background array to avoid modifying the original array
    result_array = np.copy(background_array)

    # Overlay the image on the background using the alpha mask
    result_array[alpha_mask] = overlay_array[alpha_mask, :3]

    return result_array

# Charger l'image à monter
image = pili.open("zozor.png")  # Assumed to be a PNG file with an alpha channel
image_array = np.array(image)

# Charger l'image de fond
fond = pili.open('image_fond.jpg')
fond_array = np.array(fond)

# Ajuster la taille de l'image à monter à celle de l'image de fond
image_array = pili.fromarray(image_array).resize((fond_array.shape[1], fond_array.shape[0]))
image_array = np.array(image_array)

# Superposition des images
result_array = overlay_images(fond_array, image_array)

# Sauvegarde
image_result = pili.fromarray(result_array)
image_result.save("zozor_result.png")
