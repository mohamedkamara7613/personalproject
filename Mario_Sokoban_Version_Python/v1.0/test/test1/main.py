#coding:utf-8
#Monday july 12 2021 00:31


#Modules Importing
from data import *
import pygame

try :
#VARIABLE
	window_resolution = (window_width, window_height)

#INIT
	pygame.init()

	window_surface = pygame.display.set_mode(window_resolution, pygame.DOUBLEBUF)
	pygame.display.set_caption("Mario Sokobane")
	window_surface.fill(white_color)


#Boucle principale
	launched = True
	while launched:
#Condition-----------------------------------------------------------
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				launched = False

#Chargement d'image-------------------------------------------------
		mario = pygame.image.load("mario_bas.gif")
		mario.convert()
#-------------------------------------------------------------------
		window_surface.blit(mario, grille["11, 11"])
		












		pygame.display.flip()
except KeyboardInterrupt:
	print("Arret manuelle du programme")
	pygame.quit()