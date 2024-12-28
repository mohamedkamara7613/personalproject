#-*- coding: utf-8 -*-
#----------------------------------
# File Name     : library.py
# Author        : Mohamed Kamara
#----------------------------------
"""
	Contient les definitions des classes et methode
"""
# importation des modules necessaires
from tkinter import *
import os
savedFile = {1:""}

#==========================================================
#  - Définition de la classe de la fenetre principale 
#========================================================== 
class Win:
	def __init__(self, master, content):
		# Fenetre principale
		self.master = master
		# Main Text Widget
		self.content = content
	# Creation de la fenetre tkinter
	def create(self):
		self.master = Tk()
		self.master.title("Editeur de texte")
		self.master.geometry("700x550")
	# Methode qui ajoute la zone de texte
	def add_text(self):
		self.content = Text(self.master)
		self.content.pack(expand=1, fill='both') 
	# Generation de la fenetre principale
	def generate(self):
		self.master.mainloop()

#======================================
#  - Définition des actions des menus 
#====================================== 
#------------------------------ 
# - actions du menu Fichier 
#------------------------------- 
	def quitter(self):
		self.master.quit()
	def nouveau(self):
		os.popen("python main.py")
	def fopen(self):
		file = self.master.fileName = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("Text Files","*.txt"),("all files","*.*")))
		fp = open(file, "r")
		r = fp.read()
		self.content.insert("1.0", r)
	# Commande enregistrer sous
	def saveAs(self):
		fichier = self.master.filename=filedialog.asksaveasfilename(initialdir="/", title="Enregistrer sous", filetypes=(("Fichier Texte","*.txt"),  ("Tous les fichiers","*.*")))
		fichier = fichier + ".txt"
		savedFile[1] = fichier
		f = open(fichier, "w")
		s = self.content.get("1.0", END)
		f.write(s)
		f.close()
	# Commande enregistrer
	def save(self):
		if(savedFile[1] == ""):
			self.saveAs()
		else:
			f = open(savedFile[1], "w")
		s = self.content.get("1.0", END)
		f.write()
		f.closr()
#------------------------------ 
# - actions du menu Edition
#------------------------------- 
	def copy(self):
		self.content.clipboardclear()
		self.content.clipboard_append(self.content.selection_get())
	def past(self):
		self.content.insert(INSERT, self.content.clipboard_get())
	def cut(self):
		self.copy()
		self.content.delete("sel.first", "sel.last")
#======================================
#  - Methode d'ajout des menus 
#====================================== 
	def add_menu(self):
		# Creation de la barre des menus
		menuBar = Menu(self.master)
		
		# Creation du menu fichier
		menuFichier = Menu(menuBar, tearoff=0)
		menuBar.add_cascade(label="Fichier", menu=menuFichier)
		# Creation des sous menus du menu fichier
		menuFichier.add_command(label="Nouveau", command=self.nouveau)
		menuFichier.add_command(label="Ouvrir", command=self.fopen)
		menuFichier.add_command(label="Enregistrer", command=self.save)
		menuFichier.add_command(label="Enregistrer sous", command=self.saveAs)
		menuFichier.add_command(label="Quitter", command=self.quitter)


		# Creation du menu edition
		menuEdition = Menu(menuBar, tearoff=0)
		menuBar.add_cascade(label="Edition", menu=menuEdition)
		menuEdition.add_command(label="Annuler")
		menuEdition.add_command(label="Rétablir")
		menuEdition.add_command(label="Copier", command=self.copy)
		menuEdition.add_command(label="Couper", command=self.cut)
		menuEdition.add_command(label="Coller", command=self.past)

		# Creation du menu Outils
		menuOutils = Menu(menuBar, tearoff=0)
		menuBar.add_cascade(label="Outils", menu=menuOutils)
		menuOutils.add_command(label="Préférences")

		# Creation du menu aide
		menuAide = Menu(menuBar, tearoff=0)
		menuBar.add_cascade(label="Aide", menu=menuAide)
		menuAide.add_command(label="A propos")

		self.master.config(menu=menuBar)



