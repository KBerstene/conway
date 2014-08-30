#!/usr/bin/python

import pygame
from pygame.locals import *
from pygame import Color
from threading import Thread


class Interface():
	# Constructor
	def __init__(self, *args, **kwargs):
		# Initialize pygame, create a window,
		# and create clock to limit FPS
		pygame.init()
		self.window = pygame.display.set_mode((801,601))
		pygame.display.set_caption("Conway's Game of Life")
		self.fpsClock = pygame.time.Clock()

		# Create the grid array that will contain
		# data on which cells are alive or dead
		self.grid=[[False for x in xrange(30)] for x in xrange(40)]

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
			i = 0
			while i < 40:
				j = 0
				while j < 30:
					pygame.draw.rect(self.window, Color("black"), (i*20,j*20,21,21), not(self.grid[i][j]))
					j += 1
				i += 1

			# Draw the window and tick the clock
			pygame.display.update()
			self.fpsClock.tick(30)
