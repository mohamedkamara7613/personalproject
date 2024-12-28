#coding:utf-8

"""
	Module ou est definit les principales fonctions de la gestion du pendu
"""
# IMPORTATION DE MODULE----------------------------------------------------------------------
import random 
import pickle
import os
import datetime

#VARIABLE GENERALE---------------------------------------------------------------------------
nom_fichier_scores = "doc/score"

# Traitement de l'entrée----------------------------------------------------------------------------------------
def lire_caractere():
	log("Lecture de caractere")
	"""
		Fonction qui lit la lettre entrée par l'utilisateur et retourne le premier caractere entré en magiscule
	"""
	while 1:
		print("\t", end="")
		caractere = input("\n\tProposez une lettre : ")

		caractere = caractere.upper()
		if caractere == "PENDU":
			return 76 
		try:
			caractere = caractere[0]
			return caractere
		except IndexError:
			log("Saisie incorrecte")
			texte = " Saisie incorrecte "
			texte = texte.center(50, "-")
			print(texte)
			continue

def verifier_caractere(caractere, mot_secret, mot_actuel):
	log("Vérification des caracteres")
	"""
		Fonction qui vérifie le caractère entré par l'utilisateur
		Vérifie si le caractere se trouve dans le mot caché ou non
	"""
	bonne_lettre = False
	i = 0
	if caractere == 76:
		with open("doc/dictionnaire", "r") as file:
			texte = file.read()
			print(texte)
		return False
	for car in mot_secret:
		if caractere == car:
			bonne_lettre = True
			mot_actuel[i] = caractere
		i += 1

	return bonne_lettre
#----------------------------------------------------------------------------------------

def gagner(mot_actuel, mot_secret):
	log("Verification si le joueur à gagner ou non")
	"""
		Vérifie si le joueur à gagner ou non, si l'un des caractères est fausse le joueur perd
	"""
	joueur_gagner = False
	mot_actuel = "".join(mot_actuel)
	
	if mot_actuel == mot_secret:
		joueur_gagner = True

	return joueur_gagner

def piocher_mot(mot_secret):
	log("Choix du mot secret")
	"""	
		choisie un mot dans le fichier dictionnaire
	"""
	num_mot_choisi = 0
	nombre_mot = -1

	try:
		with open("doc/dictionnaire", "r") as file:
			texte = file.read()
			texte = texte.upper()
			mots = texte.split("\n")
			
			for mot in mots:
				nombre_mot += 1
			if nombre_mot == 1:
				texte = "Il n'y a pas de mot dans le fichier 'dictionnaire'"
				texte = texte.center(50, "-")
				print(texte)
				exit(1)

			num_mot_choisi = random.randrange(0,nombre_mot)
			
			return mots[num_mot_choisi]


	except FileNotFoundError:
		log("Fichier 'dictionnaire' Introuvable")
		texte = " Fichier 'dictionnaire' Introuvable "
		texte = texte.center(50, "-")
		print(texte)
		exit(1)

# ENREGISTREMENT, SUPPRESSION ET RECUPERATION DE SCORE----------------------------------------------------
# Enrengistre la liste des scores
def enregistrer_score(score):
	log("Enrengistrement de la liste des scores")
	with open(nom_fichier_scores, "bw") as file:
		record = pickle.Pickler(file)
		record.dump(score)	

# Retourne la liste des scores
def recup_score():
	log("Recuperation de la liste des scores")
	score = {"joueur 1":0}
	try:
		if os.path.exists(nom_fichier_scores):
			with open(nom_fichier_scores, "br") as file:
				get_record = pickle.Unpickler(file)
				score = get_record.load()
		else:
			with open(nom_fichier_scores, "bw") as file:
				pass
	except EOFError:
		pass
	return score

# Recuperation du nom du joueur
def recup_nomjoueur():
	log("Recupération du nom du joueur")
	"""Fonction chargée de récupérer le nom de l'utilisateur.
	Le nom de l'utilisateur doit être composé de 4 caractères minimum,
	chiffres et lettres exclusivement.
	Si ce nom n'est pas valide, on appelle récursivement la fonction
	pour en obtenir un nouveau"""
	nom_joueur = input("\tTapez votre nom: ")
	# On met la première lettre en majuscule et les autres en minuscules
	nom_joueur = nom_joueur.capitalize()
	if not nom_joueur.isalnum() or len(nom_joueur)<4:
		print("\tCe nom est invalide.")
		# On appelle de nouveau la fonction pour avoir un autre nom
		return recup_nomjoueur()
	else:
		return nom_joueur

def afficher_score(score):
	log("Affichage des scores")
	meilleur_joueur = ""
	meilleur_score = 0
	print()
	for i,j in score.items():
		print("\tNom : {} ---> {} points".format(i,j))

		if j > meilleur_score:
			meilleur_joueur = i
			meilleur_score = j
	print("\tMeilleur score : {} --> {} \n".format(meilleur_joueur,meilleur_score))

def supprimer_joueur(score):
	log("Supprimer un joueur")
	entre = input("\tVoulez-vous supprimer un joueur ? (O/n) : ")
	entre = entre.upper()

	if entre == "O":
		entre = input("\tEntrez le nom du joueur à supprimer : ")
		if entre not in score:
			print("\t'{}' Ce joueur n'existe pas !!".format(entre))
		else:
			score.pop(entre)
			print("\t'{}' a été supprimer !! ".format(entre))

	else:
		print("\tAucun joueur n'a été supprimer")


def log(message="NÉANT"):
	with open("doc/log.txt", "a") as file:
		chaine = "DATE : " + str(datetime.datetime.now()) + "\n"
		file.write(chaine)

		chaine = "MESSAGE : " + message + "\n"

		file.write(chaine)



#TEST---------------------------------------------------------------------------------------
if __name__ == "__main__":
	log("Imposible")
	pass
	#nom_joueur, score = enregistrer()
	#print(nom_joueur, score)


"""
		texte = file.read()
		texte = texte.split("\n")
		print(texte)

		for elt in texte:
			nombre_ligne += 1

		i = 0
		while i < nombre_ligne:
			ligne = file.readligne()
			if donnees_joueur == 

		
		dico = dict(texte)
		print(type(dico))


	return score

def supprime_joueur(score={"joueur 1":0}):
	entre = input("\tVoulez vous supprimer un joueur ? (o/n)")
	if entre == 'o':
		nom_joueur = input("\tEntrez le nom du joueur : ")
		if nom_joueur not in score:
			print("\tCe joueur n'existe pas")
			return supprime_joueur(score)
		else:
			print(score)
			del score[nom_joueur]
			print(score)
			print("\t{} supprimé ".format(nom_joueur))
	else:
		return score


"""