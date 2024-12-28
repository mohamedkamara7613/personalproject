from PIL import Image, ImageFilter

# Charger l'image
image = Image.open('test0.jpg')

# Appliquer le flou gaussien
flou_image = image.filter(ImageFilter.GaussianBlur(radius=15))

# Enregistrer l'image floutée
flou_image.save('test0_flou.jpg')

# Afficher l'image floutée
flou_image.show()

