#coding:utf-8
#import pygame


bloc_size = 34
nb_bloc_height = 12
nb_bloc_width = 12
window_height = nb_bloc_height * bloc_size
window_width = nb_bloc_width * bloc_size


direction = {"HAUT": 0, "BAS": 1, "GAUCHE": 2, "DROITE": 3}
items = {"VIDE":0, "MUR":1, "CAISSE":2, "OBJECTIF":3, "MARIO":4, "CAISSE_OK":5}

#Couleur
white_color = (255, 255, 255)

#mario = {"haut":0, "bas":0, "gauche":0, "droite":0}

#carte


grille = {}
y = 0
j = 0
while y < window_height:
	x = 0
	i = 0
	while x < window_width:
		texte = "{}, {}".format(i, j)
		grille[texte] = (x, y)
		i += 1
		x += bloc_size
	j += 1
	y += bloc_size	

print(grille)