#coding:utf-8

import sys

if len(sys.argv)  < 2:
	print("Entrez au moins 2 arguments")
	exit(1)

list_args = sys.argv
premier_arg = sys.argv[0]
deuxieme_arg = sys.argv[1]


print("TOUT LES ARGUMENTS : ",list_args)
print("le premier_arg :",premier_arg)
print("le deuxieme_arg :", deuxieme_arg)