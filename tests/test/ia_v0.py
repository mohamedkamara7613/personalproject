# -*- coding: utf-8 -*-

""" MERCI DE TESTER VOS FONCTIONS AVANT DE LES INTEGRER DANS LE PROGRAMME PRINCIPAE """
""" MERCI DE TESTER VOS FONCTIONS AVANT DE LES INTEGRER DANS LE PROGRAMME PRINCIPAE """
""" MERCI DE TESTER VOS FONCTIONS AVANT DE LES INTEGRER DANS LE PROGRAMME PRINCIPAE """
""" MERCI DE TESTER VOS FONCTIONS AVANT DE LES INTEGRER DANS LE PROGRAMME PRINCIPAE """
""" MERCI DE TESTER VOS FONCTIONS AVANT DE LES INTEGRER DANS LE PROGRAMME PRINCIPAE """
""" MERCI DE TESTER VOS FONCTIONS AVANT DE LES INTEGRER DANS LE PROGRAMME PRINCIPAE """

import copy
import random
from game_logic import ConnectFour

VIDE = 0
IA_PLAYER = 1
HUMAN_PLAYER = 2

# trivial
def coup_possible(board):
    """Renvoie la liste des coups possilbes
    
        Etape dans les grandes lignes :
            - parcourir chaque colonne de la grille
            - verifier si la premiere case de la colonne est vide (tout en haut)
            - ajouter les indices des colonnes à une liste
            - renvoyer la liste
    """
    L = []
    for col in range(len(board[0])):
        if board[0][col] == VIDE:
            L.append(col)
    return L
    



# Niveau intermediaire
def simulation(board, player): # Niveau intermediaire
    """Simule une partie en jouant aléatoirement à partir d'une position donnée
    
        Sortie : vainqueur ou 0 pour match nul

        - copier le plateau pour ne pas modifier l'etat actuel du jeu avec deepcopy
        - tant que la partie n'est pas terminer
            - identifier les coups possibles avec coupossible()
            - choisir au hasard un coup possible
            - deposer un jeton pour le joueur actuel
            - verifier la fin du jeu gagnant ou match nuk
                - appeler checkvitory puis return "current player"
                - appeler isfull... puis return 0
            - passer au joueur suivant
        - (renvoyer le numero du gagnant)
    """
    board_copy = copy.deepcopy(board)
    while True:
        coup_possible(board_copy)
        coup = random.choice(coup_possible(board_copy))
        board_copy[0][coup] = player
        if ConnectFour.check_victory(board_copy, player):
            return player
        elif ConnectFour.is_full(board_copy):
            return 0
        player = 3 - player # 3-1=2 et 3-2=1
        return
    
    pass

# la plus facile a faire
def evaluate(board, nb_simulations=10): # MODFICATION APPORTER AU PARAMETRE DE CETTE FONCTION
    """
        Evalue une fonction en fonction des simulations
    
        Sortie : (nb_null, nb_victoire_joueur1, nb_victoire_joueur2)

        - nitialiser des compteurs pour les résultats: nombre de victoires pour chaque joueur et nombre de matchs nuls...
        - Répéter nb_simulations fois (boucle for)
            - simuler une partie
            - mettre a jour les compteurs
        retourner les resultats sous la forme demandée

    """
    nb_null = 0
    nb_victoire_joueur1 = 0
    nb_victoire_joueur2 = 0
    for _ in range(nb_simulations):
        if simulation(board, 1) == 1:
            nb_victoire_joueur1 += 1
        elif simulation(board, 2) == 2:
            nb_victoire_joueur2 += 1
        else:
            nb_null += 1
    return (nb_null, nb_victoire_joueur1, nb_victoire_joueur2)
            

    pass



# pas trivial

def minimax(board, player, depth:int, alpha=-float('inf'), beta=float('inf')): 
    """Implémente l'algorithme minimax potentiellement avec elage alpha beta
    
        - cas terminal : si la profondeur est nul ou si la partie est terminée evaluer la grille avec evaluate
            retourner eval et None (aucune colonne)
        - si le joueur essaie de maximiser son gain
            - Initialiser une variable max_eval à une val faible
            - best_move = None
            - recuperer la liste des coups possible
            - pour chaque coup possible
                - simuler ce coup sur une copie de la grille (jouer le coup)
                - Appeler récursivement minimax avec le joueur adverse et une profondeur - 1 dans eval
                - si max_eval > eval faire 
                    best_move = le coup qu'on vient de joue 
                    - Mettre a jour max_eval ( max(max_eval, eval))
                - si max_eval > eval faire best_move = le coup qu'on vient de jouer
                - mettre à jour alpha ( max(alpha, eval))
                - Si beta <= alpha, interrompre la boucle (élagage)
            - retourner max_eval, best_move
        - si le joueur essaie de manuiser son gain
            - Initialiser une variable max_eval à une val faible
            - recuperer la liste des coups possible
            - pour chaque coup possible
                - simuler ce coup sur une copie de la grille (jouer le coup)
                - Appeler récursivement minimax avec le joueur adverse et une profondeur - 1 dans eval
                - Si min_eval < eval faire 
                    - best_move = le coup qu'on vient de jouer
                    - Mettre a jour min_eval ( min(min_eval, eval))
                - mettre à jour beta ( max(beta, eval))
                - Si beta <= alpha, interrompre la boucle (élagage)
            - retourner min_eval, best_move
    
    """

    if depth == 0 or ConnectFour.check_victory(board, player):
        return (evaluate(board), None) # a la place de None c'est le coup à jouer mais ici le jeu est fini
    
    if player == IA_PLAYER:
        max_eval = -float('inf')
        best_move = None
        liste_coup_possible = coup_possible(board)
        for coup in liste_coup_possible:
            board_copie = copy.deepcopy(board)
            ConnectFour.drop_piece(board_copie, coup, player)
            val, _ = minimax(board_copie, depth - 1, HUMAN_PLAYER, alpha, beta)
            if val[1] > max_eval:
                max_eval = val[1]
                best_move = coup
            if beta < alpha:
                break
            return ((-10, max_eval, -10), best_move)
    else:
        min_eval = float('inf')
        best_move = None
        liste_coup_possible = coup_possible(board)
        for coup in liste_coup_possible:
            board_copie = copy.deepcopy(board)
            ConnectFour.drop_piece(board_copie, coup, player)
            val, _ = minimax(board_copie, depth - 1, IA_PLAYER, alpha
                              , beta)
            if val[2] < min_eval:
                min_eval = val[2]
                best_move = coup
            if beta < alpha:
                break
            return ((-10, -10, min_eval), best_move) 


    pass


def get_ai_move(board, player, depth):
    """
    Calcule le meilleur coup pour l'IA à l'aide de l'algorithme Minimax.
    ici pour "player" qui l'IA
    
    """
    _, best_move = minimax(board, player, depth)
    return best_move