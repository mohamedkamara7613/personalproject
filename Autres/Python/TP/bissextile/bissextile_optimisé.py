#coding:utf-8

print("-------------Vérifié si une année est bissextile ou non --------------")

try:
	annee = int(input("Entrez une année : "))
except:
	print("Saisie incorrecte.................................")

bissextile = False

if (annee % 400) == 0 or (annee % 4) == 0 and (annee % 100) != 0 :
	bissextile = True

if bissextile is True:
	print("L'année {} est bissextile".format(annee))
else:
	print("L'année {} est bissextile".format(annee))