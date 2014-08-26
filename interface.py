#!/usr/bin/python

import pygame
from pygame.locals import *
from pygame import Color

grid=[[False for x in xrange(30)] for x in xrange(40)]
grid[25][15]=True

pygame.init()
fpsClock = pygame.time.Clock()

window = pygame.display.set_mode((801,601))
pygame.display.set_caption('Test')


while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()

	window.fill(Color("white"))

	i = 0
	while i < 40:
		j = 0
		while j < 30:
			pygame.draw.rect(window, Color("black"), (i*20,j*20,21,21), not(grid[i][j]))
			j += 1
		i += 1

	pygame.display.update()
	fpsClock.tick(30)
