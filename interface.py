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
		self.window = pygame.display.set_mode((801,601))
		pygame.display.set_caption("Conway's Game of Life")
		self.fpsClock = pygame.time.Clock()

		# Create a 40x30 array of cells
		self.grid=[[Cell((0, 0), (21, 21)) for x in xrange(30)] for x in xrange(40)]

		# Set each square's location
		i = 0
		while i < 40:
			j = 0
			while j < 30:
				self.grid[i][j].left=i*20
				self.grid[i][j].top=j*20
				self.grid[i][j].coords=(i, j)
				j += 1
			i += 1

		# Get multithreading ready
		self.thread=Thread(target=self.run)

	# Start the seperate thread
	def start(self):
		self.thread.start()

	# What runs in the asynchronous thread
	def run(self):
		while True:
			# Get pygame events to see if exit is called
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					exit()

			# Set background as white
			self.window.fill(Color("white"))

			# Iterate through grid and print white square as dead and black square as alive
			for row in self.grid:
				for cell in row:
					pygame.draw.rect(self.window, Color("black"), cell, not(cell.getStatus()))


			# Draw the window and tick the clock
			pygame.display.update()
			self.fpsClock.tick(30)


class Cell(pygame.Rect):
	def __init__(self, (left, top), (width, height)):
		super(Cell, self).__init__((left, top), (width, height))
		self.alive=False
		self.coords=(0, 0)

	def getStatus(self):
		return self.alive

	def setStatus(self, alive):
		self.alive = alive

	def getCoords(self):
		return self.coords

	def setCoords(self, (x, y)):
		self.coords=(x, y)

