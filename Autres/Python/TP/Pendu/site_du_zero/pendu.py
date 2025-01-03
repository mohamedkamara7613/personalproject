#coding:utf-8
"""Ce fichier contient le jeu du pendu.
Il s'appuie sur les fichiers :
- donnees.py
- fonctions.py"""
from donnees import *
from fonctions import *

# On récupère les scores de la partie
scores = recup_scores()

# On récupère un nom d'utilisateur
utilisateur = recup_nom_utilisateur()

# Si l'utilisateur n'a pas encore de score, on l'ajoute
if utilisateur not in scores.keys():
	scores[utilisateur] = 0 # 0 point pour commencer

# Notre variable pour savoir quand arrêter la partie
continuer_partie = 'o'
while continuer_partie != 'n':
	print("Joueur {0}: {1} point(s)".format(utilisateur,
	scores[utilisateur]))
	mot_a_trouver = choisir_mot()
	lettres_trouvees = []
	mot_trouve = recup_mot_masque(mot_a_trouver, lettres_trouvees)
	nb_chances = nb_coups
	while mot_a_trouver!=mot_trouve and nb_chances>0:
		print("Mot à trouver {0} (encore {1} chances)".format(mot_trouve, nb_chances))
		lettre = recup_lettre()
		if lettre in lettres_trouvees: # La lettre a déjà été choisie
			print("Vous avez déjà choisi cette lettre.")
		elif lettre in mot_a_trouver: # La lettre est dans le mot à trouver
			lettres_trouvees.append(lettre)
			print("Bien joué.")
		else:
			nb_chances -= 1
			print("... non, cette lettre ne se trouve pas dans le mot...")
		mot_trouve = recup_mot_masque(mot_a_trouver, lettres_trouvees)
	# A-t-on trouvé le mot ou nos chances sont-elles épuisées ?
	if mot_a_trouver==mot_trouve:
		print("Félicitations ! Vous avez trouvé le mot {0}.".format(mot_a_trouver))
	else:
		print("PENDU !!! Vous avez perdu.")
	# On met à jour le score de l'utilisateur
	scores[utilisateur] += nb_chances
	continuer_partie = input("Souhaitez-vous continuer la partie (O/N) ?")
	continuer_partie = continuer_partie.lower()
# La partie est finie, on enregistre les scores
enregistrer_scores(scores)
# On affiche les scores de l'utilisateur
print("Vous finissez la partie avec {0} points.".format(scores[utilisateur]))