#!/usr/bin/python

import pygame
import math
from namedtuples import *

class Grid():
	# Constructor
	def __init__(self, dimensions, location, cellSize = Dimensions(21,21)):
		# Create surface and static rect
		self.surface = pygame.Surface(dimensions)
		self.rect = self.surface.get_rect(left=location.left, top=location.top)
		
		# Calculate size of grid
		self.gridWidth = math.ceil((dimensions.width - 1) / (cellSize.width - 1))
		self.gridHeight = math.ceil((dimensions.height - 1) / (cellSize.height - 1))
	
		# Create an array of cells
		self.cells = [[Cell() for x in range(self.gridHeight)] for x in range(self.gridWidth)]
		
		# Set each square's position
		for i in range(self.gridWidth):
			for j in range(self.gridHeight):
				self.cells[i][j] = Cell(Position((i*(cellSize.width - 1)) + self.rect.left, (j*(cellSize.height - 1)) + self.rect.top), size = cellSize)

		# Create each cell's neighbors list
		self.createCellNeighbors()
		
	def draw(self, surface):
		# Iterate through grid and print white square as dead and black square as alive
		for row in self.cells:
			for cell in row:
				pygame.draw.rect(surface, pygame.Color("black"), cell, not(cell.alive))
	
	def createCellNeighbors(self):
		# Create neighbors list for each cell
		for i in range(self.gridWidth):
			for j in range(self.gridHeight):
			# Clear neighbors list
				self.cells[i][j].neighbors = []
				
			# Top left
				if i > 0 and j > 0: self.cells[i][j].neighbors.append(self.cells[i-1][j-1])
			# Top middle
				if j > 0: self.cells[i][j].neighbors.append(self.cells[i][j-1])
			# Top right
				if j > 0 and i + 1 < self.gridWidth: self.cells[i][j].neighbors.append(self.cells[i+1][j-1])
				
			# Left
				if i > 0: self.cells[i][j].neighbors.append(self.cells[i-1][j])
			# Right
				try: self.cells[i][j].neighbors.append(self.cells[i+1][j])
				except: pass
				
			# Bottom left
				if i > 0 and j + 1 < self.gridHeight: self.cells[i][j].neighbors.append(self.cells[i-1][j+1])
			# Bottom middle
				try: self.cells[i][j].neighbors.append(self.cells[i][j+1])
				except: pass
			# Bottom right
				try: self.cells[i][j].neighbors.append(self.cells[i+1][j+1])
				except: pass
	
	def collidepoint(self, pos):
		if self.rect.collidepoint(pos):
			for row in self.cells:
				for cell in row:
					if cell.collidepoint(pos):
						cell.alive = not(cell.alive)
						return True
		return False
	
	def getCell(self, pos):
		if self.rect.collidepoint(pos):
			for row in self.cells:
				for cell in row:
					if cell.collidepoint(pos):
						return cell
		return None
	
	def resize(self, size, position):
		# Resize surface
		self.surface = pygame.transform.scale(self.surface, size)
		self.rect = self.surface.get_rect(left=position.left, top=position.top)
		
		# Recalculate size of grid
		self.gridWidth = math.ceil((size.width - 1) / (self.cells[0][0].width - 1))
		self.gridHeight = math.ceil((size.height - 1) / (self.cells[0][0].height - 1))
		
		# Create array of new size
		newArray = [[Cell() for x in range(self.gridHeight)] for x in range(self.gridWidth)]
		
		# Set each square's position
		for i in range(self.gridWidth):
			for j in range(self.gridHeight):
				try:
					newArray[i][j] = self.cells[i][j]
				except (IndexError):
					newArray[i][j] = Cell(Position((i*(self.cells[0][0].width - 1)) + self.rect.left, (j*(self.cells[0][0].height - 1)) + self.rect.top), size = self.cellSize)
		
		self.cells = newArray
		self.createCellNeighbors()
	
	
# Subclass of Rect to add alive/dead status
class Cell(pygame.Rect):
	# Constructor
	def __init__(self, pos=Position(0, 0), size=Dimensions(21, 21)):
		super(Cell, self).__init__((pos.left, pos.top), (size.width, size.height))
		self.alive=False
		self.neighbors=[]
	
	def resize(self, newSize):
		self.width = newSize.width
		self.height = newSize.height
	
	def move(self, newPos):
		self.left = newPos.left
		self.top = newPos.top
