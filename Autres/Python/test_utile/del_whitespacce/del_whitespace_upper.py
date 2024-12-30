#conding:utf-8 

"""	
	Met tous les mots du dictionnaire en magiscule et supprime les espaces
"""
import time
nombre_mot = 0

try:
  #LECTURE
  with open("dictionnaire.txt", "r") as file:
  
    print("Lecture du dictionnaire...")
  # Lecture du fichier
    mots = file.read()
  
    time.sleep(1)
    print("Traitement des mots, effacement des espaces au niveau des mots et mise en magiscule...")
  #Mise en magiscule 
    mots = mots.upper()
  # effacement des espaces avant et aprés
    mots = mots.strip()
  # Séparations des mots dans une liste
    mots = mots.split("\n")
  # Effacement des espaces dans les mots
    new_mots = []
    for mot in mots:
      nombre_mot += 1
      mot = mot.strip()
      mot = mot.split(" ")
      mot = "".join(mot)
      new_mots.append(mot)
      print("{} traité...".format(mot))



  #ECRITURE
  with open("dictionnaire_whitespace_deleted.txt","w") as file:
    for mot in new_mots:
      file.write(mot+"\n")

  time.sleep(3)	  
  print("Fin...")
  time.sleep(1)
  print("\t{} mots ont été traités".format(nombre_mot))
  print("Fichier : 'dictionnaire_whitespace_deleted.txt' généré avec succes !")

except KeyboardInterrupt:
  with open("dictionnaire_whitespace_deleted.txt","w") as file:
    for mot in new_mots:
      file.write(mot+"\n")

  time.sleep(3)	  
  print("Fin...")
  time.sleep(1)
  print("\t{} mots ont été traités".format(nombre_mot))
  print("Fichier : 'dictionnaire_whitespace_deleted.txt' généré avec succes !")
