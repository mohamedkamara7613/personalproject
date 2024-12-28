#coding:utf-8

def gagner(taille_mot, mot_actuel):
	"""
		Fonction qui verifie si le, joueur a gagné ou non
	"""
	joueur_gagne = True
	i = 0
	#parcours du tableau mot_actuel
	while i < taille_mot:
		if mot_actuel[i] == False:
			joueur_gagne = False 
		i += 1
	return joueur_gagne

#------------------------------------------------------------------------------------------------------------------------------
def lire_caractere():
	"""
		fonction lire_caractere() qui retourne le premier caractere en majuscule
	"""
	while 1:
		caractere = input("\nProposer un caractere : ")
		#mettre tous les caracteres en majuscule et prendre le premier caractere entré
		caractere = caractere.upper()
		try:
			caractere = caractere[0]
			return caractere
		except IndexError:
			print("-------Saisie incorrect------")
			continue


#------------------------------------------------------------------------------------------------------------------------------
def verifier_caractere(caractere_entrer, mot_secret, mot_actuel):
	"""
		Fonction qui verifie si le caractere entré par l'utilisateur est la bonne, c'est a dire se trouve dans le mot_secret
		le caractere doit etre en majuscule de meme que le lettre du mot secret.
	"""
	bonne_lettre = False
	i = 0

	#parcours de mot_secret en comparant le caractere_entrer par les lettres du mot secret
	for lettre in mot_secret:
		#si caractere_entrer == mot_secret[i] mettre bonne lettre == Vrai et le tableau mot_actuel == vrai a l'indice correspondant
		if caractere_entrer == lettre:
			bonne_lettre = True
			mot_actuel[i] = True
		i += 1
	return bonne_lettre


#------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
	car = lire_caractere()
	actuel = [False]*6
	#verifier_caractere("M", "MARRON", actuel)
