import pygame
import random

# Paramètres du labyrinthe
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Départ
RED = (255, 0, 0)  # Arrivée
BLUE = (0, 0, 255)  # Exploration

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labyrinthe")

# Création de la grille
maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]  # 1 = mur, 0 = chemin

# Directions possibles (haut, bas, gauche, droite)
DIRECTIONS = [(0, -2), (0, 2), (-2, 0), (2, 0)]

# Fonction de génération du labyrinthe (DFS récursif)
def generate_maze(x, y):
    maze[y][x] = 0  # Marquer la cellule comme vide
    random.shuffle(DIRECTIONS)  # Mélanger les directions pour un labyrinthe unique
    
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 1:
            maze[y + dy // 2][x + dx // 2] = 0  # Casser le mur entre les cellules
            generate_maze(nx, ny)

# Générer un labyrinthe à partir du coin supérieur gauche
generate_maze(0, 0)

# Départ et arrivée
start = (0, 0)
goal = (COLS - 1, ROWS - 1)
maze[goal[1]][goal[0]] = 0  # Assurer un chemin vers la sortie

# Fonction d'affichage
def draw_maze():
    screen.fill(WHITE)
    for y in range(ROWS):
        for x in range(COLS):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Marquer le départ et l'arrivée
    pygame.draw.rect(screen, GREEN, (start[0] * CELL_SIZE, start[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (goal[0] * CELL_SIZE, goal[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Boucle principale
running = True
while running:
    draw_maze()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
