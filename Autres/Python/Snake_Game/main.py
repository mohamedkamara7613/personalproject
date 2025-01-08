""" Optimisation de la grille :

Tu utilises une grille 2D (self.grid) pour stocker les états des cases. 
Cela pourrait devenir inefficace en termes de mémoire et de performance 
si la grille est grande. Une alternative serait de garder uniquement la 
liste des coordonnées du serpent et de la nourriture.
 """


import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 222, 0)
YELLOW = (250, 250, 5)



WIDTH = 600
HEIGHT = 600
BOX_SIZE = 30

class SnakeGame():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")

        self.columns, self.rows = WIDTH // BOX_SIZE, HEIGHT // BOX_SIZE
        self.grid = []
        self.snake = []
        self.snake_head = {}
        self.snake_head_img = GREEN
        self.snake_body_img = WHITE

        self.food = {}
        self.food_img = YELLOW
        self.score = 0
        self.current_score = 0 # peut etre recuperer depuis un fichier
        
    def init(self):
        # Initialisation de la grille
        self.grid = [[0 for _ in range(self.rows)] for _ in range(self.columns)]
        
        # Initialisation de la tete du serpent au centre de l'ecran 
        self.snake = []
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


    def handleCollisions(self):
        # Si le serpent mange la nourriture
        if self.snake_head["x"]  == self.food["x"] and self.snake_head["y"] == self.food["y"]:
            self.score += 1
            self.generate_food()
            last_segment = self.snake[-1]
            new_segment = {
                "x": last_segment["x"],
                "y": last_segment["y"],
                "img" : last_segment["img"],
                "direction": last_segment["direction"]
            }
            self.snake.append(new_segment)
            return False

        # Si le serpent se touche lui meme
        for i in range(1,len(self.snake)):
            if self.snake_head["x"] == self.snake[i]["x"] and self.snake_head["y"] == self.snake[i]["y"]:
                return True
            
        
    def updateGame(self):
        # Réinitialiser la grille
        self.grid = [[0 for _ in range(self.rows)] for _ in range(self.columns)]

        # Mise à jour des positions des segments du corps
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i]["x"] = self.snake[i - 1]["x"]
            self.snake[i]["y"] = self.snake[i - 1]["y"]

        # Mise a jour de la position du serpent
        if self.snake_head["direction"] == "up":
            self.snake_head["y"] = (self.snake_head["y"] - 1) % self.rows 
        elif self.snake_head["direction"] == "down":
            self.snake_head["y"] = (self.snake_head["y"] + 1) % self.rows
        elif self.snake_head["direction"] == "left":
            self.snake_head["x"] = (self.snake_head["x"] - 1) % self.columns
        elif self.snake_head["direction"] == "right":
            self.snake_head["x"] = (self.snake_head["x"] + 1) % self.columns


        # Placer le serpent dans la grille
        for i in range(len(self.snake)):
            self.grid[self.snake[i]["x"]][self.snake[i]["y"]] = self.snake[i]["img"] # j'ai un doute sur la performence cad la grille va contenir des sprites

        # Placer le food dans la grille
        self.grid[self.food["x"]][self.food["y"]] = self.food["img"]
                


    def drawGrid(self):
        self.screen.fill(BLACK)
        
        for j in range(self.rows):
            for i in range(self.columns):
                # Faire apparaitre la grille
                pygame.draw.rect(self.screen, WHITE, (i*BOX_SIZE, j*BOX_SIZE, BOX_SIZE, BOX_SIZE), 1)
                
                # Dessiner les elements de la grille
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
        if game.handleCollisions():
            print("Perdu")
            pygame.time.wait(2000)
            game.init()

        game.updateGame()
        game.drawGrid()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()