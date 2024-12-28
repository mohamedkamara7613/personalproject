import PIL.Image as pili
import numpy as np

correction_gamma = lambda a, gamma=1: 255*(a/255)**gamma


# Correction gamma Image Noir et blanc
imageNB = pili.open("batmanNB.bmp")
dataImageNB = np.array(imageNB)
l, n = dataImageNB.shape
dataImageNB_cp = np.zeros((l, n), dtype="uint8")

for i in range(l):
    for j in range(n):
        dataImageNB_cp[i,j] = correction_gamma(dataImageNB[i,j], 0.5)

image_gammaNB = pili.fromarray(dataImageNB_cp)
image_gammaNB.save("image_gammaNB.bmp")


# Correction gamma Image Couleur
image = pili.open("batman.jpg")
dataImage = np.array(image)

l, c , n = dataImage.shape
dataImage_cp = np.zeros((l, c, n), dtype="uint8")

for i in range(l):
    for j in range(c):
        for k in range(n):
            dataImage_cp[i, j, k] = correction_gamma(dataImage[i, j, k], 50)

image_gamma = pili.fromarray(dataImage_cp)
image_gamma.save("image_gamma.bmp")