#-*- coding: utf-8 -*-

from tkinter import *
from lib.library import *

# Creation d'une instance de lediteur de texte
root = TextEditor()

# creation de la fenetre
root.create()
# creation de la zone de saisie
root.addTextArea()
# ajout des menus
root.add_menu()
# maintient de l'affichage de la fenetre
root.generate()