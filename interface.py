#!/usr/bin/python

import pygame
from pygame.locals import *
from algorithms import *
from namedtuples import *
from grid import Grid
from controls import Controls

class Interface():
	# Constructor
	def __init__(self, resolution = Dimensions(1001, 601), calcThread=None):
		# Declare constants
			# General
		self.fpsLimit = 60
		self.simRunning = False
		self.calcThread = calcThread
			# Section sizes
		# Control width is actually a bit flexible now.
		# The value below is the max value it will reach.
		# The minimum value it will reach is
		# (self.control_width - cell size + 1)
		# so large cells can squish it a bit.
		self.control_width = 200
			# Key presses
		self.L_SHIFT = 1
		self.R_SHIFT = 2
		self.L_CTRL = 64
		self.R_CTRL = 128
		self.L_ALT = 256
		self.R_ALT = 512
	
		# Declare variables
		self.populationLimit = 3
		self.populationMin = 2
		self.generation = 0
		
		# Initialize pygame window
		pygame.init()
		self.window = pygame.display.set_mode(resolution, pygame.RESIZABLE)
		pygame.display.set_caption("Conway's Game of Life")
		
		# Create clock to limit FPS
		self.fpsClock = pygame.time.Clock()

		# Enable key hold repeating and set limits
		pygame.key.set_repeat(500,75)
		
		# Create the initial grid
		self.grid = Grid(Dimensions(self.window.get_rect().width - self.control_width, self.window.get_rect().height), Position(0, 0))
		
		# Create control section
		self.controls = Controls(Dimensions(self.control_width, self.window.get_rect().height),
								Position(self.grid.width, 0), self)
	
	###########################################
	# MAIN INTERFACE LOOP METHODS             #
	###########################################
	
	def update(self):
		# Process any mouse/keyboard events
		if not self.processEvents():
			# Tell calcThread to exit
			self.calcThread.killswitch = True
			return False
		
		# Get list of objects to update
		updates = self.draw()
		
		# Update window
		pygame.display.update(updates)
		
		# Limit FPS
		self.fpsClock.tick(self.fpsLimit)
		
		return True
	
	def processEvents(self):
		click_pos=(-1,-1)

		# Get pygame events to see if/what key is pressed
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				return False
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1: # Left click
					if self.controls.collidepoint(pygame.mouse.get_pos()):
						pass
					elif self.grid.collidepoint(pygame.mouse.get_pos()):
						self.grid.clickCell(self.grid.getCell(pygame.mouse.get_pos()))
				elif event.button == 4: # Scroll wheel up
					self.zoomIn(pygame.mouse.get_pos()) # Zoom in
				elif event.button == 5: # Scroll wheel down
					self.zoomOut(pygame.mouse.get_pos()) # Zoom out
				else:
					pass
			elif event.type == KEYDOWN:
				mods = pygame.key.get_mods()# Get modifier keys
				if event.key == K_LEFT:
					if mods == self.L_SHIFT:
						self.popLimitDown()
					elif mods == self.L_CTRL:
						self.popMinDown()
					else:
						self.speedDown()
				elif event.key == K_RIGHT:
					if mods == self.L_SHIFT:
						self.popLimitUp()
					elif mods == self.L_CTRL:
						self.popMinUp()
					else:
						self.speedUp()
				elif event.key == K_SPACE:
					self.pause()
				elif event.key == K_RETURN:
					self.stepForward()
				else:
					pass
			elif event.type == VIDEORESIZE:
				self.resize(event.dict['size'])
			else:
				pass
		return True
	
	###########################################
	# DRAWING AND SIZE MANIPULATION METHODS   #
	###########################################
	
	def draw(self):
		# Set list of rects that will be updated and returned
		updateList = []
		
		# Draw grid
		updateList.extend(self.grid.draw(self.window))
		
		# Draw control interface
		updateList.extend(self.controls.draw(self.window))
		
		# Return list of rects to be updated
		return updateList
	
	def resize(self, size):
		self.window = pygame.display.set_mode(size, pygame.RESIZABLE)
		self.grid.resize(Dimensions(self.window.get_rect().width - self.control_width, self.window.get_rect().height), Position(0, 0))
		self.controls.resize(Dimensions(self.control_width, self.window.get_rect().height), Position(self.grid.width, 0))
	
	def zoomIn(self, pos, sizeChange = 2):
		##############################################
		# Get necessary constants for error checking #
		##############################################
		
		# Find the new size of the cell
		newSize = Dimensions(self.grid.cellSize.width + sizeChange, self.grid.cellSize.height + sizeChange)
		
		# Get the cell that was zoomed in on
		zoomedCell = self.grid.getCell(pos)
		
		############################################
		# Make sure that this zoom action is valid #
		############################################
		
		# Make sure we're not going outside of size limits
		if (newSize <= self.grid.minSize) or (newSize >= self.grid.maxSize):
			return
		# If no cell was zoomed in on, quit now
		if zoomedCell == None:
			return
		
		########################################
		# Calculate new cell position based on #
		# current mouse location               #
		########################################
		
		# Find position of cursor relative to the cell (should be from 0 to cell width)
		relativePos = Position(pos[0] - zoomedCell.left, pos[1] - zoomedCell.top)
		# Find the ratio between the relative pos and the cell size
		posRatio = Position(relativePos.left/zoomedCell.width, relativePos.top/zoomedCell.height)
		# Calculate the new position of the cell.
		newPos = Position(zoomedCell.left - (posRatio.left*sizeChange), zoomedCell.top - (posRatio.top*sizeChange))
		
		#######################################
		# Move and resize all cells in grid   #
		# based on zoomed cell's new location #
		#######################################
		
		# Find the index of the cell that was zoomed on
		index = self.grid.getCellIndex(zoomedCell) # Returns a tuple with the x/y position in the cell array
		
		# Using the index, we can calculate how far away the cells should be from the zoomed cell.
		# While we're iterating through, we also resize each cell (so we only iterate once).
		for x in range(len(self.grid.cells)):
			for y in range(len(self.grid.cells[x])):
				self.grid.cells[x][y].resize(newSize)
				self.grid.cells[x][y].move(Position(newPos.left - ((newSize.width - 1)*(index.x - x)), newPos.top - ((newSize.height - 1)*(index.y - y))))
				
				# This is supposed to fix a minor cell-wall-width variation I only see in the top row or left column
				# 2017-07-17 Kevin T. Berstene
				if self.grid.cells[x][y].x <= 0:
					self.grid.cells[x][y].move(Position(self.grid.cells[x][y].x - 1, self.grid.cells[x][y].y))
				if self.grid.cells[x][y].y <= 0:
					self.grid.cells[x][y].move(Position(self.grid.cells[x][y].x, self.grid.cells[x][y].y - 1))
		
		# Set new grid cellSize
		# This needs to be done before adding cells
		# so any added cells will be of the right size
		self.grid.cellSize = newSize
		
		########################################################
		# Add or remove cells that have moved on or off screen #
		########################################################
		
		self.grid.autoAddRemoveCells()
	
		#########################################
		# Schedule entire grid for redrawing    #
		#########################################
		
		self.grid.redrawAll()
	
	def zoomOut(self, pos, sizeChange = 2):
		# Do everything zoom out does,
		# but with negative sizeChange
		self.zoomIn(pos, 0 - sizeChange)
	
	##################################################
	# SIMULATION CONTROLS AND PARAMETER MANIPULATION #
	##################################################
	
	def pause(self):
		self.simRunning = not(self.simRunning)
		self.controls.updateStatusDisplay(self.simRunning)
	
	def popLimitDown(self):
		if self.populationLimit > 1:
			self.populationLimit -= 1
			self.controls.updatePopLimitDisplay(self.populationLimit)
			
	def popLimitUp(self):
		if self.populationLimit < 8:
			self.populationLimit += 1
			self.controls.updatePopLimitDisplay(self.populationLimit)
	
	def popMinDown(self):
		if self.populationMin > 1:
			self.populationMin -= 1
			self.controls.updatePopMinDisplay(self.populationMin)
	
	def popMinUp(self):
		if self.populationMin < 8:
			self.populationMin += 1
			self.controls.updatePopMinDisplay(self.populationMin)
			
	def reset(self):
		self.__init__(Dimensions(self.window.get_rect().width, self.window.get_rect().height), self.calcThread)
		self.calcThread.__init__(self)
	
	def setCalcThread(self,calcThread):
		self.calcThread = calcThread
		self.controls.updateSpeedDisplay(self.calcThread.speed)
	
	def speedDown(self):
		if (self.calcThread.speed > 1):
			self.calcThread.speed -= 1
			self.controls.updateSpeedDisplay(self.calcThread.speed)
	
	def speedUp(self):
		self.calcThread.speed += 1
		self.controls.updateSpeedDisplay(self.calcThread.speed)
	
	def stepForward(self):
		if self.simRunning:
			self.pause()
		self.calcThread.calc()
		return self.simRunning
	