import constants
import pygame
import random
from constants import Direction

class Snowman(pygame.sprite.Sprite):
	speed = None
	snowflakes = None
	game = None
	number = None
	color = None
	
	def __init__(self, game, number, multiplier = 2, color = constants.WHITE, speed = 5):
		pygame.sprite.Sprite.__init__(self)
		
		self.game = game
		self.number = number
		
		self.image = pygame.Surface([16 * multiplier, 29 * multiplier])
		self.image.fill(constants.BLACK)
		self.image.set_colorkey(constants.BLACK)
		
		# Draw a circle for the head
		pygame.draw.ellipse(self.image, color, [5 * multiplier, 0, 6 * multiplier, 6 * multiplier])
		# Draw the middle snowman circle
		pygame.draw.ellipse(self.image, color, [3 * multiplier, 5 * multiplier, 10 * multiplier, 10 * multiplier])
		# Draw the bottom snowman circle
		pygame.draw.ellipse(self.image, color, [0, 13 * multiplier, 16 * multiplier, 16 * multiplier])
		
		self.rect = self.image.get_rect()
		
		#set the speed
		self.speed = speed
		self.color = color
		
		# for non-player controlled movement
		self.vector_x = 0
		self.vector_y = 0
		# for player controlled movement
		self.direction_x = 0
		self.direction_y = 0

		#how long to bounce for
		self.bounce_duration = 0

	def accelerate(self, direction):
		''' accelerate in a cardinal direction.  0 is N, 1 is E, 2 is S, and 3 is W 
			used for keyboard control '''
		if direction == Direction.NORTH:
			self.direction_y -= 1
		elif direction == Direction.EAST:
			self.direction_x += 1
		elif direction == Direction.SOUTH:
			self.direction_y += 1
		elif direction == Direction.WEST:
			self.direction_x -= 1
			
	def move(self, direction, modifier = 1.0):
		''' move in a cardinal direction.  0 is N, 1 is E, 2 is S, and 3 is W 
			used for joystick control '''
		if direction == 0:
			self.direction_y = -1 * modifier
		elif direction == 1:
			self.direction_x = 1 * modifier
		elif direction == 2:
			self.direction_y = 1 * modifier
		elif direction == 3:
			self.direction_x = -1 * modifier
	
	def bounce(self, vector_x, vector_y):
		self.bounce_duration = 15
		self.vector_x = vector_x
		self.vector_y = vector_y
		
	def update(self):
		''' update the player sprite with his new location, making sure he doesn't leave the area '''
		
		if not self.bounce_duration:
			self.rect.x += self.direction_x * self.speed
			self.rect.y += self.direction_y * self.speed
		else:
			self.rect.x += self.vector_x * self.speed
			self.rect.y += self.vector_y * self.speed
			self.bounce_duration -= 1
			
		# check if any borders are being touched
		if self.rect.x < 0:
			self.rect.x = 0
		if self.rect.x + self.rect.width > self.game.screen_width:
			self.rect.right = self.game.screen_width
		if self.rect.y < 0:
			self.rect.y = 0
		if self.rect.y + self.rect.height > self.game.screen_height:
			self.rect.bottom = self.game.screen_height