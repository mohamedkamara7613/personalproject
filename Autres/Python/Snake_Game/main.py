import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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
        self.snake_head = {
            "x": self.columns // 2,
            "y": self.rows // 2,
            "img": self.snake_head_img, # Par la suite img sera un sprite
            "direction": "none"
        }
        # L'ajouter au snake
        self.snake.append(self.snake_head)

        # Initialisation du score
        self.score = 0

        # Initialisation de la position du food
        self.generate_food()

    def generate_food(self):
        ok = True
        while ok:
            x = random.randint(0, self.columns - 1)
            y = random.randint(0, self.rows - 1)
            for segment in self.snake:
                if segment["x"] != x and segment["y"] != y:
                    self.food = {
                        "x": x,
                        "y": y,
                        "img": self.food_img
                    } 
                    ok = False

    def handleEvenement(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake[0]["direction"] != "down":
                    self.snake[0]["direction"] = "up"
                if event.key == pygame.K_DOWN and self.snake[0]["direction"] != "up":
                    self.snake[0]["direction"] = "down"
                if event.key == pygame.K_RIGHT and self.snake[0]["direction"] != "left":
                    self.snake[0]["direction"] = "right"
                if event.key == pygame.K_LEFT and self.snake[0]["direction"] != "right":
                    self.snake[0]["direction"] = "left"

        return True

    def updateGame(self):
        # Mise a jour de la position du serpent
        if self.snake_head["direction"] == "up":
            self.snake_head["y"] -= 1   
        elif self.snake_head["direction"] == "down":
            self.snake_head["y"] += 1
        elif self.snake_head["direction"] == "left":
            self.snake_head["x"] -= 1
        elif self.snake_head["direction"] == "right":
            self.snake_head["x"] += 1


        # Placer le serpent dans la grille
        for i in range(len(self.snake)):
            self.grid[self.snake[i]["x"]][self.snake[i]["y"]] = self.snake[i]["img"] # j'ai un doute sur la performence cad la grille va contenir des sprites

        # Placer le food dans la grille
        self.grid[self.food["x"]][self.food["y"]] = self.food["img"]

    def handleCollisions(self):
        pass
                


    def drawGrid(self):
        self.screen.fill(BLACK)
        
        for i in range(self.rows):
            for j in range(self.columns):
                # Faire apparaitre la grille
                pygame.draw.rect(self.screen, WHITE, (i*BOX_SIZE, j*BOX_SIZE, BOX_SIZE, BOX_SIZE), 1)

                if self.grid[i][j] == self.snake_head_img:
                    #self.screen.blit(self.snake_head_img, (i*BOX_SIZE, j*BOX_SIZE))
                    pygame.draw.rect(self.screen, self.snake_head_img, (i*BOX_SIZE, j*BOX_SIZE, BOX_SIZE, BOX_SIZE))
                elif self.grid[i][j] == self.food_img:
                    #self.screen.blit(self.food_img, (i*BOX_SIZE, j*BOX_SIZE))
                    pygame.draw.rect(self.screen, self.food_img, (i*BOX_SIZE, j*BOX_SIZE, BOX_SIZE, BOX_SIZE))

        pygame.display.update()



def main():
    
    game = SnakeGame()
    game.init()

    fps = 5
    clock = pygame.time.Clock()

    run = True
    while run:

        run = game.handleEvenement()
        game.updateGame()
        game.drawGrid()
        clock.tick(fps)
    pygame.quit()


if __name__ == "__main__":
    main()