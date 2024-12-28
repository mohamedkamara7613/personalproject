import PIL.Image as pili
import numpy as np

imageNB = pili.open("batmanNB.bmp")
imageNB_array = np.array(imageNB)
rows, cols = imageNB_array.shape
p = 50

# Initialiser un tableau pour le résultat de la convolution
imageFlou_array = np.zeros_like(imageNB_array, dtype=np.uint8)

# Appliquer la contraste avec le noyau de moyenne sur chaque canal
for x in range(p, rows - p):
    for y in range(p, cols - p):
        sum_neighbors = 0
        for dx in range(-p, p+1):
            for dy in range(-p, p+1):
                sum_neighbors += imageNB_array[x + dx, y + dy]
        imageFlou_array[x, y] = int(sum_neighbors / ((2*p+1)**2))

# Créer une nouvelle image à partir du tableau flouté
imageFlou = pili.fromarray(imageFlou_array)
imageFlou.save("imageFlou_vraiment_vraiment.bmp")
