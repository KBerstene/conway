#!/usr/bin/python

import pygame
import math
from namedtuples import *

class Grid():
	# Constructor
	def __init__(self, dimensions, location):
		# Create surface and static rect
		self.surface = pygame.Surface(dimensions)
		self.rect = self.surface.get_rect(left=location.left, top=location.top)
		
		# Calculate size of grid
		self.gridWidth = math.ceil((dimensions.width - 1) / 20)
		self.gridHeight = math.ceil((dimensions.height - 1) / 20)
	
		# Create a array of cells
		self.array = [[Cell() for x in range(self.gridHeight)] for x in range(self.gridWidth)]
		
		# Set each square's position
		for i in range(self.gridWidth):
			for j in range(self.gridHeight):
				self.array[i][j] = Cell(Position((i*20) + self.rect.left, (j*20) + self.rect.top))

	def draw(self, surface):
		# Iterate through grid and print white square as dead and black square as alive
		for row in self.array:
			for cell in row:
				pygame.draw.rect(surface, pygame.Color("black"), cell, not(cell.alive))
	
	def collidepoint(self, pos):
		if self.rect.collidepoint(pos):
			for row in self.array:
				for cell in row:
					if cell.collidepoint(pos):
						cell.alive = not(cell.alive)
						return True
		return False
	
	def resize(self, size, position):
		# Resize surface
		self.surface = pygame.transform.scale(self.surface, size)
		self.rect = self.surface.get_rect(left=position.left, top=position.top)
		
		# Recalculate size of grid
		self.gridWidth = math.ceil((size.width - 1) / 20)
		self.gridHeight = math.ceil((size.height - 1) / 20)
		
		# Create array of new size
		newArray = [[Cell() for x in range(self.gridHeight)] for x in range(self.gridWidth)]
		
		# Set each square's position
		for i in range(self.gridWidth):
			for j in range(self.gridHeight):
				try:
					newArray[i][j] = self.array[i][j]
				except (IndexError):
					newArray[i][j] = Cell(Position((i*20) + self.rect.left, (j*20) + self.rect.top))
		
		self.array = newArray

		
# Subclass of Rect to add alive/dead status
class Cell(pygame.Rect):
	# Constructor
	def __init__(self, pos=Position(0, 0), size=Dimensions(21, 21)):
		super(Cell, self).__init__((pos.left, pos.top), (size.width, size.height))
		self.alive=False
