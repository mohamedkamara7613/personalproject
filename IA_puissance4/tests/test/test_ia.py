
# -*- coding: utf-8 -*-
import sys
import pygame
import random
from game_logic import *
import ia_v0

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

    def draw_board(self, board):
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



# ----------- Fonction principale avec IA -------------------------------------------------------------------------------------
def main():
    game = ConnectFour()
    console_ui = ConsoleUI()
    graphic_ui = GraphicUI()

    console_ui.draw_board(game.board)
    graphic_ui.draw_board(game.board)

    running = True
    while running:
        graphic_ui.display_current_player(game.current_player)  # Affiche le joueur actuel

        if game.current_player == IA_PLAYER:  # Tour de l'IA
            graphic_ui.display_message("L'IA réfléchit...", (255, 255, 255))
            best_move = ia_v0.get_ai_move(game.board, IA_PLAYER, depth=4)

            if best_move is not None:  # Si un meilleur coup est trouvé
                ConnectFour.drop_piece(game.board, best_move, IA_PLAYER)
            else:  # Cas où l'IA ne trouve pas de coup, elle joue aléatoirement
                random_move = random.choice([c for c in range(COLONNES) if game.board[0][c] == VIDE])
                ConnectFour.drop_piece(game.board, random_move, IA_PLAYER)

            console_ui.draw_board(game.board)
            graphic_ui.draw_board(game.board)

            # Vérification de la victoire ou du match nul
            if ConnectFour.check_victory(game.board, IA_PLAYER):
                graphic_ui.display_message("L'IA a gagné !", VERT)
                pygame.time.wait(3000)
                running = False
            elif ConnectFour.is_full(game.board):
                graphic_ui.display_message("Match nul !", VERT)
                pygame.time.wait(3000)
                running = False

            # Passer au joueur suivant
            game.current_player = ConnectFour.switch_player(game.current_player)
            continue  # Sauter les événements pygame pour ce tour

        # Gestion des événements pour le joueur humain
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                column = graphic_ui.get_column_from_mouse()  # Récupère la colonne cliquée
                if ConnectFour.drop_piece(game.board, column, game.current_player):  # Tente de placer le jeton
                    console_ui.draw_board(game.board)
                    graphic_ui.draw_board(game.board)

                    # Vérification de la victoire ou du match nul
                    if ConnectFour.check_victory(game.board, game.current_player):
                        graphic_ui.display_message(f"Joueur {game.current_player} a gagné !", VERT)
                        pygame.time.wait(3000)
                        running = False
                    elif ConnectFour.is_full(game.board):
                        graphic_ui.display_message("Match nul !", VERT)
                        pygame.time.wait(3000)
                        running = False

                    # Passer au joueur suivant
                    game.current_player = ConnectFour.switch_player(game.current_player)
                else:
                    graphic_ui.display_message("Colonne pleine !", ROUGE)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()