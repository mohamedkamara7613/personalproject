#coding:utf-8
import random
def piocher_mot():
	#VARIABLE
	nombre_mot = 0
	num_mot_choisi = -1
	#DEBUT
	try:
		with open("doc/dictionnaire.txt", "r") as file:
			tout_fichier = file.read()
			tout_fichier = tout_fichier.split("\n")
			
			#compter le nombre de mot
			for mot in tout_fichier:
				nombre_mot += 1	

			num_mot_choisi = random.randrange(nombre_mot)
			return tout_fichier[num_mot_choisi]

	except FileNotFoundError:
		print("-------Ouverture de fichier impossible, fichier introuvable-------")
		exit(1)




		#verifier que le fichier est ouvert sinon retourner false et quitter

	#lire ligne par ligne le fichier pour compter le nombre de mot si y a 0 mot quitter

	#num_mot_choisi = random.randrange(nombre_mot)

	#retour au debut du fichier
	#tant que num_mot_choisi est different de 0 continuer la boucle
		#lire linge par ligne le fichier a chaque tour de boucle enlever 1 a num_mot_choisi

	#lire la ligne dans mot_secret

	#retourner vrai tout s'est bien passé


if __name__ == "__main__":
	mot_secret = ""
	mot = piocher_mot()
	print(mot)