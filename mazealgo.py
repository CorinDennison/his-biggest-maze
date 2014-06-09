import pygame
import numpy
from numpy.random import random_integers as rand

def maze(width=51, height=51, screen=False, wall_image=False, floor_image=False, up_image=False, down_image=False, cell_size=30, speed=60, unfracturedness=100):
	def is_dead_end(maze, cell):
		# running total of number of walls surrounding this cell
		walls=0
		# check north wall
		if not maze[cell[0], cell[1] - 1]:
			walls += 1
		# check east wall
		if not maze[cell[0] + 1, cell[1]]:
			walls += 1
		# check south wall
		if not maze[cell[0], cell[1] + 1]:
			walls += 1
		# check west wall
		if not maze[cell[0] - 1, cell[1]]:
			walls += 1
		if walls == 3:
			return True
		else:
			return False
			
			
	# If a screen was passed in then set up drawing
	if screen:
		pygame.init()
		clock = pygame.time.Clock()
		
    # Only odd shapes
	width = (width // 2) * 2 + 1
	height = (height // 2) * 2 + 1
    # initialize maze with all walls and cells filled in
	The_Maze = numpy.zeros((width, height), dtype=int)
	if screen:
		for i in range(width):
			for j in range(height):
				screen.blit(wall_image, [i * cell_size, j * cell_size])
		pygame.display.flip()
		clock.tick(speed)
		
	# start building maze
	current_x = rand(1, width // 2) * 2 - 1
	current_y = rand(1, height // 2) * 2 - 1
	# 0 means filled in, 1 means dug out, 2 means start, and 3 means finish
	The_Maze[current_x, current_y] = 2
	if screen:
		screen.blit(up_image, [current_x * cell_size, current_y * cell_size])
		pygame.display.flip()
		clock.tick(speed)
		
	# a list of neighbouring walls to be potentially removed, the cell on the other side, and the orgininating cell.  
	# A wall looks like x, y, next cell x, next cell y, original cell x, original cell y
	walls = [(current_x, current_y - 1, current_x, current_y - 2, current_x, current_y)]
	walls.append((current_x + 1, current_y, current_x + 2, current_y, current_x, current_y))
	walls.append((current_x, current_y + 1, current_x, current_y + 2, current_x, current_y))
	walls.append((current_x - 1, current_y, current_x - 2, current_y, current_x, current_y))
	
	# the main maze building loop continues until it runs out of walls
	while len(walls):
		#keep picking walls until you find a dead end or look at x number of walls 
		for i in range(unfracturedness + 1):
			wallnum = rand(0, len(walls) -1)
			wall = walls[wallnum]
			if is_dead_end(The_Maze, (wall[4], wall[5])):
				break
		# we found a wall to examine so remove it from the list
		walls.pop(wallnum)
		
		# if the wall belongs to a border then ignore it
		if wall[0] == 0 or wall[1] == 0 or wall[0] == width - 1 or wall[1] == height - 1:
			continue
		# checks if the cell on the other side is already part of the maze
		elif The_Maze[wall[2], wall[3]]:
			continue
		else:
			# the wall and the opposite cell become passages
			The_Maze[wall[0], wall[1]] = 1
			The_Maze[wall[2], wall[3]] = 1
			# add the new cell to current and add its walls to walls
			current_x = wall[2]
			current_y = wall[3]
			walls.append((current_x, current_y - 1, current_x, current_y - 2, current_x, current_y))
			walls.append((current_x + 1, current_y, current_x + 2, current_y, current_x, current_y))
			walls.append((current_x, current_y + 1, current_x, current_y + 2, current_x, current_y))
			walls.append((current_x - 1, current_y, current_x - 2, current_y, current_x, current_y))
			
			#draw the new passage if necessary
			if screen:
				screen.blit(floor_image, [wall[0] * cell_size, wall[1] * cell_size])
				screen.blit(floor_image, [wall[2] * cell_size, wall[3] * cell_size])
				pygame.display.flip()
				clock.tick(speed)
	# the last cell dug out becomes the finish
	The_Maze[current_x, current_y] = 3
	if screen:
		screen.blit(down_image, [current_x * cell_size, current_y * cell_size])
		pygame.display.flip()
		clock.tick(speed)
	return The_Maze
	
# # the size of the maze
# h = 40
# w = 40
# # make sure the height and width are odd
# h = (h // 2) * 2 + 1
# w = (w // 2) * 2 + 1

# m = maze(h, w)

# # print out the maze
# for i in range(h):
	# for j in range(w):
		# #print start or finish
		# if m[i, j] == 2:
			# print("S", end = "")
		# elif m[i, j] == 3:
			# print("F", end = "")
		# #print a wall or a space
		# elif not m[i, j]:
			# print("X", end = "")
		# else:
			# print(" ", end = "")
	# print("")