import random
import pygame
import constants
import falling

class Timer(pygame.sprite.Sprite):
	repeats = None
	frames = None
	duration = None
	game = None
	def __init__(self, game):
		pygame.sprite.Sprite.__init__(self)
		self.game = game
		self.frames = 0

	def active_update(self):
		self.frames += 1

class Escalate(Timer):
	def __init__(self, game):
		Timer.__init__(self, game)
		self.repeats = 0
		self.duration = 5
	
	def active_update(self):
		self.frames += 1
		if self.frames > self.duration * 60:
			self.repeats += 1
			self.frames = 0
			for i in range(1, self.game.num_players + 1):
				snow = falling.Snow(self.game, i, self.game.player[i].color)
				snow.reset_pos()
				self.game.snowflakes[i].add(snow)
				self.game.all_sprites_list.add(snow)
				