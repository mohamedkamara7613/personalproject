# -*- coding: utf-8 -*-
from ia_perso_v0 import *
#from ia_perso_v1 import *
#from ia_engine import *

import sys
import os
import random

# Ajouter le chemin local de Pygame au PATH
pygame_path = os.path.join(os.path.dirname(__file__), "libs")
sys.path.insert(0, pygame_path)

import pygame

# ----------- Constantes -----------------------
# les différents états possibles pour chaque case de la grille
VIDE = 0  # Case vide
IA_PLAYER = 1  # Case occupée par le joueur 1
JOUEUR_2 = 2  # Case occupée par le joueur 2

# Couleurs pour l'affichage graphique
WHITE = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
VIOLET = (49, 116, 227)

COULEUR_VIDE = (200, 200, 200)  # Gris clair pour les cases vides
COULEUR_JOUEUR_1 = (255, 0, 0)  # Rouge pour le joueur 1
COULEUR_JOUEUR_2 = (255, 255, 0)  # Jaune pour le joueur 2
COULEUR_GRILLE = (0, 0, 255)  # Bleu pour la grille

# Dimensions des cases et marges
LARGEUR_COLONNE = 100  # Largeur d'une colonne
HAUTEUR_LIGNE = 100  # Hauteur d'une ligne
MARGE = 5  # Espace entre les cercles et les bords de la grille

# Taille de la grille
COLONNES = 7
LIGNES = 6
LARGEUR = COLONNES * LARGEUR_COLONNE
HAUTEUR = (LIGNES + 1) * HAUTEUR_LIGNE
DIMENSIONS = (LARGEUR, HAUTEUR)

# ----------- Classe ConnectFour ----------------------------------------------------------------------------------------
# Tout ce qui concerne la logique du jeu
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
        print(f"{color_code}{message}\033[0m")



# ----------- Classe GraphicUI ----------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class GraphicUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(DIMENSIONS)
        pygame.display.set_caption("Puissance 4")
        self.clock = pygame.time.Clock()

    def draw_board2(self, board):
        self.screen.fill((0, 0, 0))
        for row in range(LIGNES):
            for col in range(COLONNES):
                pygame.draw.rect(
                    self.screen, COULEUR_GRILLE,
                    (col * LARGEUR_COLONNE, (row + 1) * HAUTEUR_LIGNE, LARGEUR_COLONNE, HAUTEUR_LIGNE)
                )
                couleur = COULEUR_VIDE
                if board[row][col] == IA_PLAYER:
                    couleur = COULEUR_JOUEUR_1
                elif board[row][col] == JOUEUR_2:
                    couleur = COULEUR_JOUEUR_2
                pygame.draw.circle(
                    self.screen, couleur,
                    (col * LARGEUR_COLONNE + LARGEUR_COLONNE // 2, (row + 1) * HAUTEUR_LIGNE + HAUTEUR_LIGNE // 2),
                    LARGEUR_COLONNE // 2 - MARGE
                )
        pygame.display.update()

    def draw_board(self, board):
        self.screen.fill((0, 0, 0))  # Remplir l'écran de noir
        font = pygame.font.SysFont("monospace", 30)  # Choisir une police et une taille

        for row in range(LIGNES):
            for col in range(COLONNES):
                # Dessiner les rectangles pour les cellules de la grille
                pygame.draw.rect(
                    self.screen, COULEUR_GRILLE,
                    (col * LARGEUR_COLONNE, (row + 1) * HAUTEUR_LIGNE, LARGEUR_COLONNE, HAUTEUR_LIGNE)
                )
                # Déterminer la couleur des cercles
                couleur = COULEUR_VIDE
                if board[row][col] == IA_PLAYER:
                    couleur = COULEUR_JOUEUR_1
                elif board[row][col] == JOUEUR_2:
                    couleur = COULEUR_JOUEUR_2
                # Dessiner les cercles représentant les jetons
                pygame.draw.circle(
                    self.screen, couleur,
                    (col * LARGEUR_COLONNE + LARGEUR_COLONNE // 2, (row + 1) * HAUTEUR_LIGNE + HAUTEUR_LIGNE // 2),
                    LARGEUR_COLONNE // 2 - MARGE
                )
        
        # Ajouter les numéros des colonnes en dessous de la grille
        for col in range(COLONNES):
            # Créer le texte du numéro de colonne
            text = font.render(str(col + 1), True, WHITE)  # Blanc pour le texte
            # Calculer la position du texte
            text_x = col * LARGEUR_COLONNE + LARGEUR_COLONNE // 2 - text.get_width() // 2
            text_y = (LIGNES + 1) * HAUTEUR_LIGNE + 10  # En dessous de la dernière ligne
            # Dessiner le texte sur l'écran
            self.screen.blit(text, (text_x, text_y))
        
        pygame.display.update()  # Mettre à jour l'affichage


    def get_column_from_mouse(self):
        x_pos = pygame.mouse.get_pos()[0]
        return x_pos // LARGEUR_COLONNE

    def display_message(self, message, color):
        font = pygame.font.SysFont("monospace", 50)
        text = font.render(message, True, color)
        self.screen.fill((0, 0, 0), (0, 0, LARGEUR, 50))  # Efface le message précédent
        self.screen.blit(text, (20, 10))
        pygame.display.update()

    def display_current_player(self, player):
        """
        Affiche quel joueur doit jouer.
        """
        font = pygame.font.SysFont("monospace", 40)
        color = VIOLET
        text = font.render(f"Joueur {player} à vous de jouer", True, color)
        self.screen.fill((0, 0, 0), (0, 0, LARGEUR, 50))  # Efface le message précédent
        self.screen.blit(text, (20, 10))
        pygame.display.update()


# ----------- Fonction principale ----------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

def main():
    """
    Fonction principale pour exécuter le jeu en mode console.
    """
    game = ConnectFour()  # Initialisation de la logique du jeu
    console_ui = ConsoleUI()
    graphic_ui = GraphicUI()

    console_ui.draw_board(game.board)  # Affiche la grille initiale
    graphic_ui.draw_board(game.board)


    running = True
    while running:
        graphic_ui.display_current_player(game.current_player) # affiche le joueur actuel

        if game.current_player == IA_PLAYER:
            # L'IA joue
            graphic_ui.display_message("L'IA réfléchit...", WHITE)
            best_move = get_ai_move(game.board, IA_PLAYER, depth=4, nb_simulation=50)

            if best_move is not None:
                
                game.drop_piece(game.board, best_move, IA_PLAYER)
            else: # Dans le cas ou l'ia ne trouve pas de coup il joue aléatoirement
                graphic_ui.display_message("Pas de meilleur coup trouvé", ROUGE)
                #console_ui.display_message("random", color_code="\033[31m")
                print("random")
                random_move = random.choice([c for c in range(COLONNES) if game.board[0][c] == VIDE])
                game.drop_piece(game.board, random_move, IA_PLAYER)

            console_ui.draw_board(game.board)
            graphic_ui.draw_board(game.board)

            # Verification de la victoire ou du match nul
            if game.check_victory(game.board, IA_PLAYER):
                graphic_ui.display_message("L'IA a gagné", VERT)
                console_ui.display_message( f"Dommage ! L'IA a gagné !", color_code="\033[35m")
                pygame.time.wait(3000)
                running = False
            elif game.is_full(game.board):
                graphic_ui.display_message("Match nul !", VERT)
                console_ui.display_message(f"Match nul !!", color_code="\033[35m")
                pygame.time.wait(3000)
                running = False

            # Passer au joueur suivant
            game.current_player = game.switch_player(game.current_player)
            continue

        # Gestion des evenements pour le joueur Humain
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                column = graphic_ui.get_column_from_mouse() # Récupère la colonne sélectionnée par l'utilisateur
                if game.drop_piece(game.board, column, game.current_player): # tente de palcer le jeton
                    console_ui.draw_board(game.board)
                    graphic_ui.draw_board(game.board)

                    if game.check_victory(game.board, game.current_player): # Vérifie si le joueur a gagné
                        graphic_ui.display_message(f"Joueur {game.current_player} a gagné !", VERT)
                        console_ui.display_message(f"Félicitation ! Joueur 2 (O) a gagné !", color_code="\033[35m")
                        pygame.time.wait(3000)
                        running = False

                    elif game.is_full(game.board): # Vérifie si la grille est pleine
                        graphic_ui.display_message("Match nul !", VERT)
                        console_ui.display_message(f"Match nul !!", color_code="\033[35m")
                        pygame.time.wait(3000)
                        running = False

                    game.current_player = game.switch_player(game.current_player)
                else:
                    graphic_ui.display_message("Colonne pleine !", ROUGE)
    
    pygame.quit()
    sys.exit()  # Quitte le programme



if __name__ == "__main__":
    main()




    