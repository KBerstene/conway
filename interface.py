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
				if event.button == 1:
					self.controls.collidepoint(pygame.mouse.get_pos())
					self.grid.collidepoint(pygame.mouse.get_pos())
			elif event.type == KEYDOWN:
				pass
			elif event.type == VIDEORESIZE:
				self.resize(event.dict['size'])
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

	def resize(self, size):
		self.window = pygame.display.set_mode(size, pygame.RESIZABLE)
		self.grid.resize(Dimensions(self.window.get_rect().width - self.control_width, self.window.get_rect().height), Position(0, 0))
		self.controls.resize(Dimensions(self.control_width, self.window.get_rect().height), Position(self.grid.rect.width, 0))
	
	def reset(self):
		self.__init__(Dimensions(self.window.get_rect().width, self.window.get_rect().height), self.calcThread)
		self.calcThread.__init__(self)

	def pause(self):
		self.simRunning = not(self.simRunning)
		print("intpause")
		return self.simRunning

	def speedUp(self):
		print("speedup")
		if (self.calcThread.speed < 9):
			self.calcThread.speed += 1
			self.controls.updateSpeedDisplay(self.calcThread.speed)
	
	def speedDown(self):
		print("speeddown")
		if (self.calcThread.speed > 1):
			self.calcThread.speed -= 1
			self.controls.updateSpeedDisplay(self.calcThread.speed)
	