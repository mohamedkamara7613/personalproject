#coding:utf-8

def table(nb=0, max=10):
	i = 0
	while i <= max:
		print("{} x {} = {}".format(i, nb, i * nb))
		i += 1

try:
	nb = int(input("Entrez un entier : "))
	maximum = int(input("Précisez l'entier maximum pour multiplier : "))
	table(nb, maximum)
except:
	print("Saisie incorrect !")



