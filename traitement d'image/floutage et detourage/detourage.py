import PIL.Image as pili
import numpy as np


imageNB = pili.open("batmanNB.bmp")
imageNB_array = np.array(imageNB)
imageFlou = pili.open("imageFlou_vraiment_vraiment.bmp")
imageFlou_array = np.array(imageFlou)

rows, cols = imageNB_array.shape

imageDetoure_array = abs(imageNB_array - imageFlou_array)

imageDetoure = pili.fromarray(imageDetoure_array)
imageDetoure.save("imageDetoure_2.bmp")
imageDetoure.show()


"""

for i in range(rows):
    for j in range(cols):
        imageDetoure_array[i, j] = abs(imageFlou_array[i, j] - imageNB_array[i, j])
"""