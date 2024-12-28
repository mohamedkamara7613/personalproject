#coding:utf-8
import pygame

try:
	pygame.init()
	pygame.display.set_caption("Dessin bonhomme")
	# Creation de couleur
	white_color = (255, 255, 255)
	black_color = (0, 0, 0)
	red_color = (255, 0, 0)

	window_resolution = (590, 420)
	window_surface = pygame.display.set_mode(window_resolution)
	window_surface.fill(white_color)

# tete
	pygame.draw.circle(window_surface, black_color, [300, 55], 40, 2)
# oeil droit
	pygame.draw.circle(window_surface, black_color, [285, 50], 10, 7)
# oeil gauche
	pygame.draw.circle(window_surface, black_color, [315, 50], 10, 7)
# nez
	pygame.draw.circle(window_surface, red_color, [300, 65], 5)
# bouche
	pygame.draw.line(window_surface, black_color, (295, 75), (305, 75), 2)

# cou
	pygame.draw.line(window_surface, black_color, (300, 95), (300, 110), 2)
# tronc
	rectangle_form = pygame.Rect(260, 110, 80, 120)
	pygame.draw.rect(window_surface, black_color, rectangle_form)

# bras droit
	pygame.draw.line(window_surface, black_color, (260, 110), (120, 140), 2)
# bras gauche
	pygame.draw.line(window_surface, black_color, (340, 110), (480, 140), 2)
# pied droit
	pygame.draw.line(window_surface, black_color, (280, 230), (230, 400), 3)
# pied gauche
	pygame.draw.line(window_surface, black_color, (320, 230), (370, 400), 3)



	pygame.display.flip()
	#Boucle princpale
	launched = True
	while launched:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				launched = False 
except KeyboardInterrupt:
	print("Arret manuelle du programme")
	pygame.quit()