""" 
    A FAIRE:
        - rajouter les sprites
        - Sauvegarder le high_score dans un fichier text ou crypter a la fin du jeu jeu et a chaque perte
          et recuper au demarrage du jeu
        - rajouter de la music, les effets
Optimisation de la grille :

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
RED = (255, 0, 0)
BLUE = (0, 0, 222)


HEADING = 100
WIDTH = 900
HEIGHT = 800
BOX_SIZE = 30

class SnakeGame():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT+HEADING))
        pygame.display.set_caption("Snake Game")

        # Charger tous les images et la music
        self.load_assets()

        self.columns, self.rows = WIDTH // BOX_SIZE, HEIGHT // BOX_SIZE
        self.grid = []
        self.snake = []
        self.snake_head = {}
        self.snake_body_img = self.snake_imgs["body_vertical"]

        self.food = {}
        self.score = 0
        self.high_score = 0
        self.current_score = 0 # peut etre recuperer depuis un fichier


    def load_assets(self):
        try:
            # Images pour la nourriture du serpent
            self.food_img = pygame.image.load("images/apple.png")
            self.food_img = pygame.transform.scale(self.food_img, (BOX_SIZE, BOX_SIZE))

            # Images pour le serpent
            # Pour la tete
            head_up = pygame.image.load("images/head_up.png")
            head_up = pygame.transform.scale(head_up, (BOX_SIZE, BOX_SIZE))

            head_down = pygame.image.load("images/head_down.png")
            head_down = pygame.transform.scale(head_down, (BOX_SIZE, BOX_SIZE))

            head_left = pygame.image.load("images/head_left.png")
            head_left = pygame.transform.scale(head_left, (BOX_SIZE, BOX_SIZE))

            head_right = pygame.image.load("images/head_right.png")
            head_right = pygame.transform.scale(head_right, (BOX_SIZE, BOX_SIZE))

            # Pour le corps
            body_bottomleft = pygame.image.load("images/body_bottomleft.png")
            body_bottomleft = pygame.transform.scale(body_bottomleft, (BOX_SIZE, BOX_SIZE))

            body_bottomright = pygame.image.load("images/body_bottomright.png")
            body_bottomright = pygame.transform.scale(body_bottomright, (BOX_SIZE, BOX_SIZE))

            body_horizontal = pygame.image.load("images/body_horizontal.png")
            body_horizontal = pygame.transform.scale(body_horizontal, (BOX_SIZE, BOX_SIZE))

            body_vertical = pygame.image.load("images/body_vertical.png")
            body_vertical = pygame.transform.scale(body_vertical, (BOX_SIZE, BOX_SIZE))

            body_topleft = pygame.image.load("images/body_topleft.png")
            body_topleft = pygame.transform.scale(body_topleft, (BOX_SIZE, BOX_SIZE))

            body_topright = pygame.image.load("images/body_topright.png")
            body_topright = pygame.transform.scale(body_topright, (BOX_SIZE, BOX_SIZE))

            # Pour la queue
            tail_up = pygame.image.load("images/tail_up.png")
            tail_up = pygame.transform.scale(tail_up, (BOX_SIZE, BOX_SIZE))

            tail_down = pygame.image.load("images/tail_down.png")
            tail_down = pygame.transform.scale(tail_down, (BOX_SIZE, BOX_SIZE))

            tail_left = pygame.image.load("images/tail_left.png")
            tail_left = pygame.transform.scale(tail_left, (BOX_SIZE, BOX_SIZE))

            tail_right = pygame.image.load("images/tail_right.png")
            tail_right = pygame.transform.scale(tail_right, (BOX_SIZE, BOX_SIZE))

            self.snake_imgs = {
                "head_up": head_up,
                "head_down": head_down,
                "head_left": head_left,
                "head_right": head_right,
                "body_bottomleft": body_bottomleft,
                "body_bottomright": body_bottomright,
                "body_horizontal": body_horizontal,
                "body_vertical": body_vertical,
                "body_topleft": body_topleft,
                "body_topright": body_topright,
                "tail_up": tail_up,
                "tail_down": tail_down,
                "tail_left": tail_left,
                "tail_right": tail_right    
            }

            
        except pygame.error as e:
            print(e)
            self.snake_imgs = {
                "head_up": RED,
                "head_down": RED,
                "head_left": RED,
                "head_right": RED,
                "body_bottomleft": GREEN,
                "body_bottomright": GREEN,
                "body_horizontal": GREEN,
                "body_vertical": GREEN,
                "body_topleft": GREEN,
                "body_topright": GREEN,
                "tail_up": BLUE,
                "tail_down": BLUE,
                "tail_left": BLUE,
                "tail_right": BLUE    
            }
        
    def init(self):
        # Initialisation de la grille
        self.grid = [[0 for _ in range(self.rows)] for _ in range(self.columns)]
        
        # Initialisation de la tete du serpent au centre de l'ecran 
        self.snake = []
        self.snake_head = {
            "x": self.columns // 2,
            "y": self.rows // 2,
            "img": self.snake_imgs["head_up"],
            "direction": "none"
        }
        # L'ajouter au snake
        self.snake.append(self.snake_head)

        # Initialisation du score
        self.score = 0

        # Initialisation de la position du food
        self.generate_food()

    def generate_food(self):
        ok = False
        while not ok:
            x = random.randint(0, self.columns - 1)
            y = random.randint(0, self.rows - 1)
            ok = True # On suppose d'abord que (x, y) est valide

            for segment in self.snake:
                if segment["x"] == x and segment["y"] == y:
                     ok = False # Si une collision est détectée, (x, y) n'est pas valide
                     break # Pas besoin de continuer à vérifier les autres segments
                
            # Si ok reste False après la boucle, cela signifie que (x, y) est libre
            self.food = {
                "x": x,
                "y": y,
                "img": self.food_img
            } 
                   

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
            last_segment = self.snake[len(self.snake)-1]

            print(self.snake)
            if last_segment["direction"] == "up":
                img = self.snake_imgs["tail_up"]
            elif last_segment["direction"] == "down":
                img = self.snake_imgs["tail_down"]
            elif last_segment["direction"] == "left":
                img = self.snake_imgs["tail_left"]
            elif last_segment["direction"] == "right":
                img = self.snake_imgs["tail_right"]

            new_segment = {
                "x": last_segment["x"],
                "y": last_segment["y"],
                "img" : img,
                "direction": last_segment["direction"]
            }
            self.snake.append(new_segment)
            return False

        # FIN DU JEU
        # Si le serpent se touche lui meme 
        for i in range(1,len(self.snake)):
            if self.snake_head["x"] == self.snake[i]["x"] and self.snake_head["y"] == self.snake[i]["y"]:
                self.high_score = self.score
                return True
            
        
    def updateGame(self):
        # Réinitialiser la grille
        self.grid = [[0 for _ in range(self.rows)] for _ in range(self.columns)]

        # Mise à jour des positions des segments du corps
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i]["x"] = self.snake[i - 1]["x"]
            self.snake[i]["y"] = self.snake[i - 1]["y"]

        # Mise a jour de la position et l'image de la tete du serpent
        if self.snake_head["direction"] == "up":
            self.snake_head["y"] = (self.snake_head["y"] - 1) % self.rows 
            self.snake_head["img"] = self.snake_imgs["head_up"]
        elif self.snake_head["direction"] == "down":
            self.snake_head["y"] = (self.snake_head["y"] + 1) % self.rows
            self.snake_head["img"] = self.snake_imgs["head_down"]
        elif self.snake_head["direction"] == "left":
            self.snake_head["x"] = (self.snake_head["x"] - 1) % self.columns
            self.snake_head["img"] = self.snake_imgs["head_left"]
        elif self.snake_head["direction"] == "right":
            self.snake_head["x"] = (self.snake_head["x"] + 1) % self.columns
            self.snake_head["img"] = self.snake_imgs["head_right"]
        
        # Mise à jour des images du corps
        for i in range(1, len(self.snake) - 1):
            prev_segment = self.snake[i - 1]
            current_segment = self.snake[i]
            next_segment = self.snake[i + 1]

            # Déterminer la direction entre les segments précédents et suivants
            prev_dx = prev_segment["x"] - current_segment["x"]
            prev_dy = prev_segment["y"] - current_segment["y"]
            next_dx = next_segment["x"] - current_segment["x"]
            next_dy = next_segment["y"] - current_segment["y"]

            # Cas des segments droits
            if prev_dx == next_dx == 0:
                current_segment["img"] = self.snake_imgs["body_vertical"]
            elif prev_dy == next_dy == 0:
                current_segment["img"] = self.snake_imgs["body_horizontal"]

            # Cas des coins
            elif (prev_dx == -1 and next_dy == 1) or (next_dx == -1 and prev_dy == 1):
                current_segment["img"] = self.snake_imgs["body_bottomleft"]
            elif (prev_dx == 1 and next_dy == 1) or (next_dx == 1 and prev_dy == 1):
                current_segment["img"] = self.snake_imgs["body_bottomright"]
            elif (prev_dx == -1 and next_dy == -1) or (next_dx == -1 and prev_dy == -1):
                current_segment["img"] = self.snake_imgs["body_topleft"]
            elif (prev_dx == 1 and next_dy == -1) or (next_dx == 1 and prev_dy == -1):
                current_segment["img"] = self.snake_imgs["body_topright"]

        # Mise à jour de l'image de la queue
        if len(self.snake) > 1:
            tail = self.snake[-1]
            prev_segment = self.snake[-2]

            if prev_segment["x"] < tail["x"]:  # Queue dirigée vers la droite
                tail["img"] = self.snake_imgs["tail_right"]
            elif prev_segment["x"] > tail["x"]:  # Queue dirigée vers la gauche
                tail["img"] = self.snake_imgs["tail_left"]
            elif prev_segment["y"] < tail["y"]:  # Queue dirigée vers le bas
                tail["img"] = self.snake_imgs["tail_up"]
            elif prev_segment["y"] > tail["y"]:  # Queue dirigée vers le haut
                tail["img"] = self.snake_imgs["tail_down"]





        # Placer le serpent dans la grille
        for i in range(len(self.snake)):
            self.grid[self.snake[i]["x"]][self.snake[i]["y"]] = self.snake[i]["img"] # j'ai un doute sur la performence cad la grille va contenir des sprites

        # Placer le food dans la grille
        self.grid[self.food["x"]][self.food["y"]] = self.food["img"]
                


    def drawGrid(self):
        # Effacer l'ecran
        self.screen.fill(BLACK)

        # Difinition de la police et Affichage du score et du high_score
        font = pygame.font.SysFont("monospace", 40)  # Choisir une police et une taille
        score_text = font.render(f"Score : {self.score}", True, WHITE)
        high_score_text = font.render(f"High Score : {self.high_score}", True, WHITE)
        self.screen.blit(high_score_text, (WIDTH-(high_score_text.get_width() + 20), 20))
        self.screen.blit(score_text, (20,20))
        
        for j in range(self.rows):
            for i in range(self.columns):
                # Faire apparaitre la grille
                pygame.draw.rect(self.screen, WHITE, (0, HEADING, WIDTH, HEIGHT), 1)

                # Dessiner le serpent
                for segment in self.snake:
                    self.screen.blit(segment["img"], (segment["x"]*BOX_SIZE, segment["y"]*BOX_SIZE + HEADING))
               
                # Dessiner le food (nourriture)
                if self.grid[i][j] == self.food_img:
                    self.screen.blit(self.food_img, (i*BOX_SIZE, j*BOX_SIZE + HEADING))
                    #pygame.draw.rect(self.screen, self.food_img, (i*BOX_SIZE, j*BOX_SIZE + HEADING, BOX_SIZE, BOX_SIZE))

                
                   

        pygame.display.update()



def main():
    
    game = SnakeGame()
    game.init()

    fps = 6.5
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