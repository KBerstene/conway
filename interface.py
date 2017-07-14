#!/usr/bin/python

import pygame
from pygame.locals import *
from algorithms import *
from namedtuples import *
from grid import Grid
from controls import Controls
import time
import math

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
		self.grid = Grid(Dimensions(self.window.get_rect().width - self.control_width, self.window.get_rect().height), Position(0, 0))#, cellSize = Dimensions(4,4))
		
		# Create control section
		self.controls = Controls(Dimensions(self.control_width, self.window.get_rect().height),
								Position(self.grid.rect.width, 0), self)


	def setCalcThread(self,calcThread):
		self.calcThread = calcThread
		self.controls.updateSpeedDisplay(self.calcThread.speed)
		
	def update(self):
		start = time.time()
		# Process any mouse/keyboard events
		if not self.processEvents():
			return False
		events = time.time()
		# Draw objects
		updates = self.draw()
		draw = time.time()
		# Update window
		pygame.display.update(updates)
		windowupdate = time.time()
		# Limit FPS
		self.fpsClock.tick(self.fpsLimit)
		print("Events: " + str((events-start)*1000) + "ms")
		print("Draw:   " + str((draw-events)*1000) + "ms")
		print("Update: " + str((windowupdate-draw)*1000) + "ms")
		return True
		
	def processEvents(self):
		click_pos=(-1,-1)

		# Get pygame events to see if exit is called
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				return False
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					self.controls.collidepoint(pygame.mouse.get_pos())
					self.grid.collidepoint(pygame.mouse.get_pos())
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
		# Set list of rects that will be updated and returned
		updateList = []
	
		# Draw grid
		updateList.extend(self.grid.draw(self.window))

		# Draw control interface
		updateList.extend(self.controls.draw(self.window))
				
		# Return list of rects to be updated
		return updateList
		
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
	