#coding:utf-8

#IMPORTATION DE MODULE
from math import ceil
from random import randrange
from os import system
import pickle

try:
	#VARIABLE
	jeu_lancee = True
	with open("data", "bw") as file:
		pass

	#FONCTION
	def gagner(numchoisi, numGagnant):
		if numGagnant == numchoisi:
			return 1
		elif numGagnant % 2 == numchoisi % 2 : #ils sont tous les deux paires ou tous les deux impaires 
			return 2
		else:
			return 3
	def lancee():
		return randrange(50)

	def save_data(argentUtilisateur):
		with open("data", "bw") as file:
			record = pickle.Pickler(file)
			record.dump(argentUtilisateur)
		
	def aide():
		print("---------------------------------------------------------------------------------")
		print("\tLe joueur mise sur un numéro compris entre 0 et 49 (50 numéros en tout).")
		print("\tEn choisissant son numéro, il y dépose la somme qu'il souhaite miser.")
		print("\tLa roulette est constituée de 50 cases allant naturellement de 0 à 49.")
		print("\tLes numéros pairs sont de couleur noire, les numéros impairs sont de")
		print("\tcouleur rouge Le croupier lance la roulette, lâche la bille et quand")
		print("\tla roulette s'arrête le croupier relève le numéro de la case dans")
		print("\tlaquelle la bille s'est arrêtée. Le numéro sur lequel s'est arrêtée la")
		print("\tbille est, naturellement, le numéro gagnant Si le numéro gagnant est celui")
		print("\tsur lequel le joueur a misé (probabilité de 1/50, plutôt faible), le croupier")
		print("\tlui remet 3 fois la somme misée. Sinon, le croupier regarde si le numéro misé")
		print("\tpar le joueur est de la même couleur que le numéro gagnant (s'ils sont tous")
		print("\tles deux pairs ou tous les deux impairs). Si c'est le cas, le croupier lui")
		print("\tremet 50 % de la somme misée. Si ce n'est pas le cas, le joueur perd sa mise")
		print("\tDans les deux scénarios gagnants vus ci-dessus (le numéro misé et le numéro")
		print("\tgagnant sont identiques ou ont la même couleur), le croupier remet au joueur ")
		print("\tla sommeinitialement misée avant d'y ajouter ses gains. Cela veut dire que,")
		print("\tdans ces deux scénarios, le joueur récupère de l'argent. Il n'y a que dans le")
		print("\ttroisième cas qu'il perd la somme misée.")

	def main():
		#VARIABLE
		argentMiser = 0
		numeroChoisi = -1
		chiffreGagant = -3
		continuerPartie = True

		try:
			#recuperation des données
			with open("data", "rb") as file:
				get_record = pickle.Unpickler(file)
				argentUtilisateur = get_record.load()
		except EOFError:
			argentUtilisateur = 1000

		while continuerPartie:
			print("---------------------------------------------------------------------------------")
			print("\t\tVous vous installez à la table avec ", argentUtilisateur,"$")
			argentMiser = input("\tEntrez la somme à miser : ")
			numeroChoisi = input("\tTapez le nombre sur lequel vous voulez miser (entre 0 et 49) : ")
			print("--------------------------------------------------------------------------------")
			#Essaie de convertion en entier des entrées de l'utilisateur
			try:
				numeroChoisi = int(numeroChoisi)
				argentMiser = int(argentMiser)
			except ValueError as erreur:
				print("\tSaisie incorrecte")
				argentMiser = -1
				numeroChoisi = -1
				continue

			#Vérification du numéro choisi
			if 49 < numeroChoisi < 0: 
				print("\tLe numéro choisi n'est pas dans l'intervalle 0 et 49")
				continue
			#Vérification de l'argent misée
			if argentMiser > argentUtilisateur:
				print("\tDésolé vous n'avez pas assez d'argent, vous n'avez que", argentUtilisateur,"$")
				continue
			if argentMiser < 0:
				print("\tVous avez rien miser ou somme inférieur à 0")
				continue

			chiffreGagnant = lancee()
			print("\tLa roulette tourne........ et s'arrête sur le numéro", chiffreGagnant)
			print("--------------------------------------------------------------------------------")

			retour = gagner(numeroChoisi, chiffreGagnant) 

			if retour == 1:
				print("\tBravo c'était le bon numéro")
				print("\tVous avez gagné le triple de la somme misée")
				argentUtilisateur = (3 * argentMiser) + argentUtilisateur
				print("\tMaintenant vous avez", argentUtilisateur,"$")
				print("--------------------------------------------------------------------------------")
			elif retour == 2:
				print("\tCe n'est pas le bon numéro mais c'est la bonne couleur")
				print("\tVous avez gagné la moitié de votre montant de mise")
				argentUtilisateur = ceil(argentMiser / 2) + argentUtilisateur
				print("\tMaintenant vous avez", argentUtilisateur,"$")
				print("--------------------------------------------------------------------------------")
			elif retour == 3:
				print("\tDomage c'est pas le bon numéro ni la bonne couleur")
				print("\tVous avez perdu la somme misée")
				argentUtilisateur -= argentMiser
				print("--------------------------------------------------------------------------------")
			#Interruption de la partie
			if argentUtilisateur <= 0:
				print("\tVous êtes ruiné ! c'est la fin de la partie.")
				continuerPartie = False
			else:
				#Affichage de l'argent du joueur
				print("\t\tVous avez à présent", argentUtilisateur,"$")
				quitter = input("\tSouhaite-vous quitter le casino (o/n) ? ")
				if quitter == 'o' or quitter == 'O':
					print("\tVous quittez le casino avec vos gains.")
					continuerPartie = False
					
					if argentUtilisateur > 0:
						save_data(argentUtilisateur)

	#PROGRAMME PRINCIPALE
	while jeu_lancee:
		print("----------------------------- Bienvenu sur ZCasino -----------------------------")
		print("\t\t1: Commencer   2: Help   3: Quitter")
		entree = input("\tTapez le numéro de votre choix: ")

		try:
			entree = int(entree)
		except ValueError:
			print("\tSaisie incorrecte")
			continue

		if entree == 3:
			jeu_lancee = False
		elif entree == 2:
			aide()
		else:
			main()
except KeyboardInterrupt:
	print("\n--------------------Arret prématuré du programme------------------")
		