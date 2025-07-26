""" Snake Game Logic Module
    Version: 1.0
    Auteur: Mohamed Kamara
    Date: 2023-10-20
    Description: Un jeu de serpent simple où le serpent grandit en mangeant de la nourriture
    et le jeu se termine si le serpent se mord la queue ou touche les bords de l'écran.
  Le jeu utilise Pygame pour l'affichage et la gestion des événements.
  Les images du serpent et de la nourriture sont chargées depuis des fichiers.
 """


import pygame
import random
import numpy as np
import pickle

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
    def __init__(self, display=True):
        self.display = display
        
        if self.display:
            pygame.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT+HEADING))
            pygame.display.set_caption("Snake Game")

            # Charger tous les images et la music
        self.load_assets()

        self.columns, self.rows = WIDTH // BOX_SIZE, HEIGHT // BOX_SIZE
        self.grid = []
        self.snake = []
        self.snake_head = {}
        #if not self.display:
        self.snake_body_img = self.snake_imgs["body_vertical"]

        self.food = {}
        self.score = 0
        self.high_score = 0
        self.load()
        self.current_score = 0 # peut etre recuperer depuis un fichier
        self.steps_since_last_food = 0

    # -------------------------------------------------------------------------------------------------------
    def save(self, file_name="high_score.pkl"):
        """Sauvegarde le score le plus élevé dans un fichier."""
        if self.score > self.high_score:
            self.high_score = self.score
        with open(file_name, "wb") as f:
            pickle.dump(self.high_score, f)
            print(f"✅ High score sauvegardé dans {file_name}")
    
    # -------------------------------------------------------------------------------------------------------
    def load(self, file_name="high_score.pkl"):
        """Charge le score le plus élevé depuis un fichier."""
        try:
            with open(file_name, "rb") as f:
                self.high_score = pickle.load(f)
                print(f"📦 High score chargé depuis {file_name}")
        except FileNotFoundError:
            print(f"❌ Le fichier {file_name} n'existe pas. Le Fichier va etre créer.")
            self.save(file_name)
    # -------------------------------------------------------------------------------------------------------
    def load_assets(self):
        try:
            # Images de fond
            #self.background = pygame.image.load("images/textureStone.png")
            #self.background = pygame.image.load("images/floor.png")
            #self.background = pygame.image.load("images/alienfloor1_specular.jpg")

            #self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            #self.background = pygame.transform.scale(self.background, (BOX_SIZE, BOX_SIZE))

            # Images pour la nourriture du serpent
            #self.food_img = pygame.image.load("images/apple.png")
            #self.food_img = pygame.transform.scale(self.food_img, (BOX_SIZE, BOX_SIZE))
            self.food_img = YELLOW

            # Images pour le serpent
            # Pour la tete
            """head_up = pygame.image.load("images/head_up.png")
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
            }"""
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
            "direction": "up"
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
                   

    def handleFood(self):
        # Si le serpent mange la nourriture
        if self.snake_head["x"]  == self.food["x"] and self.snake_head["y"] == self.food["y"]:
            self.score += 1
            self.generate_food()
            last_segment = self.snake[len(self.snake)-1]

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
            return True
        return False
        
    def handleDeath(self):
        # FIN DU JEU
        # Si le serpent se touche lui meme 
        for i in range(1,len(self.snake)):
            if self.snake_head["x"] == self.snake[i]["x"] and self.snake_head["y"] == self.snake[i]["y"]:
                return True
            
        # Si le serpent touche le bord
        if not (0 <= self.snake_head["x"] < self.columns):
            return True
        elif not (0 <= self.snake_head["y"] < self.rows):
            return True
        
    def handleCollisions(self):
        # Si le serpent mange la nourriture
        if self.snake_head["x"]  == self.food["x"] and self.snake_head["y"] == self.food["y"]:
            self.score += 1
            self.generate_food()
            last_segment = self.snake[len(self.snake)-1]

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
                return True
            
        # Si le serpent touche le bord
        if (self.snake_head["x"] == 0) or (self.snake_head["x"] == self.columns):
            return True
        elif (self.snake_head["y"] == 0) or (self.snake_head["y"]) == self.rows:
            return True
        
    def updateGame(self):
        if self.score > self.high_score:
            self.high_score = self.score
            
        # Réinitialiser la grille
        self.grid = [[0 for _ in range(self.rows)] for _ in range(self.columns)]

        # Mise à jour des positions des segments du corps
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i]["x"] = self.snake[i - 1]["x"]
            self.snake[i]["y"] = self.snake[i - 1]["y"]

        # Mise a jour de la position et l'image de la tete du serpent
        if self.snake_head["direction"] == "up":
            self.snake_head["y"] -= 1 
            self.snake_head["img"] = self.snake_imgs["head_up"]
        
        elif self.snake_head["direction"] == "down":
            self.snake_head["y"] += 1
            self.snake_head["img"] = self.snake_imgs["head_down"]
       
        elif self.snake_head["direction"] == "left":
            self.snake_head["x"] -= 1
            self.snake_head["img"] = self.snake_imgs["head_left"]
       
        elif self.snake_head["direction"] == "right":
            self.snake_head["x"] += 1
            self.snake_head["img"] = self.snake_imgs["head_right"]
        
        # Mise à jour des images du corps
        # Parcours de tous les segments du serpent, excepté la tête et la queue
        for i in range(1, len(self.snake) - 1):
            prev_segment = self.snake[i - 1]  # Segment précédent
            current_segment = self.snake[i]  # Segment actuel
            next_segment = self.snake[i + 1]  # Segment suivant

            # Calcul des différences de position entre les segments voisins pour déterminer leur orientation
            prev_dx = prev_segment["x"] - current_segment["x"]  # Différence en X entre le segment précédent et actuel
            prev_dy = prev_segment["y"] - current_segment["y"]  # Différence en Y entre le segment précédent et actuel
            next_dx = next_segment["x"] - current_segment["x"]  # Différence en X entre le segment suivant et actuel
            next_dy = next_segment["y"] - current_segment["y"]  # Différence en Y entre le segment suivant et actuel

            # Cas des segments droits : la direction est purement verticale ou horizontale
            if prev_dx == next_dx == 0:  # Si la direction est verticale
                current_segment["img"] = self.snake_imgs["body_vertical"]  # Image du segment vertical
            elif prev_dy == next_dy == 0:  # Si la direction est horizontale
                current_segment["img"] = self.snake_imgs["body_horizontal"]  # Image du segment horizontal

            # Cas des coins en prenant en compte les bords (transition du serpent quand il traverse les bords de l'écran)
            
            # Coin bas-gauche : Le segment tourne vers le bas et vers la gauche
            elif (prev_dx == -1 and next_dy == 1) or (next_dx == -1 and prev_dy == 1):
                # Si le segment est en train de sortir par le bord gauche ou bas,
                # on ajuste l'image pour montrer l'angle approprié
                if current_segment["x"] == 0:  # Si le segment est à gauche de l'écran
                    current_segment["img"] = self.snake_imgs["body_bottomleft"]  # Coin bas-gauche
                elif current_segment["y"] == HEIGHT - 1:  # Si le segment est en bas de l'écran
                    current_segment["img"] = self.snake_imgs["body_bottomleft"]  # Coin bas-gauche
                else:
                    current_segment["img"] = self.snake_imgs["body_bottomleft"] 

            # Coin bas-droit : Le segment tourne vers le bas et vers la droite
            elif (prev_dx == 1 and next_dy == 1) or (next_dx == 1 and prev_dy == 1):
                # Si le segment est en train de sortir par le bord droit ou bas,
                # on ajuste l'image pour montrer l'angle approprié
                if current_segment["x"] == WIDTH - 1:  # Si le segment est à droite de l'écran
                    current_segment["img"] = self.snake_imgs["body_bottomright"]  # Coin bas-droit
                elif current_segment["y"] == HEIGHT - 1:  # Si le segment est en bas de l'écran
                    current_segment["img"] = self.snake_imgs["body_bottomright"]  # Coin bas-droit
                else:
                    current_segment["img"] = self.snake_imgs["body_bottomright"]

            # Coin haut-gauche : Le segment tourne vers le haut et vers la gauche
            elif (prev_dx == -1 and next_dy == -1) or (next_dx == -1 and prev_dy == -1):
                # Si le segment est en train de sortir par le bord gauche ou haut,
                # on ajuste l'image pour montrer l'angle approprié
                if current_segment["x"] == 0:  # Si le segment est à gauche de l'écran
                    current_segment["img"] = self.snake_imgs["body_topleft"]  # Coin haut-gauche
                elif current_segment["y"] == 0:  # Si le segment est en haut de l'écran
                    current_segment["img"] = self.snake_imgs["body_topleft"]  # Coin haut-gauche
                else:
                    current_segment["img"] = self.snake_imgs["body_topleft"]

            # Coin haut-droit : Le segment tourne vers le haut et vers la droite
            elif (prev_dx == 1 and next_dy == -1) or (next_dx == 1 and prev_dy == -1):
                # Si le segment est en train de sortir par le bord droit ou haut,
                # on ajuste l'image pour montrer l'angle approprié
                if current_segment["x"] == WIDTH - 1:  # Si le segment est à droite de l'écran
                    current_segment["img"] = self.snake_imgs["body_topright"]  # Coin haut-droit
                elif current_segment["y"] == 0:  # Si le segment est en haut de l'écran
                    current_segment["img"] = self.snake_imgs["body_topright"]  # Coin haut-droit
                else:
                    current_segment["img"] = self.snake_imgs["body_topright"]  # Coin haut-droit

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
        #self.screen.blit(self.background, (0,HEADING))

        # Difinition de la police et Affichage du score et du high_score
        font = pygame.font.SysFont("monospace", 40)  # Choisir une police et une taille
        score_text = font.render(f"Score : {self.score}", True, WHITE)
        high_score_text = font.render(f"High Score : {self.high_score}", True, WHITE)
        self.screen.blit(high_score_text, (WIDTH-(high_score_text.get_width() + 20), 20))
        self.screen.blit(score_text, (20,20))
        
        
        for j in range(self.rows+1):
            for i in range(self.columns):
                 # Faire apparaitre la grille
                #self.screen.blit(self.background, (i*BOX_SIZE, j* BOX_SIZE + HEADING))
                pygame.draw.rect(self.screen, WHITE, (0, HEADING, WIDTH, HEIGHT), 1)
                

        # Dessiner le food (nourriture)
        #self.screen.blit(self.food_img, (self.food["x"]*BOX_SIZE, self.food["y"]*BOX_SIZE + HEADING))
        pygame.draw.rect(self.screen, self.food_img, (self.food["x"]*BOX_SIZE, self.food["y"]*BOX_SIZE + HEADING, BOX_SIZE, BOX_SIZE))

        # Dessiner le serpent
        for segment in self.snake:
            #self.screen.blit(segment["img"], (segment["x"]*BOX_SIZE, segment["y"]*BOX_SIZE + HEADING))
            pygame.draw.rect(self.screen, segment["img"], (segment["x"]*BOX_SIZE, segment["y"]*BOX_SIZE + HEADING, BOX_SIZE, BOX_SIZE))

        #self.draw_vision(self.screen)
        self.draw_local_grid(self.screen)
        pygame.display.update()

    def display_game_over(self):
        
        # Afficher un rectangle rouge avec "GAME OVER" en rouge
        font = pygame.font.SysFont("Arial", 60)
        game_over_text = font.render("GAME OVER", True, RED)
        rect = game_over_text.get_rect(center=(WIDTH // 2, (HEIGHT + HEADING) // 2))
        
        # Dessiner le fond rouge
        pygame.draw.rect(self.screen, BLUE, rect.inflate(50, 50))
        
        # Afficher le texte en rouge
        self.screen.blit(game_over_text, rect)
        #self.screen.blit(game_over_text, (WIDTH//2, (HEIGHT+HEADING)//2))
        
        self.save()  # Sauvegarder le score le plus élevé

        pygame.display.update()

    """
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
    """

#--------------------------------------------------------------------------------------------------------------------------
# Pour l'agent IA
#--------------------------------------------------------------------------------------------------------------------------
    def get_distance_to_food(self):
        dx = self.food["x"] - self.snake_head["x"]
        dy = self.food["y"] - self.snake_head["y"]
        return np.sqrt(dx**2 + dy**2)
#--------------------------------------------------------------------------------------------------------------------------
    
    def step(self, action):
        reward = 0
        #pos_actuel = (self.snake_head["x"], self.snake_head["y"])
        done = False
        old_distance = self.get_distance_to_food()
        self.steps_since_last_food += 1
        
       

       # === Convertir l'action en direction ===   
        if action == 0 and self.snake[0]["direction"] != "down": # 0 = up
            self.snake[0]["direction"] = "up"
        if action == 1 and self.snake[0]["direction"] != "up": # 1 = down
            self.snake[0]["direction"] = "down"
        if action == 2 and self.snake[0]["direction"] != "left": # 2 = right
            self.snake[0]["direction"] = "right"
        if action == 3 and self.snake[0]["direction"] != "right":  # 3 = left
            self.snake[0]["direction"] = "left" 
    
        # === Mettre à jour la position du serpent ===
        self.updateGame()


        # === Récompense ===
        if self.handleDeath():
            reward = -20 # mort = mauvais
            done  = True
        elif self.handleFood():
            reward = +15 # manger = bon
            self.steps_since_last_food = 0 # Réinitialiser le compteur de pas depuis la dernière nourriture
            done = False
        elif self.steps_since_last_food > 50:  # Si le serpent n'a pas mangé depuis longtemps
            reward -= 1.0 # pénalité pour ne pas manger
            done = False
        else:
            reward = 0 # rien de special*

        new_distance = self.get_distance_to_food()

        # === Récompense basée sur la distance à la nourriture ===
        # Ne pas appliquer de pénalité si le serpent est déja mort ou a mangé
        if done or self.handleFood():
            return (reward, done, self.score)
        
        if new_distance < old_distance:
            reward += 0.5  # bonus pour rapprochement
        else:
            reward -= 0.2  # pénalité pour éloignement

        #pos_suivant = (self.snake_head["x"], self.snake_head["y"]) # celle obtenue en faisant l'action

        return (reward, done, self.score)
    #--------------------------------------------------------------------------------------------------------------------------
    def is_collision_at(self, x, y):
        # mur
        if x < 0 or x >= self.columns or y < 0 or y >= self.rows:
            return True
        # serpent
        for segment in self.snake[1:]:
            if segment["x"] == x and segment["y"] == y:
                return True
        return False
    #--------------------------------------------------------------------------------------------------------------------------
    def is_danger_straight(self):
        head = self.snake_head
        x, y = head["x"], head["y"]
        direction = head["direction"]

        if direction == "up":
            y -= 1
        elif direction == "down":
            y += 1
        elif direction == "left":
            x -= 1
        elif direction == "right":
            x += 1

        return self.is_collision_at(x, y)

    #--------------------------------------------------------------------------------------------------------------------------
    def is_danger_right(self):
        head = self.snake_head
        x, y = head["x"], head["y"]
        direction = head["direction"]

        if direction == "up":
            x += 1
        elif direction == "down":
            x -= 1
        elif direction == "left":
            y -= 1
        elif direction == "right":
            y += 1 

        return self.is_collision_at(x, y)
# -----------------------------------------------------------------------------------------------------------------------------
    def is_danger_left(self):
        head = self.snake_head
        x, y = head["x"], head["y"]
        direction = head["direction"]

        if direction == "up":
            x -= 1
        elif direction == "down":
            x += 1
        elif direction == "left":
            y += 1
        elif direction == "right":
            y -= 1 

        return self.is_collision_at(x, y)
    #--------------------------------------------------------------------------------------------------------------------------
    def get_state_old(self):
        # === Direction du serpent ===
        dir_up = self.snake_head["direction"] == "up"
        dir_down = self.snake_head["direction"] == "down"
        dir_left = self.snake_head["direction"] == "left"
        dir_right = self.snake_head["direction"] == "right"

        # === Position relative du food ===
        food_right = self.food["x"] > self.snake_head["x"]
        food_left = self.food["x"] < self.snake_head["x"]
        food_up = self.food["y"] < self.snake_head["y"]
        food_down = self.food["y"] > self.snake_head["y"]

        # === Danger ===
        danger_straight = self.is_danger_straight()
        danger_right = self.is_danger_right()
        danger_left = self.is_danger_left()

        # === Coordonnées normalisées food vs head ===
        dx = (self.food["x"] - self.snake_head["x"]) / WIDTH
        dy = (self.food["y"] - self.snake_head["y"]) / HEIGHT

        # === Distances aux murs (normalisées) ===
        dist_left = self.snake_head["x"] / WIDTH
        dist_right = (WIDTH - self.snake_head["x"]) / WIDTH
        dist_up = self.snake_head["y"] / HEIGHT
        dist_down = (HEIGHT - self.snake_head["y"]) / HEIGHT

        # === Taille du serpent (normalisée à une valeur raisonnable) ===
        snake_length = len(self.snake) / (WIDTH * HEIGHT / 10)

        state = [
            int(dir_up), int(dir_down), int(dir_left), int(dir_right),
            int(food_right), int(food_left), int(food_up), int(food_down),
            int(danger_straight), int(danger_right), int(danger_left),
            dx, dy,
            dist_left, dist_right, dist_up, dist_down,
            snake_length
        ]

        return np.array(state, dtype=np.float32)

#--------------------------------------------------------------------------------------------------------------------------
  
    def get_state(self):
        head_x = self.snake_head["x"]
        head_y = self.snake_head["y"]

        # === 1. Direction actuelle (one-hot) ===
        direction = self.snake_head["direction"]
        dir_onehot = [
            int(direction == "up"),
            int(direction == "down"),
            int(direction == "left"),
            int(direction == "right"),
        ]

        # === 2. Champ de vision directionnel ===
        # Directions (8 sens)
        directions = [
            (0, -1),  # ↑
            (1, -1),  # ↗
            (1, 0),   # →
            (1, 1),   # ↘
            (0, 1),   # ↓
            (-1, 1),  # ↙
            (-1, 0),  # ←
            (-1, -1), # ↖
        ]

        vision = []

        for dx, dy in directions:
            food_seen = 0
            danger_seen = 0
            inv_dist = 0

            step = 1
            while True:
                check_x = head_x + dx * step
                check_y = head_y + dy * step

                # Hors grille → mur
                if not (0 <= check_x < self.columns and 0 <= check_y < self.rows):
                    danger_seen = 1
                    break

                # Serpent ? → danger
                if any(seg["x"] == check_x and seg["y"] == check_y for seg in self.snake[1:]):
                    danger_seen = 1
                    break

                # Nourriture ?
                if self.food["x"] == check_x and self.food["y"] == check_y:
                    food_seen = 1
                    inv_dist = 1 / step
                    break

                step += 1
                if step > max(self.columns, self.rows):  # Sécurité
                    break

            vision.extend([food_seen, danger_seen, inv_dist])

        # === 3. Grille locale autour de la tête (5x5) ===
        local_grid = []
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                cell_x = head_x + dx
                cell_y = head_y + dy

                # Hors grille = mur (valeur neutre ici → 0)
                if not (0 <= cell_x < self.columns and 0 <= cell_y < self.rows):
                    local_grid.append(1)  # ou -1 si tu veux distinguer
                    continue

                if self.food["x"] == cell_x and self.food["y"] == cell_y:
                    local_grid.append(2)
                elif any(seg["x"] == cell_x and seg["y"] == cell_y for seg in self.snake):
                    local_grid.append(1)
                else:
                    local_grid.append(0)

        # === Final state vector ===
        state = vision + local_grid + dir_onehot
        return np.array(state, dtype=np.float32)

#--------------------------------------------------------------------------------------------------------------------------
    
    def relative_to_absolute_direction(self, current_direction, action):
        directions = ['up', 'right', 'down', 'left']
        idx = directions.index(current_direction)

        if action[1]:  # tout droit
            new_direction = directions[idx]
        elif action[0]:  # à gauche
            new_direction = directions[(idx - 1) % 4]
        elif action[2]:  # à droite
            new_direction = directions[(idx + 1) % 4]

        mapping = {'up': 0, 'down': 1, 'left': 2, 'right': 3}
        return mapping[new_direction]

    #--------------------------------------------------------------------------------------------------------------------------

    def draw_vision(self, surface):
        head_x = self.snake_head["x"]
        head_y = self.snake_head["y"]
        head_px = head_x * BOX_SIZE + BOX_SIZE // 2
        head_py = head_y * BOX_SIZE + HEADING + BOX_SIZE // 2

        directions = [
            (0, -1),   # ↑
            (1, -1),   # ↗
            (1, 0),    # →
            (1, 1),    # ↘
            (0, 1),    # ↓
            (-1, 1),   # ↙
            (-1, 0),   # ←
            (-1, -1),  # ↖
        ]

        for dx, dy in directions:
            step = 1
            while True:
                cx = head_x + dx * step
                cy = head_y + dy * step

                # Sortie de la grille
                if not (0 <= cx < self.columns and 0 <= cy < self.rows):
                    break

                px = cx * BOX_SIZE + BOX_SIZE // 2
                py = cy * BOX_SIZE + HEADING + BOX_SIZE // 2

                is_body = any(seg["x"] == cx and seg["y"] == cy for seg in self.snake[1:])
                is_food = (self.food["x"] == cx and self.food["y"] == cy)

                # Couleurs différentes selon la nature de l'objet vu
                if is_food:
                    color = YELLOW # Vert pour food
                elif is_body:
                    color = GREEN  # Rouge pour corps
                else:
                    color = (150, 150, 150)  # Gris clair pour vide

                # Dessine une ligne de la tête jusqu'à cette case
                pygame.draw.line(surface, color, (head_px, head_py), (px, py), 2)

                if is_body or is_food:
                    break

                step += 1
                
    #--------------------------------------------------------------------------------------------------------------------------
                
    def draw_local_grid(self, surface, grid_size=5):
        """Dessine une grille locale centrée sur la tête du serpent."""
        head_x = self.snake_head["x"]
        head_y = self.snake_head["y"]
        offset = grid_size // 2

        for dy in range(-offset, offset + 1):
            for dx in range(-offset, offset + 1):
                cx = head_x + dx
                cy = head_y + dy

                if not (0 <= cx < self.columns and 0 <= cy < self.rows):
                    continue  # Hors de la grille

                # Coordonnées en pixels
                px = cx * BOX_SIZE
                py = cy * BOX_SIZE + HEADING

                rect = pygame.Rect(px, py, BOX_SIZE, BOX_SIZE)

                if cx == self.food["x"] and cy == self.food["y"]:
                    color = (0, 255, 0)  # Pomme : vert
                elif any(seg["x"] == cx and seg["y"] == cy for seg in self.snake):
                    color = (255, 0, 0)  # Corps du serpent : rouge
                elif cx == head_x and cy == head_y:
                    color = (255, 255, 0)  # Tête du serpent : jaune
                else:
                    color = (50, 50, 50)  # Zone vide : gris foncé

                pygame.draw.rect(surface, color, rect, 2)

# ------------------------------------------------------------------------------------------------------------------------------
    def draw_path(self, path, color=(255, 0, 255)):
        """
        Dessine le chemin donné sur la grille du jeu.
        
        Paramètres :
        - game : instance de SnakeGame
        - path : liste de directions (ex: ["up", "right", "right", ...])
        - color : couleur du tracé (par défaut violet)
        """
        if not path:
            return  # aucun chemin à dessiner

        cell_size = BOX_SIZE
        x, y = self.snake_head["x"], self.snake_head["y"]
        DIRS = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }

        for direction in path:
            dx, dy = DIRS[direction]
            x += dx
            y += dy

            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(self.screen, color, rect, width=2)

#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------


def main():
    
    game = SnakeGame()
    game.init()

    fps = 6.5
    clock = pygame.time.Clock()

    run = True
    while run:
        
        run = game.handleDeath()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        if run:
            game.display_game_over()
            pygame.time.wait(2000)
            game.init()
            continue

        game.updateGame()
        game.drawGrid()
        clock.tick(fps)

    pygame.quit()

# ----------------------------------------------------------------------------------------------------------------------------
# === Etape Teste ===
# ----------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    import time
    import random
    import numpy as np

    # Imaginons que tu as un objet game du type GameSnake
    game = SnakeGame()  # Adapter à ton nom exact
    game.init()

    fps = 6.5
    clock = pygame.time.Clock()

    # Boucle principale pour test
    while True:
        state = game.get_state()  # état du jeu
        action = random.randint(0, 2)  # 0 = gauche, 1 = tout droit, 2 = droite
        pos_actuel, reward, done, pos_suivant = game.step(action)

        print(f"État : {state}")
        print(f"Action choisie : {action}")
        print(f"Reward : {reward}")
        print(f"Position : {pos_actuel} → {pos_suivant}")
        print("-------------")

        time.sleep(0.2)  # pour ralentir un peu l'affichage

        if done:
            print("💀 Game Over")
            break

        game.updateGame()
        game.drawGrid()
        clock.tick(fps)






    