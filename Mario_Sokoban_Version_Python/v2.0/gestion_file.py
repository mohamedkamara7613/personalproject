# coding:utf-8

"""
	starting at Wen 27 Aug 2021
	Par Mohamed Kamara
--------------------- Mario Sokoban v2.0 --------------------------
-------------- gestion_file.py


	Rôle du fichier : s'occupe de l'ecriture et de la lecture des fichiers
"""

from data import *
import os
import pickle


def load_level(niveau):
	global niveaux
	global grille
	line = ''
	dernier_niveau = 0

	if not os.path.exists("doc/level.lvl"):
		with open("doc/level.lvl", "wb") as file:
			record = pickle.Pickler(file)
			record.dump(niveaux)

	try:
		# Chargement du dictionnaire dans 'niveaux'
		with open("doc/level.lvl", "rb") as file:
			get_record = pickle.Unpickler(file)
			niveaux = get_record.load()

		# Recherche de la derniere cle du dictionnaire niveaux
		for key in niveaux:
			dernier_niveau = key

		# Selection du niveau demandé
		if niveau > dernier_niveau:
			return 76
		elif niveau < 0:
			niveau = 0

		line = niveaux[niveau]

		# Ecriture du niveau sur la carte
		i = 0
		while i < nb_bloc_width:
			j = 0
			while j < nb_bloc_height:
				if line[(i * nb_bloc_width) + j] == '0':
					grille[i][j] = 0

				elif line[(i * nb_bloc_width) + j] == '1':
					grille[i][j] = 1

				elif line[(i * nb_bloc_width) + j] == '2':
					grille[i][j] = 2

				elif line[(i * nb_bloc_width) + j] == '3':
					grille[i][j] = 3

				elif line[(i * nb_bloc_width) + j] == '4':
					grille[i][j] = 4

				elif line[(i * nb_bloc_width) + j] == '5':
					grille[i][j] = 5

				j += 1
			i += 1
	except FileNotFoundError:
		return False


# ////////////////////////////////////////////////////////////////////////////////////////////////

def save_level(grille):
	niveau = 0
	niveaux = {}
	line = ""

	try:
		# Chargement du dictionnaire 'niveaux'
		with open('doc/level.lvl', 'rb') as file:
			get_record = pickle.Unpickler(file)
			niveaux = get_record.load()

		# Recherche de la derniere cle du dictionnaire
		for key in niveaux:
			niveau = key
		niveau += 1

		# Ajout d'un nouveau niveau avec une nouvelle cle
		i = 0
		while i < nb_bloc_width:
			j = 0
			while j < nb_bloc_height:
				line = line + str(grille[i][j])
				niveaux[niveau] = line
				j += 1
			i += 1

		# Ecriture du dictionnaire dans un fichier en binaire
		with open("doc/level.lvl", "wb") as file:
			record = pickle.Pickler(file)
			record.dump(niveaux)

	except FileNotFoundError:
		return False
