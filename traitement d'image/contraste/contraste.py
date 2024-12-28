import PIL.Image as pili
import numpy as np

correction_contraste = lambda a, seuil=255//2, alpha=0.1: int(255/2 * (1 + np.tanh(alpha * (a - seuil))))

# Contraste
image = pili.open("zozor_vert.jpg")
dataImage = np.array(image)

l, c , n = dataImage.shape
dataImage_cp = np.zeros((l, c, n), dtype="uint8")

for i in range(l):
    for j in range(c):
        for k in range(n):
            dataImage_cp[i, j, k] = correction_contraste(dataImage[i, j, k])

image_contraste = pili.fromarray(dataImage_cp)
image_contraste.save("image_contraste_tanh1.bmp")
