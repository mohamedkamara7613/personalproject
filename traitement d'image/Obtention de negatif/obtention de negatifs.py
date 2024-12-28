
import PIL.Image as pili
import numpy as np 

batman = pili.open("batman.jpg")

databatman = np.array(batman)

#print(databatman)

l, c, n = databatman.shape



# Transformation de l'image en niveaux de gris

batmanNB = batman.convert("L")
batmanNB.save("batmanNB.bmp")
dataBatmanNB = np.array(batmanNB)

# Transformation noir et blanc en negatif
dataBatmanNeg = np.zeros((l,c), dtype='uint8')

for i in range(l):
    for j in range(c):
        dataBatmanNeg[i,j] = 255 - dataBatmanNB[i,j]

batmanNegNB = pili.fromarray(dataBatmanNeg)
batmanNegNB.save("batmanNegNB.jpg")

# Transformation de l'image en couleur en negatif

dataBatmanNeg = np.zeros((l,c, n), dtype="uint8")

for i in range(l):
    for j in range(c):
        for k in range(n):
            dataBatmanNeg[i,j, k] = abs(255 - databatman[i,j,k])
            
batmanNeg = pili.fromarray(dataBatmanNeg)
batmanNeg.save("batmanNeg.jpg")









