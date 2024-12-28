# -*- coding: utf-8 -*-



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
            





# pas trivial

def minimax(board, player, depth, nb_simulation, alpha=-float('inf'), beta=float('inf')): 
    """Implémente l'algorithme minimax potentiellement avec elage alpha beta
    
        Paramètres :
    - board : liste de listes représentant la grille du jeu
    - player : joueur actuel (1 pour l'IA, 2 pour l'humain)
    - depth : profondeur maximale de recherche
    - alpha : meilleure évaluation obtenue pour le joueur maximisant
    - beta : meilleure évaluation obtenue pour le joueur minimisant
    - nb_simulation : ...

    Retourne : (meilleure évaluation, meilleur coup)
    
    """
    #print(f"Profondeur actuelle : {depth}, Alpha : {alpha}, Beta : {beta}")
    
    
    if depth == 0 or ConnectFour.check_victory(board, IA_PLAYER)  or ConnectFour.check_victory(board, HUMAN_PLAYER) or ConnectFour.is_full(board):
        evaluation = evaluate(board, nb_simulation)
        #print(evaluation)
        score = evaluation[1] - evaluation[2]  # Différence entre les victoires de l'IA et celles de l'humain
        return (score, None) # a la place de None c'est le coup à jouer mais ici le jeu est fini donc pas de coup à jouer
    
    # Liste des coups possible
    coups_possibles = coup_possible(board)
    if not coups_possibles:
        return (0, None)  # Pas de coup possible


    if player == IA_PLAYER:
        max_eval = -float('inf')
        best_move = None
        for coup in coups_possibles:
            # Simuler le coup
            board_copy = copy.deepcopy(board)
            ConnectFour.drop_piece(board_copy, coup, player)

            # Appel recursif pour le joueur adverse
            eval_score, _ = minimax(board_copy, HUMAN_PLAYER, depth - 1, nb_simulation, alpha, beta)

            # Mettre a jour le meilleur coup et le meilleur evaluation
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = coup

            # Mettre a jour alpha et elaguer si necessaire
            alpha = max(alpha, eval_score)
            if alpha >= beta :
                break
        return (max_eval, best_move)
    else:
        min_eval = float('inf')
        best_move = None
        for coup in coups_possibles:
            # Simule le coup 
            board_copy = copy.deepcopy(board)
            ConnectFour.drop_piece(board_copy, coup, player)

            # appel recursid pour l'IA
            eval_score, _ = minimax(board_copy, IA_PLAYER, depth - 1, nb_simulation, alpha, beta)

            # Mettre a jour le meilleur coup et le meilleur evaluation
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = coup

            # Mettre a jour beta et elaguer si necessaire
            beta = min(beta, eval_score)
            if alpha >= beta:
                break
        return (min_eval, best_move) 



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
    
    
    

    #print(isinstance(board, list))
    #for row in board:
        #print(isinstance(row, list))


    score, best_move = minimax(board, IA_PLAYER, depth=3)
    print("Meilleure évaluation :", score)
    print("Meilleur coup :", best_move)
