# Importation des bibliotheques
from subprocess import call
from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox

# ------------------------FONCTION ---------------------------------------------------------
def se_connecter():
    surnom = entrynom_user.get()
    mdp = entrymdp.get()

    if(surnom == "" and mdp == ""):
        messagebox.showerror("Erreur de connexion","Veuillez remplir les champs !")
        entrynom_user.delete("0", "end")
        entrymdp.delete("0", "end")
    elif(surnom == "admin" and mdp == "admin"):
        messagebox.showinfo("", "Bienvenue")
        entrynom_user.delete("0", "end")
        entrymdp.delete("0", "end")
        root.destroy()
        call(["python", "interface_user.py"])
    else:
        messagebox.showerror("Erreur de connexion", "Information non valide !")
        entrynom_user.delete("0", "end")
        entrymdp.delete("0", "end")

# -------------------------Ma fenetre--------------------------------------------------------
root = Tk()
root.title("Fenêtre de connexion")
root.configure(background="#091821")
root.resizable(False, False)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
fen_width = 430
fen_height = 300
pos_x = (screen_width // 2) - (fen_height // 2)
pos_y = (screen_height // 2) - (fen_height // 2)
geo = '{}x{}+{}+{}'.format(fen_width, fen_height, pos_x, pos_y)
root.geometry(geo)

# Ajouter le titre
lbltitre = Label(root, text="Formulaire de connexion",  relief=SUNKEN, borderwidth=2, font=("Sans Serif", 25), bg="#091821", fg="white", padx=50)
lbltitre.place(x=0, y=0, width=430)

lblnom_user = Label(root, text="Nom Utilisateur : ", font=('Arial', 14), bg="#091821", fg="white")
lblnom_user.place(x=5, y=100, width=150)
entrynom_user = Entry(root, bd=4, font=("Arial, 10"))
entrynom_user.place(x=160, y=100, width=200, height=25)

lblmdp = Label(root, text="Mot De Passe : ", font=('Arial', 14), bg="#091821", fg="white")
lblmdp.place(x=5, y=150, width=150)
entrymdp = Entry(root, show='*', bd=4, font=("Arial, 14"))
entrymdp.place(x=160, y=150, width=200, height=25)

# Bouton Connecter
btnconnexion = Button(root, text="Connexion", font=('Arial, 16'), bg="#FF4500", fg="white", command=se_connecter)
btnconnexion.place(x=120, y=225,  width=200)



root.mainloop()