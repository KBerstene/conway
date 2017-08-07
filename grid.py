#!/usr/bin/python

import pygame
import math
from namedtuples import *

class Grid(pygame.Rect):
	# Constructor
	def __init__(self, dimensions, location, cellSize = Dimensions(20,20)):
		# Call Rect constructor
		super().__init__(location.left, location.top, dimensions.width, dimensions.height)
		
		# Calculate size of grid
		self.cellSize = cellSize
		self.gridWidth = math.ceil((dimensions.width - 1) / (self.cellSize.width - 1))
		self.gridHeight = math.ceil((dimensions.height - 1) / (self.cellSize.height - 1))

		# Create constants
		self.minSize = Dimensions(5,5)
		self.maxSize = Dimensions(100, 100)
		
		# Create array of grid lines and populate
		# with first horizontal and vertical lines
		self.gridLines = [[((0, 0), (self.width, 0))], [((0, 0), (0, self.height))]]
		
		# Create grid lines
		self.addLines()
		
		# Create dict for cells to be called by coordinates
		self.cells = {}
		
		# Create list of cells that need to be drawn
		self.cellsToRedraw = []
		
		# Create list of cells that need to be dead/alive
		self.cellsToCalc = []
		
		# Create redraw flags
		self.redrawAll = True
		self.redrawGrid = True
	
	###########################################
	# DRAWING METHODS                         #
	###########################################
	
	def draw(self, surface):
		# Set list of sections to be update
		updateList = []
	
		# Check if everything should be redrawn
		if self.redrawAll:
			# Fill background
			surface.fill(pygame.Color("grey"))
			# Tell grid to redraw
			self.redrawGrid = True
			# Tell cells to redraw
			pass
		
		# Check to redraw grid lines
		if self.redrawGrid:
			for lines in self.gridLines:
				for gridLine in lines:
					pygame.draw.polygon(surface, pygame.Color("black"), gridLine, 1)
		
		# Check cells to redraw
		for cell in self.cellsToRedraw:
			updateList.append(cell.draw(surface))
		
		# Pass whole grid rect and reset flags if needed
		if self.redrawAll or self.redrawGrid:
			self.redrawAll = False
			self.redrawGrid = False
			updateList = [self]
		
		return updateList
		
		
		#################
		#      OLD      #
		#################
		
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
		self.redrawAll = True
	
	###########################################
	# GRID SIZE MANIPULATION METHODS          #
	###########################################
	
	def addLines(self):
		#################################################
		# A note on the ordering of gridline arrays:    #
		# The four parts, in order, are:                #
		#   0: Horizontal lines; 1: Vertical lines      #
		#   Index of the tuple of line coordinates      #
		#   The set of coordinates (2 per line)         #
		#   0: x-coordinate; 1: y-coordinate            #
		#################################################
	
		# Add horizontal
		while self.gridLines[0][-1][0][1] < self.height:
			nextTop = self.gridLines[0][-1][0][1] + self.cellSize.height
			self.gridLines[0].append(((0, nextTop), (self.width, nextTop)))
		
		# Add vertical
		while self.gridLines[1][-1][0][0] < self.width:
			nextLeft = self.gridLines[1][-1][0][0] + self.cellSize.width
			self.gridLines[1].append(((nextLeft, 0), (nextLeft, self.height)))
		
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
		else:
			# Create new column
			# Add new column onto end of cell array
			self.cells.append([None for x in range(self.gridHeight)])
			
			# Set position for new cells in column
			i = self.gridWidth - 2
			for j in range(self.gridHeight):
				self.cells[i+1][j] = Cell(Position(self.cells[i][j].left + self.cellSize.width - 1, self.cells[i][j].top), size = self.cellSize)
			
		# After new column is created, create neighbors for each cell
		# and update neighbors for cells in the column next to it
		self.createColumnNeighbors(i)
		self.createColumnNeighbors(i+1)
		
	def addRow(self, prepend = False):
		# Grid gets one taller
		self.gridHeight = self.gridHeight + 1
		
		if prepend:
			# Add a cell into each column to form a new row
			j = 0
			for i in range(self.gridWidth):
				self.cells[i].insert(0, Cell(Position(self.cells[i][j].left, self.cells[i][j].top - self.cellSize.height + 1), size = self.cellSize))
		else:
			# Add a cell into each column to form a new row
			j = self.gridHeight - 2
			for i in range(self.gridWidth):
				self.cells[i].append(Cell(Position(self.cells[i][j].left, self.cells[i][j].top + self.cellSize.height - 1), size = self.cellSize))
			
		# After new row is created, create neighbors for each cell
		# and update neighbors for cells in the row next to it
		self.createRowNeighbors(j)
		self.createRowNeighbors(j+1)
				
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
	
	def removeColumn(self, columnIndex):
		self.cells.pop(columnIndex)
		
		# Grid gets one thinner
		self.gridWidth = self.gridWidth - 1
	
	def removeRow(self, rowIndex):
		for column in self.cells:
			column.pop(rowIndex)
		
		# Grid gets one shorter
		self.gridHeight = self.gridHeight - 1
	
	def resize(self, size, location):
		# Currently not working
		return
		
		# Add and remove cells that have moved on or off screen
		self.autoAddRemoveCells(size)
		
		# Reset constants
		self.left=location.left
		self.top=location.top
		self.width=size.width
		self.height=size.height
		
		# Schedule all cells for redrawAll
		self.redrawAll()
	
	###########################################
	# NEIGHBOR CREATION METHODS               #
	###########################################
	
	def createCell(self, pos):
		# Locate cell position on screen
		posx = math.floor(pos[0]/self.cellSize.width)
		posy = math.floor(pos[1]/self.cellSize.height)
		
		# Find cell grid coordinates
		if len(self.cells) == 0:
			x = 0
			y = 0
		else:
			origin = self.cells[(0,0)].center
			xDiff = pos[0] - origin[0]
			yDiff = pos[1] - origin[1]
			
			x = round(xDiff / self.cellSize.width)
			y = round(yDiff / self.cellSize.height)
			
		# Create new cell
		newCell = Cell(Coordinates(x, y), Position(posx * self.cellSize.width, posy * self.cellSize.height), self.cellSize)
		
		# Add cell to list and dict
		self.cells[(x, y)] = newCell
		
		# Set new cell to redraw
		self.cellsToRedraw.append(newCell)
		
		return newCell

	def createNeighbors(self, cell):
		cell.neighbors = []
		
		for j in range(-1, 2):
			for i in range (-1, 2):
				relativeCoords = (cell.coords[0] + i, cell.coords[1] + j)
				if relativeCoords in self.cells:
					cell.neighbors.append(self.cells[relativeCoords])
				else:
					self.createCell(pos = (cell.centerx + (self.cellSize.width * i), cell.centery + (self.cellSize.height * j)))
					cell.neighbors.append(self.cells[relativeCoords])
		
		# Remove the cell itself as a neighbor
		cell.neighbors.pop(4)
	
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
	
	###########################################
	# CELL ISOLATION AND MANIPULATION METHODS #
	###########################################
	
	def clickCell(self, cell):
		# This method is supposed to be called
		# when a cell is left-clicked on.
		
		# Flip cell's alive status
		cell.alive = not cell.alive
		
		# Check if cell has neighbors yet
		if not cell.neighborsAdded:
			self.createNeighbors(cell)
			cell.neighborsAdded = True
		
		# Set cell for redrawing
		self.cellsToRedraw.append(cell)
		
		# Set cell for recalculation
		if not cell.added:
			self.cellsToCalc.append(cell)
			cell.added = True
		
		return cell.alive
	
	def getCell(self, pos):
		cellList = list(self.cells.values())
		index = pygame.Rect(pos, (0,0)).collidelist(cellList)
		
		if index == -1:
			return None
		else:
			return self.cells[cellList[index].coords]
	
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
		
	def indexGrid(self):
		for x in range(self.gridWidth):
			for y in range(self.gridHeight):
				self.cells[x][y].gridx = x
				self.cells[x][y].gridy = y
	

class Cell(pygame.Rect):
	# Constructor
	def __init__(self, coords = Coordinates(0, 0), pos = Position(0, 0), size = Dimensions(0, 0)):
		# Rect collision ignores their 1px borders, so the cell has to be slightly larger
		# than its border and have a rectangle that needs to be drawn slightly smaller
		# than its border
		super().__init__((pos.left - 1, pos.top - 1), (size.width + 2, size.height + 2))
		self.drawableRect = pygame.Rect((pos.left + 1, pos.top + 1), (size.width - 1, size.height - 1))
		
		# Grid coordinates
		self.coords = coords
		
		# Variables
		self.alive = False
		self.neighbors = []
		self.neighborsAdded = False
		self.added = False
		self.tempAlive = False
	
	def draw(self, surface):
		if self.alive:
			color = "black"
		else:
			color = "white"
		
		surface.fill(pygame.Color(color), self.drawableRect)
		
		return self.drawableRect
	
	def resize(self, newSize):
		self.width = newSize.width
		self.height = newSize.height
	
	def move(self, newPos):
		self.left = newPos.left
		self.top = newPos.top
