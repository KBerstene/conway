#!/usr/bin/python

import pygame
import math
from namedtuples import *

class Grid(pygame.Rect):
	# Constructor
	def __init__(self, dimensions, location, cellSize = Dimensions(21,21)):
		# Calculate size of grid
		self.cellSize = cellSize
		self.gridWidth = math.ceil((dimensions.width - 1) / (self.cellSize.width - 1))
		self.gridHeight = math.ceil((dimensions.height - 1) / (self.cellSize.height - 1))

		# Call Rect constructor
		super().__init__(location.left, location.top, (self.gridWidth * (self.cellSize.width - 1) + 1), (self.gridHeight * (self.cellSize.height - 1) + 1))
		
		# Create constants
		self.cellSize = cellSize
		self.minSize = Dimensions(5,5)
		self.maxSize = Dimensions(100, 100)
		
		# Create list of cells that need to be drawn
		self.cellsToRedraw = []
	
		# Create an array of cells
		self.cells = [[Cell() for x in range(self.gridHeight)] for x in range(self.gridWidth)]
		
		# Set each square's position
		for i in range(self.gridWidth):
			for j in range(self.gridHeight):
				self.cells[i][j] = Cell(Position((i*(self.cellSize.width - 1)) + self.left, (j*(self.cellSize.height - 1)) + self.top), size = self.cellSize)
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
	
	def redrawAll(self):
		for row in self.cells:
			for cell in row:
				self.cellsToRedraw.append(cell)
	
	def autoAddRemoveCells(self, size = None):
		# I can't assign self attributes as a default parameter value,
		# so if size isn't passed, assign the default value here.
		if size == None:
			size = Dimensions(self.width, self.height)
	
		################################################
		# Add additional cells that have come onscreen #
		################################################
		
		# Check to add top row
		while self.cells[0][0].top > 0:
			self.addRow(prepend = True)
		
		# Check to add bottom row
		while self.cells[-1][-1].top + self.cellSize.height < size.height:
			self.addRow(prepend = False)
		
		# Check to add left column
		while self.cells[0][0].left > 0:
			self.addColumn(prepend = True)
		
		# Check to add right column
		while self.cells[-1][-1].left + self.cellSize.width < size.width:
			self.addColumn(prepend = False)
		
		##########################################
		# Remove cells that have moved offscreen #
		##########################################
		
		# Check to remove top rows
		while self.cells[0][0].top + self.cellSize.height < 0:
			self.removeRow(0)
		
		# Check to remove bottom rows
		while self.cells[-1][-1].top > size.height:
			self.removeRow(-1)
		
		# Check to remove left columns
		while self.cells[0][0].left + self.cellSize.width < 0:
			self.removeColumn(0)
		
		# Check to remove right columns
		while self.cells[-1][-1].left > size.width:
			self.removeColumn(-1)
	
	def addRow(self, prepend = False):
		# Grid gets one taller
		self.gridHeight = self.gridHeight + 1
		
		if prepend:
			# Add a cell into each column to form a new row
			j = 0
			for i in range(self.gridWidth):
				self.cells[i].insert(0, Cell(Position(self.cells[i][j].left, self.cells[i][j].top - self.cellSize.height + 1), size = self.cellSize))
				
			# After new row is created, create neighbors for each cell
			# and update neighbors for cells in the row next to it
			self.createRowNeighbors(j)
			self.createRowNeighbors(j+1)
		else:
			# Add a cell into each column to form a new row
			j = self.gridHeight - 2
			for i in range(self.gridWidth):
				self.cells[i].append(Cell(Position(self.cells[i][j].left, self.cells[i][j].top + self.cellSize.height - 1), size = self.cellSize))
			
			# After new row is created, create neighbors for each cell
			# and update neighbors for cells in the row next to it
			self.createRowNeighbors(j)
			self.createRowNeighbors(j-1)
				
	def addColumn(self, prepend = False):
		# Grid gets one wider
		self.gridWidth = self.gridWidth + 1
		
		if prepend:
			# Create new column
			# Add new column onto end of cell array
			self.cells.insert(0, [None for x in range(self.gridHeight)])
			
			# Set position for new cells in column
			i = 0
			for j in range(self.gridHeight):
				self.cells[i][j] = Cell(Position(self.cells[i+1][j].left - self.cellSize.width + 1, self.cells[i+1][j].top), size = self.cellSize)
			
			# After new column is created, create neighbors for each cell
			# and update neighbors for cells in the column next to it
			self.createColumnNeighbors(i)
			self.createColumnNeighbors(i+1)
		else:
			# Create new column
			# Add new column onto end of cell array
			self.cells.append([None for x in range(self.gridHeight)])
			
			# Set position for new cells in column
			i = self.gridWidth - 1
			for j in range(self.gridHeight):
				self.cells[i][j] = Cell(Position(self.cells[i-1][j].left + self.cellSize.width - 1, self.cells[i-1][j].top), size = self.cellSize)
			
			# After new column is created, create neighbors for each cell
			# and update neighbors for cells in the column next to it
			self.createColumnNeighbors(i)
			self.createColumnNeighbors(i-1)
		
	def removeRow(self, rowIndex):
		for column in self.cells:
			column.pop(rowIndex)
		
		# Grid gets one shorter
		self.gridHeight = self.gridHeight - 1
	
	def removeColumn(self, columnIndex):
		self.cells.pop(columnIndex)
		
		# Grid gets one thinner
		self.gridWidth = self.gridWidth - 1
	
	def createCellNeighbors(self):
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

	def createColumnNeighbors(self, index):
		for j in range(self.gridHeight):
			# Clear neighbors list
			self.cells[index][j].neighbors = []
				
			# Top left
			if index > 0 and j > 0: self.cells[index][j].neighbors.append(self.cells[index-1][j-1])
			# Top middle
			if j > 0: self.cells[index][j].neighbors.append(self.cells[index][j-1])
			# Top right
			if j > 0 and index + 1 < self.gridWidth: self.cells[index][j].neighbors.append(self.cells[index+1][j-1])
			
			# Left
			if index > 0: self.cells[index][j].neighbors.append(self.cells[index-1][j])
			# Right
			try: self.cells[index][j].neighbors.append(self.cells[index+1][j])
			except: pass
			
			# Bottom left
			if index > 0 and j + 1 < self.gridHeight: self.cells[index][j].neighbors.append(self.cells[index-1][j+1])
			# Bottom middle
			try: self.cells[index][j].neighbors.append(self.cells[index][j+1])
			except: pass
			# Bottom right
			try: self.cells[index][j].neighbors.append(self.cells[index+1][j+1])
			except: pass

	def createRowNeighbors(self, index):
		for i in range(self.gridWidth):
			# Clear neighbors list
			self.cells[i][index].neighbors = []
			
			# Top left
			if i > 0 and index > 0: self.cells[i][index].neighbors.append(self.cells[i-1][index-1])
			# Top middle
			if index > 0: self.cells[i][index].neighbors.append(self.cells[i][index-1])
			# Top right
			if index > 0 and i + 1 < self.gridWidth: self.cells[i][index].neighbors.append(self.cells[i+1][index-1])
		
			# Left
			if i > 0: self.cells[i][index].neighbors.append(self.cells[i-1][index])
			# Right
			try: self.cells[i][index].neighbors.append(self.cells[i+1][index])
			except: pass
		
			# Bottom left
			if i > 0 and index + 1 < self.gridHeight: self.cells[i][index].neighbors.append(self.cells[i-1][index+1])
			# Bottom middle
			try: self.cells[i][index].neighbors.append(self.cells[i][index+1])
			except: pass
			# Bottom right
			try: self.cells[i][index].neighbors.append(self.cells[i+1][index+1])
			except: pass
	
	def getCell(self, pos):
		if self.collidepoint(pos):
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
	
	# Called when a cell is left-clicked on
	def clickCell(self, cell):
		# Flip cell's alive status
		cell.alive = not cell.alive
		
		# Set cell for redrawing
		self.cellsToRedraw.append(cell)
		
	def resize(self, size, location):
		# Add and remove cells that have moved on or off screen
		self.autoAddRemoveCells(size)
		
		self.gridWidth = math.ceil((size.width - 1) / (self.cellSize.width - 1))
		self.gridHeight = math.ceil((size.height - 1) / (self.cellSize.height - 1))
		
		self.left=location.left
		self.top=location.top
		self.width=(self.gridWidth * (self.cellSize.width - 1) + 1)
		self.height=(self.gridHeight * (self.cellSize.height - 1) + 1)
		
		# Schedule all cells for redrawAll
		self.redrawAll()
	
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
