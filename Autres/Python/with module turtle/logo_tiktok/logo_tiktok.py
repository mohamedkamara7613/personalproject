#!/usr/bin/env/python3
#coding:utf-8

from turtle import *

width(20)
bgcolor('black') 
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


"""
	turtle est un module qui permet de faire des dessins grace a une tortue 
	représenté par un curseur a point
"""