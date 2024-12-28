# -*- coding: utf-8 -*-
import sys


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
    
    
    

    
# ----------- Classe ConsoleUI ----------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class ConsoleUI:
    """
    Classe pour gérer l'affichage et les interactions en mode console.
    """
    
    @staticmethod
    def draw_board(board):
        """
        Affiche la grille dans la console avec des symboles colorés.
        """
        symbols = {VIDE: '.', IA_PLAYER: "\033[31mX\033[0m", JOUEUR_2: "\033[33mO\033[0m"}
        spacing = '   '  # Triple espace pour séparer les colonnes
        for row in board:
            print(spacing.join(symbols[cell] for cell in row))
            print()
        print("-" * (4 * COLONNES - 1))  # Ajuste la taille du séparateur horizontal
        print(spacing.join(map(str, range(1,COLONNES+1))))  # Affiche les indices des colonnes

    @staticmethod
    def get_player_input():
        """
        Demande à l'utilisateur de choisir une colonne.
        Valide l'entrée pour s'assurer qu'elle est correcte.
        """
        while True:
            try:
                column = int(input("Choisissez une colonne (0-6) : "))
                return (column - 1)
            except ValueError:
                print("\033[31mErreur : Veuillez entrer un numéro valide.\033[0m")

    @staticmethod
    def display_message(message, color_code="\033[32m"):
        """
        Affiche un message dans la console avec une couleur spécifique.
        """
        print(f"\n\t\t\t{color_code}{message}\033[0m\n")

# ----------- Fonction principale ----------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

def main():
    """
    Fonction principale pour exécuter le jeu en mode console.
    """
    game = ConnectFour()  # Initialisation de la logique du jeu
    ConsoleUI.draw_board(game.board)  # Affiche la grille initiale

    while True:
        # Affiche le joueur actuel
        ConsoleUI.display_message(
            f"Joueur {game.current_player} ({'X' if game.current_player == IA_PLAYER else 'O'}), à vous !"
        )
        """
        if game.current_player == IA_PLAYER:  # Supposons que IA_PLAYER est une constante pour l'IA
            print("L'IA réfléchit...")
            best_move = None #ia_engine.get_ai_move(game.board, depth=4)
            if best_move is not None:
                game.drop_piece(best_move)
            if game.check_victory():
                print("L'IA a gagné !")
                break
        else:"""
        # Demande à l'utilisateur de choisir une colonne
        column = ConsoleUI.get_player_input()

        # Tente de placer un jeton dans la colonne choisie
        if ConnectFour.drop_piece(game.board, column, game.current_player):
            ConsoleUI.draw_board(game.board)  # Met à jour la grille après le coup

            # Vérifie si le joueur actuel a gagné
            if ConnectFour.check_victory(game.board, game.current_player):
                ConsoleUI.display_message(
                    f"Félicitations ! Joueur {game.current_player} ({'X' if game.current_player == IA_PLAYER else 'O'}) a gagné !",
                    color_code="\033[35m"
                )
                break

            # Vérifie si le plateau est plein (match nul)
            if ConnectFour.is_full(game.board):
                ConsoleUI.display_message("Match nul ! Le plateau est plein.", color_code="\033[33m")
                break

            # Change de joueur
            game.current_player = ConnectFour.switch_player(game.current_player)
        else:
            ConsoleUI.display_message("Cette colonne est pleine ou invalide. Essayez encore.", color_code="\033[31m")

    sys.exit()  # Quitte le programme



if __name__ == "__main__":
    main()




    # Test des fonctions
    # la liste de liste contient des 0, 1 ou 2
    game = ConnectFour()
    print(ConnectFour.is_full(game.board))
    print(ConnectFour.check_victory(game.board, IA_PLAYER))
    print(ConnectFour.drop_piece(game.board, 0, IA_PLAYER))
    print(ConnectFour.switch_player(IA_PLAYER))