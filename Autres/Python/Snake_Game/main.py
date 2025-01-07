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
        self.snake_head_img = GREEN
        self.snake_body_img = WHITE

        self.food = {}
        self.food_img = YELLOW
        self.score = 0
        self.current_score = 0 # peut etre recuperer depuis un fichier
        
    def init(self):
        # Initialisation de la tete du serpent au centre de l'ecran 
        self.head_snake = {
            "x": self.columns // 2,
            "y": self.rows // 2,
            "img": self.snake_head_img, # Par la suite img sera un sprite
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
            "img": self.food_img
        }

        
    def handleEvenement(self):
        pass

    def updateGame(self):
        # Placer le serpent dans la grille
        for i in range(len(self.snake)):
            self.grid[self.snake[i]["x"]][self.snake[i]["y"]] = self.snake[i]["img"] # j'ai un doute sur la performence cad la grille va contenir des sprites

        # Placer le food dans la grille
        self.grid[self.food["x"]][self.food["y"]] = self.food["img"]

    def handleCollisions(self):
        pass

    def generate_food(self):
        pass

    def drawGrid(self, screen):
        
        for i in range(self.rows):
            for j in range(self.columns):
                # Faire apparaitre la grille
                pygame.draw.rect(screen, WHITE, (i*BOX_SIZE, j*BOX_SIZE, BOX_SIZE, BOX_SIZE), 1)

                if self.grid[i][j] == self.snake_head_img:
                    #screen.blit(self.snake_head_img, (i*BOX_SIZE, j*BOX_SIZE))
                    pygame.draw.rect(screen, self.snake_head_img, (i*BOX_SIZE, j*BOX_SIZE, BOX_SIZE, BOX_SIZE))
                elif self.grid[i][j] == self.food_img:
                    #screen.blit(self.food_img, (i*BOX_SIZE, j*BOX_SIZE))
                    pygame.draw.rect(screen, self.food_img, (i*BOX_SIZE, j*BOX_SIZE, BOX_SIZE, BOX_SIZE))

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
        
        game.updateGame()
        game.drawGrid(game.screen)
        clock.tick(fps)
    pygame.quit()


if __name__ == "__main__":
    main()