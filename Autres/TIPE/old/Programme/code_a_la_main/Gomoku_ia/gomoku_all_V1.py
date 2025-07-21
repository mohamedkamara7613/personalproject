#-------------------------------------------------------------------------------
# Name:        Gomoku Version Orienté Objet + Implementation d'une IA
# Purpose:
#
# Author:      KAMARA Mohamed
#
# Created:     01/01/2023
#-------------------------------------------------------------------------------

# A FAIRE prochainement : L'implementation du TSS dans la fonction evaluate
# implementer des limites de temps pour l'ia
# verifier l'ordre d'elagage qui joue enormément sur le temps d'execution
# tenter un profiling avec cProfile Pour determiner lesparties gourmands en temps
#utilisation de la transposition de table
#virer une partie de la fonction alphabeta dans le cas terminzl


##########################################################################################################
##########################################################################################################
                #                        JEU DE BASE                         #
##########################################################################################################
##########################################################################################################
import time
import numpy as np


class Gomoku_game():
    def __init__(self, size=8):
        self.size = size
        self.board:int = np.zeros((self.size, self.size), dtype=int)
        self.empty = '.'
        self.playerX = "X"
        self.playerO = "O"
        self.current_player = self.playerX # A decider en fonction des regles du jeu ?
        self.align:int = 3
        
    def initialize_AI(self):
        self.ai = Gomoku_AI(self)

    #----------------------------------------------------------------------------------------------
    def show_board(self):
        #print(self.board)
        # Methode pour afficher le plateau
        board_displayed = [ ["" for _ in range(self.size) ] for _ in range(self.size)] # Copier la grille
        for row in range(self.size):
            for col in range(self.size):
                # Mettre les bons caractere au bon endroit
                if self.board[row][col] == 0:
                    board_displayed[row][col] = self.empty
                if self.board[row][col] == 1:
                     board_displayed[row][col] = self.playerX
                if self.board[row][col] == -1:
                     board_displayed[row][col] = self.playerO

        espace = '   '
        i=0
        for row in board_displayed:
            print(f" {i:02d} |" + espace, espace.join(row))  # affcihe chaque ligne du plateau
            i += 1

        print( end=" "*9) # pas top,  une amelioration est possible
    	# affiche les numeros de chaque colonne
    	# peut etre ameliorer pour s'adapter a lespace des colonnes'
        for i in range(self.size):
            print(f"{i:02d}", end="  ")
        print()
    
    #----------------------------------------------------------------------------------------------

    def make_move(self, move, player):
        row, col = move[0], move[1]

        # Verification des limites du tableu et de la case vide
        if 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == 0:
            # Place le symbole du joueur actuel dans la case
            if player == self.playerX:
                self.board[row][col] = 1
                return True
            elif player == self.playerO:
                self.board[row][col] = -1
                return True
        else:
            return False # Retourne Fasle si le mouvement n'est pas valide
#---------------------------------------------------------------------------------------------
    def is_null(self):
        """ Renvoie vrai si toutes les cases sont occupées (1) ou (-1), sinon renvoie faux"""
        for line in self.board:
            if not all([val==1 or val==-1 for val in line]):
                return False
        return True
        
    
    def is_winner(self, player):
        # Check for horizontal wins
        for row in range(self.size):
            for col in range(self.size - self.align + 1):
                if all(self.board[row][col + i] == player for i in range(self.align)):
                    return True

        # Check for vertical wins
        for col in range(self.size):
            for row in range(self.size - self.align + 1):
                if all(self.board[row + i][col] == player for i in range(self.align)):
                    return True

        # Check for diagonal (top-left to bottom-right) wins
        for row in range(self.size - self.align + 1):
            for col in range(self.size - self.align + 1):
                if all(self.board[row + i][col + i] == player for i in range(self.align)):
                    return True

        # Check for diagonal (top-right to bottom-left) wins
        for row in range(self.size - self.align + 1):
            for col in range(self.align - 1, self.size):
                if all(self.board[row + i][col - i] == player for i in range(self.align)):
                    return True

        return False

                   

#---------------------------------------------------------------------------------------------

    def is_game_over(self, row, col, player):
        #player = 1 if self.current_player == self.playerX else -1
        

        # Recherche Horizontale
        consecutive = 1
        for compteur in range(1, 5): # Verification des positions à gauche
            if col - compteur < 0 or self.board[row][col - compteur] != player:
                break
            consecutive += 1
        for compteur in range(1, 5): # Verification des positions à droite
            if col + compteur >= self.size or self.board[row][col + compteur] != player:
                break
            consecutive += 1
        if consecutive >= self.align:
            return True

        #--------------- Recherche verticale
        consecutive = 1
        for compteur in range(1, 5): # Verification des positions en Haut
            if row - compteur < 0 or self.board[row - compteur][col] != player:
                break
            consecutive += 1
        for compteur in range(1, 5):# Verification des positions en Bas
            if row + compteur >= self.size or self.board[row + compteur][col] != player:
                break
            consecutive += 1
        if consecutive >= self.align:
            return True

        #--------------- Recherche diagonale bas-droite
        consecutive = 1
        for compteur in range(1, 5): # Verification des positions en bas droite
            if row + compteur >= self.size or col + compteur >= self.size or self.board[row + compteur][col + compteur] != player:
                break
            consecutive += 1
        for compteur in range(1, 5): # Verification des positions en haut gauche
            if row - compteur < 0 or col - compteur < 0 or self.board[row - compteur][col - compteur] != player:
                break
            consecutive += 1
        if consecutive >= self.align:
            return True

        #--------------- Recherche diagonale bas-gauche
        consecutive = 1
        for compteur in range(1, 5): # Verification des positions en bas gauche
            if row + compteur >= self.size or col - compteur < 0 or self.board[row + compteur][col - compteur] != player:
                break
            consecutive += 1
        for compteur in range(1, 5): # Verification des positions en haut droit
            if row - compteur < 0 or col + compteur >= self.size or self.board[row - compteur][col + compteur] != player:
                break
            consecutive += 1
        if consecutive >= self.align:
            return True
        
        # if len(self.get_empty_locations()) == 0: # match null
        #     return False

        return False

    #----------------------------------------------------------------------------------------------
    def play(self):
        self.initialize_AI()
        while True:
            self.show_board()     #Afficher le plateau

            if self.current_player == self.playerO:
                print(f"C'est le tour  de {self.playerO} :")
                # Ce bloc peut etre mis dans un bloc try except pour la gestion de l'erreur du cast
                row = int(input("Entrer le num de la ligne : "))
                col = int(input("Entrer le num de la colonne : "))
                move = (row, col)

                if self.make_move(move, self.playerO):
                    if self.is_game_over(row, col, -1):
                        self.show_board()
                        print(f"Fin du Jeu, {self.playerO} a gagné !! ")
                        break
                    else:
                        self.current_player = self.playerX                
                else:
                    print("\n !! Commande invalide !! Try again \n")
            else:
                #self.ai.score_position(self.board)
                start_time = time.time()
                ai_move = self.ai.findBestMove()
                end_time = time.time()
                elapsed_time = end_time - start_time
                elapsed_minutes = round((elapsed_time)/60)
                elapsed_seconds = round((elapsed_time%60))
                print(f"Board size : {self.size}, Elapsed Time : {elapsed_minutes}mn {elapsed_seconds}s ")

                if self.make_move(ai_move, self.playerX):
                    if self.is_game_over(ai_move[0], ai_move[1], 1):
                        self.show_board()
                        print("Fin du Jeu, L' IA a gagné !! ")
                        break
                    else:
                        self.current_player = self.playerO
                else:
                        print('Impossible to make AI Move')
                    

    ##########################################################################################################
    ##########################################################################################################
                    #                        CREATION DU JOUEUR IA                          #
    ##########################################################################################################
    ##########################################################################################################


class Gomoku_AI():
    def  __init__(self, Gomoku_game_instance):
        self.Gomoku_game_instance = Gomoku_game_instance
        self.board = self.Gomoku_game_instance.board
        self.playerX = 1
        self.playerO = -1
        self.empty = 0
        self.size = self.Gomoku_game_instance.size
        self.align:int = self.Gomoku_game_instance.align

    def evaluate_window(self, window):
        score = 0
        playerX_count = np.count_nonzero(window == self.playerX)  # Compter le nombre d'occurrences de playerX dans la fenêtre

        if playerX_count == self.align:
            score += 100
        elif playerX_count == self.align - 1 and np.count_nonzero(window == self.empty) == 1:
            score += 5
        elif playerX_count == self.align - 2 and np.count_nonzero(window == self.empty) == 2:
            score += 2

        return score


    def score_position_optimised(self, board):
        score = 0

        # Score center
        center_count = board[self.size // 2, self.size // 2]  # Utilisation de l'index du centre du plateau pour calculer le score
        score += center_count * (self.align - 1)  # Ajout du score du centre au score total

        # Score Horizontal
        for r in range(self.size):
            for c in range(self.size - self.align + 1):
                window = board[r, c:c + self.align]  # Extraction d'une fenêtre horizontale
                score += self.evaluate_window(window)  # Évaluation de la fenêtre et ajout au score total

        # Score Vertical
        for c in range(self.size):
            for r in range(self.size - self.align + 1):
                window = board[r:r + self.align, c]  # Extraction d'une fenêtre verticale
                score += self.evaluate_window(window)  # Évaluation de la fenêtre et ajout au score total

        # Score positive diagonale
        for r in range(self.size - self.align + 1):
            for c in range(self.size - self.align + 1):
                window = np.diag(board[r:r + self.align, c:c + self.align])  # Extraction d'une fenêtre diagonale
                score += self.evaluate_window(window)  # Évaluation de la fenêtre et ajout au score total

        # Score negative diagonale
        for r in range(self.align - 1, self.size):
            for c in range(self.size - self.align + 1):
                window = np.diag(np.fliplr(board)[r - self.align + 1:r + 1, c:c + self.align])  # Extraction d'une fenêtre diagonale inversée
                score += self.evaluate_window(window)  # Évaluation de la fenêtre et ajout au score total

        return score

    def score_position_basic(self, board):
        #print("I'm in")
        score = 0

        # Score center
        center_array = [int(i) for i in list(board[self.size//2:, self.size//2])]
        center_count = center_array.count(self.playerX)
        score += center_count * (self.align-1)

        # Score Horizontale
        for r in range(self.size):
            row_array = [int(i) for i in board[r, :]]
            for c in range(self.size-self.align-1):
                window = row_array[c:c+self.align]
                score += self.evaluate_window(window)

        # Score Verticale
        for c in range(self.size):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.size-self.align-1):
                window = col_array[r:r+self.align]
                score += self.evaluate_window(window)
        

        # Score positive diagonale
        for r in range(self.size-self.align-1):
            for c in range(self.size-self.align-1):
                window = [ board[r+i][c+i] for i in range(self.align)]
                score += self.evaluate_window(window)
                

        # Score negative diagonale
        for r in range(self.size-self.align-1):
            for c in range(self.size-self.align-1):
                window = [ board[r+self.align-1-i][c+i] for i in range(self.align)]
                score += self.evaluate_window(window)

        return score
    
    def is_terminal_node(self):
        return self.Gomoku_game_instance.is_winner(self.playerO) or self.Gomoku_game_instance.is_winner(self.playerX) or self.Gomoku_game_instance.is_null()

    def alphaBeta(self, depth=2, alpha=None, beta=None, maximizing_player=False):
        if maximizing_player:
            alpha = float('-inf')  # Initialisation pour le joueur maximisant
            beta = float('inf')
        else:
            alpha = float('-inf')
            beta = float('inf')   # Initialisation pour le joueur minimisant

        if depth == 0 or self.is_terminal_node():
            if self.is_terminal_node():
                if self.Gomoku_game_instance.is_winner(self.playerX):
                    return 10000000
                elif self.Gomoku_game_instance.is_winner(self.playerO):
                    return -10000000
                else:
                    return 0
            return self.score_position_basic(self.board)

        if maximizing_player:
            max_eval = float('-inf')
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] == 0:
                        self.board[i][j] = 1
                        eval = self.alphaBeta(depth - 1, alpha, beta, False)
                        self.board[i][j] = 0
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] == 0:
                        self.board[i][j] = -1  
                        eval = self.alphaBeta(depth - 1, alpha, beta, True)
                        self.board[i][j] = 0
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval


    def findBestMove(self):  
          
        best_move = None
        best_score = float('-inf')
        

        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    self.board[r][c] = 1
                    score = self.alphaBeta(depth=2)
                    #score = self.score_position_basic(self.board)
                    #score = self.TSS_algorithm(self.board)
                    self.board[r][c] = 0

                    if score > best_score :
                        best_score = score
                        best_move = (r,c)
            
        return best_move


##########################################################################################################
##########################################################################################################
##########################################################################################################""
if __name__ == "__main__":
    game = Gomoku_game()
    game.play()
    ai = Gomoku_AI(game)
