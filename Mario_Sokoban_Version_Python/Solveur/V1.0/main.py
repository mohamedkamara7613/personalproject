#!/usr/bin/python3
# coding:utf-8
"""
	starting at Wen 27 Aug 2021
	Par Mohamed Kamara
--------------------- Mario Sokoban v2.0 --------------------------
-------------- main.py


	Rôle du fichier : redirige vers les differents sections du programme
"""

# Importation
from data import *
import game

import sys
import pygame

try:
	pygame.init()

	# Setting icon
	icon = pygame.image.load('doc/src_img/icone.png')  # Ne pas utiliser la methode convert
	pygame.display.set_icon(icon)

	# Mading window
	window_surface = pygame.display.set_mode(dimension_window, pygame.DOUBLEBUF)
	pygame.display.set_caption("Mario Sokoban v2.0")

	# loading soung
	font_soung = pygame.mixer.Sound("doc/son/font_soung.ogg")
	# Play soung
	font_soung.play(-1)
	font_soung.set_volume(0.9)

	# Loading picture
	img1 = pygame.image.load("doc/src_img/menu/1.png")
	# window_height-(window_height-10)
	pos_img1 = [int((window_width / 2) - (img1.get_width() / 2)), window_height - (window_height - 10)]

	img2 = pygame.image.load("doc/src_img/menu/2.png")
	pos_img2 = [int((window_width / 2) - (img1.get_width() / 2)), pos_img1[1] + img1.get_height() + 60]

	img3 = pygame.image.load("doc/src_img/menu/3.png")
	pos_img3 = [int((window_width / 2) - (img1.get_width() / 2)), pos_img2[1] + img2.get_height() + 10]

	img4 = pygame.image.load("doc/src_img/menu/4.png")
	pos_img4 = [int((window_width / 2) - (img1.get_width() / 2)), pos_img3[1] + img3.get_height() + 10]

	img5 = pygame.image.load("doc/src_img/menu/5.png")
	pos_img5 = [int((window_width / 2) - (img1.get_width() / 2)), pos_img4[1] + img4.get_height() + 90]

	img6 = pygame.image.load("doc/src_img/menu/signature.png")
	pos_img6 = [int((window_width / 2) - (img1.get_width() / 2)), pos_img5[1] + img5.get_height() + 10]

	# Main Loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

				elif event.key == pygame.K_KP1:
					game.afficher_instructions_console()
					game.play(window_surface)

				elif event.key == pygame.K_KP2:
					# editor.edit(window_surface)
					print("You are in a editor")

		# Effecement de l'ecran
		window_surface.fill(font)

		# Blittage du menu
		window_surface.blit(img1, pos_img1)
		window_surface.blit(img2, pos_img2)
		window_surface.blit(img3, pos_img3)
		window_surface.blit(img4, pos_img4)
		window_surface.blit(img5, pos_img5)
		window_surface.blit(img6, pos_img6)
		pygame.display.flip()

except KeyboardInterrupt:
	print("------------Arret manuel-------------")
	pygame.quit()
