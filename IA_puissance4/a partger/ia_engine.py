# -*- coding: utf-8 -*-


import copy
import random
from game_logic import ConnectFour

VIDE = 0
IA_PLAYER = 1
HUMAN_PLAYER = 2

# trivial
def coup_possible(board):
    """But : Trouver les colonnes où un coup est encore possible.

    Algorithme :
    Créer une liste vide L.
    Pour chaque colonne "col" dans la grille :
    Si la première case de la colonne est vide :
    Ajouter l'indice de la colonne à L.
    Retourner la liste L
"""
    """Renvoie la liste des coups possilbes"""
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
        coup = random.choice(coup_possible(board_copy))
        ConnectFour.drop_piece(board_copy, coup, player)
        if ConnectFour.check_victory(board_copy, player):
            return player
        elif ConnectFour.is_full(board_copy):
            return 0
        player = 3 - player # 3-1=2 et 3-2=1

# la plus facile a faire
def evaluate(board, nb_simulations): # MODFICATION APPORTER AU PARAMETRE DE CETTE FONCTION
    """
        But : Évaluer la grille actuelle en simulant plusieurs parties aléatoires.

    Algorithme :
    Initialiser trois compteurs :
    nb_null pour les matchs nuls.
    nb_victoire_joueur1 pour les victoires de l'IA.
    nb_victoire_joueur2 pour les victoires de l'humain.
    Répéter nb_simulations fois :
    Simuler une partie avec simulation(board, IA_PLAYER).
    Si l'IA gagne, incrémenter nb_victoire_joueur1.
    Si l'humain gagne, incrémenter nb_victoire_joueur2.
    Sinon, incrémenter nb_null.
    Retourner un tuple (nb_null, nb_victoire_joueur1, nb_victoire_joueur2)

    """

    #évalue une position donnée en fonction de plusieurs stimulations
    nb_null=0
    nb_victoire_joueur1=0
    nb_victoire_joueur2=0
    for i in range (0,nb_simulations):
        if simulation(board, IA_PLAYER)==IA_PLAYER:
            nb_victoire_joueur1+=1
        elif simulation( board, HUMAN_PLAYER)==HUMAN_PLAYER:
            nb_victoire_joueur2+=1
        else:
            nb_null+=1
    return (nb_null, nb_victoire_joueur1, nb_victoire_joueur2)
    
            



# pas trivial

def minimax(board, player, depth, nb_simulation, alpha=-float('inf'), beta=float('inf')): 
    """But : Calculer le meilleur coup à jouer à l'aide de l'algorithme Minimax avec élagage alpha-beta

    Si depth == 0 ou si la partie est terminée (l'un des deux joueur a gagné ou match nul) :
    -> avec ConnectFour.check_victory(grille, player) pour savoir si "player" a gagné
    -> avec ConnectFour.is_full(grille) <- partie nulle
    Calculer l'évaluation de la grille avec evaluate.
    definir score = Différence entre les victoires de l'IA et celles de l'humain
    Retourner (score, None).
    Recuperer la liste des coups possible avec coup_possible(board)
    s'il y en a pas retourner (0, None)
    Si le joueur est l'IA (maximisant) :
    Initialiser max_eval = -inf et best_move = None.
    Pour chaque coup possible :
    Simuler le coup sur une copie de la grille en faisant -> ConnectFour.drop_piece(grille, coup_a_jouer, player)
    Appeler minimax de manière récursive avec HUMAIN comme joueur et avec depth - 1 en respectant l'ordre des parametres.
    Si le score retourné est meilleur que max_eval :
    Mettre à jour max_eval et best_move -> max_eval = eval_score et best_move = coup
    Mettre à jour alpha avec le maximum entre alpha et max_eval.
    Si alpha >= beta, interrompre la boucle (élagage).
    Retourner (max_eval, best_move).
    Si le joueur est l'humain (minimisant) :
    Initialiser min_eval = +inf et best_move = None.
    Pour chaque coup possible :
    Simuler le coup sur une copie de la grille.
    Appeler minimax de manière récursive pour l'IA avec depth - 1.
    Si le score retourné est plus petit que min_eval : 
    Mettre à jour min_eval et best_move. -> min_eval = eval_score et best_move = coup
    Mettre à jour beta avec le minimum entre beta et min_eval.
    Si alpha >= beta, interrompre la boucle (élagage).
    Retourner (min_eval, best_move).
    
    """

    if depth ==0 or ConnectFour.check_victory(board, player) or ConnectFour.is_full(board):
        eval=evaluate(board, nb_simulation)
        score=eval[1]-eval[2]
        return (score,None)
    
    coups_possibles=coup_possible(board)
    if len(coups_possibles) == 0:
        return (0,None)
    
    if player == IA_PLAYER:
        max_eval=-float('inf')
        best_move=None
        for i in coups_possibles:
            grille=copy.deepcopy(board)
            ConnectFour.drop_piece(grille, i, player)
            eval_score=minimax(grille, HUMAN_PLAYER, depth-1, nb_simulation, alpha, beta)
            if eval_score[0]>max_eval:
                max_eval=score
                best_move=i
            alpha=max(alpha,max_eval)
            if alpha>=beta:
                break
        return (max_eval,best_move)
    elif player == HUMAN_PLAYER:
        min_eval=float('inf')
        best_move=None
        for i in coups_possibles:
            grille=copy.deepcopy(board)
            ConnectFour.drop_piece(grille, i, player)
            eval_score=minimax(grille, IA_PLAYER, depth-1, nb_simulation, alpha, beta)
            if eval_score[0]<min_eval:
                min_eval=eval_score
                best_move=i
            beta=min(beta,min_eval)
            if alpha>=beta:
                break
        return (min_eval,best_move)
     
    


def get_ai_move(board, player, depth, nb_simulation):
    
    """
    Calcule le meilleur coup pour l'IA à l'aide de l'algorithme Minimax.
    ici pour "player" qui l'IA
    board est une liste de liste
    
    """
    
    _, best_move = minimax(board, player, depth, nb_simulation)
    return best_move