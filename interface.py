#!/usr/bin/python

import pygame
from pygame.locals import *
from time import time
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
		
		# Declare variables
		self.populationLimit = 3
		self.populationMin = 2
		self.generation = 0
		
		# Declare mouse event flags
		self.processMouse = False
		self.multiCellDrag = False
		self.multiCellDragState = True
		self.mouseHeld = False
		self.mouseRepeatDelayed = False
		self.mouseClickTime = 0
		
		# Initialize pygame window
		pygame.init()
		self.window = pygame.display.set_mode(resolution, pygame.RESIZABLE)
		pygame.display.set_caption("Conway's Game of Life")
		
		# Create clock to limit FPS
		self.fpsClock = pygame.time.Clock()

		# Enable key and mouse hold repeating and set limits
		pygame.key.set_repeat(500,75)
		self.mouseRepeat = (500, 75)
		
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
				if event.button <= 3: # Left, middle, or right click get special processing
					# Turn mouse processing on
					self.processMouse = True
					# Pretend like the delay has gone through so
					# the first click will process
					self.mouseRepeatDelayed = True
					# Set a very long time in the future so the interval will process
					self.mouseClickTime = time() + time()
				elif event.button == 4: # Scroll wheel up
					self.zoomIn(pygame.mouse.get_pos()) # Zoom in
				elif event.button == 5: # Scroll wheel down
					self.zoomOut(pygame.mouse.get_pos()) # Zoom out
				else:
					pass
			elif event.type == MOUSEBUTTONUP:
				# Turn mouse processing off
				self.processMouse = False
				# Reset mouse flags
				self.multiCellDrag = False
				self.mouseHeld = False
			elif event.type == MOUSEMOTION:
				if self.processMouse:
					self.multiCellDrag = True
			elif event.type == KEYDOWN:
				mods = pygame.key.get_mods()# Get modifier keys
				if event.key == K_LEFT:
					if mods == KMOD_LSHIFT:
						self.popLimitDown()
					elif mods == KMOD_LCTRL:
						self.popMinDown()
					else:
						self.speedDown()
				elif event.key == K_RIGHT:
					if mods == KMOD_LSHIFT:
						self.popLimitUp()
					elif mods == KMOD_LCTRL:
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
		
		if self.processMouse:
			self.processMouseEvents()
		return True
	
	def processMouseEvents(self):
		# Get current time
		currentTime = time()
		
		# Get mouse info
		leftClick = pygame.mouse.get_pressed()[0] # Left click
		middleClick = pygame.mouse.get_pressed()[1] # Middle click
		rightClick = pygame.mouse.get_pressed()[2] # Right click
		mousePos = pygame.mouse.get_pos()
		
		###########################################################
		# Process mouse events that only happen once              #
		###########################################################
		
		if not self.mouseHeld:
			if leftClick:
				if self.controls.collidepoint(mousePos):
					pass
			if middleClick:
				pass
			if rightClick:
				pass
		
		###########################################################
		# Process instantly repeated mouse events                 #
		###########################################################
		
		if leftClick:
			if self.grid.collidepoint(mousePos):
				clickedCell = self.grid.getCell(mousePos)
				if clickedCell == None:
					clickedCell = self.grid.createCell(mousePos)
				
				if not self.mouseHeld:
					# Activate the cell to change its alive status
					# We want to be able to drag its new status onto other cells
					self.multiCellDragState = self.grid.clickCell(clickedCell)
				elif self.multiCellDrag:
					# If we are trying to bring multiple cells to life,
					# then check the clicked cell's alive state before
					# clicking on it.
					if clickedCell.alive != self.multiCellDragState:
						self.grid.clickCell(clickedCell)
		if middleClick:
			pass
		if rightClick:
			pass
		
		###########################################################
		# Process mouse events that repeat, but need delay        #
		###########################################################
		
		# See if delay is needed
		if self.mouseHeld:
			# Has enough time passed since the first delay?
			if (not self.mouseRepeatDelayed) and (currentTime - self.mouseClickTime < (self.mouseRepeat[0]/1000)):
				return
		
			# Enough time has passed since the first delay, skip delay check next time
			self.mouseRepeatDelayed = True
		
			# Has enough time passed for another repeat to happen?
			if currentTime - self.mouseClickTime < (self.mouseRepeat[1]/1000):
				return
		
		# Process events for the first time and
		# after the appropriate delay interval
		if leftClick:
			pass
		if middleClick:
			pass
		if rightClick:
			pass
		
		###########################################################
		# Turn on mouseHeld flag so the next time this processes  #
		# it will know that we've been holding it down            #
		# and how long we've been holding it down                 #
		###########################################################
		
		self.mouseHeld = True
		self.mouseClickTime = currentTime

	###########################################
	# DRAWING AND SIZE MANIPULATION METHODS   #
	###########################################
	
	def draw(self):
		# Set list of rects that will be updated and returned
		updateList = []
		
		# Draw grid
		updateList.extend(self.grid.draw(self.window))
		
		# See if any cells that need draw updates collide with
		# any controls, and set those controls to redraw as well
		self.controls.checkGridOverlap(updateList)
		
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
	
		############################################
		# Schedule controls and grid for redrawing #
		############################################
		
		self.controls.redrawAll()
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
		if(self.calcThread.speed < self.calcThread.speedLimit):
			self.calcThread.speed += 1
			self.controls.updateSpeedDisplay(self.calcThread.speed)
	
	def stepForward(self):
		if self.simRunning:
			self.pause()
		self.calcThread.calc()
		return self.simRunning
	