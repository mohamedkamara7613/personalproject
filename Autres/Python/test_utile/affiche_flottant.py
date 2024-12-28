#coding:utf-8
def affiche_flottant(flottant):
	"""
		Fonction prenant en parametre un flottant et renvoyant 
		une chaine de caractere représentant la troncature de ce nombre
		La partie flottant a une longueur de 3 chiffres
		Et le point décimal est remplacé par la virgule
	"""
	if type(flottant) is not float:
		raise ValueError("Le nombre doit être un flottant")		
	flottant = str(flottant)
	partie_entiere, partie_decimal = flottant.split(".")
	result = ",".join([partie_entiere, partie_decimal[:3]])
	print(result)


# PROGRAMME PRINCIPALE
nombre = float(input("Entrez un nombre décimal : "))
affiche_flottant(nombre)