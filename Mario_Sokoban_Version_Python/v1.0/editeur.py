#coding:utf-8


# -------------- Mario Sokoban v1.0 -----------------------------------


""" 
#Monday july 12 2021 00:31 debut de developpement
	editeur.py
-----------------
	Par Mohamed kamara 
	
	Role : Permet de creer des niveaux
"""


from data import *
import fichiers
import pygame


def edit(window_surface):
	pygame.init()
	global grille


#VARIABLE
	#Personnage
		#MARIO
	mario = pygame.image.load("src_img/mario_bas.gif")
	mario.convert()


	#Chargement des sprites
	mur = pygame.image.load("src_img/mur.jpg")
	mur.convert()
	
	caisse = pygame.image.load("src_img/caisse.jpg")
	caisse.convert()
	
	caisse_ok = pygame.image.load("src_img/caisse_ok.jpg")
	caisse_ok.convert()
	
	objectif = pygame.image.load("src_img/objectif.png")
	objectif.convert()
	
	instructions = pygame.image.load("src_img/instructions.jpg")
	instructions.convert()

	joueurActuel = mario
	positionActuel = [0, 0]
	positionJoueur = [0, 0]
	clicGaucheEnCours = False
	clicDroitEnCours = False
	joueurBlitter = False
	joueurChoosed = False
	objetActuel = items["MUR"]

	#Chargement du niveau, chargement de la grille
	if fichiers.chargerNiveau() == False:
		exit("Impossible de charger le niveau\n No such 'level.lvl'")

#Affichage des instructions de l'editeur
	launched = True
	while launched:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				launched = False
			if event.type == pygame.QUIT:
				launched = False
				pygame.quit()
				return 0

		window_surface.fill(white_color)
		window_surface.blit(instructions, [0, 0])
		pygame.display.flip()

#BOUCLE PRINCIPALE
	launched = True
	while launched:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				launched = False
				break

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == pygame.BUTTON_LEFT:
					#On met l'objet choisi(mur, caisse...) a l'endroit du clic 
					if objetActuel == items["MARIO"]:
						positionJoueur = [(event.pos[0] // bloc_size) * bloc_size, (event.pos[1] // bloc_size) * bloc_size]
						joueurBlitter = True

					grille[event.pos[0] // bloc_size][event.pos[1] // bloc_size] = objetActuel
					clicGaucheEnCours = True
				
				elif event.button == pygame.BUTTON_RIGHT:
					if grille[event.pos[0] // bloc_size][event.pos[1] // bloc_size] == items["MARIO"]:
						positionJoueur = [0, 0]
						joueurBlitter = False

					grille[event.pos[0] // bloc_size][event.pos[1] // bloc_size] = items["VIDE"]
					clicDroitEnCours = True

			if event.type == pygame.MOUSEMOTION:
				if clicGaucheEnCours:
					grille[event.pos[0] // bloc_size][event.pos[1] // bloc_size] = objetActuel
				
				elif clicDroitEnCours:
					grille[event.pos[0] // bloc_size][event.pos[1] // bloc_size] =  items["VIDE"]

				positionActuel = event.pos

			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == pygame.BUTTON_LEFT:
					clicGaucheEnCours = False
				
				elif event.button == pygame.BUTTON_RIGHT:
					clicDroitEnCours = False


			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					launched = False

				elif event.key == pygame.K_s:
					fichiers.sauvegarderNiveau(grille) # A besoin de la grille pour fonctionner

				elif event.key == pygame.K_c:
					fichiers.chargerNiveau()

				elif event.key == pygame.K_KP1:
					objetActuel = items["MUR"]
					joueurChoosed = False

				elif event.key == pygame.K_KP2:
					objetActuel = items["CAISSE"]
					joueurChoosed = False

				elif event.key == pygame.K_KP3:
					objetActuel = items["OBJECTIF"]
					joueurChoosed = False

				elif event.key == pygame.K_KP4:
					objetActuel = items["CAISSE_OK"]
					joueurChoosed = False

				elif event.key == pygame.K_KP5:
					objetActuel = items["MARIO"]
					joueurChoosed = True





	#Effacement de l'ecran
		window_surface.fill(white_color)
	#Placement des objets a l'ecran
		i = 0
		while i < nb_bloc_width:
			j = 0
			while j < nb_bloc_height:
				
				position = [i * bloc_size, j * bloc_size]

				if grille[i][j] == items["MUR"]:
					window_surface.blit(mur, position)

				elif grille[i][j] == items["CAISSE"]:
					window_surface.blit(caisse, position)

				elif grille[i][j] == items["OBJECTIF"]:
					window_surface.blit(objectif, position)

				elif grille[i][j] == items["CAISSE_OK"]:
					window_surface.blit(caisse_ok, position)

				elif grille[i][j] == items["MARIO"]:
					if joueurBlitter ==  True:
						window_surface.blit(mario, positionJoueur)


				j += 1
			i += 1

	#Affichage de l'objet selectionné
		if objetActuel == items["MUR"]:
			window_surface.blit(mur, positionActuel)

		elif objetActuel == items["CAISSE"]:
			window_surface.blit(caisse, positionActuel)

		elif objetActuel == items["OBJECTIF"]:
			window_surface.blit(objectif, positionActuel)

		elif objetActuel == items["CAISSE_OK"]:
			window_surface.blit(caisse_ok, positionActuel)
			
		elif objetActuel == items["MARIO"]:
			window_surface.blit(joueurActuel, positionActuel)

	#Mise a jour de l'ecran 
		pygame.display.flip()

