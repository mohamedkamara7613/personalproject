#coding:utf-8
from tkinter import *

main = Tk()
main.geometry("350x270+300+200")
nb1 = ""

def ajout(nb):
    global nb1
    nb1 += nb
    label["text"] = nb1

def num1():
    ajout("1")

def num2():
    ajout("2")

def num3():
    ajout("3")

def num4():
    ajout("4")

def num5():
    ajout("5")

def num6():
    ajout("6")

def num7():
    ajout("7")

def num8():
    ajout("8")

def num9():
    ajout("9")

def zero():
    ajout("0")

def point():
    ajout(".")

def clear():
    global nb1
    nb1 = "0"
    label["text"] = nb1

def add():
    global nb1, op, nb2
    nb2 = float(nb1)
    nb1 = ""
    op = 1
    label["text"] = "+"

def sous():
    global nb1, op, nb2
    nb2 = float(nb1)
    nb1 = ""
    op = 2
    label["text"] = "-"

def fois():
    global nb1, op, nb2
    nb2 = float(nb1)
    nb1 = ""
    op = 3
    label["text"] = "x"

def div():
    global nb1, op, nb2
    nb2 = float(nb1)
    nb1 = ""
    op = 4
    label["text"] = "/"

def egal():
    global nb1
    nb1 = float(nb1)
    
    if(op == 1):
        result = round(nb2 + nb1,10)
    elif(op == 2):
        result = round(nb2 - nb1,10)
    elif(op == 3):
        result = round(nb2 * nb1,10)
    elif(op == 4):
        try:
            result = round(nb2 / nb1,10)
        except ZeroDivisionError:
            result = "Error Math"

    label["text"] = result
    nb1 = str(result)
    result = 0

label = Label(main, text="0")
label.place(x=10, y=10)
button = Button(main, text=" 1 ", command=num1).place(x=10, y=110)
button = Button(main, text=" 2 ", command=num2).place(x=70, y=110)
button = Button(main, text=" 3 ", command=num3).place(x=130, y=110)
button = Button(main, text=" 4 ", command=num4).place(x=10, y=150)
button = Button(main, text=" 5 ", command=num5).place(x=70, y=150)
button = Button(main, text=" 6 ", command=num6).place(x=130, y=150)
button = Button(main, text=" 7 ", command=num7).place(x=10, y=190)
button = Button(main, text=" 8 ", command=num8).place(x=70, y=190)
button = Button(main, text=" 9 ", command=num9).place(x=130, y=190)
button = Button(main, text=" 0 ", command=zero).place(x=70, y=230)
button = Button(main, text=" . ", command=point).place(x=10, y=230)

button = Button(main, text=" C ", command=clear).place(x=190, y=110)
button = Button(main, text=" + ", command=add).place(x=190, y=150)
button = Button(main, text=" -  ", command=sous).place(x=250, y=150)
button = Button(main, text=" x ", command=fois).place(x=250, y=110)
button = Button(main, text=" / ", command=div).place(x=190, y=190)
button = Button(main, text=" = ", command=egal).place(x=250, y=190)


main.mainloop()