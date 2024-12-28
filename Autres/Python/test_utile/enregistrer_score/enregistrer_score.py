#coding:utf-8
"""
	ALGORITHME
		envoyer en parametre le score a enregistrer
		score est un dictionnaire
		enregistrer(score) 
			si le fichier n'existe pas le creer
				mettre score par defaut joueur 1 et 0

			sinon ouvrir le fichier dans lequel enregistrer le score 
				enregistrer score
"""
import os
import pickle


nom_fichier_scores = "scores"

def enregistrer_score(score):
	with open(nom_fichier_scores, "bw") as file:
		record = pickle.Pickler(file)
		record.dump(score)

def recup_nom_joueur():
	return "joueur 1"
	

def recup_score():
	score = {"joueur 1":0}
	if os.path.exists(nom_fichier_scores):
		with open(nom_fichier_scores, "br") as file:
			get_record = pickle.Unpickler(file)
			score = get_record.load()
	else:
		with open(nom_fichier_scores, "bw") as file:
			pass

	return score


#Debut 
nom_joueur = recup_nom_joueur()
score = recup_score()
print(score)

#le jeu se passe
essais = 12
if nom_joueur not in score:
	score[nom_joueur] = 0

print(score)

score[nom_joueur] = score[nom_joueur] + essais


enregistrer_score(score)
print(score)