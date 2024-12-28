# -*- coding: utf-8 -*-
import sys
import pygame

# ----------- Constantes -----------------------
# les différents états possibles pour chaque case de la grille
VIDE = 0  # Case vide
IA_PLAYER = 1  # Case occupée par le joueur 1
JOUEUR_2 = 2  # Case occupée par le joueur 2

# Couleurs pour l'affichage graphique
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
# ---------------------------------------------------------------------------------------------------------------------
class ConnectFour:
    def __init__(self):
        """Initialisation de la grille et du joueur actuel"""
        self.board = [[VIDE for _ in range(COLONNES)] for _ in range(LIGNES)]
        self.current_player = IA_PLAYER

    @staticmethod
    def drop_piece(board, column, player):
        if column < 0 or column >= COLONNES or board[0][column] != VIDE:
            return False
        for row in reversed(range(len(board))):
            if board[row][column] == VIDE:
                board[row][column] = player
                return True
        return False

    @staticmethod
    def switch_player(player):
        return 3 - player

    @staticmethod
    def check_victory(board, player):
        for row in range(LIGNES):
            for col in range(COLONNES - 3):
                if all(board[row][col + i] == player for i in range(4)):
                    return True
        for col in range(COLONNES):
            for row in range(LIGNES - 3):
                if all(board[row + i][col] == player for i in range(4)):
                    return True
        for row in range(LIGNES - 3):
            for col in range(COLONNES - 3):
                if all(board[row + i][col + i] == player for i in range(4)):
                    return True
        for row in range(3, LIGNES):
            for col in range(COLONNES - 3):
                if all(board[row - i][col + i] == player for i in range(4)):
                    return True
        return False

    @staticmethod
    def is_full(board):
        return all(board[0][col] != VIDE for col in range(COLONNES))

# ----------- Classe ConsoleUI ----------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class ConsoleUI:
    @staticmethod
    def draw_board(board):
        symbols = {VIDE: '.', IA_PLAYER: "\033[31mX\033[0m", JOUEUR_2: "\033[33mO\033[0m"}
        spacing = '   '
        for row in board:
            print(spacing.join(symbols[cell] for cell in row))
            print()
        print("-" * (4 * COLONNES - 1))
        print(spacing.join(map(str, range(1, COLONNES + 1))))

    @staticmethod
    def get_player_input():
        while True:
            try:
                column = int(input("Choisissez une colonne (1-7) : ")) - 1
                return column
            except ValueError:
                print("\033[31mErreur : Veuillez entrer un numéro valide.\033[0m")

    @staticmethod
    def display_message(message, color_code="\033[32m"):
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
        self.screen.blit(text, (20, 10))
        pygame.display.update()

# ----------- Fonction principale -------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def main():
    game = ConnectFour()
    console_ui = ConsoleUI()
    graphic_ui = GraphicUI()

    console_ui.draw_board(game.board)
    graphic_ui.draw_board(game.board)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                column = graphic_ui.get_column_from_mouse()
                if ConnectFour.drop_piece(game.board, column, game.current_player):
                    console_ui.draw_board(game.board)
                    graphic_ui.draw_board(game.board)

                    if ConnectFour.check_victory(game.board, game.current_player):
                        graphic_ui.display_message(f"Joueur {game.current_player} a gagné !", (255, 255, 255))
                        pygame.time.wait(3000)
                        running = False

                    elif ConnectFour.is_full(game.board):
                        graphic_ui.display_message("Match nul !", (255, 255, 255))
                        pygame.time.wait(3000)
                        running = False

                    game.current_player = ConnectFour.switch_player(game.current_player)
                else:
                    graphic_ui.display_message("Colonne pleine !", (255, 0, 0))

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
