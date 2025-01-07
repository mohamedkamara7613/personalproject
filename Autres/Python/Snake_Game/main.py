import pygame

WIDTH = 600
HEIGHT = 600

class SnakeGame():
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")

        self.snake = []
        self.snake_head = {}
        self.score = 0
        self.current_score = 0 # peut etre recuperer depuis un fichier
        
    def init(self):
        print("OK")

    def handleEvenement(self):
        pass

    def updateGame(self):
        pass

    def handleCollisions(self):
        pass

    def generate_food(self):
        pass




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
        pygame.display.update()
        
    pygame.quit()


if __name__ == "__main__":
    main()