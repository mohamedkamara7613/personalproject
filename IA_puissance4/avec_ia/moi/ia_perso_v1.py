# -*- coding: utf-8 -*-
"""
    Amelioration POuvant etre ajoutée
        la fonction evaluate_window ne gere pas pour l'instant les contre attaque sur la diagonale
    AMELIORATION APPORTÉ
        - Meilleur heuristique
            - favoriser les colonnes centrales
            - bloquer les menaces adverses
        - Adaptation dynamique de la profondeur
        - utilisation de la memoïsation
        - tri des coups possibles  OK


"""


import copy
import random
from game_logic import ConnectFour

VIDE = 0
IA_PLAYER = 1
HUMAN_PLAYER = 2

# trivial
def coup_possible(board):
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
            

def score_position(board, player):
    """
    Calcule un score pour une position donnée en évaluant les alignements.
    """
    score = 0

    # Poids pour privilégier les colonnes centrales
    center_column = [row[len(board[0]) // 2] for row in board]
    score += center_column.count(player) * 3  # Favoriser la colonne centrale

    # Évaluer les alignements horizontaux, verticaux et diagonaux
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            window = [board[row][col + i] for i in range(4)]
            score += evaluate_window(window, player)

    # Ajouter des vérifications verticales et diagonales similaires
    return score

def evaluate_window(window, player):
    """
    Évalue une fenêtre de 4 cases.
    """
    score = 0
    opponent = 3 - player
    if window.count(player) == 4:
        score += 100  # Victoire
    elif window.count(player) == 3 and window.count(VIDE) == 1:
        score += 10  # Opportunité
    elif window.count(player) == 2 and window.count(VIDE) == 2:
        score += 5  # Potentiel
    if window.count(opponent) == 3 and window.count(VIDE) == 1:
        score -= 50  # Bloquer l'adversaire
    return score


cache = {}

def minimax(board, player, depth, nb_simulation, alpha=-float('inf'), beta=float('inf')):
    if depth == 0 or ConnectFour.check_victory(board, IA_PLAYER) or ConnectFour.check_victory(board, HUMAN_PLAYER) or ConnectFour.is_full(board):
        score = score_position(board, IA_PLAYER) - score_position(board, HUMAN_PLAYER)
        return score, None

    # Mise en place de la memoisation
    if len(cache) > 100000:  # Limite arbitraire
        cache.clear()
    board_tuple = tuple(tuple(row) for row in board)  # Convertir en immuable
    # Cas de base
    if board_tuple in cache:
        return cache[board_tuple]


    # tri des coups possibles en fonction de leur score
    coups_possibles = sorted(coup_possible(board), key=lambda x: score_position(board, player), reverse=True)
    if not coups_possibles:
        return 0, None
    
    if len(coups_possibles) < 4:
        depth += 1  # Explorer davantage quand peu d'options
    elif len(coups_possibles) > 10:
        depth -= 1  # Explorer moins quand trop de possibilité


    if player == IA_PLAYER:
        max_eval = -float('inf')
        best_move = None
        for coup in coups_possibles:
            board_copy = copy.deepcopy(board)
            ConnectFour.drop_piece(board_copy, coup, player)

            eval_score, _ = minimax(board_copy, HUMAN_PLAYER, depth - 1, nb_simulation, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = coup
            alpha = max(alpha, eval_score)
            if alpha >= beta:
                break
        # Mise a jour du cache
        cache[board_tuple] = (max_eval, best_move)
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for coup in coups_possibles:
            board_copy = copy.deepcopy(board)
            ConnectFour.drop_piece(board_copy, coup, player)

            eval_score, _ = minimax(board_copy, IA_PLAYER, depth - 1, nb_simulation, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = coup
            beta = min(beta, eval_score)
            if alpha >= beta:
                break
        cache[board_tuple] = (min_eval, best_move)
        return min_eval, best_move




def get_ai_move(board, player, depth, nb_simulation):
    
    """
    Calcule le meilleur coup pour l'IA à l'aide de l'algorithme Minimax.
    ici pour "player" qui l'IA
    
    """
    
    _, best_move = minimax(board, player, depth, nb_simulation)
    return best_move


if __name__ == "__main__":
    board = [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0]]

    
