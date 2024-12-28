# -*- coding: utf-8 -*-

VIDE = 0
JOUEUR_1 = 1
JOUEUR_2 = 2

class ConnectFour:
    def __init__(self, rows=6, columns=7):
        """Initialisation de la grille et du joueur actuelle"""
        self.rows = rows
        self.columns = columns
        self.board = [[VIDE for _ in range(columns)] for _ in range(rows)]
        self.current_player = JOUEUR_1 # au choix

    def drop_piece(self, column):
        """
            Ajoute un jeton dans une colonne si valide
                Vérifie la validité d'un coup
                Entrée : int 
                Sortie : None
            
        """
        # Cas non valide
        if column < 0 or column >= self.columns or self.board[0][column] != VIDE:
            return False
        
        # ATTENTION on inverse la liste
        for row in reversed(range(self.rows)):
            if self.board[row][column] == VIDE:
                self.board[row][column] = self.current_player
                return True
        return False # dans le cas où il y a eu un probleme
    
    def switch_player(self):
        self.current_player = 3 - self.current_player
        
        # OU AUTRE VERSION
        # self.current_player = JOUEUR_2 if self.current_player == JOUEUR_1 else JOUEUR_1


    def check_victory(self):
        """
        Vérifie si le joueur actuel a gagné.
        Retourne True s'il y a une victoire, sinon False.
        """

        # Vérifier toutes les directions pour le joueur actuel
        player = self.current_player

        # Parcourir chaque ligne du plateau
        for row in range(self.rows):
            # Parcourir chaque série de 4 colonnes dans la ligne
            for col in range(self.columns - 3):  # On s'arrête avant les 3 dernières colonnes
                # Vérifie les 4 colonnes consécutives
                if (self.board[row][col] == player and
                    self.board[row][col + 1] == player and
                    self.board[row][col + 2] == player and
                    self.board[row][col + 3] == player):
                    # Si toutes les cases appartiennent au joueur, retournez True
                    return True

        # Vérification verticale
        for col in range(self.columns):
            for row in range(self.rows - 3):  # -3 pour éviter de sortir des limites
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True

        # Vérification diagonale montante (\)
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True

        # Vérification diagonale descendante (/)
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True

        return False
    
    def is_full(self):
        """
            Vérifie si le plateau est plein
                Entrée : None
                Sortie ; bool
        """
        return all(self.board[0][col] != VIDE for col in range(self.columns))