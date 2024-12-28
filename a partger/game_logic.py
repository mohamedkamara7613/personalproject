
# ----------- Constantes -----------------------
# les différents états possibles pour chaque case de la grille
VIDE = 0  # Case vide
IA_PLAYER = 1  # Case occupée par le joueur 1
JOUEUR_2 = 2  # Case occupée par le joueur 2

# Taille de la grille
COLONNES = 7
LIGNES = 6

# ----------- Classe ConnectFour ----------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class ConnectFour:
    def __init__(self):
        """Initialisation de la grille et du joueur actuelle"""
        #self.rows = rows
        #self.columns = columns
        self.board = [[VIDE for _ in range(COLONNES)] for _ in range(LIGNES)]
        self.current_player = IA_PLAYER # au choix

    @staticmethod
    def is_full(board):
        """
            Vérifie si le plateau est plein
                Entrée : None
                Sortie ; bool
        """
        return all(board[0][col] != VIDE for col in range(COLONNES))
    
    @staticmethod
    def switch_player(player):
        """ alterne les joueurs"""
        return (3 - player)    
        # OU AUTRE VERSION
        # self.current_player = JOUEUR_2 if self.current_player == IA_PLAYER else IA_PLAYER

    @staticmethod
    def drop_piece(board, column, player):
        """
            Ajoute un jeton dans une colonne si valide
                Vérifie la validité d'un coup
                Entrée : int 
                Sortie : None      
        """
        # Cas non valide
        if column < 0 or column >= COLONNES or board[0][column] != VIDE:
            return False
        
        # ATTENTION on inverse la liste
        for row in reversed(range(len(board))):
            if board[row][column] == VIDE:
                board[row][column] = player
                return True
        return False # dans le cas où il y a eu un probleme
    
    @staticmethod
    def check_victory(board, player):
        """
        Vérifie si le joueur actuel a gagné.
        Retourne True s'il y a une victoire, sinon False.
        """
        # lignes = len(board)
        # colonnes = len(board[0])

        # Vérifier toutes les directions pour le joueur actuel
        # Parcourir chaque ligne du plateau
        for row in range(LIGNES):
            # Parcourir chaque série de 4 colonnes dans la ligne
            for col in range(COLONNES - 3):  # On s'arrête avant les 3 dernières colonnes
                # Vérifie les 4 colonnes consécutives
                if (board[row][col] == player and
                    board[row][col + 1] == player and
                    board[row][col + 2] == player and
                    board[row][col + 3] == player):
                    # Si toutes les cases appartiennent au joueur, retournez True
                    return True

        # Vérification verticale
        for col in range(COLONNES):
            for row in range(LIGNES - 3):  # -3 pour éviter de sortir des limites
                if all(board[row + i][col] == player for i in range(4)):
                    return True

        # Vérification diagonale montante (\)
        for row in range(LIGNES - 3):
            for col in range(COLONNES - 3):
                if all(board[row + i][col + i] == player for i in range(4)):
                    return True

        # Vérification diagonale descendante (/)
        for row in range(3, LIGNES):
            for col in range(COLONNES - 3):
                if all(board[row - i][col + i] == player for i in range(4)):
                    return True

        return False