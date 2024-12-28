
# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------

# Module Importation
import pygame 
import os
import time
import random
pygame.font.init()

# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------

# Window's dimensions definition
WIDTH, HEIGHT = 750, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# -----------------------------------------------------------------------------------------------------------

# Load Image
# Enemy ship
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# -----------------------------------------------------------------------------------------------------------
# Definition of some class
# -----------------------------------------------------------------------------------------------------------
class Laser:

	def __init__(self, x, y, img):
		self.x = x 
		self.y = y 
		self.img = img 
		# For manage collision
		self.mask = pygame.mask.from_surface(self.img)
	# -----------------------------------------------------------------------------------------------------------

	def draw(self, window):
		window.blit(self.img, (self.x, self.y))
	# -----------------------------------------------------------------------------------------------------------

	def move(self, vel):
		self.y +=  vel # vel can be negative (for go backward)
	# -----------------------------------------------------------------------------------------------------------

	def off_screen(self, heigth):
		"""
			Said if the laser out of screen to remove it or another thing 
		"""
		return not(self.y <= heigth and  self.y  >= 0)
	# -----------------------------------------------------------------------------------------------------------

	def collision(self, obj):
		"""
			Said if laser collide with obj
		"""
		return collide(self, obj)

# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------

class Ship:
	"""
		A support from which will be created enemies and player
	"""
	# -----------------------------------------------------------------------------------------------------------
	COOLDOWN = 30 # the time that the player must wait before shooting again
	# -----------------------------------------------------------------------------------------------------------
	
	def __init__(self, x, y, health=100):
		self.x = x
		self.y = y
		self.health = health
		# all both will be personnalized after
		self.ship_img = None 
		self.laser_img = None
		self.lasers = [] # The list of lasers that the player has
		self.cool_down_counter = 0
	# -----------------------------------------------------------------------------------------------------------

	def draw(self, window):
		window.blit(self.ship_img, (self.x, self.y))
		for laser in self.lasers:
			laser.draw(window)
		#pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50)) # mettre en variable le width et height
	# -----------------------------------------------------------------------------------------------------------

	def move_lasers(self, vel, obj):
		"""
		obj is passed in parameter to specify the target
		"""
		self.cooldown()
		for laser in self.lasers:
			laser.move(vel)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			elif laser.collision(obj):
				obj.health -= 10
				self.lasers.remove(laser)
	# -----------------------------------------------------------------------------------------------------------

	def cooldown(self):
		if self.cool_down_counter >= self.COOLDOWN:
			self.cool_down_counter = 0
		elif self.cool_down_counter > 0:
			self.cool_down_counter += 1

	# -----------------------------------------------------------------------------------------------------------

	def shoot(self):
		"""
			this method create the lasers the player can use
		"""
		if self.cool_down_counter == 0: # We can create a laser only if COOLDOWN is passed here 30 seconds
			laser = Laser(self.x, self.y, self.laser_img)
			self.lasers.append(laser)
			"""
			 A short description of the variable "self.cool_down_counter " :
			 		more "self.cool_down_counter" is near to 30 more the player can shoot many laser then create laser
			 		plus cette variable est proche de 30 plus il y aura des laser disponible car "self.cool_down_counter" atteindra 30 plus rapidement est elle sera reinitialiser à 0 dans la mathode cooldown qui va permettre à la methode shoot() d'ajouter un laser a la liste des lasers
			"""
			self.cool_down_counter = 5

	# -----------------------------------------------------------------------------------------------------------

	def get_width(self):
		return self.ship_img.get_width()
	# -----------------------------------------------------------------------------------------------------------

	def get_height(self):
		return self.ship_img.get_height()

# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------

class Enemy(Ship):
	COLOR_MAP = {
				"red" : (RED_SPACE_SHIP, RED_LASER),
				"green": (GREEN_SPACE_SHIP, GREEN_LASER),
				"blue" : (BLUE_SPACE_SHIP, BLUE_LASER)
	}
	# -----------------------------------------------------------------------------------------------------------

	def __init__(self, x, y, color, health=100):
		super().__init__(x, y, health)
		self.ship_img, self.laser_img  = self.COLOR_MAP[color]
		self.mask = pygame.mask.from_surface(self.ship_img) # Pour gerer les collisions
	# -----------------------------------------------------------------------------------------------------------

	def shoot(self):
		if self.cool_down_counter == 0:
			laser = Laser(self.x-20, self.y, self.laser_img)
			self.lasers.append(laser)
			self.cool_down_counter = 1
	# -----------------------------------------------------------------------------------------------------------

	def move(self, vel):
		self.y += vel

# -----------------------------------------------------------------------------------------------------------

class Player(Ship):
	def __init__(self, x, y, health=100):
		super().__init__(x, y, health)
		self.ship_img = YELLOW_SPACE_SHIP
		self.laser_img = YELLOW_LASER
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.max_health = health
	
	# -----------------------------------------------------------------------------------------------------------
	def draw(self, window):
		super().draw(window)
		self.healthbar(window)

	# -----------------------------------------------------------------------------------------------------------
	def move_lasers(self, vel, objs):
		self.cooldown()
		for laser in self.lasers:
			laser.move(vel)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			else:
				for obj in objs:
					if laser.collision(obj):
						objs.remove(obj)
						if laser in self.lasers:
							self.lasers.remove(laser)

	# -----------------------------------------------------------------------------------------------------------
	def healthbar(self, window):
		pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10)) 
		pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10)) 

# -----------------------------------------------------------------------------------------------------------
# Simple Function
# -----------------------------------------------------------------------------------------------------------

def collide(obj1, obj2):
	# Managing collision with mask
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# -----------------------------------------------------------------------------------------------------------

def main():
	run = True
	lost = False
	lost_count = 0
	FPS = 60
	level = 1
	lives = 5
	main_font = pygame.font.SysFont("comicsans", 50)
	lost_font = pygame.font.SysFont("comicsans", 60)
	player_vel = 5
	enemy_vel = 1
	laser_vel = 6  

	enemies = []
	wave_lenght = 5
	player = Player(300, 570)

	clock = pygame.time.Clock()
	# -----------------------------------------------------------------------------------------------------------

	def redraw_window():
		WIN.blit(BG, (0,0))
		
		for enemy in enemies:
			enemy.draw(WIN)

		player.draw(WIN)
		
		# draw label
		lives_label = main_font.render(f"Lives {lives}", 1, (255, 255, 255))
		level_label = main_font.render(f"Level {level}", 1, (255, 255, 255))


		WIN.blit(lives_label, (10, 10))
		WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

		if lost:
			lost_label = lost_font.render("You lost !!!", 1, (255, 255, 255))
			WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
			

		pygame.display.update()

	# -----------------------------------------------------------------------------------------------------------
	while run :
		clock.tick(FPS)
		redraw_window()
		# -----------------------------------------------------------------------------------------------------------

		if lives <= 0 or player.health <= 0:
			lost = True
			lost_count += 1

		if lost:
			if lost_count > FPS * 3: # 3 * FPS = 3 seconds
				run = False
			else:
				continue

		if len(enemies) == 0:
			level += 1
			wave_lenght += 5
			for i in range(wave_lenght):
				enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "green", "blue"]))
				enemies.append(enemy)
		# -----------------------------------------------------------------------------------------------------------
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				break

		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] and player.x - player_vel > 0: # left
			player.x -= player_vel
		if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: # right
			player.x += player_vel
		if keys[pygame.K_UP] and player.y - player_vel > 0: # up
			player.y -= player_vel
		if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
			player.y += player_vel
		if keys[pygame.K_SPACE]:
			player.shoot()
		# -----------------------------------------------------------------------------------------------------------

		for enemy in enemies[:]: # Copier la liste des enemies
			enemy.move(enemy_vel)
			enemy.move_lasers(laser_vel, player)

			if random.randrange(0, 2*FPS) == 1:
				enemy.shoot()

			if collide(enemy, player):
				player.health -= 10
				enemies.remove(enemy)

			elif enemy.y + enemy.get_height() > HEIGHT:
				# losque les enemies arrive au bord de la fenetre augmenter le niveau
				lives -= 1
				enemies.remove(enemy)


		player.move_lasers(-laser_vel, enemies)

# -----------------------------------------------------------------------------------------------------------

def main_menu():
	title_font = pygame.font.SysFont("comicsans", 50)
	run = True
	# -----------------------------------------------------------------------------------------------------------
	while run:
		WIN.blit(BG, (0,0))
		title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
		WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
		pygame.display.update()
		# -----------------------------------------------------------------------------------------------------------
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				main()
	pygame.quit()


# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------

main_menu()

#--------------------------------------------------------

"""
	pygame.mask.from_surface(img) cette fonction creer un mask cad reconnait que les parties de l'image où il y a des pixels
"""