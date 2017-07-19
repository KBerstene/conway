#!/usr/bin/python

import pygame
import math
from namedtuples import *

class Grid():
	# Constructor
	def __init__(self, dimensions, location, cellSize = Dimensions(21,21)):
		# Calculate size of grid
		self.cellSize = cellSize
		self.gridWidth = math.ceil((dimensions.width - 1) / (self.cellSize.width - 1))
		self.gridHeight = math.ceil((dimensions.height - 1) / (self.cellSize.height - 1))

		# Create constants
		self.cellSize = cellSize
		self.minSize = Dimensions(5,5)
		self.maxSize = Dimensions(100, 100)
		
		# Create surface and static rect
		self.surface = pygame.Surface(((self.gridWidth * (self.cellSize.width - 1) + 1), (self.gridHeight * (self.cellSize.height - 1) + 1)))
		self.rect = self.surface.get_rect(left=location.left, top=location.top)
		
		# Create list of cells that need to be drawn
		self.cellsToRedraw = []
	
		# Create an array of cells
		self.cells = [[Cell() for x in range(self.gridHeight)] for x in range(self.gridWidth)]
		
		# Set each square's position
		for i in range(self.gridWidth):
			for j in range(self.gridHeight):
				self.cells[i][j] = Cell(Position((i*(self.cellSize.width - 1)) + self.rect.left, (j*(self.cellSize.height - 1)) + self.rect.top), size = self.cellSize)
				self.cellsToRedraw.append(self.cells[i][j])

		# Create each cell's neighbors list
		self.createCellNeighbors()
		
	def draw(self, surface):
		# Set list of rects that will be updated and returned
		updateList = []
		
		# Iterate through cells that need to be redrawn
		for cell in self.cellsToRedraw:
			if cell.alive:
				# If it's alive, fill a solid black rectangle
				surface.fill(pygame.Color("black"), cell)
			else:
				# If it's dead, draw white and then the outline
				surface.fill(pygame.Color("white"), cell)
				pygame.draw.rect(surface, pygame.Color("black"), cell, 1)
			
			# Add cell to list to be updated
			updateList.append(cell)
		
		# Clear list of cells to be redrawn
		self.cellsToRedraw.clear()
		
		# Return list of rects to be updated on surface
		return updateList
	
	def addRow(self, prepend = False):
		pass
	
	def addColumn(self, prepend = False):
		if prepend:
			pass
		else:
			# Grid gets one wider
			self.gridWidth = self.gridWidth + 1
			
			# Create new column
			# Add new column onto end of cell array
			self.cells.append([Cell() for x in range(self.gridHeight)])
			
			# Set position for new cells in column
			i = self.gridWidth - 1
			for j in range(self.gridHeight):
				self.cells[i][j] = Cell(Position((i*(self.cellSize.width - 1)) + self.rect.left, (j*(self.cellSize.height - 1)) + self.rect.top), size = self.cellSize)
	
	def removeRow(self, rowIndex):
		for column in self.cells:
			column.pop(rowIndex)
	
	def removeColumn(self, columnIndex):
		self.cells.pop(columnIndex)
	
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
						self.cellsToRedraw.append(cell)
						return True
		return False
	
	def getCell(self, pos):
		if self.rect.collidepoint(pos):
			for row in self.cells:
				for cell in row:
					if cell.collidepoint(pos):
						return cell
		return None
	
	def getCellIndex(self, cell):
		for row in self.cells:
			try:
				# If the cell isn't in this row, it will drop into the except block
				# Once it's found, it will index the row and break out of the loop
				y = row.index(cell)
				x = self.cells.index(row)
				break
			except:
				pass
		return Coordinates(x, y)
	
	def resize(self, size, position):
		# Recalculate size of grid
		self.gridWidth = math.ceil((size.width - 1) / (self.cellSize.width - 1))
		self.gridHeight = math.ceil((size.height - 1) / (self.cellSize.height - 1))
		
		# Resize surface
		self.surface = pygame.transform.scale(self.surface, ((self.gridWidth * (self.cellSize.width - 1) + 1), (self.gridHeight * (self.cellSize.height - 1) + 1)))
		self.rect = self.surface.get_rect(left=position.left, top=position.top)
		
		# Create array of new size
		newArray = [[Cell() for x in range(self.gridHeight)] for x in range(self.gridWidth)]
		
		# Set each square's position
		for i in range(self.gridWidth):
			for j in range(self.gridHeight):
				try:
					newArray[i][j] = self.cells[i][j]
				except (IndexError):
					newArray[i][j] = Cell(Position((i*(self.cellSize.width - 1)) + self.rect.left, (j*(self.cellSize.height - 1)) + self.rect.top), size = self.cellSize)
				
				# New cell needs to be redrawn
				self.cellsToRedraw.append(newArray[i][j])
		
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
