#coding:utf-8

import tkinter
from details import *

#FONCTION
def record():
	var_label1.set("Voici les scores")
def aide():
	with open("doc/aide", "r") as file:
		var_label1.set(file.read())

def jeu_principale():
	print("Le jeu a commencé")

def configurer_menu(app):
	mainmenu = tkinter.Menu(app)

	first_menu = tkinter.Menu(mainmenu, tearoff=0)
	first_menu.add_command(label="Commencer", command=jeu_principale)
	first_menu.add_command(label="Records", command=record)
	first_menu.add_command(label="Aide", command=aide)
	first_menu.add_separator()
	first_menu.add_command(label="Quitter", command=app.quit)

	mainmenu.add_cascade(label="Option", menu=first_menu)

	app.config(menu=mainmenu)


#DEBUT DU PROGRAMME-----------------------------------------------------------
app = tkinter.Tk()
app.title("----PENDU----")
initialiser_fenetre(app)

# Menu
configurer_menu(app)

#Widget....
var_label1 = tkinter.StringVar()
label1 = tkinter.Label(app, textvariable=var_label1)
label1.pack()

#................
app.mainloop()


"""
def update_label1(*arg):
	if var_entry.get() == "4":
		exit("Programme terminé")
	elif var_entry.get() == "3":
		var_label1.set("Voici le score des joueurs")

	elif var_entry.get() == "2":

	elif var_entry.get() == "1":
		var_label1.set("Le jeu a commené")"""