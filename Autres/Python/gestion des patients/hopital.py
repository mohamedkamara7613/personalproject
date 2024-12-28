# coding:utf-8
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
# ---------------------------------------------------------------------FONCTION--------------------------------------------------------------------------------------
def ajouter():
    matricule = entrymatricule.get()
    nom = entrynom.get()
    prenom = entryprenom.get()
    age = entryage.get()
    sexe = entrysexe.get()
    adresse = entryadresse.get()
    telephone = entrytelephone.get()
    remarque = entryremarque.get()

    print("LE BOUTON MARCHE BIEN")

   #Creeons la connexion a la base de donnee
    #con =  sqlite3.connect('hopital.db')
    #curser = con.cursor()
  #  curser.execute("insert into patient('code', 'nom', 'prenom', 'age', 'sexe', 'adresse', 'telephone', 'remarque') values(?,?,?,?,?,?,?,?)", (matricule, nom, prenom, age, sexe, adresse, telephone, remarque))
   # con.commit()
 #   con.close()
   # messagebox.showinfo("Le patient a été ajouté avec succés !!")

    #  afficher
    #con = sqlite3.connect("hopital.db")
    #curser = con.cursor()
    #select = curser.execute("select * from patient order by code desc")
    #select = list(select)
    #table.insert(",END, values=select[0])
    #con.close()

    pass

def modifier():
    print("LE BOUTON MARCHE BIEN")
    matricule = entrymatricule.get()
    nom = entrynom.get()
    prenom = entryprenom.get()
    age = entryage.get()
    sexe = entrysexe.get()
    adresse = entryadresse.get()
    telephone = entrytelephone.get()
    remarque = entryremarque.get()

    # Creeons la connexion a la base de donnee
    # con =  sqlite3.connect('hopital.db')
    # curser = con.cursor()
   # curser.execute("update patient set nom=?m prenom=?, age=?, sexe=?, adresse=?, telephone=?, remarque=? where code=?", (nom, prenom, age, sexe, adresse, telephone, remarque, matricule))
    #con.commit()
    #con.close()
    # messagebox.showinfo("Le patient a été ajouté avec succés !!")

    #  afficher
    #con = sqlite3.connect("hopital.db")
    #curser = con.cursor()
    #select = curser.execute("select * from patient order by code desc")
    #select = list(select)
    #table.insert(",END, values=select[0])
    #con.close()
    pass

def supprimer():
   #codeSelectionner = table.item(table.selection())['valuess'][0]
   # con = sqlite3.connect("hopital.db")
   # curser = con.cursor()
   #delete = curser.execute("delete from patient where code={}".format(codeSelectionner))
   #con.commit()
   #table.delete(table.selection())



    pass



# --------------------------------------------------------------------MAIN------------------------------------------------------------------------------------------
# Creation de la fenetre
root = Tk()
root.title("Gestion des patients d'un hopital")

screen_width = int(root.winfo_screenwidth())
screen_height = int(root.winfo_screenheight())
fen_width = 1400
fen_height = 700
pos_X = (screen_width // 2) - (fen_width // 2)
pos_Y = (screen_height // 2) - (fen_height // 2)
geo = "{}x{}+{}+{}".format(fen_width, fen_height, pos_X, pos_Y)
root.geometry(geo)

#root.resizable(width=False, height=False )

# ceation du grand titre
lblgrandtitre = Label(root, bd=20, relief=RIDGE, text="GESTION DES PATIENTS DE L'HOPITAL DALAL JAMM", font=("Arial, 30"), bg="darkblue", fg="white")
lblgrandtitre.place(x=0, y=0, width=1400)

# label du titre liste des patients
lbllistpatient = Label(root, text="LISTE DES PATIENTS", font=("Arial", 16), bg="darkblue", fg="white")
lbllistpatient.place(x=600, y=100, width=800)

# text_matricule
lblmatricule = Label(root, text="Matricule Patient", font=("Arial", 16), bg="black", fg="white")
lblmatricule.place(x=0, y=100, width=200)
entrymatricule = Entry(root)
entrymatricule.place(x=200, y=100, width=160, height=30)

# text_nom
lblnom = Label(root, text="Nom ", font=("Arial", 16), bg="black", fg="white")
lblnom.place(x=0, y=150, width=200)
entrynom = Entry(root)
entrynom.place(x=200, y=150, width=220, height=30)

# text_prenom
lblprenom = Label(root, text="Prénom ", font=("Arial", 16), bg="black", fg="white")
lblprenom.place(x=0, y=200, width=200)
entryprenom = Entry(root)
entryprenom.place(x=200, y=200, width=220, height=30)

# text_age
lblage = Label(root, text="Âge ", font=("Arial", 16), bg="black", fg="white")
lblage.place(x=0, y=250, width=200)
entryage = Entry(root)
entryage.place(x=200, y=250, width=160, height=30)

# text_sexe
lblsexe = Label(root, text="Sexe ", font=("Arial", 16), bg="black", fg="white")
lblsexe.place(x=0, y=300, width=200)
entrysexe = Entry(root)
entrysexe.place(x=200, y=300, width=160, height=30)

# text_adresse
lbladresse = Label(root, text="Adresse ", font=("Arial", 16), bg="black", fg="white")
lbladresse.place(x=0, y=350, width=200)
entryadresse = Entry(root)
entryadresse.place(x=200, y=350, width=300, height=30)

# text_telephone
lbltelephone = Label(root, text="Téléphone ", font=("Arial", 16), bg="black", fg="white")
lbltelephone.place(x=0, y=400, width=200)
entrytelephone = Entry(root)
entrytelephone.place(x=200, y=400, width=160, height=30)

# text_remarque
lblremarque = Label(root, text="Remarque ", font=("Arial", 16), bg="black", fg="white")
lblremarque.place(x=0, y=450, width=200)
entryremarque = Entry(root)
entryremarque.place(x=200, y=450, width=300, height=30)

# creation des boutons d'interaction
btnregister = Button(root, text="Enregistrer", command=ajouter, font=("Arial", 16), bg="darkblue", fg="yellow", activebackground="darkgreen", activeforeground="white", relief=RIDGE, bd=10)
btnregister.place(x=20, y=500, width=150)

btnmodifier = Button(root, text="Modifier", command=modifier, font=("Arial", 16), bg="darkblue", fg="yellow", activebackground="darkgrey", relief=RIDGE, bd=10)
btnmodifier.place(x=200, y=500, width=150)

btnsupprimer = Button(root, text="Supprimer", command=supprimer, font=("Arial", 16), bg="darkblue", fg="yellow", activebackground="red", relief=RIDGE, bd=10)
btnsupprimer.place(x=100, y=570, width=150)
btnsupprimer.place(x=100, y=570, width=150)

# TABLE
table = ttk.Treeview(root, columns=(1,2,3,4,5,6,7,8), height=5,  show="headings")
table.place(x=600, y=150, width=800, height=450)

# ENTETES
table.heading(1, text='CODE')
table.heading(2, text='NOM')
table.heading(3, text='PRENOM')
table.heading(4, text='AGE')
table.heading(5, text='SEXE')
table.heading(6, text='ADRESSE')
table.heading(7, text='TELEPHONE')
table.heading(8, text='REMARQUE')

# DEFINIR LA DIMENSION DES COILONNES
table.column(1, width=30)
table.column(2, width=90)
table.column(3, width=90)
table.column(4, width=20)
table.column(5, width=20)
table.column(6, width=100)
table.column(7, width=60)
table.column(8, width=100)

# afficher les informations de la table
#con = sqlite3.connect('hopital.db')
#curser = con.cursor()
#select = curser.execute("select * from patient")
#for row in select:
 #   table.insert(",END,value=row)
#con.close()



root.mainloop()