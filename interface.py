#!/usr/bin/python

import pygame
from pygame.locals import *
from algorithms import *
from namedtuples import *
from grid import Grid
from controls import Controls

class Interface():
	# Constructor
	def __init__(self, calcThread=None):
		# Declare constants
			# General
		self.fpsLimit = 60
		self.simRunning = False
		self.calcThread = calcThread
			# Section sizes
		self.grid_width = 801
		self.control_width = 200
		self.window_height = 601
		
		# Initialize pygame window
		pygame.init()
		self.window = pygame.display.set_mode((self.grid_width + self.control_width, self.window_height))
		pygame.display.set_caption("Conway's Game of Life")
		
		# Create clock to limit FPS
		self.fpsClock = pygame.time.Clock()

		# Create the initial grid
		self.grid = Grid(Dimensions(self.grid_width, self.window_height), Position(0, 0))

		# Create control section
		self.controls = Controls(Dimensions(self.control_width, self.window_height),
								Position(self.grid_width, 0), self)


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
				if event.button == 1:
					self.controls.collidepoint(pygame.mouse.get_pos())
					self.grid.collidepoint(pygame.mouse.get_pos())
			elif event.type == KEYDOWN:
				pass
			else:
				pass
		return True
		
	
	def draw(self):
		# Set background as white
		self.window.fill(pygame.Color("white"))

		# Draw control interface
		self.controls.draw(self.window)
		
		# Draw grid
		self.grid.draw(self.window)

	def reset(self):
		self.__init__(self.calcThread)
