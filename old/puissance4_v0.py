VIDE = 0
JOUEUR_1 = 1
JOUEUR_2 = 2

class ConnectFour:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.board = [[VIDE for _ in range(self.columns)] for _ in range(self.rows)]
        self.current_player = JOUEUR_1

    def print_board(self):
        """
        Affiche le plateau avec des symboles pour chaque joueur
        Gère tout ce qui touche l'affichage
        Entrée : None
        Sortie : None
        """
        symbols = {VIDE: '.', JOUEUR_1: "\033[31mX\033[0m", JOUEUR_2: "\033[32mO\033[0m"}
        spacing = '   '  # Triple espace pour séparer les colonnes
        for row in self.board:
            # Ajouter un espacement plus large entre les cellules
            print(spacing.join(symbols[cell] for cell in row))
            print()
        print("-" * (4 * self.columns - 1))  # Ajuster la taille du séparateur horizontal
        print(spacing.join(map(str, range(self.columns))))

    def drop_piece(self, column):
        """
            Ajoute un jeton dans une colonne si valide
                Vérifie la validité d'un coup
                Entrée : int 
                Sortie : None
            
        """
        if column < 0 or column >= self.columns or self.board[0][column] != VIDE:
            return False
        for row in reversed(range(self.rows)):
            if self.board[row][column] == VIDE:
                self.board[row][column] = self.current_player
                return True
        return False

    def switch_player(self):
        """Alterner entre les joueurs"""
        self.current_player = JOUEUR_2 if self.current_player == JOUEUR_1 else JOUEUR_1

    def is_full(self):
        """
            Vérifie si le plateau est plein
                Entrée : None
                Sortie ; bool
        """
        return all(self.board[0][col] != VIDE for col in range(self.columns))
        
    def check_victory(self):
        """
        Vérifie si le joueur actuel a gagné.
        Retourne True s'il y a une victoire, sinon False.
        """
        # Vérifier toutes les directions pour le joueur actuel
        player = self.current_player

        # Vérification horizontale
        for row in range(self.rows):
            for col in range(self.columns - 3):  # -3 pour éviter de sortir des limites
                if all(self.board[row][col + i] == player for i in range(4)):
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




# --- Boucle principale ---
def main():
    game = ConnectFour()
    game.print_board()

    while True:
        print(f"\nJoueur {game.current_player} ({'X' if game.current_player == JOUEUR_1 else 'O'}), à vous ! ٩(˘◡˘)۶\n")
        try:
            column = int(input("Choisissez une colonne (0-6) : "))

            if game.drop_piece(column):
                game.print_board()

                 # Vérification de la victoire
                if game.check_victory():
                    print(f"Félicitations ! Joueur {game.current_player} ({'X' if game.current_player == JOUEUR_1 else 'O'}) a gagné ! (ㆆ_ㆆ)")
                    break

                # VérifiacaTIon du matcnul
                if game.is_full():
                    print("Match nul ! Le plateau est plein.")
                    break

                game.switch_player()
            else:
                print("\nCette colonne est pleine ou invalide. Essayez encore. ¯\_( ͡❛ ͜ʖ ͡❛)_/¯\n")
        except ValueError:
            print("Veuillez entrer un numéro de colonne valide.")

if __name__ == "__main__":
    main()

