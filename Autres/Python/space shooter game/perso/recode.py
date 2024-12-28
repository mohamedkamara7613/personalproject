# Importation
import os
import pygame
pygame.init()

#---------------------------------------------------------------------------------------------

WIDTH, HEIGHT = 750, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game")

# Color
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 255, 0)

# Load Image
# Load and adaptation of Background
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png"))

# Ship
RED_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_yellow.png"))


#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
class Ship:
	def __init__(self, x, y, health=100):
		self.x = x
		self.y = y
		self.health = health
		self.Ship_img = None
		self.laser_img = None
		self.lasers = []
		self.cool_down_counter = 0

	def draw(self, window):
		pygame.draw.rect(window, GREEN_COLOR, (self.x, self.y, 30, 30))

#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------


def main():
	run = True
	clock = pygame.time.Clock()
	FPS = 60
	level = 0
	lives = 5
	main_font = pygame.font.SysFont("comicsans", 50)

	ship = Ship(450, 600)

	# Subfunction----------------------------------
	def redraw_window():
		WIN.blit(BG, (0, 0))

		#Show label
		level_label = main_font.render(f"Level : {level}", 1, WHITE_COLOR)
		lives_label = main_font.render(f"Lives : {lives}", 1, WHITE_COLOR)
		WIN.blit(level_label, (WIDTH - level_label.get_width(), 10))
		WIN.blit(lives_label, (10, 10))

		ship.draw(WIN)

		pygame.display.update()

	while run:
		clock.tick(FPS)
		#---------------------------------------------------------------------------------------------
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		#---------------------------------------------------------------------------------------------
		# Gestion de l'affichage en general
		redraw_window()
	

	pygame.quit()


if __name__ == "__main__":
	main()