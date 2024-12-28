#!/usr/bin/env python3
#coding:utf-8



# Malheureusement ce code ne marche pa encore 

"""
	Name File : calculatrice.py

	By Mohamed Kamara

	Object : It is the main of program where are difined all variables and functions
"""


# Importation --------------------------------------------------------------
from tkinter import *

# Variables ----------------------------------------------------------------
main = Tk()
number1 = ""
operateur = 0

# Fonctions ----------------------------------------------------------------
def ajout(nb):
    global number1
    number1 += nb
    label["text"] = number1

def Numero_1():
    ajout("1")

def Numero_2():
    ajout("2")

def Numero_3():
    ajout("3")

def Numero_4():
    ajout("4")

def Numero_5():
    ajout("5")

def Numero_6():
    ajout("6")

def Numero_7():
    ajout("7")

def Numero_8():
    ajout("8")

def Numero_9():
    ajout("9")

def Zero():
    ajout("0")

def Point():
    ajout(".")

def Clear():
    global number1
    number1 = "0"
    label["text"] = number1

def Addition():
    global number1, operateur, number2
    number2 = float(number1)
    number1 = ""
    operateur = 1
    label["text"] = "+"

def Soustraction():
    global number1, operateur, number2
    number2 = float(number1)
    number1 = ""
    operateur = 2
    label["text"] = "-"

def Multiplication():
    global number1, operateur, number2
    number2 = float(number1)
    number1 = ""
    operateur = 3
    label["text"] = "x"

def Division():
    global number1, operateur, number2
    number2 = float(number1)
    number1 = ""
    operateur = 4
    label["text"] = "/"

def Equal():
    global number1
    number1 = float(number1)
    
    if(operateur == 1):
        result = round(number2 + number1,10)
    elif(operateur == 2):
        result = round(number2 - number1,10)
    elif(operateur == 3):
        result = round(number2 * number1,10)
    elif(operateur == 4):
        try:
            result = round(number2 / number1,10)
        except ZeroDivisionError:
            result = "Error Math"

    label["text"] = result
    number1 = str(result)
    result = 0

# Programme principale -----------------------------------------------------
main.geometry("350x270+300+200")

label = Label(main, text="0").place(x=10, y=10)

# chiffre de calcul
button = Button(main, text=" 1 ", command=Numero_1).place(x=10, y=110)
button = Button(main, text=" 2 ", command=Numero_2).place(x=70, y=110)
button = Button(main, text=" 3 ", command=Numero_3).place(x=130, y=110)
button = Button(main, text=" 4 ", command=Numero_4).place(x=10, y=150)
button = Button(main, text=" 5 ", command=Numero_5).place(x=70, y=150)
button = Button(main, text=" 6 ", command=Numero_6).place(x=130, y=150)
button = Button(main, text=" 7 ", command=Numero_7).place(x=10, y=190)
button = Button(main, text=" 8 ", command=Numero_8).place(x=70, y=190)
button = Button(main, text=" 9 ", command=Numero_9).place(x=130, y=190)
button = Button(main, text=" 0 ", command=Zero).place(x=70, y=230)
button = Button(main, text=" . ", command=Point).place(x=10, y=230)

# operateur de calcul 
button = Button(main, text=" C ", command=Clear).place(x=190, y=110)
button = Button(main, text=" + ", command=Addition).place(x=190, y=150)
button = Button(main, text=" -  ", command=Soustraction).place(x=250, y=150)
button = Button(main, text=" x ", command=Multiplication).place(x=250, y=110)
button = Button(main, text=" ÷ ", command=Division).place(x=190, y=190)
button = Button(main, text=" = ", command=Equal).place(x=250, y=190)




# Boucle principale
main.mainloop()