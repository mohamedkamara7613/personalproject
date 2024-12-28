#coding:utf-8
from turtle import *
from os import system


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
done()

# abs(pos()) est egale a racine de x²+y²