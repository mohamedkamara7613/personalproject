#coding:utf-8

"""
	Name File : main.py

	By Mohamed Kamara

	Object : resume all functions and variables of calculator
"""

from tkinter import *
from tkinter.font import Font as f
import math


def evaluer(event):
	try:
		chaine.configure(text=str(entree.get())+" = "+str(eval(entree.get())))
	except ZeroDivisionError:
		chaine["text"] = "Math Error"
	except:
		chaine["text"] = "Syntax Error"

# Programme principale
fen = Tk()
fen.title("Calculatrice")

entree = Entry(fen, width=20)
entree.bind("<Return>", evaluer)
entree.config(font = f(size=30))

chaine = Label(fen, fg = 'black')
chaine.config(font = f(size=30))

entree.pack()
chaine.pack()
fen.mainloop()