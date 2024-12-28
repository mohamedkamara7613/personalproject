#coding:utf-8

#NOTE : prendre le nom du joueur pour enregistrer on ajoute le nombre de coup restant au score du joueur
#coder la fonction enregistrer
from fonctions import *

#VARIABLE
jeu_lance = True

try:
	chaine = "\n\nLancement du programme et importation des modules\n"+"".center(120,"-")
	log(chaine)
	#FONCTION
	def aide():
		log("Affichage de l'aide")
		with open("doc/aide", "r") as file:
			texte = file.read()
			print(texte)

	def main(nom_joueur): 
		log("Lancement d'une partie de jeu")
	# Initialisation--------------------------------------------------------------------------------
		essais = 10
		
		# recuper la liste des scores
		score = recup_score()

		# verifier si le joueur existe pour initialiser son score à 0
		if nom_joueur not in score:
			score[nom_joueur] = 0

		# Initialisation du mot caché et du mot actuel de l'utilisateur	
		mot_secret = []
		mot_secret  = piocher_mot(mot_secret)
		taille_mot = len(mot_secret)
		mot_actuel = [""]*taille_mot
		caractere = ""
		
	# Debut du jeu---------------------------------------------------------------------------------
		while essais > 0 and gagner(mot_actuel, mot_secret) == False:
				print("\n\n\t{} votre score est de {} ".format(nom_joueur, score[nom_joueur]))
				print("\tDévinez le mot caché, vous avez {} essais : ".format(essais), end="")

				# afficher les lettres trouvées
				i = 0
				for lettre in mot_secret:
					if mot_actuel[i] == lettre:
						print(lettre, end="")
					else:
						print("*", end="")
					i += 1

				caractere = lire_caractere()
				if verifier_caractere(caractere, mot_secret, mot_actuel) == False:
					essais -= 1

		# A la sorti de la boucle, vérification si le joueur à gagner ou non
		if gagner(mot_actuel, mot_secret) == True:
			print("\n\t\tBien joué, le mot caché était bien : {} ".format(mot_secret))
			# Ajouter le nombre d'essais restant au score du joueur
			score[nom_joueur] = score[nom_joueur] + essais
		else:
			print("\n\t\tPerdu ! le mot caché est : {} ".format(mot_secret))
		
		# Afficher le score du joueur a la fin d'une partie
		print("\tVotre score est maintenant de {} points".format(score[nom_joueur]))

		# Enregistrer le score du joueur
		enregistrer_score(score)

		while 1:
			entre = input("\tVoulez vous continer (o/n) : ")
			if entre == "n":
				return 0
			else:
				os.system("clear")
				os.system("cls")
				return main(nom_joueur)

	

#DEBUT DU PROGRAMME PRINCIPALE................................................................

	while jeu_lance == True:
		print("\n\n\t1: Commencer   2: Aide   3: Records   4: Quitter")
		entre = input("\tChoississez un numéro : ")	
		#................................................................................
		if entre == "4":
			chaine = "Fin du programme\n"+"".center(120,"-")
			log(chaine)
			texte = " A bientôt ! "
			texte = texte.center(50, "-")
			print(texte)
			break			
		#................................................................................
		elif entre == "3":
			score = recup_score()

			afficher_score(score)

			supprimer_joueur(score)

			afficher_score(score)
			
			enregistrer_score(score)
		#................................................................................	
		elif entre == "2":
			aide()

		#................................................................................
		else:
			nom_joueur = recup_nomjoueur()
			main(nom_joueur)
			os.system("clear")
			os.system("cls")

except KeyboardInterrupt:
	chaine = "Arret prématuré du programme\n"+"".center(120,"-")
	log(chaine)
	texte = " Arret prématuré du programme "
	texte = texte.center(50, "-")
	print("\n",texte)

	"""
			texte = "Saisie incorrecte"
			texte = texte.center(50, "-")
			print(texte)
		"""