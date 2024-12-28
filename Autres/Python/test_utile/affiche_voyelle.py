#!/usr/bin/python3
#coding:utf-8
import time

chaine = input("Entrez votre texte ici : ")

for lettre in chaine:
	if lettre in "AEIOUYaeiouy ":
		print(lettre, end="")
	else:
		print("*", end="")
print("")

time.sleep(5)