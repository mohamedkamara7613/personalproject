import PIL.Image as pili
import numpy as np

R, V, B = 0, 1, 2

## #Loading "image"--------------------------------------------------
# Charger l'image a monter
image = pili.open("zozor_vert.jpg") # c'est l'image de zozor sur fond vert
image_array = np.array(image)
width, height = image.size

# Charger l'image de fond
fond = pili.open('image_fond.jpg')
fond_array = np.array(fond)
width_font, height_font, n = fond_array.shape

 

## # Creation d'un fond vert------------------------------------------
# Creation d'une image de taille correspondant a l'image de fond
image_result_array = np.zeros((width_font, height_font, n), dtype="uint8")

# Remplissage du fond de cette image en vert
for i in range(width_font):
    for j in range(height_font):
        image_result_array[i][j][V] = 255
        image_result_array[i][j][B] = 0
        image_result_array[i][j][R] = 0
        
## # Collage de l'image a monter sur le fond vert --------------------
for i in range(width_font):
    for j in range(height_font):
        if (i < width and j < height):
            image_result_array[i][j] = image_array[i][j] 
            # possibilité de centrer l'image a monter cad calculer ced coords

## # Subtition du fond vert par l'image fond d'ecran
for i in range(width_font):
    for j in range(height_font):

        if 100 <= image_result_array[i][j][V] <= 255 and 0 <= image_result_array[i][j][B] <= 50 and 0 <= image_result_array[i][j][R] <= 30:
            image_result_array[i][j] = fond_array[i][j]





## # Saving------------------------------------------------------------
image_result = pili.fromarray(image_result_array)
image_result.save("zozor_result.bmp")