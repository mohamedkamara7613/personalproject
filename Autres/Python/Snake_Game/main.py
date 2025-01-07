import pygame
import random

WHITE = (255, 255, 255)
GREEN = (0, 222, 0)
YELLOW = (250, 250, 5)



WIDTH = 600
HEIGHT = 600
BOX_SIZE = 20

class SnakeGame():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")

        self.columns, self.rows = WIDTH // BOX_SIZE, HEIGHT // BOX_SIZE
        self.grid = [[0 for _ in range(self.rows)] for _ in range(self.columns)]
        self.snake = []
        self.snake_head = {}
        self.food = {}
        self.score = 0
        self.current_score = 0 # peut etre recuperer depuis un fichier
        
    def init(self):
        # Initialisation de la tete du serpent au centre de l'ecran 
        self.head_snake = {
            "x": self.columns // 2,
            "y": self.rows // 2,
            "img": GREEN,
            "direction": "right"
        }
        # L'ajouter au snake
        self.snake.append(self.head_snake)

        # Initialisation du score
        self.score = 0

        # Initialisation de la position du food
        self.food = {
            "x": random.randint(0, self.columns - 1),
            "y": random.randint(0, self.rows - 1),
            "img": YELLOW
        }

    def handleEvenement(self):
        pass

    def updateGame(self):
        pass

    def handleCollisions(self):
        pass

    def generate_food(self):
        pass

    def drawGrid(self, screen):
        for i in range(self.rows):
            for j in range(self.columns):
                pygame.draw.rect(screen, WHITE, (i*BOX_SIZE, j*BOX_SIZE, BOX_SIZE, BOX_SIZE), 1)

        pygame.display.update()



def main():
    
    game = SnakeGame()
    game.init()

    fps = 60
    clock = pygame.time.Clock()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        clock.tick(fps)
        game.drawGrid(game.screen)
        
    pygame.quit()


if __name__ == "__main__":
    main()