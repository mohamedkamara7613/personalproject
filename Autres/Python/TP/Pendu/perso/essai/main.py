#coding:utf-8

#IMPORTATION
#import random
from pendu import *
from dico import *

try:
	#VARIABLE
	essai = 5 #10
	lettre_Trouver = 0
	mot_secret = ""#tableau de chaine de caractere
	#tableau de booleen(faux initialement), taille tableau egale au nombre caractere de mot secret
	caractere_entrer = ""


	#FONCTION 


	#DEBUT PROGRAMME PRINCIPALE
	mot_secret = piocher_mot()
	taille_mot = len(mot_secret)

	# initialiser tableau de booleen
	mot_actuel = [False]*taille_mot
	
	#boucle qui continue tant que : coup > 0 et gagner() != 0
	while (essai > 0 and gagner(taille_mot, mot_actuel) != True):
		print("Vous avez {} essai(s) : ".format(essai), end=" ")

		#parcours du tableau de booleen mot_actuel 
		i = 0
		while i < taille_mot:
			#SI vrai afficher lettre a l'indice correspondant sinon afficher *
			if mot_actuel[i] == True:
				print(mot_secret[i], end="") 
			else:
				print("*", end="")
			i += 1	

		#fonction lire_caractere() qui retourne un seule caractere en majuscule
		caractere_entrer = lire_caractere() 

		#si fonction de verifier_caractere() retourne faux le caractere n'est pas dans le mor secret, enlever un essai
		if verifier_caractere(caractere_entrer, mot_secret, mot_actuel) != True:
			essai -= 1
	
	#si gagner() retourne vrai 
	if gagner(taille_mot, mot_actuel):
		print("Bien jouer ! Le mot caché était bien : {} ".format(mot_secret))
	else:
		print("Le mot secret était : {} ".format(mot_secret))
		
except KeyboardInterrupt:
	print("\n-------Arret prématuré du programme-------")