import pygame
import random
import constants
import spritesheet
import falling
import player
import timers
from constants import Direction

class Game():
	# width and height of the play area
	screen_width = None
	screen_height = None

	# Loop until the user clicks the close button.
	game_over = None
	
	# Snowflake lists (snowflakes 1-4 are used only) relative in position to player list
	snowflakes = [None, None, None, None, None]
	
	# The list of powerup sprites
	bonus_list = None
	timer_list = None
	
	# This is a list of every sprite.
	all_sprites_list = None
	
	# The players (players 1-4 are used only)
	num_players = None
	player = [None, None, None, None, None]
	
	# score for players 1 and 2
	white_score = None
	red_score = None
	score_limit = None
	
	# joystick variables
	joystick_count = None
	my_joystick = None
	
	def __init__(self, width, height):
		# set play area height and width
		self.screen_width = width
		self.screen_height = height
	
		# set score player needs to reach for game over
		self.game_over = False
		self.score_limit = 10
		self.white_score = 0
		self.red_score = 0
		
		#initialize sprite lists
		self.snowflakes[1] = pygame.sprite.Group()
		self.snowflakes[2] = pygame.sprite.Group()
		self.bonus_list = pygame.sprite.Group()
		self.timer_list = pygame.sprite.Group()
		self.all_sprites_list = pygame.sprite.Group()
		
		# add a snow creating timer into the timer list
		self.timer_list.add(timers.Escalate(self))
		
		#initialize players, place them in the corners, and add them to the sprite list
		self.num_players = 2
		self.player[1] = player.Snowman(self, 1, 2, constants.WHITE, 5)
		self.player[1].rect.left = 0
		self.player[1].rect.bottom = self.screen_height
		
		self.player[2] = player.Snowman(self, 2, 2, constants.RED, 5)
		self.player[2].rect.right = self.screen_width
		self.player[2].rect.bottom = self.screen_height
		
		self.all_sprites_list.add(self.player[1])
		self.all_sprites_list.add(self.player[2])
		
		# check for joysticks
		self.joystick_count = pygame.joystick.get_count()
		if self.joystick_count != 0:
			# Use joystick #0 and initialize it
			self.my_joystick = pygame.joystick.Joystick(0)
			self.my_joystick.init()

		# create the starting snow
		for i in range(10):
			self.place_snow(1, constants.WHITE, self.snowflakes[1])
			self.place_snow(2, constants.RED, self.snowflakes[2])
			
	def place_snow(self, number, color, snow_list, diameter = 5, speed = 2):
		''' Places snow in a random location above the screen '''
		snow = falling.Snow(self, number, color, diameter, speed)
		snow.rect.x = random.randrange(self.screen_width)
		snow.rect.y = random.randrange(self.screen_height * -1, 0)
		
		snow_list.add(snow)
		self.all_sprites_list.add(snow)
		
	def place_bonus(self, bonus):
		bonus.rect.x = random.randrange(self.screen_width)
		bonus.rect.y = 0 - bonus.rect.height
		
		self.bonus_list.add(bonus)
		self.all_sprites_list.add(bonus)
		
	def blocked_collision(self, sprite1, sprite2):
		''' sprite1 slides against sprite2 '''
		#not sure how to do this right now
		
	def process_events(self):
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				return True # Flag that we are done so we exit this loop
			# game is over and player clicks
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.game_over:
					self.__init__(self.screen_width, self.screen_height)			
			# Player pressed down on a key
			if event.type == pygame.KEYDOWN:
				# Figure out if it was an arrow key. If so
				# adjust speed.
				if event.key == pygame.K_UP:
					self.player[2].accelerate(Direction.NORTH)
				if event.key == pygame.K_RIGHT:
					self.player[2].accelerate(Direction.EAST)
				if event.key == pygame.K_DOWN:
					self.player[2].accelerate(Direction.SOUTH)
				if event.key == pygame.K_LEFT:
					self.player[2].accelerate(Direction.WEST)
		 
				if self.joystick_count == 0:
					if event.key == pygame.K_w:
						self.player[1].accelerate(Direction.NORTH)
					if event.key == pygame.K_d:
						self.player[1].accelerate(Direction.EAST)
					if event.key == pygame.K_s:
						self.player[1].accelerate(Direction.SOUTH)
					if event.key == pygame.K_a:
						self.player[1].accelerate(Direction.WEST)
					
				if event.key == pygame.K_RETURN:
					if self.game_over:
						self.game_over = False
						self.score_limit = self.score_limit * 2					
						
			# Player let up on a key
			if event.type == pygame.KEYUP:
				# If it is an arrow key, reset vector back to zero
				if event.key == pygame.K_DOWN:
					self.player[2].accelerate(Direction.NORTH)
				if event.key == pygame.K_LEFT:
					self.player[2].accelerate(Direction.EAST)
				if event.key == pygame.K_UP:
					self.player[2].accelerate(Direction.SOUTH)
				if event.key == pygame.K_RIGHT:
					self.player[2].accelerate(Direction.WEST)

				if self.joystick_count == 0:
					if event.key == pygame.K_s:
						self.player[1].accelerate(Direction.NORTH)
					if event.key == pygame.K_a:
						self.player[1].accelerate(Direction.EAST)
					if event.key == pygame.K_w:
						self.player[1].accelerate(Direction.SOUTH)
					if event.key == pygame.K_d:
						self.player[1].accelerate(Direction.WEST)
		
		#for joystick controls
		if self.joystick_count != 0:
		 
			hat = self.my_joystick.get_hat(0)
				
			# Move player_1 horizontally according to the hat.
			self.player[1].move(Direction.EAST, hat[0])
			# Move player_1 vertically according to the hat.
			# We use north instead of south because hats are weird.
			self.player[1].move(Direction.SOUTH, hat[1] * -1)
		
		return False # Don't close the window
		
	def run_logic(self):
		# generate some yellow orbs in random intervals
		#if not random.randrange(0, 300):
		#	self.place_snow(0, constants.YELLOW, self.bonus_list, 10, 2)
		# generate a wiggle bonus
		if not random.randrange(0, 300):
			bonus = falling.ALL_BONUSES[random.randrange(0, len(falling.ALL_BONUSES))].create(self)
			self.place_bonus(bonus)
	
		self.all_sprites_list.update()
		for timer in self.timer_list:
			timer.active_update()
		
		# check for player on player collisions
		if self.player[1].rect.colliderect(self.player[2].rect):
			self.player[1].bounce(self.player[2].direction_x, self.player[2].direction_y)
			self.player[2].bounce(self.player[1].direction_x, self.player[1].direction_y)
			
		# checks for bonus collisions
		if not self.game_over:
			for i in range(1, self.num_players + 1):
				bonus_hit_list = pygame.sprite.spritecollide(self.player[i], self.bonus_list, False)
				for bonus in bonus_hit_list:
					bonus.collide(self.player[i])
					self.timer_list.add(bonus)
		
		# checks for and deals with snow collisions
		if not self.game_over:
			player_1_orb_list = pygame.sprite.spritecollide(self.player[1], self.bonus_list, True)
			player_2_orb_list = pygame.sprite.spritecollide(self.player[2], self.bonus_list, True)
			white_snow_hit_list = pygame.sprite.spritecollide(self.player[2], self.snowflakes[1], True)
			red_snow_hit_list = pygame.sprite.spritecollide(self.player[1], self.snowflakes[2], True)
			
			for snow in white_snow_hit_list:
				self.white_score += 1
			
			for snow in red_snow_hit_list:
				self.red_score += 1
			
			for orb in player_1_orb_list:
				self.place_snow(1, constants.WHITE, self.snowflakes[1])
				self.place_snow(1, constants.WHITE, self.snowflakes[1])
				self.place_snow(1, constants.WHITE, self.snowflakes[1])
				self.place_snow(2, constants.RED, self.snowflakes[2])
				
			for orb in player_2_orb_list:
				self.place_snow(2, constants.RED, self.snowflakes[2])
				self.place_snow(2, constants.RED, self.snowflakes[2])
				self.place_snow(2, constants.RED, self.snowflakes[2])
				self.place_snow(1, constants.WHITE, self.snowflakes[1])
				
		# Check for game over
		if self.white_score > self.score_limit - 1 or self.red_score > self.score_limit - 1:
			self.game_over = True
		
	def display_frame(self, screen):
		# First, clear the screen to black. Don't put other drawing commands
		# above this, or they will be erased with this command.
		screen.fill(constants.BLACK)

		# Draw the score
		# Select the font to use, size, bold, italics
		font = pygame.font.SysFont('Calibri', 25, True, False)
		smallfont  = pygame.font.SysFont('Calibri', 12, True, False)
		# Render the text. "True" means anti-aliased text.
		red_score_text = font.render("RED SCORE: " + str(self.red_score), True, constants.RED)
		white_score_text = font.render("WHITE SCORE: " + str(self.white_score), True, constants.WHITE)
		red_snow_text = smallfont.render("snowflakes: " + str(len(self.snowflakes[2])), True, constants.RED)
		white_snow_text = smallfont.render("snowflakes: " + str(len(self.snowflakes[1])), True, constants.WHITE)
		# Put the image of the text on the screen
		screen.blit(white_score_text, [0, 0])
		screen.blit(red_score_text, [0, 40])
		screen.blit(white_snow_text, [self.screen_width - white_snow_text.get_width(), 0])
		screen.blit(red_snow_text, [self.screen_width - red_snow_text.get_width(), 40])
		
		# draw all sprites
		self.all_sprites_list.draw(screen)
		
		if self.game_over:
			font = pygame.font.SysFont("serif", 25)
			text = font.render("Game Over, click to restart or press enter to extend.", True, constants.GREEN)
			center_x = (self.screen_width // 2) - (text.get_width() // 2)
			center_y = (self.screen_height // 2) - (text.get_height() // 2)
			screen.blit(text, [center_x, center_y])
			
		# --- Go ahead and update the screen with what we've drawn.
		pygame.display.flip()

def main():
	# set up pygame and window
	pygame.init()

	# Set the width and height of the screen [width, height]
	screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
	pygame.display.set_caption("My Snowman Game")

	# Variable to check whether to keep the game running
	done = False
	
	# Used to manage how fast the screen updates
	clock = pygame.time.Clock()

	# Create the game
	game = Game(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
	
	# Main program loop
	while not done:
		done = game.process_events()
		
		game.run_logic()
		
		game.display_frame(screen)
	 
		# --- Limit to 60 frames per second
		clock.tick(60)
		 
	pygame.quit()
	
# Call the main function, start up the game
if __name__ == "__main__":
	main()