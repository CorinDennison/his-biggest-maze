import random
import pygame
import constants
from spritesheet import Sprite_sheet

# constants representing the location of the images in a sprite sheet
WIGGLE = (0, 0, 18, 31)
S_SPEED = (19, 0, 9, 31)
P_SPEED = (29, 0, 9, 31)
ROCKET = (39, 0, 21, 21)
MORE_SNOW = (61, 0, 21, 21)


class Falling_sprite(pygame.sprite.Sprite):
	vector_y = None
	vector_x = 0
	game = None
	def __init__(self, speed, game):
		pygame.sprite.Sprite.__init__(self)
		self.vector_y = speed
		self.game = game
	
	def reset_pos(self):
		self.rect.y = random.randrange(-100, 0)
		self.rect.x = random.randrange(0, self.game.screen_width)
		
	def update(self):
		self.rect.y += self.vector_y
		if self.rect.y > self.game.screen_height:
			self.reset_pos()
		self.rect.x += self.vector_x
		if self.rect.x < 0:
			self.rect.x = 0
		elif self.rect.x > self.game.screen_width - self.rect.width:
			self.rect.right = self.game.screen_width
	
class Snow(Falling_sprite):
	# The player number this list belongs to
	number = None
	# essentially vector_x and vector_y
	speed = None
	def __init__(self, game, number, color, diameter = 5, speed = 2):
		Falling_sprite.__init__(self, speed, game)

		self.number = number
		self.image = pygame.Surface([diameter, diameter])
		self.image.fill(constants.BLACK)
		self.image.set_colorkey(constants.BLACK)
		pygame.draw.ellipse(self.image, color, [0, 0, diameter, diameter])
		
		self.rect = self.image.get_rect()
	
	# just here because I havent converted yellow orbs to bonuses yet
	def collide(self, player):
		pass
		
class Bonus(Falling_sprite):
	game = None
	frames = 0
	duration = 10
	player = None
	def __init__(self, game, sprite_sheet_data, speed = 1):
		Falling_sprite.__init__(self, speed, game)
		
		# so we can create a list of bonuses before we initialize pygame
		if game:
			sprite_sheet = Sprite_sheet("bonuses.png")
			# Grab the image for this platform
			self.image = sprite_sheet.get_image(sprite_sheet_data[0],
												sprite_sheet_data[1],
												sprite_sheet_data[2],
												sprite_sheet_data[3])
			self.rect = self.image.get_rect()
		
	# creates a new instance of the bonus that is calling it
	def create(self, game):
		clazz = self.__class__
		return clazz(game)
	
	def collide(self, player):
		self.kill()
		self.player = player.number
		frames = 0
		
class More_snow_bonus(Bonus):
	def __init__(self, game):
		Bonus.__init__(self, game, MORE_SNOW)
	
	def active_update(self):
		for i in range(0, 4):
			snow = Snow(self.game, self.player, self.game.player[self.player].color)
			snow.reset_pos()
			self.game.snowflakes[self.player].add(snow)
			self.game.all_sprites_list.add(snow)
		self.kill()
			
class Player_speed_bonus(Bonus):
	def __init__(self, game):
		Bonus.__init__(self, game, P_SPEED)
		self.duration = 10
	
	def active_update(self):
		self.frames += 1
		if self.frames == 1:
			self.game.player[self.player].speed += 2
		elif not self.frames < self.duration * 60:
			self.kill()
			self.game.player[self.player].speed -= 2
				
class Snow_speed_bonus(Bonus):
	snowflakes = None
	def __init__(self, game):
		Bonus.__init__(self, game, S_SPEED)
		self.snowflakes = []
		
	def active_update(self):
		self.frames += 1
		if self.frames == 1:
			for snow in self.game.snowflakes[self.player]:
				snow.vector_y += 3
				self.snowflakes.append(snow)
		elif not self.frames < self.duration * 60:
			self.kill()
			for snow in self.snowflakes:
				snow.vector_y -= 3
		
		
		
class Rocket_bonus(Bonus):
	active = None
	speed = None
	oldspeed = None
	def __init__(self, game):
		Bonus.__init__(self, game, ROCKET)
		self.active = False
		self.speed = 1
		
	def active_update(self):
		self.frames += 1
		if not self.active:
			if self.frames == 1:
				# reset vector_x
				self.vector_x = 0
				self.vector_y = 0
				# re add itself to drawing list
				self.game.all_sprites_list.add(self)
				# pick a target player
				player = self.player
				# if it picks itself, pick again
				while self.player == player:
					self.player = random.randrange(1, self.game.num_players + 1)
			# rocket runs out of fuel
			elif not self.frames < self.duration * 60:
				self.kill()
			# follow the target player
			else:
				# the target player's x and y
				p_x = self.game.player[self.player].rect.x
				p_y = self.game.player[self.player].rect.y
				if self.rect.x > p_x:
					self.vector_x = -1 * self.speed
				elif self.rect.x < p_x:
					self.vector_x = 1 * self.speed
				else:
					self.vector_x = 0
				if self.rect.y > p_y:
					self.vector_y = -1 * self.speed
				elif self.rect.y < p_y:
					self.vector_y = 1 * self.speed
				else:
					self.vector_y = 0
				self.update()
				# if the rocket hits something
				if pygame.sprite.collide_rect(self, self.game.player[self.player]):
					self.kill()
					self.active = True
					self.frames = 0
					self.game.timer_list.add(self)
					self.duration = 4
		# if the rocket hit something then do the timer thing
		else:
			if self.frames == 1:
				self.oldspeed = self.game.player[self.player].speed
				self.game.player[self.player].bounce_duration = self.duration * 60
				self.game.player[self.player].vector_x = 0
				self.game.player[self.player].vector_y = 0
				self.kill()
			elif not self.frames < self.duration * 60:
				self.game.player[self.player].speed += self.oldspeed
				self.kill()
				
class Invulnerable_bonus(Bonus):
	def __init__(self, game):
		Bonus.__init__(self, game, None)
	
class Wiggle_bonus(Bonus):
	def __init__(self, game):
		Bonus.__init__(self, game, WIGGLE)
		
	def active_update(self):
		self.frames += 1
		for snow in self.game.snowflakes[self.player]:
			drift = random.randrange(0, 60)
			if drift == 0:
				snow.vector_x += 1
				if snow.vector_x > 1:
					snow.vector_x = 1
			elif drift == 1:
				snow.vector_x -= 1
				if snow.vector_x < -1:
					snow.vector_x = -1
			
		if not self.frames < self.duration * 60:
			self.kill()
			for snow in self.game.snowflakes[self.player]:
				snow.vector_x = 0
				
ALL_BONUSES = (Wiggle_bonus(False),
				#Invulnerable_bonus(False),
				Rocket_bonus(False),
				Snow_speed_bonus(False),
				Player_speed_bonus(False),
				More_snow_bonus(False)
				)