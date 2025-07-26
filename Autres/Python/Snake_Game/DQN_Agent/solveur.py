import pygame
from collections import deque
from DQN_game_logic import SnakeGame
from heapq import heappush, heappop

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
# ----------------------------------------------------------------------------------------------------
#       .......................................=== A* pathfinding ===.......................................
# ----------------------------------------------------------------------------------------------------
def safe_a_star(game):
    start = (game.snake_head["x"], game.snake_head["y"])
    goal = (game.food["x"], game.food["y"])
    rows, cols = game.rows, game.columns
    snake_body = [(seg["x"], seg["y"]) for seg in game.snake[1:]]  # exclure la tête

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(start, goal, forbidden):
        open_set = []
        heappush(open_set, (0 + heuristic(start, goal), 0, start, []))
        visited = set()

        while open_set:
            est_total, cost, current, path = heappop(open_set)

            if current in visited:
                continue
            visited.add(current)

            if current == goal:
                return path  # liste de directions

            for direction, (dx, dy) in DIRS.items():
                nx, ny = current[0] + dx, current[1] + dy

                if not (0 <= nx < cols and 0 <= ny < rows):
                    continue
                if (nx, ny) in forbidden:
                    continue

                heappush(open_set, (
                    cost + 1 + heuristic((nx, ny), goal),
                    cost + 1,
                    (nx, ny),
                    path + [direction]
                ))

        return []  # Aucun chemin trouvé

    # ==== 1. Chercher un chemin vers la nourriture ====
    path_to_food = a_star(start, goal, set(snake_body))
    if path_to_food:
        return path_to_food

    # ==== 2. Fallback : chemin vers la queue ====
    if len(game.snake) >= 2:
        tail = (game.snake[-1]["x"], game.snake[-1]["y"])
        # On peut marcher sur la queue car elle va bouger
        snake_body_except_tail = set(snake_body[:-1])  # exclure la queue

        path_to_tail = a_star(start, tail, snake_body_except_tail)
        if path_to_tail:
            print("🌀 Aucune nourriture atteignable → repli vers la queue")
            return path_to_tail

    # ==== 3. Aucun chemin possible ====
    print("❌ Aucun chemin vers la nourriture ni la queue")
    return []

# ----------------------------------------------------------------------------------------------------
#       .......................................=== BFS ===.......................................
# ----------------------------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------------------------------------------
#       .......................................=== Solver ===.......................................
# ------------------------------------------------------------------------------------------------------------------

def play_with_solver():
    game = SnakeGame(display=True)
    game.init()
    clock = pygame.time.Clock()
    fps = 10

    try:
        while True:
            # path = bfs(game)
            path = safe_a_star(game)

            if not path:
                print("😵 Aucun chemin trouvé. Fin du jeu.")
                print(f"🎮  Score Final : {score}, High Score : {game.high_score}")
                game.save()
                break

            for direction in path:
                action = DIR_TO_ACTION[direction]
                reward, done, score = game.step(action)

                game.drawGrid()
                game.draw_path(path)  # Dessiner le chemin
                pygame.display.flip()
                clock.tick(fps)

                if done:
                    print(f"🎮 Game Over — Score : {score}")
                    game.display_game_over()
                    pygame.time.wait(2000)
                    return
    except KeyboardInterrupt:
        print("🚫 Jeu interrompu par l'utilisateur.")
        print(f"🎮  Score Final : {score}, High Score : {game.high_score}")
        game.save()  # Sauvegarder le score finalé
    finally:
            pygame.quit()
    

if __name__ == "__main__":
    play_with_solver()
