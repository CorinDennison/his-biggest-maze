import pygame
import mazealgo
import numpy
from spritesheet import Sprite_sheet
from numpy.random import random_integers as rand
 
# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
 
# define some sizes
MAZE_WIDTH = 41
MAZE_HEIGHT = 31
SCREEN_WIDTH = 1312
SCREEN_HEIGHT = 992
CELL_SIZE = 32 # don't change this unless you change the images
CLOCK_SPEED = 60
MAZE_DRAW_SPEED = 120

# define maze unfracturedness (frequency of branches)
UNFRACTUREDNESS = 50

# wall sprite sheet values
WALL_NW			= (0, 0, 16, 16)
WALL_NW_W		= (17, 0, 16, 16)
WALL_NW_N		= (34, 0, 16, 16)
WALL_NW_NW		= (51, 0, 16, 16)
WALL_NW_CORNER	= (68, 0, 16, 16)
WALL_NE			= (0, 17, 16, 16)
WALL_NE_E		= (17, 17, 16, 16)
WALL_NE_N		= (34, 17, 16, 16)
WALL_NE_NE		= (51, 17, 16, 16)
WALL_NE_CORNER	= (68, 17, 16, 16)
WALL_SW			= (0, 34, 16, 16)
WALL_SW_W		= (17, 34, 16, 16)
WALL_SW_S		= (34, 34, 16, 16)
WALL_SW_SW		= (51, 34, 16, 16)
WALL_SW_CORNER	= (68, 34, 16, 16)
WALL_SE			= (0, 51, 16, 16)
WALL_SE_E		= (17, 51, 16, 16)
WALL_SE_S		= (34, 51, 16, 16)
WALL_SE_SE		= (51, 51, 16, 16)
WALL_SE_CORNER	= (68, 51, 16, 16)

pygame.init()

# Set the width and height of the screen [width, height]
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
#Load images
wall_sprite_sheet = Sprite_sheet("walls.png")
wall_nw_image = wall_sprite_sheet.get_image(WALL_NW)
wall_nw_w_image = wall_sprite_sheet.get_image(WALL_NW_W)
wall_nw_n_image = wall_sprite_sheet.get_image(WALL_NW_N)
wall_nw_nw_image = wall_sprite_sheet.get_image(WALL_NW_NW)
wall_nw_corner_image = wall_sprite_sheet.get_image(WALL_NW_CORNER)
wall_ne_image = wall_sprite_sheet.get_image(WALL_NE)
wall_ne_e_image = wall_sprite_sheet.get_image(WALL_NE_E)
wall_ne_n_image = wall_sprite_sheet.get_image(WALL_NE_N)
wall_ne_ne_image = wall_sprite_sheet.get_image(WALL_NE_NE)
wall_ne_corner_image = wall_sprite_sheet.get_image(WALL_NE_CORNER)
wall_sw_image = wall_sprite_sheet.get_image(WALL_SW)
wall_sw_w_image = wall_sprite_sheet.get_image(WALL_SW_W)
wall_sw_s_image = wall_sprite_sheet.get_image(WALL_SW_S)
wall_sw_sw_image = wall_sprite_sheet.get_image(WALL_SW_SW)
wall_sw_corner_image = wall_sprite_sheet.get_image(WALL_SW_CORNER)
wall_se_image = wall_sprite_sheet.get_image(WALL_SE)
wall_se_e_image = wall_sprite_sheet.get_image(WALL_SE_E)
wall_se_s_image = wall_sprite_sheet.get_image(WALL_SE_S)
wall_se_se_image = wall_sprite_sheet.get_image(WALL_SE_SE)
wall_se_corner_image = wall_sprite_sheet.get_image(WALL_SE_CORNER)

wall_image = pygame.image.load("wall.png").convert()
floor_image = pygame.image.load("floor.png").convert()
up_image = pygame.image.load("up.png").convert()
down_image = pygame.image.load("down.png").convert()

#Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# the size of the maze
w = MAZE_WIDTH
h = MAZE_HEIGHT

# make sure the height and width are odd
h = (h // 2) * 2 + 1
w = (w // 2) * 2 + 1
maze = mazealgo.Maze(w, h, screen, wall_image, floor_image, up_image, down_image, CELL_SIZE, MAZE_DRAW_SPEED, UNFRACTUREDNESS)
m = maze.generate()

# set the size of each cell such that the maze will fit in the window
# CELL_SIZE = min(size[0] // w, size[1] // h)

# some methods for determining if there are neighbouring walls
def get_north(x, y):
	if y == 0 or m[x, y - 1]:
		return False
	else:
		return True

def get_south(x, y):
	if y == h - 1 or m[x, y + 1]:
		return False
	else:
		return True
		
def get_west(x, y):
	if x == 0 or m[x - 1, y]:
		return False
	else:
		return True
		
def get_east(x, y):
	if x == w - 1 or m[x + 1, y]:
		return False
	else:
		return True
		
def get_north_west(x, y):
	if y == 0 or x == 0 or m[x - 1, y - 1]:
		return False
	else:
		return True

def get_north_east(x, y):
	if y == 0 or x == w - 1 or m[x + 1, y - 1]:
		return False
	else:
		return True
		
def get_south_east(x, y):
	if x == w - 1 or y == h - 1 or m[x + 1, y + 1]:
		return False
	else:
		return True
		
def get_south_west(x, y):
	if x == 0 or y == h - 1 or m[x - 1, y + 1]:
		return False
	else:
		return True
		
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done = True # Flag that we are done so we exit this loop
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN: 
				maze.reset()
  
    # --- Game logic should go here
	
	
    # --- Drawing code should go here
     
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
	screen.fill(WHITE)
	
	m = maze.step_generate()
 
	for i in range(w):
		for j in range(h):
			#print start or finish
			if m[i, j] == 2:
				screen.blit(up_image, [i * CELL_SIZE, j * CELL_SIZE])
			elif m[i, j] == 3:
				screen.blit(down_image, [i * CELL_SIZE, j * CELL_SIZE])
			#print a wall
			elif not m[i, j]:
				# screen.blit(wall_image, [i * CELL_SIZE, j * CELL_SIZE])
				#draw nw corner of wall to join neighbouring walls
				if get_west(i, j) and get_north(i, j):
					if get_north_west(i, j):
						screen.blit(wall_nw_image, [i * CELL_SIZE, j * CELL_SIZE])
					else:
						screen.blit(wall_nw_corner_image, [i * CELL_SIZE, j * CELL_SIZE])
				elif get_west(i, j):
					screen.blit(wall_nw_n_image, [i * CELL_SIZE, j * CELL_SIZE])
				elif get_north(i, j):
					screen.blit(wall_nw_w_image, [i * CELL_SIZE, j * CELL_SIZE])
				else:
					screen.blit(wall_nw_nw_image, [i * CELL_SIZE, j * CELL_SIZE])
				#draw ne corner of wall to join neighbouring walls
				if get_east(i, j) and get_north(i, j):
					if get_north_east(i, j):
						screen.blit(wall_ne_image, [i * CELL_SIZE + CELL_SIZE / 2, j * CELL_SIZE])
					else:
						screen.blit(wall_ne_corner_image, [i * CELL_SIZE + CELL_SIZE / 2, j * CELL_SIZE])
				elif get_east(i, j):
					screen.blit(wall_ne_n_image, [i * CELL_SIZE + CELL_SIZE / 2, j * CELL_SIZE])
				elif get_north(i, j):
					screen.blit(wall_ne_e_image, [i * CELL_SIZE + CELL_SIZE / 2, j * CELL_SIZE])
				else:
					screen.blit(wall_ne_ne_image, [i * CELL_SIZE + CELL_SIZE / 2, j * CELL_SIZE])
				#draw sw corner of wall to join neighbouring walls
				if get_west(i, j) and get_south(i, j):
					if get_south_west(i, j):
						screen.blit(wall_sw_image, [i * CELL_SIZE, j * CELL_SIZE + CELL_SIZE / 2])
					else:
						screen.blit(wall_sw_corner_image, [i * CELL_SIZE, j * CELL_SIZE + CELL_SIZE / 2])
				elif get_west(i, j):
					screen.blit(wall_sw_s_image, [i * CELL_SIZE, j * CELL_SIZE + CELL_SIZE / 2])
				elif get_south(i, j):
					screen.blit(wall_sw_w_image, [i * CELL_SIZE, j * CELL_SIZE + CELL_SIZE / 2])
				else:
					screen.blit(wall_sw_sw_image, [i * CELL_SIZE, j * CELL_SIZE + CELL_SIZE / 2])
				#draw se corner of wall to join neighbouring walls
				if get_east(i, j) and get_south(i, j):
					if get_south_east(i, j):
						screen.blit(wall_se_image, [i * CELL_SIZE + CELL_SIZE / 2, j * CELL_SIZE + CELL_SIZE / 2])
					else:
						screen.blit(wall_se_corner_image, [i * CELL_SIZE + CELL_SIZE / 2, j * CELL_SIZE + CELL_SIZE / 2])
				elif get_east(i, j):
					screen.blit(wall_se_s_image, [i * CELL_SIZE + CELL_SIZE / 2, j * CELL_SIZE + CELL_SIZE / 2])
				elif get_south(i, j):
					screen.blit(wall_se_e_image, [i * CELL_SIZE + CELL_SIZE / 2, j * CELL_SIZE + CELL_SIZE / 2])
				else:
					screen.blit(wall_se_se_image, [i * CELL_SIZE + CELL_SIZE / 2, j * CELL_SIZE + CELL_SIZE / 2])
			#print a floor
			else:
				screen.blit(floor_image, [i * CELL_SIZE, j * CELL_SIZE])
		
    # --- Go ahead and update the screen with what we've drawn.
	pygame.display.flip()
 
    # --- Limit to 60 frames per second
	clock.tick(MAZE_DRAW_SPEED)
     
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()


		