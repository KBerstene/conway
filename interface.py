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
		self.control_width = 200
		
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
								Position(self.grid.rect.width, 0), self)


	def setCalcThread(self,calcThread):
		self.calcThread = calcThread
		self.controls.updateSpeedDisplay(self.calcThread.speed)
		
	def update(self):
		# Process any mouse/keyboard events
		if not self.processEvents():
			return False

		# Draw objects
		self.draw()

		# Update window
		pygame.display.update()
		
		# Limit FPS
		self.fpsClock.tick(self.fpsLimit)

		return True
		
	def processEvents(self):
		click_pos=(-1,-1)

		# Get pygame events to see if exit is called
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				return False
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1: # Left click
					self.controls.collidepoint(pygame.mouse.get_pos())
					self.grid.collidepoint(pygame.mouse.get_pos())
				elif event.button == 4: # Scroll wheel up
					self.zoomIn(pygame.mouse.get_pos()) # Zoom in
				elif event.button == 5: # Scroll wheel down
					self.zoomOut(pygame.mouse.get_pos()) # Zoom out
				else:
					pass
			elif event.type == KEYDOWN:
				if event.key == K_LEFT:
					self.speedDown()
					self.controls.updateSpeedDisplay(self.calcThread.speed)
				elif event.key == K_RIGHT:
					self.speedUp()
					self.controls.updateSpeedDisplay(self.calcThread.speed)
				elif event.key == K_SPACE:
					self.pause()
				else:
					pass
			elif event.type == VIDEORESIZE:
				self.resize(event.dict['size'])
			else:
				pass
		return True
	
	def draw(self):
		# Set background as white
		self.window.fill(pygame.Color("white"))

		# Draw grid
		self.grid.draw(self.window)

		# Draw control interface
		self.controls.draw(self.window)

	def resize(self, size):
		# Resize window
		self.window = pygame.display.set_mode(size, pygame.RESIZABLE)
		
		# Resize grid
		if (self.window.get_rect().width < self.control_width):
			# Grid size is less than zero, so set it to 2x2 pixels instead
			# (which should create a single cell).
			# It will get covered by the controls, anyway.
			# If grid is 0x0 and the calcThread starts, it will crash
			self.grid.resize(Dimensions(2, 2), Position(0, 0))
		else:
			self.grid.resize(Dimensions(self.window.get_rect().width - self.control_width, self.window.get_rect().height), Position(0, 0))
		
		# Resize controls
		self.controls.resize(Dimensions(self.control_width, self.window.get_rect().height), Position(self.grid.rect.width, 0))
	
	def reset(self):
		self.__init__(Dimensions(self.window.get_rect().width, self.window.get_rect().height), self.calcThread)
		self.calcThread.__init__(self)

	#################################
	# Simulation speed manipulation #
	#################################
	def pause(self):
		self.simRunning = not(self.simRunning)
		self.controls.updateStatusDisplay(self.simRunning)

	def speedUp(self):
		self.calcThread.speed += 1
		self.controls.updateSpeedDisplay(self.calcThread.speed)
	
	def speedDown(self):
		if (self.calcThread.speed > 1):
			self.calcThread.speed -= 1
			self.controls.updateSpeedDisplay(self.calcThread.speed)
	
	def stepForward(self):
		if self.simRunning:
			self.pause()
		self.calcThread.calc()

	################################
	# Visual size manipulation     #
	################################
	def resize(self, size):
		self.window = pygame.display.set_mode(size, pygame.RESIZABLE)
		self.grid.resize(Dimensions(self.window.get_rect().width - self.control_width, self.window.get_rect().height), Position(0, 0))
		self.controls.resize(Dimensions(self.control_width, self.window.get_rect().height), Position(self.grid.rect.width, 0))
	
	def zoomIn(self, pos, sizeChange = 2):
		# Find the new size of the cell
		newSize = Dimensions(self.grid.cellSize.width + sizeChange, self.grid.cellSize.height + sizeChange)
		
		# Make sure we're not going outside of size limits
		if (newSize <= self.grid.minSize) or (newSize >= self.grid.maxSize):
			return
		
		# Get the cell that was zoomed in on
		zoomedCell = self.grid.getCell(pos)
		
		# If no cell was zoomed in on, quit now
		if zoomedCell == None:
			return
		
		# Calculate where the cell should be under the mouse after resizing
			# Find position of cursor relative to the cell (should be from 0 to cell width)
		relativePos = Position(pos[0] - zoomedCell.left, pos[1] - zoomedCell.top)
			# Find the ratio between the relative pos and the cell size
		posRatio = Position(relativePos.left/zoomedCell.width, relativePos.top/zoomedCell.height)
			# Calculate the new position of the cell.
		newPos = Position(zoomedCell.left - (posRatio.left*sizeChange), zoomedCell.top - (posRatio.top*sizeChange))
			
		# Resize and move first cell
		# zoomedCell.resize(newSize)
		# zoomedCell.move(newPos)
		
		# Now we have a size for the cells and a grid location to start on
		# Find the index of the cell that was zoomed on
		index = self.grid.getCellIndex(zoomedCell) # Returns a tuple with the x/y position in the cell array
		
		# Using the index, we can calculate how far away the cells should be from the zoomed cell.
		# While we're iterating through, we also resize each cell.
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
		
		####################################
		# AFTER ZOOM, ADD OR REMOVE ADDITIONAL CELLS
		####################################
		
		# Set new grid cellSize
		self.grid.cellSize = newSize
	
	def zoomOut(self, pos, sizeChange = 2):
		self.zoomIn(pos, 0 - sizeChange)
