#!/usr/bin/python

import pygame
from pygame.locals import *
from pygame import Color
from threading import Thread


class Interface():
	def __init__(self, *args, **kwargs):
		pygame.init()
		self.fpsClock = pygame.time.Clock()

		self.grid=[[False for x in xrange(30)] for x in xrange(40)]
		self.grid[39][29]=True

		self.thread=Thread(target=self.run)

		self.window = pygame.display.set_mode((801,601))
		pygame.display.set_caption('Test')

	def start(self):
		self.thread.start()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					exit()

			self.window.fill(Color("white"))

			i = 0
			while i < 40:
				j = 0
				while j < 30:
					pygame.draw.rect(self.window, Color("black"), (i*20,j*20,21,21), not(self.grid[i][j]))
					j += 1
				i += 1

			pygame.display.update()
			self.fpsClock.tick(30)
