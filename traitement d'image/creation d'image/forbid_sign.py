import PIL.Image as pili
import numpy as np

R, V, B = 0, 1, 2

def draw_circle(centre, radius):
    # Place the center in red (optional)
    image_array[50, 50][R] = 255

    for i in range(l):
        for j in range(c):
            if np.sqrt((i - centre) ** 2 + (j - centre) ** 2) <= radius:
                image_array[i][j][R] = 255
                image_array[i][j][V] = 0
                image_array[i][j][B] = 0

def draw_rect(width, height, size):
    posx_rect = abs((size // 2) - (width // 2))
    posy_rect = abs((size // 2) - (height // 2))
    for i in range(l):
        for j in range(c):
            if j >= posx_rect and j <= posx_rect + width and i >= posy_rect and i <= posy_rect + height:
                image_array[i][j][R] = 255
                image_array[i][j][V] = 255
                image_array[i][j][B] = 255

size = 500
image_array = np.zeros((size, size, 3), dtype="uint8")
l, c, _ = image_array.shape

# Fill the background with white
for i in range(l):
    for j in range(c):
        image_array[i][j] = 255

centre = size // 2
radius = 200
draw_circle(centre, radius)

draw_rect(200, 50, size)

image = pili.fromarray(image_array)
image.save("image.bmp")
