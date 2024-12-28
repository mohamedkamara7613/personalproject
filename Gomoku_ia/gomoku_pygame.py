import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des constantes et des couleurs
SIZE = 15
CELL_SIZE = 40  # Taille de chaque cellule en pixels
WIDTH = HEIGHT = SIZE * CELL_SIZE  # Dimensions de la fenêtre
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gomoku")

# Classe du jeu
class Gomoku:
    def __init__(self, size=15):
        self.size = size
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 1  # 1 pour X, -1 pour O

    def draw_grid(self):
        """Dessine la grille du plateau."""
        for row in range(self.size):
            for col in range(self.size):
                pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def draw_pieces(self):
        """Dessine les pions des joueurs sur le plateau."""
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 1:  # Joueur X
                    pygame.draw.circle(screen, RED, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
                elif self.grid[row][col] == -1:  # Joueur O
                    pygame.draw.circle(screen, GREEN, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    def make_move(self, row, col):
        """Gère le placement des pions par les joueurs."""
        if self.grid[row][col] == 0:  # Vérifie si la case est vide
            self.grid[row][col] = self.current_player
            self.current_player = -self.current_player  # Change de joueur

    def is_game_over(self, row, col):
        """Vérifie si un joueur a gagné."""
        player = self.current_player
        align = 5

        # Directions : horizontal, vertical, diagonale (\), diagonale (/)
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)],  # Diagonale \
            [(1, -1), (-1, 1)]   # Diagonale /
        ]

        for direction in directions:
            consecutive = 1
            for dx, dy in direction:
                for step in range(1, align):
                    r, c = row + step * dx, col + step * dy
                    if 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == player:
                        consecutive += 1
                    else:
                        break
            if consecutive >= align:
                return True

        return False

# Fonction principale
def main():
    game = Gomoku()
    running = True

    while running:
        screen.fill(BLACK)  # Remplir l'écran en noir
        game.draw_grid()  # Dessiner la grille
        game.draw_pieces()  # Dessiner les pions

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    # Obtenir la position du clic
                    col = event.pos[0] // CELL_SIZE
                    row = event.pos[1] // CELL_SIZE

                    # Faire un mouvement
                    game.make_move(row, col)

                    # Vérifier si le jeu est terminé
                    if game.is_game_over(row, col):
                        winner = "Joueur X" if game.current_player == -1 else "Joueur O"
                        print(f"{winner} a gagné !")
                        pygame.time.wait(5000)
                        running = False

        pygame.display.flip()  # Mettre à jour l'écran

    pygame.quit()  # Quitter Pygame
    sys.exit()

if __name__ == "__main__":
    main()
