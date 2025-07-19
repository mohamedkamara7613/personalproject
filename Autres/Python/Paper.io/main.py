# -*- coding: utf-8 -*-
import pygame
import sys

# --- Constants ---
WIDTH, HEIGHT = 500, 500
GRID_SIZE = 10  # Each cell will be 10x10 pixels
FPS = 60

PLAYER_COLOR = (0, 200, 0)
TRAIL_COLOR = (0, 100, 0)
TERRITORY_COLOR = (0, 255, 0)
BG_COLOR = (230, 230, 230)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# --- Initialize Pygame ---
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Game State ---
player_pos = [WIDTH // (2 * GRID_SIZE), HEIGHT // (2 * GRID_SIZE)]  # Grid position
direction = RIGHT

territory = set()  # Set of (x, y) grid positions that are owned
trail = []         # List of (x, y) positions outside the base

# Initialize base
for dx in range(-2, 3):
    for dy in range(-2, 3):
        territory.add((player_pos[0] + dx, player_pos[1] + dy))

# --- Game Loop ---
running = True
while running:
    clock.tick(FPS)
    win.fill(BG_COLOR)

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Input Handling ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        direction = UP
    elif keys[pygame.K_DOWN]:
        direction = DOWN
    elif keys[pygame.K_LEFT]:
        direction = LEFT
    elif keys[pygame.K_RIGHT]:
        direction = RIGHT

    # --- Update Position ---
    new_pos = [player_pos[0] + direction[0], player_pos[1] + direction[1]]

    # Check collision with walls
    if not (0 <= new_pos[0] < WIDTH // GRID_SIZE and 0 <= new_pos[1] < HEIGHT // GRID_SIZE):
        print("Game Over: Out of bounds")
        running = False
        continue

    # If outside base, record trail
    if tuple(new_pos) not in territory:
        if tuple(new_pos) in trail:
            print("Game Over: Self collision")
            running = False
            continue
        trail.append(tuple(new_pos))
    else:
        # Player returned to base, convert trail to territory
        for cell in trail:
            territory.add(cell)
        trail.clear()

    player_pos = new_pos

    # --- Draw Territory ---
    for cell in territory:
        pygame.draw.rect(win, TERRITORY_COLOR,
                         (cell[0]*GRID_SIZE, cell[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # --- Draw Trail ---
    for cell in trail:
        pygame.draw.rect(win, TRAIL_COLOR,
                         (cell[0]*GRID_SIZE, cell[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # --- Draw Player ---
    pygame.draw.rect(win, PLAYER_COLOR,
                     (player_pos[0]*GRID_SIZE, player_pos[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()

pygame.quit()
sys.exit()
