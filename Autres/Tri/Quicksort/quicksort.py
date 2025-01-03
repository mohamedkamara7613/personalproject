# -*- coding: utf-8 -*-
def quicksort(liste):
    # Cas terminale : si on a un seule element dans la liste
    if len(liste) <= 1:
        return liste
    
    # Definition du pivot qui sera le dernier element de la liste
    pivot = liste.pop()

    # Creation des conteants pour la division de la liste en deux
    premier_partie = []
    deuxieme_partie = []

    for i in range(len(liste)):
        # Separation des elements de la liste en fonction du pivot
        if liste[i] < pivot:
            premier_partie.append(liste[i])
        else:
            deuxieme_partie.append(liste[i])

        # Appelle recursive de quicksort sur les deux sous liste et concaténation des resultats
        # Attention à bien mettre le pivot en debut de deuxieme partie
    return quicksort(premier_partie) + [pivot] + quicksort(deuxieme_partie)
    

# Exemple d'utilisation
liste = [5, 2, 8, 1, 9]
print(quicksort(liste))  # [1, 2, 5, 8, 9]