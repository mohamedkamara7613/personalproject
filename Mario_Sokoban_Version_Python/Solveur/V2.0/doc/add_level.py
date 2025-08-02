# coding:utf-8



# Importing
import pickle
import os
import time

# VARIABLE
niveaux = {}

try :
	print("\n\n--------------------SECTION RESÉRVÉ AU DEVELOPPEUR---------------------------\n\n")


	# Si le fichier level.lvl n'existe pas il faut le creer avec deux niveaux par defaut
	if os.path.exists("level.lvl") is False:
		print("---------------Le fichier 'level.lvl' n'existe pas -------------------------------")
		print("---------------- 2 NIVEAUX CRÉER -----------------------")
		print("Niveau 1 : 111111111111111111111111111111111111111111111111111111111111114200000311111111111111111111111111111111111111111111111111111111111111111111111111")
		print("Niveau 2 : 111111111111111111111111111111111111111400001111111111221111111111001111111111001111111111031111111111011111111111011111111111311111111111111111")
		
		niveaux = {
			0: "111111111111111111111111111111111111111111111111111111111111114200000311111111111111111111111111111111111111111111111111111111111111111111111111",
			1: "111111111111111111111111111111111111111400001111111111221111111111001111111111001111111111031111111111011111111111011111111111311111111111111111"}

		with open("level.lvl", "wb") as file:
			record = pickle.Pickler(file)
			record.dump(niveaux)

		exit("...Fichier 'level.lvl' créer avec succés...")

	else:
		while True:
		# Si le fichier level.lvl existe pour ajouter un niveau de plus
			# il faut d'abord sauvegarder les niveaux déja présent 
			with open("level.lvl", "rb") as file:
				get_record = pickle.Unpickler(file)
				niveaux = get_record.load()

			


			valide = False
			while valide is False:
				# Demander la nouvelle ligne
				new_line = input("Collez le nouveau niveau : ")
				
				if len(new_line) != 144:
					print("\n---------------------TAILLE DE LA CHAINE INCORRECT (144 lettres requis) ------------------------\n")
					valide = False

				elif len(new_line) == 144:
					pos = 0
					for letter in new_line:
						pos += 1
						letter = int(letter)
						if letter > 5:
							print("------- : {} NON VALIDE (position {} dans la chaine)".format(letter, pos))
							valide = False
						else:
							valide = True

				for key in niveaux:
					if niveaux[key] == new_line:
						print("--------NIVEAU DEJA PRESENT----------")
						valide = False

			print("\n-----------Niveau Valide-------------")

			# A ce stade tout va bien
			print(niveaux,"\n\n")

			for key in niveaux:
				new = key
			
			#niveaux.pop(key)
			
			new += 1
			niveaux[new] = new_line

			with open("level.lvl", "wb") as file:
				record = pickle.Pickler(file)
				record.dump(niveaux)

			print(niveaux)
			print("\n --------------Niveau enregistré avec succés-----------")
except KeyboardInterrupt:
	print("\nFin de l'ajout des niveaux")