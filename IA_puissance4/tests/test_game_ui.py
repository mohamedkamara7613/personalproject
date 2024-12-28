# -*- coding: utf-8 -*-
import pygame
import sys
from game_logic import ConnectFour

# ----------- Constantes -----------------------
VIDE = 0
JOUEUR_1 = 1
JOUEUR_2 = 2

COULEUR_VIDE = (200, 200, 200)
COULEUR_JOUEUR_1 = (255, 0, 0)
COULEUR_JOUEUR_2 = (255, 255, 0)
COULEUR_GRILLE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

LARGEUR_COLONNE = 130
HAUTEUR_LIGNE = 130
MARGE = 5
COLONNES = 7
LIGNES = 6
LARGEUR = COLONNES * LARGEUR_COLONNE
HAUTEUR = (LIGNES + 1) * HAUTEUR_LIGNE
DIMENSIONS = (LARGEUR, HAUTEUR)

FPS = 60

# ----------- Fonctions d'affichage -----------------------
def draw_board_console(game):
    """Affiche la grille dans la console."""
    print(f"\nJoueur {game.current_player} ({'X' if game.current_player == JOUEUR_1 else 'O'}), à vous !")
    symbols = {VIDE: '.', JOUEUR_1: "\033[31mX\033[0m", JOUEUR_2: "\033[32mO\033[0m"}
    spacing = '   '
    for row in game.board:
        print(spacing.join(symbols[cell] for cell in row))
        print()
    print("-" * (4 * COLONNES - 1))
    print(spacing.join(map(str, range(COLONNES))))


def draw_board_graphique(screen, game):
    """Dessine la grille sur une interface graphique."""
    for row in range(game.rows):
        for col in range(game.columns):
            pygame.draw.rect(
                screen, COULEUR_GRILLE,
                (col * LARGEUR_COLONNE, (row + 1) * HAUTEUR_LIGNE, LARGEUR_COLONNE, HAUTEUR_LIGNE)
            )
            couleur = COULEUR_VIDE
            if game.board[row][col] == JOUEUR_1:
                couleur = COULEUR_JOUEUR_1
            elif game.board[row][col] == JOUEUR_2:
                couleur = COULEUR_JOUEUR_2
            pygame.draw.circle(
                screen, couleur,
                (col * LARGEUR_COLONNE + LARGEUR_COLONNE // 2,
                 (row + 1) * HAUTEUR_LIGNE + HAUTEUR_LIGNE // 2),
                LARGEUR_COLONNE // 2 - MARGE
            )


def draw_board(mode, screen, game):
    """Affiche la grille en fonction du mode choisi."""
    if mode == "console":
        draw_board_console(game)
    elif mode == "graphique":
        draw_board_graphique(screen, game)


# ----------- Fonction principale -----------------------
def main(mode="console"):
    pygame.init()
    screen = None
    font = None

    if mode == "graphique":
        screen = pygame.display.set_mode(DIMENSIONS)
        pygame.display.set_caption("Puissance 4")
        font = pygame.font.SysFont("monospace", 50)

    clock = pygame.time.Clock()
    game = ConnectFour()
    running = True

    while running:
        if mode == "graphique":
            screen.fill(BLACK)

        draw_board(mode, screen, game)

        if mode == "console":
            try:
                column = int(input("Choisissez une colonne (0-6) : "))
                if not game.drop_piece(column):
                    print("Colonne invalide ou pleine. Essayez encore.")
                    continue
            except ValueError:
                print("Entrez un numéro de colonne valide.")
                continue
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    column = event.pos[0] // LARGEUR_COLONNE
                    if not game.drop_piece(column):
                        print("Colonne pleine !")
                        continue

        if game.check_victory():
            draw_board(mode, screen, game)
            if mode == "console":
                print(f"Joueur {game.current_player} a gagné !")
            else:
                winner_text = font.render(f"Joueur {game.current_player} gagne !", True, WHITE)
                screen.blit(winner_text, (40, 10))
                pygame.display.update()
                pygame.time.wait(3000)
            running = False
        elif game.is_full():
            draw_board(mode, screen, game)
            if mode == "console":
                print("Match nul !")
            else:
                draw_text = font.render("Match nul !", True, WHITE)
                screen.blit(draw_text, (50, 10))
                pygame.display.update()
                pygame.time.wait(3000)
            running = False
        else:
            game.switch_player()

        if mode == "graphique":
            pygame.display.update()
            clock.tick(FPS)

    if mode == "graphique":
        pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main("graphique")
