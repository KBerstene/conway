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
		
		# Create dict for cells to be called by coordinates
		self.cells = {}
		
		# Create list of cells that need to be drawn
		self.cellsToRedraw = []
		
		# Create list of cells that need to be dead/alive
		self.cellsToCalc = []
		
		# Create array of grid lines
		self.gridLines = []
		
		# Create grid lines
		self.addLines()
		
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
			surface.fill(pygame.Color("white"))
			# Tell grid to redraw
			self.redrawGrid = True
			# Tell cells to redraw
			self.cellsToRedraw = list(self.cells.values())
		
		# Check to redraw grid lines
		if self.redrawGrid:
			for lines in self.gridLines:
				for gridLine in lines:
					pygame.draw.polygon(surface, pygame.Color("black"), gridLine, 1)
		
		# Check cells to redraw
		for index in surface.get_rect().collidelistall(self.cellsToRedraw):
			updateList.append(self.cellsToRedraw[index].draw(surface))
		
		# Clear cells to redraw
		self.cellsToRedraw.clear()
		
		# Pass whole grid rect and reset flags if needed
		if self.redrawAll or self.redrawGrid:
			self.redrawAll = False
			self.redrawGrid = False
			updateList = [self]
		
		return updateList
	
	###########################################
	# GRID SIZE MANIPULATION METHODS          #
	###########################################
	
	def addLines(self):
		###################################################
		# A note on the ordering of gridline arrays:      #
		# The four parts, in order, are:                  #
		#   0: Horizontal lines; 1: Vertical lines        #
		#   0-len: Index of the tuple of line coordinates #
		#   0-1: The set of coordinates (2 per line)      #
		#   0: x-coordinate; 1: y-coordinate              #
		###################################################
		
		# Find position of origin cell
		try:
			originCellPos = (self.cells[(0,0)].left + 1, self.cells[(0,0)].top +  1)
		except KeyError:
			# If no cells yet, set origin cell's position as (0,0)
			# as though the cell had been placed in the top left corner
			originCellPos = (0,0)
		
		# Set initial two gridlines relative to origin cell's position
		posOffset = (originCellPos[0]%self.cellSize[0], originCellPos[1]%self.cellSize[1])
		self.gridLines = [[((0, posOffset[1]), (self.width - 1, posOffset[1]))], [((posOffset[0], 0), (posOffset[0], self.height - 1))]]
		
		# Add horizontal
		while self.gridLines[0][-1][0][1] < self.height - 1:
			nextTop = self.gridLines[0][-1][0][1] + self.cellSize.height
			self.gridLines[0].append(((0, nextTop), (self.width - 1, nextTop)))
		
		# Add vertical
		while self.gridLines[1][-1][0][0] < self.width - 1:
			nextLeft = self.gridLines[1][-1][0][0] + self.cellSize.width
			self.gridLines[1].append(((nextLeft, 0), (nextLeft, self.height - 1)))
	
	def resize(self, size, location):
		# Reset constants
		self.left=location.left
		self.top=location.top
		self.width=size.width
		self.height=size.height
		
		# Add grid lines
		self.addLines()
		
		# Schedule all cells for redrawAll
		self.redrawAll = True
		
	def zoom(self, pos, sizeChange = 2):
		##############################################
		# Get necessary constants for error checking #
		##############################################
		
		# Find the new size of the cell
		newSize = Dimensions(self.cellSize.width + sizeChange, self.cellSize.height + sizeChange)
		
		# Get the cell that was zoomed in on
		zoomedCell = self.getCell(pos)
		
		############################################
		# Make sure that this zoom action is valid #
		############################################
		
		# Make sure we're not going outside of size limits
		if (newSize <= self.minSize) or (newSize >= self.maxSize):
			return
		# If no cell was zoomed in on, quit now
		if zoomedCell == None:
			return
		
		########################################
		# Calculate new cell position based on #
		# current mouse location               #
		########################################
		
		# Find position of cursor relative to the cell (should be from 0 to cell width)
		relativePos = Position(pos[0] - (zoomedCell.left + 1), pos[1] - (zoomedCell.top + 1))
		# Find the ratio between the relative pos and the cell size
		posRatio = Position(relativePos.left/self.cellSize.width, relativePos.top/self.cellSize.height)
		# Calculate the new position of the cell.
		newPos = Position((zoomedCell.left + 1) - (posRatio.left*sizeChange), (zoomedCell.top + 1) - (posRatio.top*sizeChange))
	
		#######################################
		# Move and resize all cells in grid   #
		# based on zoomed cell's new location #
		#######################################
		
		# Find the index of the cell that was zoomed on
		index = zoomedCell.coords # Returns a tuple with the x/y position in the cell array
		
		# Using the index, we can calculate how far away the cells should be from the zoomed cell.
		# While we're iterating through, we also resize each cell (so we only iterate once).
		for cell in self.cells.values():
				#cell.resize(newSize)
				#cell.move(Position(newPos.left - ((newSize.width)*(index.x - cell.coords.x)), newPos.top - ((newSize.height)*(index.y - cell.coords.y))))
				cell.resizeAndMove(Position(newPos.left - ((newSize.width)*(index.x - cell.coords.x)), newPos.top - ((newSize.height)*(index.y - cell.coords.y))), newSize)
				
				# This is supposed to fix a minor cell-wall-width variation I only see in the top row or left column
				# 2017-07-17 Kevin T. Berstene
				#if cell.x <= 0:
				#	cell.move(Position(cell.x - 1, cell.y))
				#if cell.y <= 0:
				#	cell.move(Position(cell.x, cell.y - 1))
		
		# Set new grid cellSize
		# This needs to be done before adding cells
		# so any added cells will be of the right size
		self.cellSize = newSize
		
		###################################
		# Recreate grid lines at new size #
		###################################
		
		self.addLines()
	
	###########################################
	# NEIGHBOR CREATION METHODS               #
	###########################################
	
	def createCell(self, pos, coords = None):
		try:
			###############################################
			# Create cell in grid relative to origin cell #
			###############################################
			
			# Get origin cell information
			originCellPos = (self.cells[(0,0)].left + 1, self.cells[(0,0)].top + 1)
			originCenter = self.cells[(0,0)].center
			
			# Find cell grid coordinates
			if coords == None:
					xDiff = pos[0] - originCenter[0]
					yDiff = pos[1] - originCenter[1]
					
					x = round(xDiff / self.cellSize.width)
					y = round(yDiff / self.cellSize.height)
			else:
				x = coords[0]
				y = coords[1]
			
			# Create new cell relative to origin cell
			newCell = Cell(Coordinates(x, y), Position((x * self.cellSize.width) + originCellPos[0], (y * self.cellSize.height) + originCellPos[1]), self.cellSize)
		
		except KeyError:
			#############################################
			# No cells exist yet, so create origin cell #
			#############################################
			x = 0
			y = 0
			
			# Locate cell position on screen
			posx = math.floor(pos[0]/self.cellSize.width)
			posy = math.floor(pos[1]/self.cellSize.height)
			
			# Create first cell
			newCell = Cell(Coordinates(x, y), Position(posx * self.cellSize.width, posy * self.cellSize.height), self.cellSize)
		
		# Add cell to list and dict
		self.cells[(x, y)] = newCell
		self.addLines()
		self.redrawAll = True
		# Set new cell to redraw
		self.cellsToRedraw.append(newCell)
		
		return newCell
	
	def createNeighbors(self, cell, createNewCells = True):
		cell.neighbors = []
		
		for j in range(-1, 2):
			for i in range (-1, 2):
				relativeCoords = (cell.coords[0] + i, cell.coords[1] + j)
				if relativeCoords in self.cells:
					cell.neighbors.append(self.cells[relativeCoords])
				else:
					if createNewCells:
						self.createCell(pos = (cell.centerx + (self.cellSize.width * i), cell.centery + (self.cellSize.height * j)), coords = relativeCoords)
						cell.neighbors.append(self.cells[relativeCoords])
		
		# Once neighbors are created, check each of them
		# to see if they need to update their neighbors list
		if createNewCells:
			for neighbor in cell.neighbors:
				if not neighbor.neighborsAdded:
					self.createNeighbors(neighbor, createNewCells = False)
		
		# Remove the cell itself as a neighbor
		try:
			cellSelfIndex = cell.neighbors.index(cell)
			cell.neighbors.pop(cellSelfIndex)
		except ValueError:
			pass
	
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
	
	def resizeAndMove(self, pos, size):
		super().__init__((pos.left - 1, pos.top - 1), (size.width + 2, size.height + 2))
		self.drawableRect = pygame.Rect((pos.left + 1, pos.top + 1), (size.width - 1, size.height - 1))

	def draw(self, surface):
		if self.alive:
			color = "black"
		else:
			color = "white"
		
		if self.drawableRect.left < 0:
			if self.drawableRect.top < 0:
				tempRect = pygame.Rect(0, 0, self.drawableRect.width + self.drawableRect.left, self.drawableRect.height + self.drawableRect.top)
			else:
				tempRect = pygame.Rect(0, self.drawableRect.top, self.drawableRect.width + self.drawableRect.left, self.drawableRect.height)
		else:
			if self.drawableRect.top < 0:
				tempRect = pygame.Rect(self.drawableRect.left, 0, self.drawableRect.width, self.drawableRect.height + self.drawableRect.top)
			else:
				tempRect = self.drawableRect

		surface.fill(pygame.Color(color), tempRect)
		
		return tempRect
	
