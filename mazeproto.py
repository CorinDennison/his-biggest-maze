import pygame
import mazealgo
import numpy
from numpy.random import random_integers as rand
 
# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
 
# define some sizes
MAZE_WIDTH = 40
MAZE_HEIGHT = 35
SCREEN_WIDTH = 1230
SCREEN_HEIGHT = 1080

# define maze unfracturedness
UNFRACTUREDNESS = 5

pygame.init()

# Set the width and height of the screen [width, height]
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
#Load images  
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
m = mazealgo.maze(w, h, screen, wall_image, floor_image, up_image, down_image, 30, 60, UNFRACTUREDNESS)

# set the size of each cell such that the maze will fit in the window
# cell_size = min(size[0] // w, size[1] // h)
cell_size = 30
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done = True # Flag that we are done so we exit this loop
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				m = mazealgo.maze(w, h, screen, wall_image, floor_image, up_image, down_image, 30, 60, UNFRACTUREDNESS)
  
    # --- Game logic should go here
	
	
    # --- Drawing code should go here
     
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
	screen.fill(WHITE)
 
	for i in range(w):
		for j in range(h):
			#print start or finish
			if m[i, j] == 2:
				# pygame.draw.rect(screen, GREEN, [i * cell_size, j * cell_size, cell_size, cell_size], 0)
				screen.blit(up_image, [i * cell_size, j * cell_size])
			elif m[i, j] == 3:
				# pygame.draw.rect(screen, RED, [i * cell_size, j * cell_size, cell_size, cell_size], 0)
				screen.blit(down_image, [i * cell_size, j * cell_size])
			#print a wall
			elif not m[i, j]:
				# pygame.draw.rect(screen, BLACK, [i * cell_size, j * cell_size, cell_size, cell_size], 0)
				screen.blit(wall_image, [i * cell_size, j * cell_size])
			else:
				screen.blit(floor_image, [i * cell_size, j * cell_size])
		
    # --- Go ahead and update the screen with what we've drawn.
	pygame.display.flip()
 
    # --- Limit to 60 frames per second
	clock.tick(60)
     
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

