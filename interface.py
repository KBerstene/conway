#!/usr/bin/python

import pygame
from pygame.locals import *
from pygame import Color
from threading import Thread


class Interface():
	# Constructor
	def __init__(self):
		# Initialize pygame, create a window,
		# and create clock to limit FPS
		pygame.init()
		self.window = pygame.display.set_mode((1001,601))
		pygame.display.set_caption("Conway's Game of Life")
		self.fpsClock = pygame.time.Clock()
		self.simRunning=False

		# Create a 40x30 array of cells
		self.grid_width = 40
		self.grid_height = 30

		self.grid=[[Cell() for x in xrange(self.grid_height)] for x in xrange(self.grid_width)]

		# Set each square's location
		for i in xrange(self.grid_width):
			for j in xrange(self.grid_height):
				self.grid[i][j] = Cell((i*20, j*20))

		# Create interface control buttons
		self.startButton=pygame.Rect((840, 60), (120,41))
		self.startButtonText=pygame.font.Font(None, 20).render("Start Simulation", 1, Color("black"))
		self.resetButton=pygame.Rect((840, 140), (120,41))
		self.resetButtonText=pygame.font.Font(None, 20).render("Reset Simulation", 1, Color("black"))

		# Get multithreading ready
		self.thread=Thread(target=self.run)

		# ---DEBUGGING TOOLS---
		self.fpsDisplay=False


	# Start the seperate thread
	def start(self):
		self.thread.start()

	# What runs in the asynchronous thread
	def run(self):
		while True:
			click_pos=(-1,-1)
			# Get pygame events to see if exit is called
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					exit()
				elif event.type == MOUSEBUTTONDOWN:
					if event.button == 1:
						if self.startButton.collidepoint(pygame.mouse.get_pos()):
							if self.simRunning:
								self.simRunning=False
								self.startButtonText=pygame.font.Font(None, 20).render("Start Simulation", 1, Color("black"))
							else:
								self.simRunning=True
								self.startButtonText=pygame.font.Font(None, 20).render("Pause Simulation", 1, Color("black"))
						elif self.resetButton.collidepoint(pygame.mouse.get_pos()):
							self.__init__()
						else:
							click_pos=pygame.mouse.get_pos()
				elif event.type == KEYDOWN:
					if event.key == K_F3:
						self.fpsDisplay=not(self.fpsDisplay)

			# Set background as white
			self.window.fill(Color("white"))

			# Draw control buttons
			pygame.draw.rect(self.window, Color("black"), self.startButton, 1)
			if self.simRunning:
				self.window.blit(self.startButtonText, (845, 74))
			else:
				self.window.blit(self.startButtonText, (850, 74))
			pygame.draw.rect(self.window, Color("black"), self.resetButton, 1)
			self.window.blit(self.resetButtonText, (846, 154))

			# Run the calculations
			if self.simRunning:
				# Jon, call something from another file here
				pass

			# Iterate through grid and print white square as dead and black square as alive
			for row in self.grid:
				for cell in row:
					if cell.collidepoint(click_pos):
						cell.setStatus(not(cell.getStatus()))
					pygame.draw.rect(self.window, Color("black"), cell, not(cell.getStatus()))

			# ---DEBUGGING---
			# Display FPS on screen
			if self.fpsDisplay:
				self.window.blit(pygame.font.Font(None, 36).render("FPS: " + str(int(self.fpsClock.get_fps())), 1, Color("black"), Color("white")), (20,20))

			# Draw the window and tick the clock
			pygame.display.update()
			self.fpsClock.tick(30)


# Subclass of Rect to add alive/dead status
class Cell(pygame.Rect):
	# Constructor
	def __init__(self, (left, top)=(0, 0), (width, height)=(21, 21)):
		super(Cell, self).__init__((left, top), (width, height))
		self.alive=False

	# Getters/Setters
	def getStatus(self):
		return self.alive

	def setStatus(self, alive):
		self.alive = alive

