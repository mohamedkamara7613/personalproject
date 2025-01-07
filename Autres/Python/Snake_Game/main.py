import pygame

WIDTH = 600
HEIGHT = 600

class SnakeGame():
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen = pygame.display.get_surface()
        



def main():
    
    game = SnakeGame()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        
        pygame.display.update()
        
    pygame.quit()


if __name__ == "__main__":
    main()