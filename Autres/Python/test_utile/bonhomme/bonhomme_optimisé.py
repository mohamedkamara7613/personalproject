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
	centre_cercle = [300, 55]
	rayon = 40
	pygame.draw.circle(window_surface, black_color, centre_cercle, rayon, 2)
# oeil droit
	centre_oeil_droit = [centre_cercle[0]-15, centre_cercle[1]-5]
	pygame.draw.circle(window_surface, black_color, centre_oeil_droit, 10, 7) #[285, 50]
# oeil gauche
	centre_oeil_gauche = [centre_cercle[0]+15, centre_cercle[1]-5]
	pygame.draw.circle(window_surface, black_color, centre_oeil_gauche, 10, 7) #[315, 50]
# nez
	centre_nez = [centre_cercle[0], centre_cercle[1]+10]
	pygame.draw.circle(window_surface, red_color, centre_nez, 5) #[300, 65]
# bouche
	bouche_depart = (centre_cercle[0]-5, centre_cercle[1]+20)
	bouche_arrivee = (centre_cercle[0]+5, centre_cercle[1]+20)
	pygame.draw.line(window_surface, black_color, bouche_depart, bouche_arrivee, 2) #(295, 75), (305, 75)

# cou
	cou_depart = (centre_cercle[0], centre_cercle[1]+40)
	cou_arrivee = (centre_cercle[0], centre_cercle[1]+65)
	pygame.draw.line(window_surface, black_color, cou_depart, cou_arrivee, 2) #(300, 95), (300, 110)
# tronc
	rectangle_form = pygame.Rect(centre_cercle[0]-40, centre_cercle[0]-190, centre_cercle[1]+25, centre_cercle[0]-180) #260, 110, 80, 120
	pygame.draw.rect(window_surface, black_color, rectangle_form)

# bras droit
	bras_droit_depart = (centre_cercle[0]-40, centre_cercle[1]+55)
	bras_droit_arrivee = (centre_cercle[1]+65, centre_cercle[1]+85)
	pygame.draw.line(window_surface, black_color, bras_droit_depart, bras_droit_arrivee, 2) #(260, 110), (120, 140)
# bras gauche
	bras_gauche_depart = (centre_cercle[0]+40, centre_cercle[1]+55)
	bras_gauche_arrivee = (centre_cercle[0]+180, centre_cercle[1]+85)
	pygame.draw.line(window_surface, black_color, bras_gauche_depart, bras_gauche_arrivee, 2) #(340, 110), (480, 140)
# pied droit
	pied_droit_depart = (centre_cercle[0]-20, centre_cercle[0]-70)
	pied_droit_arrivee = (centre_cercle[0]-70, centre_cercle[0]+100)
	pygame.draw.line(window_surface, black_color, pied_droit_depart, pied_droit_arrivee, 3)#(280, 230), (230, 400)
# pied gauche
	pied_gauche_depart = (centre_cercle[0]+20, centre_cercle[0]-70)
	pied_gauche_arrivee = (centre_cercle[0]+70, centre_cercle[0]+100)
	pygame.draw.line(window_surface, black_color, pied_gauche_depart, pied_gauche_arrivee, 3)#(320, 230), (370, 400)



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