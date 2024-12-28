#coding:utf-8

# -------------- Mario Sokoban v1.0 -----------------------------------


"""
	#Monday july 12 2021 00:31 debut de developpement
	jeu.py
-----------------
	Par Mohamed kamara 
	
	Role : Gere une partie de complete

	Modification a faire : faire accessible la variable positionJoueur qui ne peut pas etre modifier par les fonctions jouer et deplacerJoueur

"""
from data import *
import fichiers
import pygame

#----------------------------------------------------------------------------------------
def jouer(window_surface):
	pygame.init()	
	global grille
#VARIABLE
	#Personnage
		#MARIO
	mario = {"haut" : 0, "bas" : 0, "gauche" : 0, "droite" : 0}
	
	mario["haut"] = pygame.image.load("src_img/mario_haut.gif")
	mario["haut"].convert()
	
	mario["bas"] = pygame.image.load("src_img/mario_bas.gif")
	mario["bas"].convert()
	
	mario["gauche"] = pygame.image.load("src_img/mario_gauche.gif")
	mario["gauche"].convert()
	
	mario["droite"] = pygame.image.load("src_img/mario_droite.gif")
	mario["droite"].convert()



	#Chargement des sprites
	mur = pygame.image.load("src_img/mur.jpg")
	mur.convert()
	
	caisse = pygame.image.load("src_img/caisse.jpg")
	caisse.convert()
	
	caisse_ok = pygame.image.load("src_img/caisse_ok.jpg")
	caisse_ok.convert()
	
	objectif = pygame.image.load("src_img/objectif.png")
	objectif.convert()

	#Autre
	position = [0, 0]
	global positionJoueur
	objectifRestant = False

	joueurActuel = mario["bas"]


	#Chargement du niveau
	if fichiers.chargerNiveau() == False:
		exit("Impossible de charger le niveau\n No such 'level.lvl'")

	#Recherche de la position de mario
	i = 0 
	while i < nb_bloc_width:
		j = 0
		while j < nb_bloc_height:
			if grille[i][j] == items["MARIO"]:
				positionJoueur = [i, j]
				grille[i][j] = items["VIDE"]
			j += 1
		i += 1	

#BOUCLE PRINCIPALE
	jeu_start = True
	while jeu_start:
	#Condition et capture des evenements
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				jeu_start = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					joueurActuel = mario["haut"]
					deplacerJoueur(grille, direction["HAUT"])
				elif event.key == pygame.K_DOWN:
					joueurActuel = mario["bas"]
					deplacerJoueur(grille, direction["BAS"])
				elif event.key == pygame.K_LEFT:
					joueurActuel = mario["gauche"]
					deplacerJoueur(grille, direction["GAUCHE"])
				elif event.key == pygame.K_RIGHT:
					joueurActuel = mario["droite"]
					deplacerJoueur(grille, direction["DROITE"])

	#Blitage des élements
		window_surface.fill(white_color)

		objectifRestant = False

		i = 0
		while i < nb_bloc_width:
			j = 0
			while j < nb_bloc_height:

				position = [i* bloc_size, j*bloc_size]

				if grille[i][j] == items["CAISSE"]:
					window_surface.blit(caisse, position)
				elif grille[i][j] == items["CAISSE_OK"]:
					window_surface.blit(caisse_ok, position)
				elif grille[i][j] == items["MUR"]:
					window_surface.blit(mur, position)
				elif grille[i][j] == items["OBJECTIF"]:
					window_surface.blit(objectif, position)
					objectifRestant = True
				j += 1
			i += 1

		#check win
		if objectifRestant == False:
			jeu_start = False



		#Blitage du joueur a l'ecran
		position = [(positionJoueur[0]*bloc_size) , (positionJoueur[1]*bloc_size)]
		window_surface.blit(joueurActuel, position)


		#Mise a jour de l'ecran
		pygame.display.flip()


#---------------------------------------------------------------------------------------------------------------------------------
def deplacerJoueur(grille, direction_sens):
	"""
		Fonction deplacerJoueur depalace le joueur d'une case a l'autre,
		prend en parametre la grille c'est a dire la carte du jeu et la direction dans laquelle deplacée le joueur
		Mais aussi rend accessible la variable positionJoueur pour modifier sa position 
	"""
	global positionJoueur

	if direction_sens == direction["HAUT"]:
		if positionJoueur[1] - 1 < 0: #Si le joueur depasse l'ecran, on arrete
			return False
		elif grille[positionJoueur[0]][positionJoueur[1]-1] == items["MUR"]: #s'il y a un mur au dessus du joueur on arrete
			return False
		#Si on veut pousser une caisse, il faut verifier qu'il n'y a pas de caisse apres ou le mur ou la limite du jeu
		elif (grille[positionJoueur[0]][positionJoueur[1]-1] == items["CAISSE"] or grille[positionJoueur[0]][positionJoueur[1]-1] == items["CAISSE_OK"]) and ((positionJoueur[1] - 2 < 0) or grille[positionJoueur[0]][positionJoueur[1]-2] == items["MUR"] or grille[positionJoueur[0]][positionJoueur[1]-2] == items["CAISSE"] or grille[positionJoueur[0]][positionJoueur[1]-2] == items["CAISSE_OK"]) :
			return False
		else:
			deplacerCaisse(positionJoueur, direction["HAUT"])
			positionJoueur = [positionJoueur[0], positionJoueur[1] - 1] #Modifie l'ordonnée du joueur pour le faire monter d'une case
			return True

	elif direction_sens == direction["BAS"]:
		if positionJoueur[1] + 1 >= nb_bloc_width: #Si le joueur depasse l'ecran, on arrete
			return False
		elif grille[positionJoueur[0]][positionJoueur[1]+1] == items["MUR"]: #s'il y a un mur au dessus du joueur on arrete
			return False
		elif (grille[positionJoueur[0]][positionJoueur[1]+1] == items["CAISSE"] or grille[positionJoueur[0]][positionJoueur[1]+1] == items["CAISSE_OK"] ) and ((positionJoueur[1] + 2 < 0) or grille[positionJoueur[0]][positionJoueur[1]+2] == items["MUR"] or grille[positionJoueur[0]][positionJoueur[1]+2] == items["CAISSE"] or grille[positionJoueur[0]][positionJoueur[1]+2] == items["CAISSE_OK"]) :
			return False	
		else:
			deplacerCaisse(positionJoueur, direction["BAS"])
			positionJoueur = [positionJoueur[0], positionJoueur[1] + 1] #Modifie l'ordonnée du joueur pour le faire monter d'une case
			return True

	if direction_sens == direction["GAUCHE"]:
		if positionJoueur[0] - 1 < 0: #Si le joueur depasse l'ecran, on arrete
			return False
		elif grille[positionJoueur[0]-1][positionJoueur[1]] == items["MUR"]: #s'il y a un mur au dessus du joueur on arrete
			return False
		elif (grille[positionJoueur[0]-1][positionJoueur[1]] == items["CAISSE"] or grille[positionJoueur[0]-1][positionJoueur[1]] == items["CAISSE_OK"]) and ((positionJoueur[0] - 2 < 0) or grille[positionJoueur[0]-2][positionJoueur[1]] == items["MUR"] or grille[positionJoueur[0]-2][positionJoueur[1]] == items["CAISSE"] or grille[positionJoueur[0]-2][positionJoueur[1]] == items["CAISSE_OK"]) :
			return False
		else:
			deplacerCaisse(positionJoueur, direction["GAUCHE"])
			positionJoueur = [positionJoueur[0] - 1, positionJoueur[1]] #Modifie l'ordonnée du joueur pour le faire monter d'une case
			return True

	if direction_sens == direction["DROITE"]:
		if positionJoueur[0] + 1 >= nb_bloc_height: #Si le joueur depasse l'ecran, on arrete
			return False
		elif grille[positionJoueur[0]+1][positionJoueur[1]] == items["MUR"]: #s'il y a un mur au dessus du joueur on arrete
			return False
		elif (grille[positionJoueur[0]+1][positionJoueur[1]] == items["CAISSE"] or grille[positionJoueur[0]+1][positionJoueur[1]] == items["CAISSE_OK"]) and ((positionJoueur[0] + 2 < 0) or grille[positionJoueur[0]+2][positionJoueur[1]] == items["MUR"] or grille[positionJoueur[0]+2][positionJoueur[1]] == items["CAISSE"] or grille[positionJoueur[0]+2][positionJoueur[1]] == items["CAISSE_OK"]) :
			return False
		else:
			deplacerCaisse(positionJoueur, direction["DROITE"])
			positionJoueur = [positionJoueur[0] + 1, positionJoueur[1]] #Modifie l'ordonnée du joueur pour le faire monter d'une case
			return True
 



#-------------------------------------------------------------------------------------------------------------------
def deplacerCaisse(position, direction_sens):
	"""
		fonction deplacerCaisse, prend en parametre la position du joueur qu'elle ne modifie pas
		et la direction dans laquelle deplacée la caisse
		Et rend accessible la grille (la carte) qu'elle modifiera
	"""
	global grille

	if direction_sens == direction["HAUT"]:
		if grille[position[0]][position[1]-1] == items["CAISSE"] or grille[position[0]][position[1]-1] == items["CAISSE_OK"]:
			if grille[position[0]][position[1]-2] == items["OBJECTIF"]:
				grille[position[0]][position[1]-2] = items["CAISSE_OK"]
			else:
				grille[position[0]][position[1]-2] = items["CAISSE"]

			if grille[position[0]][position[1]-1] == items["CAISSE_OK"]:
				grille[position[0]][position[1]-1] = items["OBJECTIF"]
			else:
				grille[position[0]][position[1]-1] = items["VIDE"]

	elif direction_sens == direction["BAS"]:
		if grille[position[0]][position[1]+1] == items["CAISSE"] or grille[position[0]][position[1]+1] == items["CAISSE_OK"]:
			if grille[position[0]][position[1]+2] == items["OBJECTIF"]:
				grille[position[0]][position[1]+2] = items["CAISSE_OK"]
			else:
				grille[position[0]][position[1]+2] = items["CAISSE"]

			if grille[position[0]][position[1]+1] == items["CAISSE_OK"]:
				grille[position[0]][position[1]+1] = items["OBJECTIF"]
			else:
				grille[position[0]][position[1]+1] = items["VIDE"]

	elif direction_sens == direction["GAUCHE"] :
		if grille[position[0]-1][position[1]] == items["CAISSE"] or grille[position[0]-1][position[1]] == items["CAISSE_OK"]:
			if grille[position[0]-2][position[1]] == items["OBJECTIF"]:
				grille[position[0]-2][position[1]] = items["CAISSE_OK"]
			else:
				grille[position[0]-2][position[1]] = items["CAISSE"]

			if grille[position[0]-1][position[1]] == items["CAISSE_OK"]:
				grille[position[0]-1][position[1]] = items["OBJECTIF"]
			else:
				grille[position[0]-1][position[1]] = items["VIDE"]
				
	elif direction_sens == direction["DROITE"]:
		if grille[position[0]+1][position[1]] == items["CAISSE"] or grille[position[0]+1][position[1]] == items["CAISSE_OK"]:
			if grille[position[0]+2][position[1]] == items["OBJECTIF"]:
				grille[position[0]+2][position[1]] = items["CAISSE_OK"]
			else:
				grille[position[0]+2][position[1]] = items["CAISSE"]

			if grille[position[0]+1][position[1]] == items["CAISSE_OK"]:
				grille[position[0]+1][position[1]] = items["OBJECTIF"]
			else:
				grille[position[0]+1][position[1]] = items["VIDE"]
				
