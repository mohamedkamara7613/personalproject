#-------------------------------------------------------------------------------
# Name:        Gomoku Version Orienté Objet + Implementation d'une IA
# 
#
# Author:      KAMARA Mohamed
#
# Created:     01/01/2023
#-------------------------------------------------------------------------------

# A FAIRE prochainement : L'implementation du TSS dans la fonction evaluate

##########################################################################################################
##########################################################################################################
                #                        JEU DE BASE                         #
##########################################################################################################
##########################################################################################################

class Gomoku_game():
    def __init__(self, size=15):
        self.size = size
        self.grid = [ [0 for _ in range(self.size) ] for _ in range(self.size)]
        self.symbol_init = '.'
        self.playerX = "X"
        self.playerO = "O"
        self.current_player = self.playerO # A decider en fonction des regles du jeu ?
        
    def initialize_AI(self):
        self.ai = Gomoku_AI(self)

    #----------------------------------------------------------------------------------------------
    def show_grid(self):
        # Methode pour afficher le plateau
        grid_displayed = [ [0 for _ in range(self.size) ] for _ in range(self.size)] # Copier la grille
        for row in range(self.size):
            for col in range(self.size):
                # Mettre les bons caractere au bon endroit
                if self.grid[row][col] == 0:
                    grid_displayed[row][col] = self.symbol_init
                if self.grid[row][col] == 1:
                     grid_displayed[row][col] = self.playerX
                if self.grid[row][col] == -1:
                     grid_displayed[row][col] = self.playerO

        espace = '   '
        i=0
        for row in grid_displayed:
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
        if 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] == 0:
            # Place le symbole du joueur actuel dans la case
            if self.current_player == self.playerX:
                self.grid[row][col] = 1
                return True
            elif self.current_player == self.playerO:
                self.grid[row][col] = -1
                return True
        else:
            return False # Retourne Fasle si le mouvement n'est pas valide
#---------------------------------------------------------------------------------------------

    def is_game_over(self, row, col):
        player = 1 if self.current_player == self.playerX else -1
        align = 3 ## Ligne a changer pour les test

        # Recherche Horizontale
        consecutive = 1
        for compteur in range(1, 5): # Verification des positions à gauche
            if col - compteur < 0 or self.grid[row][col - compteur] != player:
                break
            consecutive += 1
        for compteur in range(1, 5): # Verification des positions à droite
            if col + compteur >= self.size or self.grid[row][col + compteur] != player:
                break
            consecutive += 1
        if consecutive >= align:
            return True

        #--------------- Recherche verticale
        consecutive = 1
        for compteur in range(1, 5): # Verification des positions en Haut
            if row - compteur < 0 or self.grid[row - compteur][col] != player:
                break
            consecutive += 1
        for compteur in range(1, 5):# Verification des positions en Bas
            if row + compteur >= self.size or self.grid[row + compteur][col] != player:
                break
            consecutive += 1
        if consecutive >= align:
            return True

        #--------------- Recherche diagonale bas-droite
        consecutive = 1
        for compteur in range(1, 5): # Verification des positions en bas droite
            if row + compteur >= self.size or col + compteur >= self.size or self.grid[row + compteur][col + compteur] != player:
                break
            consecutive += 1
        for compteur in range(1, 5): # Verification des positions en haut gauche
            if row - compteur < 0 or col - compteur < 0 or self.grid[row - compteur][col - compteur] != player:
                break
            consecutive += 1
        if consecutive >= align:
            return True

        #--------------- Recherche diagonale bas-gauche
        consecutive = 1
        for compteur in range(1, 5): # Verification des positions en bas gauche
            if row + compteur >= self.size or col - compteur < 0 or self.grid[row + compteur][col - compteur] != player:
                break
            consecutive += 1
        for compteur in range(1, 5): # Verification des positions en haut droit
            if row - compteur < 0 or col + compteur >= self.size or self.grid[row - compteur][col + compteur] != player:
                break
            consecutive += 1
        if consecutive >= align:
            return True

        return False

    #----------------------------------------------------------------------------------------------
    def play(self):
        self.initialize_AI()
        while True:
            self.show_grid()     #Afficher le plateau

            if self.current_player == self.playerO:
                print(f"C'est le tour  de {self.playerO} :")
                # Ce bloc peut etre mis dans un bloc try except pour la gestion de l'erreur de cast
                row = int(input("Entrer le num de la ligne : "))
                col = int(input("Entrer le num de la colonne : "))
                move = (row, col)

                if self.make_move(move, self.playerO):
                    if self.is_game_over(row, col):
                        self.show_grid()
                        print(f"Fin du Jeu, {self.playerO} a gagné !! ")
                        break
                    else:
                        self.current_player = self.playerX                
                else:
                    print("\n !! Commande invalide !! Try again \n")
            else:
                ai_move = self.ai.findBestMove()
                if self.make_move(ai_move, self.playerX):
                    self.current_player = self.playerO
                else:
                    raise ValueError('Impossible to make AI Move')
                


##########################################################################################################
##########################################################################################################
                #                        CREATION DU JOUEUR IA                          #
##########################################################################################################
##########################################################################################################

class Gomoku_AI():
    def  __init__(self, Gomoku_game_instance):
        self.Gomoku_game_instance = Gomoku_game_instance
        self.board = self.Gomoku_game_instance.grid


    def check_threat_in_row(self, board, row, col):
        print("Fonction check_threat_in_row")

        player_opponent = -1
        player_ia = 1
        threat_length = 4  # Nombre de pièces consécutives pour constituer une menace

        # Vérification des menaces potentielles vers la droite
        right_threat = (
            col + threat_length <= len(board[0]) and
            all(board[row][col + k] == player_opponent for k in range(threat_length))
        )

        # Vérification des menaces potentielles vers la gauche
        left_threat = (
            col - threat_length >= 0 and
            all(board[row][col - k] == player_opponent for k in range(threat_length))
        )

        return right_threat or left_threat

    def check_threat_in_column(self, board, row, col):
        print("Fonction check_threat_in_column")
        
        player_opponent = -1
        player_ia = 1
        threat_length = 4  # Nombre de pièces consécutives pour constituer une menace

        # Vérification des menaces potentielles vers le bas
        down_threat = (
            row + threat_length <= len(board) and
            all(board[row + k][col] == player_opponent for k in range(threat_length))
        )

        # Vérification des menaces potentielles vers le haut
        up_threat = (
            row - threat_length >= 0 and
            all(board[row - k][col] == player_opponent for k in range(threat_length))
        )

        return down_threat or up_threat

    def check_threat_in_diagonal(self, board, row, col):
        print("Fonction check_threat_in_diagonal")
        player_opponent = -1
        player_ia = 1
        threat_length = 4  # Nombre de pièces consécutives pour constituer une menace

        # Vérification des menaces potentielles vers le bas à droite
        down_right_threat = (
            row + threat_length <= len(board) and col + threat_length <= len(board[0]) and
            all(board[row + k][col + k] == player_opponent for k in range(threat_length))
        )

        # Vérification des menaces potentielles vers le haut à gauche
        up_left_threat = (
            row - threat_length >= 0 and col - threat_length >= 0 and
            all(board[row - k][col - k] == player_opponent for k in range(threat_length))
        )

        # Vérification des menaces potentielles vers le bas à gauche
        down_left_threat = (
            row + threat_length <= len(board) and col - threat_length >= 0 and
            all(board[row + k][col - k] == player_opponent for k in range(threat_length))
        )

        # Vérification des menaces potentielles vers le haut à droite
        up_right_threat = (
            row - threat_length >= 0 and col + threat_length <= len(board[0]) and
            all(board[row - k][col + k] == player_opponent for k in range(threat_length))
        )

        return down_right_threat or up_left_threat or down_left_threat or up_right_threat

    def calculer_threats(self, board):
        print("Fonction Calculer_Threats")
        threats = []

        # Recherche des menaces potentielles dans les lignes, colonnes et diagonales
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:  # Case vide
                    # Vérifier les menaces potentielles pour la case vide
                    threat_in_row = self.check_threat_in_row(board, i, j)
                    threat_in_column = self.check_threat_in_column(board, i, j)
                    threat_in_diagonal = self.check_threat_in_diagonal(board, i, j)

                    # Si une menace est trouvée, l'ajouter à la liste des menaces
                    if threat_in_row or threat_in_column or threat_in_diagonal:
                        threats.append((i, j, threat_in_row, threat_in_column, threat_in_diagonal))

        return threats

    def attribuer_poids(self, threats):
        print("Fonction Attribuer_poids")
        poids_threats = [[0 for _ in range(len(self.board[0]))] for _ in range(len(self.board))]

        for threat in threats:
            row, col, threat_in_row, threat_in_column, threat_in_diagonal = threat
            poids = self.calculer_poids_threat(threat_in_row, threat_in_column, threat_in_diagonal)
            poids_threats[row][col] = poids

        return poids_threats

    def calculer_poids_threat(self, in_row, in_column, in_diagonal):
        print("Fonction Calculer_poids_threat")
        poids_base = 1  # Poids de base pour une menace
        poids_total = 0

        if in_row:
            poids_total += poids_base

        if in_column:
            poids_total += poids_base

        if in_diagonal:
            poids_total += poids_base

        return poids_total


#  -----> Fonction d'evalution <----------------------------------------------------------------------------
    def evaluate(self):
        print("Fonction evaluate")
        """ Evaluation de l'etat actuel du plateau pour décider des coups à jouer """
        board = self.board
        score = 0
        player_ia = 1
        player_opponent = -1

        threats = self.calculer_threats(board)  # Ajoutez la fonction pour calculer les menaces avec le plateau donné

        # Attribution des poids aux menaces
        poids_threats = self.attribuer_poids(threats)

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == player_ia:
                    # Ajoutez un poids positif pour les positions de l'IA
                    score += poids_threats[i][j]
                elif board[i][j] == player_opponent:
                    # Ajoutez un poids négatif pour les positions de l'adversaire
                    score -= poids_threats[i][j]

        return score



#  -----> Implementation de l'algorithme minimax <---------------------------------------------------------
    def miniMax(self, depth, maximizing_player, lastMove=None):
        print("Fonction Minimax")
        """ Retourne le coup qui devrait etre joué en fonction de l'evaluation"""
        if depth == 0 or self.Gomoku_game_instance.is_game_over(lastMove[0],lastMove[1]): # si on arrive a la fin de l'arbre on evalue la position actuelle
            return self.evaluate()
        
        # Si c'est au tour de l'IA on cherche le maximum
        if maximizing_player:
            max_eval = float('-inf')
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j]== 0: # si la case est vide
                        self.board[i][j] = 1 # on place notre pion
                        eval = self.miniMax(depth-1, False, (i,j)) # on appelle recursivement la fonction cette fois en minimisant
                        self.board[i][j] = 0 # on remet le vide apres avoir tenter une combinaison
                        max_eval = max(max_eval, eval) # on choisit le maximum
            return max_eval
        else: # De ce cas la on minimize
            min_eval = float('inf')
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if  self.board[i][j] == 0:
                        self.board[i][j] = -1
                        eval = self.miniMax(depth-1, True, (i,j))
                        self.board[i][j] = 0
                        min_eval = min(min_eval, eval)
            return  min_eval
        
    
#  -----> Implementation de l'algorithme minimax avec L ELAGAGE ALPHA BETA <-----------------------------------

    def alphaBeta(self, depth, alpha=None, beta=None, maximizing_player=False, lastMove=None):
        if maximizing_player:
            alpha = float('-inf')  # Initialisation pour le joueur maximisant
            beta = float('inf')
        else:
            alpha = float('-inf')
            beta = float('inf')   # Initialisation pour le joueur minimisant

        print("Fonction alphaBeta")
        """Retourne le coup optimal à jouer"""
        if depth == 0 or self.Gomoku_game_instance.is_game_over(lastMove[0], lastMove[1]):
            return self.evaluate()  # Passer le plateau actuel à la fonction d'évaluation

        if maximizing_player:
            max_eval = float('-inf')
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] == 0:
                        self.board[i][j] = 1
                        eval = self.alphaBeta(depth - 1, alpha, beta, False, (i, j))
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
                        self.board[i][j] = -1  # Assurez-vous que l'adversaire joue avec la bonne couleur
                        eval = self.alphaBeta(depth - 1, alpha, beta, True, (i, j))
                        self.board[i][j] = 0
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval
            
#-----> La fonction qui utilise l'algorithme minimax  sans elegage pour trouver le meilleur coup <------
    def findBestMove(self):
        print("Fonction FindBestMove")
        bestValue = float("-inf")
        bestMove = None

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] == 0:
                    self.board[r][c] = 1 # on place le pion de l'ia
                    value = self.alphaBeta(depth=3, maximizing_player=False, lastMove=(r,c)) # la profondeur est fixée à 3
                    self.board[r][c] = 0 # On retire le pion de l'ia
                    if value > bestValue:
                        bestValue = value
                        bestMove = (r,c)
        return bestMove
        
        
    
##########################################################################################################
##########################################################################################################
##########################################################################################################""
if __name__ == "__main__":
    game = Gomoku_game()
    game.play()
    ai = Gomoku_AI(game)
    

""" def  alphaBeta(self, depth, alpha, beta, maximizing_player, lastMove=None):
    """"""Retourne le coup optimal à jouer""""""
    if depth == 1 or self.Gomoku_game_instance.is_game_over(lastMove[0], lastMove[1]):
        return self.evaluate(lastMove)
    
    if maximizing_player:
        max_eval = float('-inf')
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 0:
                    self.board[i][j] = 1
                    eval = self.alphaBeta(depth - 1, alpha, beta, False, (i,j)) # eval est un poid
                    self.board[i][j] = 0
                    max_eval = max(max_eval,eval)
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
                    eval = self.alphaBeta(depth - 1, alpha, beta, True, (i,j)) # eval est un poid
                    self.board[i][j] = 0
                    min_eval = max(min_eval,eval)
                    beta = max(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval
            
"""