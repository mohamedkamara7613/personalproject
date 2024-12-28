#-------------------------------------------------------------------------------
# Name:        Gomoku Version Orienté Objet
# Purpose:
#
# Author:      Kamara
#
# Created:     02/11/2023
#
# Description: Gomoku sans implementation de l'ia  
#-------------------------------------------------------------------------------


## Defintion de la class Gomoku ###############################################
class Gomuku():
    def __init__(self, size=15):
        self.size = size
        self.grid = [ [0 for _ in range(self.size) ] for _ in range(self.size)]
        self.symbol_init = '.'
        self.playerX = "\033[31mX\033[0m"
        self.playerO = "\033[32mO\033[0m"
        self.current_player = self.playerO

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

    #----------------------------------------------------------------------------------------------


    def is_game_over(self, row, col):
        player = 1 if self.current_player == self.playerX else -1
        align = 3

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
        while True:
            self.show_grid()     #Afficher le plateau

            #if self.current_player == self.playerO:
            print(f"C'est le tour  de {self.current_player} :")
            # Ce bloc peut etre mis dans un bloc try except pour la gestion de l'erreur de cast
            row = int(input("Entrer le num de la ligne : "))
            col = int(input("Entrer le num de la colonne : "))
            move = (row, col)

            if self.make_move(move, self.current_player):
                if self.is_game_over(row, col):
                    self.show_grid()
                    print(f"Fin du Jeu, {self.current_player} a gagné !! ")
                    break
                else:
                    self.current_player = self.playerO if self.current_player == self.playerX else self.playerX
            else:
                print("\n !! Commande invalide !! Try again \n")



################################################################################
if __name__ == "__main__":
    game = Gomuku()
    game.play()






