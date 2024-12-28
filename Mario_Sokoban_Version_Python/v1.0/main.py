#coding:utf-8
# -------------- Mario Sokoban v1.0
""" 
#Monday july 12 2021 00:31 debut de developpement
	main.py
-----------------
	Par Mohamed kamara 
	
	Role : Contient le menu et redirige vers la partie souhaitée
"""

#Modules Importing
from data import *
import jeu
import editeur
import pygame
import time


try :
#INIT
	pygame.init()
	window_surface = pygame.display.set_mode(window_resolution, pygame.DOUBLEBUF)
	pygame.display.set_caption("Mario Sokobane")
	window_surface.fill(white_color)

#TEXTE
	arial_font = pygame.font.SysFont("arial", 40)


#Boucle principale
	launched = True
	while launched:
#Condition-----------------------------------------------------------
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				launched = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_KP1:
					jeu.jouer(window_surface)
					
				elif event.key == pygame.K_KP2:
					editeur.edit(window_surface)
					
				elif event.key == pygame.K_ESCAPE: #Quitter le programme avec un compte a rebours
					i = 3
					while i > 0:
						time.sleep(1)
						window_surface.fill(white_color)
						dimensions_text = arial_font.render("{}".format(i), True, black_color)
						window_surface.blit(dimensions_text, pos_text_center)
						pygame.display.flip()
						i -= 1

					window_surface.fill(white_color)
					dimensions_text = arial_font.render("...A bientôt...", True, black_color)
					window_surface.blit(dimensions_text, [window_width / 2 - 120, window_height / 2 - 40])
					pygame.display.flip()
					time.sleep(1)
					launched = False


#Chargement d'image-------------------------------------------------
		menu = pygame.image.load("src_img/menu.jpg")
		menu.convert()
#-------------------------------------------------------------------
	#BLitage des sprites
		if launched == True:
			window_surface.blit(menu, (0, 0))
	#Mise a jour de l'ecran
		pygame.display.flip()
except KeyboardInterrupt:
	print("Arret manuelle du programme")
	pygame.quit()