#coding:utf-8
nombre_mot = 0
with open("dictionnaire1.txt", "r") as file:
  texte = file.read()
  texte = texte.split("\n")
  
  for mot in texte:
    print(mot)
    nombre_mot += 1
  
print(nombre_mot)