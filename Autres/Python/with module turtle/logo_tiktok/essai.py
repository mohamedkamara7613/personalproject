#!/usr/bin/env python3
#coding:utf-8

from os import system
from turtle import *
import os

width(1)
bgcolor('black') # couleur de fond
hideturtle()
goto(0,0) # change la position de la tortue
begin_fill() # Commencement du dessin
color('red', 'yellow') # couleur de la ligne et couleur de remplissage

while True:
    forward(200) #avance de 200 pixels
    left(170) # pivote de 170 degre

    if abs(pos()) < 1:
        break
end_fill()
#done()

os.system('sleep 2')
clear()

bgcolor('black') 
width(20)
colors = ['#db0f3c', '#50ebe7', 'white']
pos = [(0, 0), (-5, 13), (-5, 5)]

for (x,y), col in zip(pos, colors):
	up()
	goto(x,y) # place la tortue au point x y
	down()
	color(col)
	left(180) # pivote de 180 degre
	circle(50, 270)
	forward(120) # avance de 120 pixel en dissinant
	left(180)
	circle(50, 90) # decrit un arc de rayon 50 et d'angle 90 degre




