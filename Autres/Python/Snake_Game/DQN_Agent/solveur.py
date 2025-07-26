import pygame
from collections import deque
from DQN_game_logic import SnakeGame
import pickle

# Directions disponibles
DIRS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

DIR_TO_ACTION = {
    "up": 0,
    "down": 1,
    "right": 2,
    "left": 3,
}

def bfs(game):
    start = (game.snake_head["x"], game.snake_head["y"])
    goal = (game.food["x"], game.food["y"])

    visited = set()
    queue = deque([(start, [])])
    visited.add(start)

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == goal:
            return path  # Liste des directions ('up', 'left'...)

        for direction, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < game.columns and 0 <= ny < game.rows:
                if any(seg["x"] == nx and seg["y"] == ny for seg in game.snake):
                    continue
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [direction]))

    return []  # Aucun chemin trouvé

def play_with_solver():
    game = SnakeGame(display=True)
    game.init()
    clock = pygame.time.Clock()
    fps = 10

    try:
        while True:
            path = bfs(game)

            if not path:
                print("😵 Aucun chemin trouvé. Fin du jeu.")
                game.save()
                break

            for direction in path:
                action = DIR_TO_ACTION[direction]
                reward, done, score = game.step(action)

                game.drawGrid()
                pygame.display.flip()
                clock.tick(fps)

                if done:
                    print(f"🎮 Game Over — Score : {score}")
                    game.display_game_over()
                    pygame.time.wait(2000)
                    return
    except KeyboardInterrupt:
        print("🚫 Jeu interrompu par l'utilisateur.")
        game.save()  # Sauvegarder le score final
    finally:
            pygame.quit()
    

if __name__ == "__main__":
    play_with_solver()
