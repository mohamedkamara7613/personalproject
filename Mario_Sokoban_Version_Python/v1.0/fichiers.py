#coding:utf-8

# -------------- Mario Sokoban v1.0 -----------------------------------


"""
#Monday july 12 2021 00:31 debut de developpement
	fichiers.py
---------------
	Par Mohamed kamara

	Role : s'occupe de la gestion des fichiers enregistrements et lectures
"""


from data import *

#--------------------------------------------------------------------------------------------------
def chargerNiveau():
	"""	
		FOnction qui charge le niveau a jouer, ne prend aucun parametre 
		mais rend accessible la variable grille (carte a 2 dimensions)
	"""
	global grille
	try:
		with open("level.lvl", "r") as file:
			ligne = file.readline()
			i = 0
			while i < nb_bloc_width:
				j = 0
				while j < nb_bloc_height:
					if ligne[(i * nb_bloc_width) + j] == "0":
						grille[i][j] = 0

					if ligne[(i * nb_bloc_width) + j] == "1":
						grille[i][j] = 1
					if ligne[(i * nb_bloc_width) + j] == "2":
						grille[i][j] = 2
					if ligne[(i * nb_bloc_width) + j] == "3":
						grille[i][j] = 3
					if ligne[(i * nb_bloc_width) + j] == "4":
						grille[i][j] = 4
					if ligne[(i * nb_bloc_width) + j] == "5":
						grille[i][j] = 5

					j += 1
				i += 1
	except FileNotFoundError:
		print("level.lvl not found")
		return False

#--------------------------------------------------------------------------------------------------


def sauvegarderNiveau(grille):
	try:
		with open("level.lvl", "w") as file:

			i = 0
			while i < nb_bloc_width :
				j = 0 
				while j < nb_bloc_height:
					texte = str(grille[i][j])
					file.write(texte)
					j += 1
				i += 1
	except FileNotFoundError:
		return False	

