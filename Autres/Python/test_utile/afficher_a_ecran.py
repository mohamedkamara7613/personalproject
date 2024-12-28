#coding:utf-8

def afficher(*valeur, fin=" ", sep=" "):
	liste_param = []
	for i in valeur:
		liste_param.append(str(i))

	chaine = sep.join(liste_param) + fin

	print(chaine)

age = 10
prenom = "amdo"
flottant = 3.14552
afficher("test", age, flottant)