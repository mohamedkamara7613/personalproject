#-*- coding: utf-8 -*-

from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox
from cProfile import label
from subprocess import call
import tkinter
import mysql.connector
#cd AppData\Local\Programs\Python\Python39
#python -m pip install mysql-connector-python
# -------------------------- Fonction --------------------------------------
def ajouter():
    matricule = entrymatricule.get()
    nom = entrynom.get()
    prenom = entryprenom.get()
    sexe = valeur_sexe.get()
    classe = combo_classe.get()
    matiere = entrymatiere.get()
    note = entrynote.get()

    ma_base = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_note_eleve")
    ma_connect = ma_base.cursor()

    try:
        code_sql = ("INSERT INTO users (code, nom, prenom, sexe, classe, matiere, note) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        valeur = (matricule, nom, prenom, sexe, classe, matiere, note)
        ma_connect.execute(code_sql, valeur)
        ma_base.commit()
        derniere_matricule = ma_connect.lastrowid

        messagebox.showinfo('Information', "Les notes ont été ajoutées avec succés !")
        root.destroy()
        call(["python3", "interface_user.py"])

    except Exception as e:
        messagebox.showerror("Erreur", e)
        ma_base.rollback()
        ma_base.close()


def modifier():
    matricule = entrymatricule.get()
    nom = entrynom.get()
    prenom = entryprenom.get()
    sexe = valeur_sexe.get()
    classe = combo_classe.get()
    matiere = entrymatiere.get()
    note = entrynote.get()

    ma_base = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_note_eleve")
    ma_connect = ma_base.cursor()

    try:
        code_sql = ("update users set nom=%s, prenom=%s, sexe=%s, classe=%s, matiere=%s, note=%s where code=%s ")
        valeur = (nom, prenom, sexe, classe, matiere, note, matricule)
        ma_connect.execute(code_sql, valeur)
        ma_base.commit()
        derniere_matricule = ma_connect.lastrowid

        messagebox.showinfo('Information', "Les notes ont été modifiées avec succés !")
        root.destroy()
        call(["python", "interface_user.py"])

    except Exception as e:
        messagebox.showerror("Erreur", e)
        ma_base.rollback()
        ma_base.close()


def supprimer():
    matricule = entrymatricule.get()
    nom = entrynom.get()
    prenom = entryprenom.get()

    ma_base = mysql.connector.connect(host="localhost", user="root", password="", database="gestion_note_eleve")
    ma_connect = ma_base.cursor()

    try:
        code_sql = ("delete from users where code=%s")
        valeur = (matricule,)
        ma_connect.execute(code_sql, valeur)
        ma_base.commit()
        derniere_matricule = ma_connect.lastrowid

        messagebox.showinfo('Information', "Les notes de l'éleve {} {} ont été supprimées avec succés !".format(prenom, nom))
        root.destroy()
        call(["python", "interface_user.py"])

    except Exception as e:
        messagebox.showerror("Erreur", e)
        ma_base.rollback()
        ma_base.close()
# --------------------------Fenetre principale-------------------------------
root = Tk()
root.title("Interface Utilisateur")
root.configure(background="#091821")
root.resizable(False, False)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
geo = "{}x{}".format(screen_width, 800)
root.geometry(geo)

# Grand titre
# flat, groove, raised, ridge, solid, or sunken
lbltitre = Label(root, bd=4, relief=SUNKEN, text="GESTION   DES   NOTES   DES   ÉLÈVES", font=('Arial', 30), bg="#2F4F4F", fg="#FFFAFA")
lbltitre.place(x=0, y=0, width=screen_width, height=100)

# Details des eleves

# Matricule
lblmatricule = Label(root, text="MATRICULE : ", font=('Arial', 18), bg="#091821", fg="white")
lblmatricule.place(x=45, y=150, width=200)
entrymatricule = Entry(root, bd=4, font=("Arial, 10"))
entrymatricule.place(x=225, y=150, width=200, height=30)

# Nom
lblnom = Label(root, text="NOM : ", font=('Arial', 18), bg="#091821", fg="white")
lblnom.place(x=45, y=210, width=200)
entrynom = Entry(root, bd=4, font=("Arial, 10"))
entrynom.place(x=225, y=210, width=300, height=30)

# Prenom
lblprenom = Label(root, text="PRÉNOM : ", font=('Arial', 18), bg="#091821", fg="white")
lblprenom.place(x=45, y=270, width=200)
entryprenom = Entry(root, bd=4, font=("Arial, 10"))
entryprenom.place(x=225, y=270, width=300, height=30)

# Sexe
valeur_sexe = StringVar()
btn_sexe_masculin = Radiobutton(root, text="MASCULIN", value="M", variable=valeur_sexe, indicatoron=0, font=("Arial", 14), bg="#091821", fg="#696969")
btn_sexe_masculin.place(x=225, y=320, width=130, height=30)

btn_sexe_feminin = Radiobutton(root, text="FÉMININ", value="F", variable=valeur_sexe, indicatoron=0, font=("Arial", 14), bg="#091821", fg="#696969")
btn_sexe_feminin.place(x=395, y=320, width=130, height=30)

# Classe
lblclasse = Label(root, text="CLASSE : ", font=('Arial', 18), bg="#091821", fg="white")
lblclasse.place(x=45, y=370, width=200)
combo_classe = ttk.Combobox(root, font=("Arial", 14))
combo_classe['values'] = ['CP', 'CE1', 'CE2', 'CM2', '6e', '5e', '4e', '3e', '2nd', '1ere', 'Terminal']
combo_classe.current(0)
combo_classe.place(x=225, y=370, width=130)

# Matiere
lblmatiere = Label(root, text="MATIERE : ", font=('Arial', 18), bg="#091821", fg="white")
lblmatiere.place(x=45, y=420, width=200)
entrymatiere = Entry(root, bd=4, font=("Arial, 10"))
entrymatiere.place(x=225, y=420, width=300, height=30)

# Note
lblnote = Label(root, text="NOTE : ", font=('Arial', 18), bg="#091821", fg="white")
lblnote.place(x=45, y=475, width=200)
entrynote = Entry(root, bd=4, font=("Arial, 10"))
entrynote.place(x=225, y=475, width=200, height=30)

# Mise en place des bouttons
# Enregistrer
btnenregistrer = Button(root, text="Enregistrer", font=("Arial", 16), bg="#D2691E", fg="white", command=ajouter)
btnenregistrer.place(x=180, y=530, width=150)

# Modifier
btnmodifier = Button(root, text="Modifier", font=("Arial", 16), bg="#D2691E", fg="white", command=modifier)
btnmodifier.place(x=350, y=530, width=150)

# Supprimer
btnsupprimer = Button(root, text="Supprimer", font=("Arial", 16), bg="#D2691E", fg="white", command=supprimer)
btnsupprimer.place(x=260, y=590, width=150)

# Table
table = ttk.Treeview(root, columns=(1,2,3,4,5,6,7), show="headings", height=5)
table.place(x = 560,y = 150, width = 790, height = 450)
# entetes
table.heading(1, text="MAT")
table.heading(2, text="NOM")
table.heading(3, text="PRENOM")
table.heading(4, text="SEXE")
table.heading(5, text="CLASSE")
table.heading(6, text="MATIERE")
table.heading(7, text="NOTE")

# definir les dimentions des colonnes
table.column(1, width=100)
table.column(2, width = 150)
table.column(3, width = 150)
table.column(4, width = 100)
table.column(5, width = 50)
table.column(6, width = 100)
table.column(7, width = 50)

#afficher les informations de la table
ma_base = mysql.connector.connect(host="localhost", user='root', password="", database="gestion_note_eleve")
ma_connexion = ma_base.cursor()
ma_connexion.execute("select * from users")
for row in ma_connexion:
    table.insert('', END, values=row)
ma_base.close()

root.mainloop()
