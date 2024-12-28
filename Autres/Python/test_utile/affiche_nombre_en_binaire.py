#coding:utf-8

nombre_binaire = ''

#Recuperation du nombre a afficher en binaire
try:
	nombre_decimal = int(input("Entrez un nombre : "))
except ValueError:
	print("Saisie incorrect")
nombre_entrer = nombre_decimal

exposant_maximum=0
while True:
	debut_test = 2**exposant_maximum
	if nombre_decimal <= debut_test:
		break
	exposant_maximum += 1


while exposant_maximum >= 0:

	exposant_test = (2**exposant_maximum)

	if nombre_decimal >= exposant_test:
		nombre_binaire += '1'
		nombre_decimal -= exposant_test
	else:
		nombre_binaire += '0'

	exposant_maximum -= 1


print("\nDecimal : ",nombre_entrer, "\n\nBinaire : ",nombre_binaire, '\n\n')


"""
Ce que nous allons faire pour un calcul, c'est de regarder si la puissance de 2 la plus élevée peut être contenue dans notre
nombre, et recommencer avec la puissance de 2 suivante.
Pour notre exemple, est-ce que 128 peut être contenu dans 45 ? Non, je mets 0 dans la colonne 128.
On passe à la puissance de 2 suivante :
Est-ce que 64 peut être contenu dans 45 ? Non, je mets 0 dans la colonne 64.
Est-ce que 32 peut être contenu dans 45 ? Oui ! Je mets 1 dans la colonne 32 ET j'ôte 32 à 45.
45 - 32 = 13
Je continue maintenant avec ce nouveau chiffre. Est-ce que 16 peut être contenu dans 13 ?
Non, je mets 0 dans la colonne 16.
Est-ce que 8 peut être contenu dans 13 ? Oui ! Je mets 1 dans la colonne 8 ET j'ôte 8 à 13. 13 - 8 = 5
Est-ce que 4 peut être contenu dans 5 ? Oui ! Je mets 1 dans la colonne 4 ET j'ôte 4 à 5.
5 - 4 = 1
Est-ce que 2 peut être contenu dans 1 ? Non, je mets 0 dans la colonne 2.
Est-ce que 1 peut être contenu dans 1 ? Oui ! Je mets 1 dans la colonne 1 ET j'ôte 1 à 1.
1 - 1 = 0 donc j'ai fini !

"""

