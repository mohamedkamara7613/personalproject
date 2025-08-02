# coding:utf-8
"""
	starting at Wen 27 Aug 2021
	modified at Wen 27 juil 2025
	Par Mohamed Kamara
--------------------- Mario Sokoban v2.0 --------------------------
-------------- game.py


	Rôle du fichier : gere une partie complete de jeu
"""

# Importing module
from data import *
import gestion_file
import personnage
import solver

import pygame
import sys
import time


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def play(window_surface):

	pygame.init()
	
	# Activation de la repetion des touches
	pygame.key.set_repeat(200, 200)

	# Pour l'animation du solver
	actions_a_jouer = []
	animation_en_cours = False
	dernier_temps_action = pygame.time.get_ticks()
	duree_entre_actions = 200  # ms entre deux coups
 
	# loading soung
	bravo_soung = pygame.mixer.Sound("doc/son/tasty.ogg")
	end_level_soung = pygame.mixer.Sound("doc/son/Ralenti.wav")
	bingo_soung = pygame.mixer.Sound("doc/son/bingo.ogg")

	# INITIALISATION DE LA VARIABLE DE TEMPS, DU TIMER
	clock = pygame.time.Clock()

	# ------------VARIABLE--------------------------------------------------------
	# Choix du Joueur
	joueur = personnage.choisir_personnage(window_surface)
	joueur_actuel = joueur["BAS"]

	# Loading sprites
	mur = pygame.image.load("doc/src_img/mur.jpg").convert_alpha()
	caisse = pygame.image.load("doc/src_img/caisse.jpg").convert_alpha()
	caisse_ok = pygame.image.load("doc/src_img/caisse_ok.jpg").convert_alpha()
	objectif = pygame.image.load("doc/src_img/objectif.png").convert_alpha()
	bravo = pygame.image.load("doc/src_img/bravo.png").convert_alpha()

	# Autre
	police_text = pygame.font.Font("doc/police.ttf", 20)
	police_terminal = pygame.font.SysFont('consolas', 18)
	objectif_restant = False
	fin_jeu = False
	global grille
	global position_joueur
	position = [0, 0]

	pos_bravo = [((window_width-800)/ 2) - (bravo.get_width() / 2), ((window_height-500 )/ 2) - (bravo.get_height() / 2)]
	niveau = 0

	# --------------------VARIABLE FIN---------------------------------------------------------

	# -------------------DEBUT-------------------------------------------------------
	# Chargement du niveau
	return_valor = gestion_file.load_level(niveau)
	if return_valor is False:
		exit("No such file 'level.lvl'\n.....loading level is impossible.\n")
	elif return_valor == 76:
		fin_jeu = True

	# Recherche de la position du joueur
	i = 0
	while i < nb_bloc_width:
		j = 0
		while j < nb_bloc_height:
			if grille[i][j] == items["JOUEUR"]:
				position_joueur = [i, j]
				grille[i][j] = items["VIDE"]
			j += 1
		i += 1

	# Affichage des instructions du jeu---------------------------------------------
	img1_instruction = pygame.image.load("doc/src_img/instruction_jeu/1.png").convert_alpha()
	pos_img1_instruction = [int((window_width / 2) - (img1_instruction.get_width() / 2)),
							window_height - (window_height - 10)]

	img2_instruction = pygame.image.load("doc/src_img/instruction_jeu/2.png").convert_alpha()
	pos_img2_instruction = [int((window_width / 2) - (img1_instruction.get_width() / 2)),
							pos_img1_instruction[1] + img1_instruction.get_height() + 40]

	img3_instruction = pygame.image.load("doc/src_img/instruction_jeu/3.png").convert_alpha()
	pos_img3_instruction = [int((window_width / 2) - (img1_instruction.get_width() / 2)),
							pos_img2_instruction[1] + img2_instruction.get_height() + 10]

	img4_instruction = pygame.image.load("doc/src_img/instruction_jeu/4.png").convert_alpha()
	pos_img4_instruction = [int((window_width / 2) - (img1_instruction.get_width() / 2)),
							pos_img3_instruction[1] + img3_instruction.get_height() + 10]

	img5_instruction = pygame.image.load("doc/src_img/instruction_jeu/5.png").convert_alpha()
	pos_img5_instruction = [int((window_width / 2) - (img1_instruction.get_width() / 2)),
							pos_img4_instruction[1] + img4_instruction.get_height() + 10]

	img6_instruction = pygame.image.load("doc/src_img/instruction_jeu/6.png").convert_alpha()
	pos_img6_instruction = [int((window_width / 2) - (img1_instruction.get_width() / 2)),
							pos_img5_instruction[1] + img5_instruction.get_height() + 10]
	launched = True
	while launched:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				launched = False

			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		window_surface.fill(font)
		window_surface.blit(img1_instruction, pos_img1_instruction)
		window_surface.blit(img2_instruction, pos_img2_instruction)
		window_surface.blit(img3_instruction, pos_img3_instruction)
		window_surface.blit(img4_instruction, pos_img4_instruction)
		window_surface.blit(img5_instruction, pos_img5_instruction)
		window_surface.blit(img6_instruction, pos_img6_instruction)
		pygame.display.flip()

	pygame.time.set_timer(pygame.USEREVENT, 2000)  # envoie l'evenement USEREVENT tous les 2s
	# Main loop---------------------------------------------------
	while True:
		# Gestion des evenements---------------------------------------------------------
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return 0
				elif event.key == pygame.K_n:
					niveau += 1
					solver.stop_solver = True
					solver.current_level = niveau
     
					# Chargement du niveau
					return_valor = gestion_file.load_level(niveau)
					if return_valor is False:
						exit("No such file 'level.lvl'\n.....loading level is impossible.\n")
					elif return_valor == 76:
						fin_jeu = True
					# Recherche de la position du joueur
					i = 0
					while i < nb_bloc_width:
						j = 0
						while j < nb_bloc_height:
							if grille[i][j] == items["JOUEUR"]:
								position_joueur = [i, j]
								grille[i][j] = items["VIDE"]
							j += 1
						i += 1

					joueur_actuel = joueur["BAS"]

					pass

				elif event.key == pygame.K_b:
					niveau -= 1
					
     
					if niveau < 0:
						niveau = 0
      
					solver.stop_solver = True
					solver.current_level = niveau
     
					# Chargement du niveau
					return_valor = gestion_file.load_level(niveau)
					if return_valor is False:
						exit("No such file 'level.lvl'\n.....loading level is impossible.\n")
					elif return_valor == 76:
						fin_jeu = True
					# Recherche de la position du joueur
					i = 0
					while i < nb_bloc_width:
						j = 0
						while j < nb_bloc_height:
							if grille[i][j] == items["JOUEUR"]:
								position_joueur = [i, j]
								grille[i][j] = items["VIDE"]
							j += 1
						i += 1

					joueur_actuel = joueur["BAS"]

					pass

				elif event.key == pygame.K_r:  # Touche r pour recommencer le niveau
					# Chargement du niveau
					return_valor = gestion_file.load_level(niveau)
					if return_valor is False:
						exit("No such file 'level.lvl'\n.....loading level is impossible.\n")
					elif return_valor == 76:
						fin_jeu = True
					# Recherche de la position du joueur
					i = 0
					while i < nb_bloc_width:
						j = 0
						while j < nb_bloc_height:
							if grille[i][j] == items["JOUEUR"]:
								position_joueur = [i, j]
								grille[i][j] = items["VIDE"]
							j += 1
						i += 1

					joueur_actuel = joueur["BAS"]
				elif event.key == pygame.K_s:  # Touche s pour solve le niveaux
					actions = solver.main(niveau)
					if actions:
						actions_a_jouer = actions
						animation_en_cours = True
						print("animation lancée")
         
         
     
				elif event.key == pygame.K_i:  # Touche i pour afficher les instructions
					afficher_instructions_console()
     
				elif event.key == pygame.K_p:
					print(grille)

				elif event.key == pygame.K_UP:
					joueur_actuel = joueur["HAUT"]
					deplacer_joueur(directions["HAUT"], grille)

				elif event.key == pygame.K_DOWN:
					joueur_actuel = joueur["BAS"]
					deplacer_joueur(directions["BAS"], grille)

				elif event.key == pygame.K_LEFT:
					joueur_actuel = joueur["GAUCHE"]
					deplacer_joueur(directions["GAUCHE"], grille)

				elif event.key == pygame.K_RIGHT:
					joueur_actuel = joueur["DROITE"]
					deplacer_joueur(directions["DROITE"], grille)

		# Fin de la gestion des evenements------------------------------------------------------------
		# Met le nombre d'image par seconde a 60 ainsi le programme aura la meme vitesse partout
		clock.tick(60)

		# Effacement de l'ecran
		window_surface.fill(font)

		# Si l'animation est en cours, on joue les actions
		if animation_en_cours and actions_a_jouer:
			maintenant = pygame.time.get_ticks()
			if maintenant - dernier_temps_action > duree_entre_actions:
				action = actions_a_jouer.pop(0)

				if action == "haut":
					deplacer_joueur(directions["HAUT"], grille)
				elif action == "bas":
					deplacer_joueur(directions["BAS"], grille)
				elif action == "gauche":
					deplacer_joueur(directions["GAUCHE"], grille)
				elif action == "droite":
					deplacer_joueur(directions["DROITE"], grille)

				dernier_temps_action = maintenant

			if not actions_a_jouer:
				animation_en_cours = False
				print("Animation terminée.")


		# Blittage des sprites--------------
		objectif_restant = False

		i = 0
		while i < nb_bloc_width:
			j = 0
			while j < nb_bloc_height:
				position = [i * bloc_size, j * bloc_size]

				if grille[i][j] == items["MUR"]:
					window_surface.blit(mur, position)
				if grille[i][j] == items["CAISSE"]:
					window_surface.blit(caisse, position)

				if grille[i][j] == items["CAISSE_OK"]:
					window_surface.blit(caisse_ok, position)

				if grille[i][j] == items["OBJECTIF"]:
					window_surface.blit(objectif, position)
					objectif_restant = True

				j += 1
			i += 1
		derniere_action = grille

		

		# Placement du joueur a la bonne position
		position = [position_joueur[0] * bloc_size, position_joueur[1] * bloc_size]
		window_surface.blit(joueur_actuel, position)
  
		# Dessiner la zone lateral pour les logs
		afficher_logs_terminal(window_surface, log_buffer, police_terminal, window_width, window_height)
  
		# afficher le titre du niveau
		afficher_titre_lateral(window_surface, niveau, window_width)
  
		pygame.display.flip()

		# Check win---------------------------------------------------------
		if objectif_restant is False:
			bravo_soung.play()
			bingo_soung.play()
			bingo_soung.set_volume(0.2)
			# Recharge du niveau suivant
			niveau += 1
			solver.stop_solver = True
			solver.current_level = niveau

			# Chargement du niveau suivant
			return_valor = gestion_file.load_level(niveau)
			if return_valor is False:
				exit("No such file 'level.lvl'\n.....loading level is impossible.\n")
			elif return_valor == 76:
				fin_jeu = True

			# Recherche de la position du joueur
			i = 0
			while i < nb_bloc_width:
				j = 0
				while j < nb_bloc_height:
					if grille[i][j] == items["JOUEUR"]:
						position_joueur = [i, j]
						grille[i][j] = items["VIDE"]
					j += 1
				i += 1

				joueur_actuel = joueur["BAS"]

			# Affichage de bravo
			launched = True
			while launched:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						time.sleep(1)
						launched = False
					elif event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()

				window_surface.blit(bravo, pos_bravo)
				pygame.display.flip()
		# Si c'est la fin du jeu
		if fin_jeu is True:
			end_level_soung.play()
			launched = True
			while launched:
				window_surface.fill(font)
				texte = police_text.render("DERNIER NIVEAU TERMINÉ", True, black_color)
				position = [(window_width / 2) - (texte.get_width() / 2),
							(window_height / 2) - (texte.get_height() / 2)]
				window_surface.blit(texte, position)
				pygame.display.flip()
				time.sleep(5)
				launched = False
				return 0


# ---------------------FIN--------------------------------------------------------------

# ///////////////////////////////////////////////////////////////////////////////////////////////

def deplacer_joueur(direction_deplacement, grille):
	global position_joueur

	pygame.init()
	# loading soung
	impossible_soung = pygame.mixer.Sound("doc/son/impossible.wav")
	move_soung = pygame.mixer.Sound("doc/son/move.wav")

	if direction_deplacement == directions["HAUT"]:
		# Verification si le joueur a le droit de se deplacer ou de deplacer une caisse
		# Si le joueur est au bord de la fenenetre
		if position_joueur[1] - 1 < 0:
			impossible_soung.play()
			return False

		# S'il y a un mur on arrete
		if grille[position_joueur[0]][position_joueur[1] - 1] == items["MUR"]:
			impossible_soung.play()
			return False

		# Si on veut pousser une caisse il faut verifier qu'il y a pas un mur derriere ou une autre caisse ou le bord de la fenetre
		if (grille[position_joueur[0]][position_joueur[1] - 1] == items["CAISSE"] or grille[position_joueur[0]][
			position_joueur[1] - 1] == items["CAISSE_OK"]) and (
				(position_joueur[1] - 2 < 0 or grille[position_joueur[0]][position_joueur[1] - 2] == items["MUR"]) or (
				grille[position_joueur[0]][position_joueur[1] - 2] == items["CAISSE"]) or (
						grille[position_joueur[0]][position_joueur[1] - 2] == items["CAISSE_OK"])):
			impossible_soung.play()
			return False

		# Si on arrive la c'est qu'on peut deplacer le joueur
		# On verifie d'abord qu'il n'y a pas de caisse a deplacer
		deplacer_caisse(directions["HAUT"], position_joueur)

		# On peut enfin deplacer le joueur
		position_joueur = [position_joueur[0], position_joueur[1] - 1]
		move_soung.play()

	if direction_deplacement == directions["BAS"]:
		# Verification si le joueur a le droit de se deplacer ou de deplacer une caisse
		# Si le joueur est au bord de la fenenetre
		if position_joueur[1] + 1 >= nb_bloc_height:
			impossible_soung.play()
			return False

		# S'il y a un mur on arrete
		if grille[position_joueur[0]][position_joueur[1] + 1] == items["MUR"]:
			impossible_soung.play()
			return False

		# Si on veut pousser une caisse il faut verifier qu'il y a pas un mur derriere ou une autre caisse ou le bord de la fenetre
		if (grille[position_joueur[0]][position_joueur[1] + 1] == items["CAISSE"] or grille[position_joueur[0]][
			position_joueur[1] + 1] == items["CAISSE_OK"]) and (
				(position_joueur[1] + 2 < 0 or grille[position_joueur[0]][position_joueur[1] + 2] == items["MUR"]) or (
				grille[position_joueur[0]][position_joueur[1] + 2] == items["CAISSE"]) or (
						grille[position_joueur[0]][position_joueur[1] + 2] == items["CAISSE_OK"])):
			impossible_soung.play()
			return False

		# Si on arrive la c'est qu'on peut deplacer le joueur
		# On verifie d'abord qu'il n'y a pas de caisse a deplacer
		deplacer_caisse(directions["BAS"], position_joueur)

		# On peut enfin deplacer le joueur
		position_joueur = [position_joueur[0], position_joueur[1] + 1]
		move_soung.play()

	if direction_deplacement == directions["GAUCHE"]:
		# Verification si le joueur a le droit de se deplacer ou de deplacer une caisse
		# Si le joueur est au bord de la fenenetre
		if position_joueur[0] - 1 < 0:
			impossible_soung.play()
			return False

		# S'il y a un mur on arrete
		if grille[position_joueur[0] - 1][position_joueur[1]] == items["MUR"]:
			impossible_soung.play()
			return False

		# Si on veut pousser une caisse il faut verifier qu'il y a pas un mur derriere ou une autre caisse ou le bord de la fenetre
		if (grille[position_joueur[0] - 1][position_joueur[1]] == items["CAISSE"] or grille[position_joueur[0] - 1][
			position_joueur[1]] == items["CAISSE_OK"]) and (
				(position_joueur[0] - 2 < 0 or grille[position_joueur[0] - 2][position_joueur[1]] == items["MUR"]) or (
				grille[position_joueur[0] - 2][position_joueur[1]] == items["CAISSE"]) or (
						grille[position_joueur[0] - 2][position_joueur[1]] == items["CAISSE_OK"])):
			impossible_soung.play()
			return False

		# Si on arrive la c'est qu'on peut deplacer le joueur
		# On verifie d'abord qu'il n'y a pas de caisse a deplacer
		deplacer_caisse(directions["GAUCHE"], position_joueur)

		# On peut enfin deplacer le joueur
		position_joueur = [position_joueur[0] - 1, position_joueur[1]]
		move_soung.play()

	if direction_deplacement == directions["DROITE"]:
		# Verification si le joueur a le droit de se deplacer ou de deplacer une caisse
		# Si le joueur est au bord de la fenenetre
		if position_joueur[0] + 1 >= nb_bloc_width:
			impossible_soung.play()
			return False

		# S'il y a un mur on arrete
		if grille[position_joueur[0] + 1][position_joueur[1]] == items["MUR"]:
			impossible_soung.play()
			return False

		# Si on veut pousser une caisse il faut verifier qu'il y a pas un mur derriere ou une autre caisse ou le bord de la fenetre
		if (grille[position_joueur[0] + 1][position_joueur[1]] == items["CAISSE"] or grille[position_joueur[0] + 1][
			position_joueur[1]] == items["CAISSE_OK"]) and (
				(position_joueur[0] + 2 < 0 or grille[position_joueur[0] + 2][position_joueur[1]] == items["MUR"]) or (
				grille[position_joueur[0] + 2][position_joueur[1]] == items["CAISSE"]) or (
						grille[position_joueur[0] + 2][position_joueur[1]] == items["CAISSE_OK"])):
			impossible_soung.play()
			return False

		# Si on arrive la c'est qu'on peut deplacer le joueur
		# On verifie d'abord qu'il n'y a pas de caisse a deplacer
		deplacer_caisse(directions["DROITE"], position_joueur)

		# On peut enfin deplacer le joueur
		position_joueur = [position_joueur[0] + 1, position_joueur[1]]
		move_soung.play()


# //////////////////////////////////////////////////////////////////////////////////////////////////
def deplacer_caisse(direction_deplacement, position_joueur):
	global grille

	if direction_deplacement == directions["HAUT"]:
		if grille[position_joueur[0]][position_joueur[1] - 1] == items["CAISSE"] or grille[position_joueur[0]][
			position_joueur[1] - 1] == items["CAISSE_OK"]:
			if grille[position_joueur[0]][position_joueur[1] - 2] == items["OBJECTIF"]:
				grille[position_joueur[0]][position_joueur[1] - 2] = items["CAISSE_OK"]

			else:
				grille[position_joueur[0]][position_joueur[1] - 2] = items["CAISSE"]

			if grille[position_joueur[0]][position_joueur[1] - 1] == items["CAISSE_OK"]:
				grille[position_joueur[0]][position_joueur[1] - 1] = items["OBJECTIF"]

			else:
				grille[position_joueur[0]][position_joueur[1] - 1] = items["VIDE"]

	if direction_deplacement == directions["BAS"]:
		if grille[position_joueur[0]][position_joueur[1] + 1] == items["CAISSE"] or grille[position_joueur[0]][
			position_joueur[1] + 1] == items["CAISSE_OK"]:
			if grille[position_joueur[0]][position_joueur[1] + 2] == items["OBJECTIF"]:
				grille[position_joueur[0]][position_joueur[1] + 2] = items["CAISSE_OK"]

			else:
				grille[position_joueur[0]][position_joueur[1] + 2] = items["CAISSE"]

			if grille[position_joueur[0]][position_joueur[1] + 1] == items["CAISSE_OK"]:
				grille[position_joueur[0]][position_joueur[1] + 1] = items["OBJECTIF"]

			else:
				grille[position_joueur[0]][position_joueur[1] + 1] = items["VIDE"]

	if direction_deplacement == directions["GAUCHE"]:
		if grille[position_joueur[0] - 1][position_joueur[1]] == items["CAISSE"] or grille[position_joueur[0] - 1][
			position_joueur[1]] == items["CAISSE_OK"]:
			if grille[position_joueur[0] - 2][position_joueur[1]] == items["OBJECTIF"]:
				grille[position_joueur[0] - 2][position_joueur[1]] = items["CAISSE_OK"]

			else:
				grille[position_joueur[0] - 2][position_joueur[1]] = items["CAISSE"]

			if grille[position_joueur[0] - 1][position_joueur[1]] == items["CAISSE_OK"]:
				grille[position_joueur[0] - 1][position_joueur[1]] = items["OBJECTIF"]

			else:
				grille[position_joueur[0] - 1][position_joueur[1]] = items["VIDE"]

	if direction_deplacement == directions["DROITE"]:
		if grille[position_joueur[0] + 1][position_joueur[1]] == items["CAISSE"] or grille[position_joueur[0] + 1][
			position_joueur[1]] == items["CAISSE_OK"]:
			if grille[position_joueur[0] + 2][position_joueur[1]] == items["OBJECTIF"]:
				grille[position_joueur[0] + 2][position_joueur[1]] = items["CAISSE_OK"]

			else:
				grille[position_joueur[0] + 2][position_joueur[1]] = items["CAISSE"]

			if grille[position_joueur[0] + 1][position_joueur[1]] == items["CAISSE_OK"]:
				grille[position_joueur[0] + 1][position_joueur[1]] = items["OBJECTIF"]

			else:
				grille[position_joueur[0] + 1][position_joueur[1]] = items["VIDE"]


# ////////////////////////////////////////////////////////////////////////////////////////////////
def afficher_instructions_console():
    ajouter_log("""
----------- Contrôles du jeu Sokoban ------------

Déplacements manuels :
  ↑  - Déplacer le joueur vers le haut
  ↓  - Déplacer le joueur vers le bas
  ←  - Déplacer le joueur vers la gauche
  →  - Déplacer le joueur vers la droite

Commandes spéciales :
  S  - Lancer le solveur automatique pour le niveau actuel
  R  - Recommencer le niveau actuel
  P  - Afficher la grille actuelle (debug)

Navigation entre niveaux :
  B   - Passer au niveau suivant
  N - Revenir au niveau précédent

Autres :
  Échap (ESC) - Quitter le niveau en cours
  I  - Afficher les instructions de contrôle
---------------------------------------------------
""")

def ajouter_log(msg):
    lignes = msg.splitlines()  # Sépare les lignes du texte
    for ligne in lignes:
        log_buffer.append(ligne)
    # On garde les X dernières lignes (ex. 30 maintenant qu'on en affiche plus)
    while len(log_buffer) > 30:
        log_buffer.pop(0)


def afficher_titre_lateral(surface, niveau, window_width, titre_height=40):
    """Affiche le titre 'Niveau : X' dans la zone latérale avec fond et séparation."""
    # Couleurs
    bg_color = (160, 160, 160)
    text_color = (20, 20, 20)
    line_color = (100, 100, 100)

    # Rect de fond pour le titre
    titre_rect = pygame.Rect(window_width - 200, 0, 200, titre_height)
    pygame.draw.rect(surface, bg_color, titre_rect)

    # Texte à afficher
    titre = "Niveau : {}".format(niveau + 1)
    
    # Police (tu peux aussi passer la police en paramètre si besoin)
    police_titre = pygame.font.SysFont('consolas', 22, bold=True)
    texte_surface = police_titre.render(titre, True, text_color)

    # Calcul pour centrer le texte horizontalement et verticalement
    texte_x = window_width - 200 + (200 - texte_surface.get_width()) // 2
    texte_y = (titre_height - texte_surface.get_height()) // 2

    # Affichage
    surface.blit(texte_surface, (texte_x, texte_y))

    # Ligne de séparation sous le titre
    pygame.draw.line(surface, line_color, (window_width - 200, titre_height), (window_width, titre_height), 2)
    
def afficher_logs_terminal(surface, log_buffer, police, window_width, window_height, 
                           zone_largeur=800, zone_hauteur=None, 
                           bg_color=(30, 30, 30), text_color=(0, 255, 0), 
                           prompt="> ", scroll_offset=0):
	"""
	Affiche les logs dans une zone latérale façon terminal, avec support du scroll.
	"""
	if zone_hauteur is None:
		zone_hauteur = window_height - 20

	x = window_width - zone_largeur
	y = 0
	log_zone_rect = pygame.Rect(x, y, zone_largeur, zone_hauteur)

	# Dessiner le fond
	pygame.draw.rect(surface, bg_color, log_zone_rect)
	pygame.draw.rect(surface, (100, 100, 100), log_zone_rect, 2)

	# Générer toutes les lignes visibles (en tenant compte des retours à la ligne)
	lignes_visibles = []
	for log in log_buffer:
		lignes_visibles.extend(couper_texte(log, police, zone_largeur - 20))

	# Calculer combien de lignes on peut afficher
	ligne_max = zone_hauteur // 20

	# Appliquer le défilement
	debut = max(0, len(lignes_visibles) - ligne_max - scroll_offset)
	fin = debut + ligne_max
	lignes_a_afficher = lignes_visibles[debut:fin]

	# Afficher les lignes
	y_actuel = y + 10
	for ligne in lignes_a_afficher:
		texte = police.render(prompt + ligne, True, text_color)
		surface.blit(texte, (x + 10, y_actuel))
		y_actuel += 20

def couper_texte(texte, font, max_width):
    mots = texte.split(" ")
    lignes = []
    ligne_courante = ""

    for mot in mots:
        test_ligne = ligne_courante + (" " if ligne_courante else "") + mot
        if font.size(test_ligne)[0] <= max_width:
            ligne_courante = test_ligne
        else:
            lignes.append(ligne_courante)
            ligne_courante = mot
    if ligne_courante:
        lignes.append(ligne_courante)
    return lignes
