#!/usr/bin/python

import pygame
from algorithms import *
from pygame.locals import *
from pygame import Color
from collections import namedtuple

Position = namedtuple('Position','left top')
Coordinates = namedtuple('Coordinates','x y')
Dimensions = namedtuple('Dimensions','width height')

class Interface():
	# Constructor
	def __init__(self):
		# Initialize pygame, create a window,
		# and create clock to limit FPS
		pygame.init()
		self.window = pygame.display.set_mode((1001,601))
		pygame.display.set_caption("Conway's Game of Life")
		self.fpsClock = pygame.time.Clock()
		self.fpsLimit = 60
		self.simRunning=False

		# Create a 40x30 array of cells
		self.grid_width = 40
		self.grid_height = 30

		self.grid=[[Cell() for x in range(self.grid_height)] for x in range(self.grid_width)]

		# Set each square's position
		for i in range(self.grid_width):
			for j in range(self.grid_height):
				self.grid[i][j] = Cell(Position(i*20, j*20))

		# Create interface control buttons
		self.startButton=pygame.Rect((840, 60), (120,41))
		self.startButtonText=pygame.font.Font(None, 20).render("Start", 1, Color("black"))
		self.resetButton=pygame.Rect((840, 140), (120,41))
		self.resetButtonText=pygame.font.Font(None, 20).render("Reset", 1, Color("black"))
		self.speedText=pygame.font.Font(None, 20).render("Speed", 1, Color("black"))
		self.speedDisplayBox=pygame.Rect((870,230), (61, 31))
		self.speedUpButton=TriButton(Coordinates(959,245),Coordinates(935,230),Coordinates(935,260))
		self.speedDownButton=TriButton(Coordinates(840,245),Coordinates(865,230),Coordinates(865,260))

	def update(self):
		print("cycle")
		
		# Process any mouse/keyboard events
		if not self.processEvents():
			return

		# Draw objects
		self.draw()

		# Update window
		pygame.display.update()
		
	def processEvents(self):
		click_pos=(-1,-1)

		# Get pygame events to see if exit is called
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				return False
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					if self.startButton.collidepoint(pygame.mouse.get_pos()):
						if self.simRunning:
							self.simRunning=False
							self.startButtonText=pygame.font.Font(None, 20).render("Start", 1, Color("black"))
						else:
							self.simRunning=True
							self.startButtonText=pygame.font.Font(None, 20).render("Pause", 1, Color("black"))
					elif self.resetButton.collidepoint(pygame.mouse.get_pos()):
						self.__init__()
					elif self.speedUpButton.collidepoint(pygame.mouse.get_pos()):
						if (self.fpsLimit < 9):
							self.fpsLimit+=1
					elif self.speedDownButton.collidepoint(pygame.mouse.get_pos()):
						if (self.fpsLimit > 1):
							self.fpsLimit-=1
					else:
						click_pos=pygame.mouse.get_pos()
			elif event.type == KEYDOWN:
				print("keypress")
				pass
			else:
				print("event")
				pass
		
		self.scanRows(click_pos)
		
		return True
		
	def scanRows(self, click_pos):
		for row in self.grid:
			for cell in row:
				if cell.collidepoint(click_pos):
					cell.setStatus(not(cell.getStatus()))
					return True
		return False
	
	
	def draw(self):
		# Set background as white
		self.window.fill(Color("white"))

		# Draw control buttons
			# Start/Pause Button
		pygame.draw.rect(self.window, Color("black"), self.startButton, 1)
		if self.simRunning:
			self.window.blit(self.startButtonText, (845, 74))
		else:
			self.window.blit(self.startButtonText, (850, 74))
			# Reset Button
		pygame.draw.rect(self.window, Color("black"), self.resetButton, 1)
		self.window.blit(self.resetButtonText, (846, 154))
			# Speed Up/Down Display
		self.window.blit(self.speedText, (844, 210))
		pygame.draw.rect(self.window, Color("black"), self.speedDisplayBox, 1)
		pygame.draw.polygon(self.window, Color("black"), self.speedUpButton.getPoints(), 1)
		pygame.draw.polygon(self.window, Color("black"), self.speedDownButton.getPoints(), 1)
		self.window.blit(pygame.font.Font(None, 30).render(str(self.fpsLimit), 1, Color("black")), (894,234))

		# Run the calculations
		if self.simRunning:
			calc_status(self.grid)

		# Iterate through grid and print white square as dead and black square as alive
		for row in self.grid:
			for cell in row:
				pygame.draw.rect(self.window, Color("black"), cell, not(cell.getStatus()))


# Subclass of Rect to add alive/dead status
class Cell(pygame.Rect):
	# Constructor
	def __init__(self, pos=Position(0, 0), size=Dimensions(21, 21)):
		super(Cell, self).__init__((pos.left, pos.top), (size.width, size.height))
		self.alive=False

	# Getters/Setters
	def getStatus(self):
		return self.alive

	def setStatus(self, alive):
		self.alive = alive
		
# Triangle Buttons
class TriButton():
	# Constructor
	def __init__(self, coords1, coords2, coords3):
		self.x = (coords1.x, coords2.x, coords3.x)
		self.y = (coords1.y, coords2.y, coords3.y)

	def getPoints(self):
		return ((self.x[0], self.y[0]), (self.x[1], self.y[1]), (self.x[2], self.y[2]))

	def collidepoint(self, mouse_pos):
		mouse_x = mouse_pos[0]
		mouse_y = mouse_pos[1]
		if mouse_x < min(self.x) or mouse_x > max(self.x):
			return False
		if mouse_y < min(self.y) or mouse_y > max(self.y):
			return False
		return True

