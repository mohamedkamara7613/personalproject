# -*- coding: utf-8 -*-
# Script qui enlève les lignes contenant des mots avec des lettres spécifiées

file_path = "liste.txt"

# Liste des lettres à vérifier
letters_to_exclude = ['é', 'è', 'ê', 'ë', 'à', 'â', 'ä', 'î', 'ï', 'ô', 'ö', 'ù', 'û', 'ü', 'ç', 'œ', 'æ', '-']
 

with open(file_path, "r") as f:  # Ouvrir en mode lecture pour récupérer les lignes
    lines = f.readlines()

new_lines = []

for line in lines:
    # Séparer les mots de chaque ligne
    words = line.split()
    
    # Filtrer les mots qui contiennent l'une des lettres à exclure
    filtered_words = [word for word in words if not any(letter in word for letter in letters_to_exclude)]
    
    # Si après filtrage, il reste des mots, ajouter la ligne à la liste
    if filtered_words:
        new_lines.append(" ".join(filtered_words))

with open(file_path, "w") as f:  # Ouvrir en mode écriture pour réécrire le fichier
    f.write("\n".join(new_lines))  # Écrire les nouvelles lignes dans le fichier
