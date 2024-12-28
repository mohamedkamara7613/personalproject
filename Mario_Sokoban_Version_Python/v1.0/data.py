#coding:utf-8

# -------------- Mario Sokoban v1.0 -----------------------------------


#import pygame
"""
#Monday july 12 2021 00:31 debut de developpement
	data.py
---------------
	Par Mohamed kamara

	Role : définit les variables et les constantes pour le programme
"""
#Constantes
bloc_size = 34
nb_bloc_height = 12
nb_bloc_width = 12
window_height = nb_bloc_height * bloc_size
window_width = nb_bloc_width * bloc_size

direction = {"HAUT": 0, "BAS": 1, "GAUCHE": 2, "DROITE": 3}
items = {"VIDE":0, "MUR":1, "CAISSE":2, "OBJECTIF":3, "MARIO":4, "CAISSE_OK":5}

#Couleur
white_color = (255, 255, 255)
black_color = (0, 0, 0)

#Autre variable
pos_text_center = [window_width / 2 - 30, window_height / 2 - 30]
window_resolution = (window_width, window_height)
positionJoueur = [14, 0]


#creation de la carte en ligne et en colone
grille = [[0] * nb_bloc_width for i  in range(nb_bloc_height)]
