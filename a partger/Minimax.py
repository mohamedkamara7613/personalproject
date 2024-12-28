from copy import *
from random import *
import sys
from game_logic import ConnectFour

VIDE = 0
IA_PLAYER = 1
HUMAN_PLAYER = 2

board = [[VIDE for _ in range(7)] for _ in range(6)]


def evaluate(a,b):
    return (randint(0,10),randint(0,10),randint(0,10))

def coup_possible():
    return([1,3,4,6])


def minimax(board, player, depth, nb_simulation, alpha=-float('inf'), beta=float('inf')):
    if depth ==0 or ConnectFour.check_victory(board, player) or ConnectFour.is_full(board):
        eval=evaluate(board, nb_simulation)
        score=eval[1]-eval[2]
        return (score,None)
    coups_possibles=coup_possible(board)
    if len(coups_possibles) == 0:
        return (0,None)
    elif player == IA_PLAYER:
        max_eval=-float('inf')
        best_move=None
        for i in coups_possibles:
            grille=deepcopy(board)
            ConnectFour.drop_piece(grille, i, player)
            eval_score=minimax(grille, HUMAN_PLAYER, depth-1, nb_simulation, alpha, beta)
            if eval_score[0]>max_eval:
                max_eval=score
                best_move=i
            alpha=max(alpha,max_eval)
            if alpha>=beta:
                return (max_eval,best_move)
    elif player == HUMAN_PLAYER:
        min_eval=float('inf')
        best_move=None
        for i in coups_possibles:
            grille=deepcopy(board)
            ConnectFour.drop_piece(grille, i, player)
            eval_score=minimax(grille, IA_PLAYER, depth-1, nb_simulation, alpha, beta)
            if eval_score[0]<min_eval:
                min_eval=eval_score
                best_move=i
            beta=min(beta,min_eval)
            if alpha>=beta:
                return (min_eval,best_move)






