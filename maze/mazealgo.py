import pygame
import numpy
from numpy.random import random_integers as rand

class Maze():
	width = None
	height = None
	screen = False
	wall_image = False
	floor_image = False
	up_image = False
	down_image = False
	cell_size = 30
	speed = 120
	unfracturedness = 100
	the_maze = None
	
	# generation variables.  Instance variables because of step_generate
	current_x = None
	current_y = None
	walls = []
	wall = None
	wallnum = -1
	
	def __init__(self, width=51, height=51, screen=False, wall_image=False, floor_image=False, 
	up_image=False, down_image=False, cell_size=False, speed=False, unfracturedness=False):
		#only odd shapes
		self.width = (width // 2) * 2 + 1
		self.height = (height // 2) * 2 + 1
		if screen:
			self.screen = screen
			if wall_image:
				self.wall_image = wall_image
			if floor_image:
				self.floor_image = floor_image
			if up_image:
				self.up_image = up_image
			if down_image:
				self.down_image = down_image
			if cell_size:
				self.cell_size = cell_size
			if speed:
				self.speed = speed
		if unfracturedness:
			self.unfracturedness = unfracturedness
		
	def is_dead_end(self, maze, cell):
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
			
	# resets the maze as if a new one had been created
	def reset(self):
		self.the_maze = None
	
		# generation variables.  Instance variables because of step_generate
		self.current_x = None
		self.current_y = None
		self.walls = []
		self.wall = None
		self.wallnum = -1
			
	def generate(self, animate = False):
		# If a screen was passed in then set up drawing
		if self.screen and animate:
			pygame.init()
			clock = pygame.time.Clock()
		
		# initialize maze with all walls and cells filled in
		self.the_maze = numpy.zeros((self.width, self.height), dtype=int)
		if self.screen and animate:
			for i in range(self.width):
				for j in range(self.height):
					self.screen.blit(self.wall_image, [i * self.cell_size, j * self.cell_size])
			pygame.display.flip()
			clock.tick(self.speed)
		
		# start building maze
		current_x = rand(1, self.width // 2) * 2 - 1
		current_y = rand(1, self.height // 2) * 2 - 1
		# 0 means filled in, 1 means dug out, 2 means start, and 3 means finish
		self.the_maze[current_x, current_y] = 2
		if self.screen and animate:
			self.screen.blit(self.up_image, [current_x * self.cell_size, current_y * self.cell_size])
			pygame.display.flip()
			clock.tick(self.speed)
		
		# a list of neighbouring walls to be potentially removed, the cells on the other side, and the originating cell.  
		# A wall looks like x, y, next cell x, next cell y, original cell x, original cell y
		walls = [(current_x, current_y - 1, current_x, current_y - 2, current_x, current_y)]
		walls.append((current_x + 1, current_y, current_x + 2, current_y, current_x, current_y))
		walls.append((current_x, current_y + 1, current_x, current_y + 2, current_x, current_y))
		walls.append((current_x - 1, current_y, current_x - 2, current_y, current_x, current_y))
	
		# the main maze building loop continues until it runs out of walls
		while len(walls):
			#keep picking walls until you find a dead end or look at x number of walls 
			for i in range(self.unfracturedness + 1):
				wallnum = rand(0, len(walls) -1)
				wall = walls[wallnum]
				if self.is_dead_end(self.the_maze, (wall[4], wall[5])):
					break
			# we found a wall to examine so remove it from the list
			walls.pop(wallnum)
			
			# if the wall belongs to a border then ignore it
			if wall[0] == 0 or wall[1] == 0 or wall[0] == self.width - 1 or wall[1] == self.height - 1:
				continue
			# checks if the cell on the other side is already part of the maze
			elif self.the_maze[wall[2], wall[3]]:
				continue
			else:
				# the wall and the next cell become passages
				self.the_maze[wall[0], wall[1]] = 1
				self.the_maze[wall[2], wall[3]] = 1
				# add the new cell to current and add its walls to walls
				current_x = wall[2]
				current_y = wall[3]
				walls.append((current_x, current_y - 1, current_x, current_y - 2, current_x, current_y))
				walls.append((current_x + 1, current_y, current_x + 2, current_y, current_x, current_y))
				walls.append((current_x, current_y + 1, current_x, current_y + 2, current_x, current_y))
				walls.append((current_x - 1, current_y, current_x - 2, current_y, current_x, current_y))
				
				#draw the new passage if necessary
				if self.screen and animate:
					self.screen.blit(self.floor_image, [wall[0] * self.cell_size, wall[1] * self.cell_size])
					self.screen.blit(self.floor_image, [wall[2] * self.cell_size, wall[3] * self.cell_size])
					pygame.display.flip()
					clock.tick(self.speed)
					
		# the last cell dug out becomes the finish
		self.the_maze[current_x, current_y] = 3
		if self.screen and animate:
			self.screen.blit(self.down_image, [current_x * self.cell_size, current_y * self.cell_size])
			pygame.display.flip()
			clock.tick(self.speed)
		return self.the_maze
		
	def step_generate(self):
		if self.wallnum == -1 and not self.the_maze == None:
			return self.the_maze
		if self.wallnum == -1:
			# initialize maze with all walls and cells filled in
			self.the_maze = numpy.zeros((self.width, self.height), dtype=int)
			
			# start building maze
			self.current_x = rand(1, self.width // 2) * 2 - 1
			self.current_y = rand(1, self.height // 2) * 2 - 1
			# 0 means filled in, 1 means dug out, 2 means start, and 3 means finish
			self.the_maze[self.current_x, self.current_y] = 2
			
			# a list of neighbouring walls to be potentially removed, the cells on the other side, and the originating cell.  
			# A wall looks like x, y, next cell x, next cell y, original cell x, original cell y
			self.walls = [(self.current_x, self.current_y - 1, self.current_x, self.current_y - 2, self.current_x, self.current_y)]
			self.walls.append((self.current_x + 1, self.current_y, self.current_x + 2, self.current_y, self.current_x, self.current_y))
			self.walls.append((self.current_x, self.current_y + 1, self.current_x, self.current_y + 2, self.current_x, self.current_y))
			self.walls.append((self.current_x - 1, self.current_y, self.current_x - 2, self.current_y, self.current_x, self.current_y))
			self.wallnum = 0
			return self.the_maze
	
		# the main maze building loop continues until it runs out of walls
		while len(self.walls):
			#keep picking walls until you find a dead end or look at x number of walls 
			for i in range(self.unfracturedness + 1):
				self.wallnum = rand(0, len(self.walls) -1)
				self.wall = self.walls[self.wallnum]
				if self.is_dead_end(self.the_maze, (self.wall[4], self.wall[5])):
					break
			# we found a wall to examine so remove it from the list
			self.walls.pop(self.wallnum)
			
			# if the wall belongs to a border then ignore it
			if self.wall[0] == 0 or self.wall[1] == 0 or self.wall[0] == self.width - 1 or self.wall[1] == self.height - 1:
				continue
			# checks if the cell on the other side is already part of the maze
			elif self.the_maze[self.wall[2], self.wall[3]]:
				continue
			else:
				# the wall and the next cell become passages
				self.the_maze[self.wall[0], self.wall[1]] = 1
				self.the_maze[self.wall[2], self.wall[3]] = 1
				# add the new cell to current and add its walls to walls
				self.current_x = self.wall[2]
				self.current_y = self.wall[3]
				self.walls.append((self.current_x, self.current_y - 1, self.current_x, self.current_y - 2, self.current_x, self.current_y))
				self.walls.append((self.current_x + 1, self.current_y, self.current_x + 2, self.current_y, self.current_x, self.current_y))
				self.walls.append((self.current_x, self.current_y + 1, self.current_x, self.current_y + 2, self.current_x, self.current_y))
				self.walls.append((self.current_x - 1, self.current_y, self.current_x - 2, self.current_y, self.current_x, self.current_y))
			break
		if not len(self.walls):			
			# the last cell dug out becomes the finish
			self.the_maze[self.current_x, self.current_y] = 3
			# set this so further steps will do nothing
			self.wallnum = -1
		return self.the_maze