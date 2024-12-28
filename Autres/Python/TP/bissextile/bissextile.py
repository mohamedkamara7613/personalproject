#coding:utf-8
"""
	Une année est dite bissextile si c'est un multiple de 4, sauf si c'est un multiple de 100. Toutefois, elle est considérée comme
	bissextile si c'est un multiple de 400. Je développe :
		Si une année n'est pas multiple de 4, on s'arrête là, elle n'est pas bissextile.
		Si elle est multiple de 4, on regarde si elle est multiple de 100.
			Si c'est le cas, on regarde si elle est multiple de 400.
				Si c'est le cas, l'année est bissextile.
				Sinon, elle n'est pas bissextile.
			Sinon, elle est bissextile.
"""


print("-------------- Vérifier si une année est bissextile ou non ------------------")

try:
	annee = int(input("Entrez une année : "))
	assert annee > 0
except ValueError as exception_retournee:
	print("Valeur de l'exception : ",exception_retournee)
	print("\tSaisie incorrecte.......................................................")
except AssertionError :
	print("Vous avez saisie une année inférieur a 0")
else:
	if (annee % 4) != 0:
		print(" l'année '{}' n'est pas bissextile".format(annee))
	elif (annee % 100) == 0:
		if (annee % 400) == 0:
			print("l'année '{}' est bissextile".format(annee))
		else:
			print("l'année '{}' n'est pas bissextile".format(annee))
	else:
		print("l'année '{}' n'est pas bissextile".format(annee))

