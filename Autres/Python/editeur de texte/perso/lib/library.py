#-*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog
import os

savedFile = {1:""}

# Definition de la class editeur de texte
class TextEditor:
	"""	
		Definit les methodes et les variables necessaires a la creation de l'editeur de texte
	"""

	def __init__(self):
		self.root = ""
		self.content = ""
	# - Creation de la fenetre
	def create(self):
		self.root = Tk()
		self.root.title("Mon propre editeur de texte")
		# centrer la fenetre
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()
		fen_width = 700
		fen_height = 500
		pos_x = (screen_width // 2) - (fen_width // 2)
		pos_y = (screen_height // 2) - (fen_height // 2)
		self.root.geometry("{}x{}+{}+{}".format(fen_width, fen_height, pos_x, pos_y))
	# - Ajout de la zone de saisie
	def addTextArea(self):
		self.content = Text(self.root, bg='white') # #3465A4
		self.content.pack(expand=True, fill = 'both')
	# - maintient de la fenetre
	def generate(self):
		self.root.mainloop()
	#--------------------------------------------
	# - Ajout des commandes pour les menus
	#--------------------------------------------
	def quitter(self):
		self.root.quit()
		
	def nouveau(self):
		os.popen("python3 main.py")

	def fopen(self):
		"""
			Permet d'ouvrir un fichier et d'afficher son contenu sans le modifier
		"""
		file = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("Text Files", "*.txt"), ("All files", "*.*")))
		f = open(file, "r")
		contenu = f.read()
		self.content.insert(1.0, contenu)
		f.close()

	def saveAs(self):
		"""
			Permet d'ouvrir un fichier existant et d'enregistrer de nouveau informations(données)
		"""
		# Recuperation du chemin de sauvegarde du fichier
		file = filedialog.asksaveasfilename(initialdir="/", title="Save as", filetypes=(("Text Files", "*.txt"), ("All files", "*.*")))
		# Sauvegarde du chemin du fichier dans notre dictionnaire
		savedFile[1] = file
		# Ouverture du fichier
		f = open(file, "w")
		# Recuperation de la saisie depuis notre editeur de texte
		contenu = self.content.get(1.0, END)
		f.write(contenu)
		f.close()


	def save(self):
		"""
			Permet de creer un fichier et d'y enregistrer des informations(données)
		"""
		if(savedFile[1] == ""):
			self.saveAs()
		else:
			f = open(savedFile[1], "w")
			contenu = self.content.get(1.0, END)
			f.write(contenu)
			f.close()

	def copy(self):
		"""
			Permet de copier du texte dans le presse papier
		"""
		pass

	def cut(self):
		"""
			Permet de couper du texte dans le presse papier
		"""
		pass
	def past(self):
		"""
			Permet de coller du texte venant du presse papier
		"""
		pass
		
	#--------------------------------------------
	# - Ajout des menus
	#--------------------------------------------
	def add_menu(self):
		menuBar = Menu(self.root, bg='#000000', fg="white", activebackground="#0846A5", activeforeground="white")

		menuFichier = Menu(menuBar, tearoff=False, bg='#000000', fg="white", activebackground="#0846A5", activeforeground="white")
		menuBar.add_cascade(label="Fichier", menu=menuFichier)
		menuFichier.add_command(label="Nouveau", command=self.nouveau)          
		menuFichier.add_command(label="Ouvrir", command=self.fopen)         
		menuFichier.add_command(label="Enregistrer", command=self.save)         
		menuFichier.add_command(label="Enregistrer sous", command=self.saveAs)         
		menuFichier.add_command(label="Quitter", command = self.quitter)           
		                  
		#3 - Création du Menu Edition         
		menuEdition= Menu(menuBar, tearoff=False, bg='#000000', fg="white", activebackground="#0846A5", activeforeground="white")         
		menuBar.add_cascade(label = "Edition ", menu=menuEdition)         
		menuEdition.add_command(label="Annuler")          
		menuEdition.add_command(label="Rétablir")                 
		menuEdition.add_command(label="Copier", command=self.copy)         
		menuEdition.add_command(label="Couper", command = self.cut)         
		menuEdition.add_command(label="Coller", command=self.past)                 
		#4 - Création du Menu Outils         
		menuOutils = Menu(menuBar, tearoff=False, bg='#000000', fg="white", activebackground="#0846A5", activeforeground="white")         
		menuBar.add_cascade(label = "Outils", menu = menuOutils)         
		menuOutils.add_command(label="Préférences")                  
		# Création du Menu Aide         
		menuAide = Menu(menuBar, tearoff=False, bg='#000000', fg="white", activebackground="#0846A5", activeforeground="white")         
		menuBar.add_cascade(label = "Aide", menu = menuAide)          
		menuAide.add_command(label="A propos")
		self.root.config(menu=menuBar)