# coding:utf-8

"""
    starting at Wen 27 Aug 2021
    Par Mohamed Kamara
--------------------- Mario Sokoban v2.0 --------------------------
-------------- data.py


    Rôle du fichier : Definit les  constantes et les variables universelles du programme
"""

bloc_size = 34
nb_bloc_width = 12
nb_bloc_height = 12

# Les dimensions de la fenetre
window_width = bloc_size * nb_bloc_width
window_height = bloc_size * nb_bloc_height
dimension_window = (window_width, window_height)

directions = {"HAUT": 0, "BAS": 1, "GAUCHE": 2, "DROITE": 3}

# Les objets du jeu
items = {"VIDE": 0, "MUR": 1, "CAISSE": 2, "OBJECTIF": 3, "JOUEUR": 4, "CAISSE_OK": 5}

# La carte qui est un tableau a deux dimensions
cols = nb_bloc_width
line = nb_bloc_height
grille = [[0] * cols for i in range(line)]
position_joueur = [0, 0]
# Il y a deux niveau par defaut
niveaux = {
    0: "000000000000000000000000000111111100000111111100000111111100000420003100000111111100000111111100000111111100000000000000000000000000000000000000",
    1: "000000000000000000000000000111111100000111111100000110001100000420003100000111111100000111111100000001111100000000000000000000000000000000000000"}

# variables de couleur
color_blue = (0, 75, 255)
black_color = (0, 0, 0)

font = color_blue # 0xFCEC6B
