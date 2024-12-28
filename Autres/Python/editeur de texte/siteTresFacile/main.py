#-*- coding: utf-8 -*-
#----------------------------------
# File Name     : main.py
# Author        : Mohamed Kamara
#----------------------------------
"""
	Contient le minimum de code principale pour le fonctionneme nt du programme
"""

# importation des bibliotheques necessaires
from tkinter import *
from tkinter import filedialog

# importation du module library
from library.library import *

# creation du dictionnaire qui stock les objets file
savedFile = {1:""}

# creation d'une instance sur la classe principale
root = Win("root", "c")

# Appel des methodes qui creer lobjet fenetre et tous ces composants
root.create()
root.add_text()
root.add_menu()
root.generate()

