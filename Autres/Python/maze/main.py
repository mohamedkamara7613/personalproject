import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SIZE = 7
WIDTH, HEIGHT = 500, 500
BOX_SIZE = WIDTH / SIZE
class Maze():
    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Labyrinthe")

        self.size = size
        self.grille = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def generate_maze(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)

        for i in range(self.size):
            for j in range(self.size):
                pygame.draw.rect(self.screen, WHITE, (i * BOX_SIZE, j * BOX_SIZE, BOX_SIZE, BOX_SIZE), 1, 1)
                
        pygame.display.update()

def main():
    maze = Maze(SIZE)
    print(maze.grille)
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        maze.draw()
    pygame.quit()


if __name__ == "__main__":
    main()