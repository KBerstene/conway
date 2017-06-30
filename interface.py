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
	def __init__(self, calcThread=None):
		# Declare constants
			# General
		self.fpsLimit = 60
		self.simRunning = False
		self.calcThread = calcThread
		self.fontPath = "res/trebuc.ttf"
			# Grid
		self.grid_width = 40
		self.grid_height = 30
		
		# Initialize pygame window
		pygame.init()
		self.window = pygame.display.set_mode((1001,601))
		pygame.display.set_caption("Conway's Game of Life")
		
		# Create clock to limit FPS
		self.fpsClock = pygame.time.Clock()

		# Create a array of cells
		self.grid=[[Cell() for x in range(self.grid_height)] for x in range(self.grid_width)]

		# Set each square's position
		for i in range(self.grid_width):
			for j in range(self.grid_height):
				self.grid[i][j] = Cell(Position(i*20, j*20))

		# Create interface control buttons
		self.startButton = RectWithText(Position(840, 60), Dimensions(120,41), "Start", self.fontPath)
		self.resetButton = RectWithText(Position(840, 140), Dimensions(120,41), "Reset", self.fontPath)
		self.speedText=pygame.font.Font(self.fontPath, 20).render("Speed", 1, Color("black"))
		self.speedDisplayBox = RectWithText(Position(870,230), Dimensions(61, 31), "2", self.fontPath)
		self.speedUpButton=TriButton(Coordinates(959,245),Coordinates(935,230),Coordinates(935,260))
		self.speedDownButton=TriButton(Coordinates(840,245),Coordinates(865,230),Coordinates(865,260))
		
	def setCalcThread(self,calcThread):
		self.calcThread = calcThread
		self.speedDisplayBox.setText(str(self.calcThread.speed))
		
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
					if self.startButton.collidepoint(pygame.mouse.get_pos()):
						if self.simRunning:
							self.simRunning=False
							self.startButton.setText("Start")
						else:
							self.simRunning=True
							self.startButton.setText("Pause")
					elif self.resetButton.collidepoint(pygame.mouse.get_pos()):
						self.__init__(self.calcThread)
					elif self.speedUpButton.collidepoint(pygame.mouse.get_pos()):
						if (self.calcThread.speed < 9):
							self.calcThread.speed +=1
							self.speedDisplayBox.setText(str(self.calcThread.speed))
					elif self.speedDownButton.collidepoint(pygame.mouse.get_pos()):
						if (self.calcThread.speed > 1):
							self.calcThread.speed -=1
							self.speedDisplayBox.setText(str(self.calcThread.speed))
					else:
						click_pos=pygame.mouse.get_pos()
			elif event.type == KEYDOWN:
				pass
			else:
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
		self.startButton.draw(self.window)
			# Reset Button
		self.resetButton.draw(self.window)
			# Speed Label
		self.window.blit(self.speedText, (844, 200))
			# Speed Arrows
		pygame.draw.polygon(self.window, Color("black"), self.speedUpButton.getPoints(), 1)
		pygame.draw.polygon(self.window, Color("black"), self.speedDownButton.getPoints(), 1)
			# Speed Display Box
		self.speedDisplayBox.draw(self.window)
		
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
		

# Rectangular Buttons
class RectWithText(pygame.Rect):
	# Constructor
	def __init__(self, pos=Position(0, 0), size=Dimensions(120,41), text = "", font = None, fontSize = 20):
		super().__init__((pos.left, pos.top), (size.width, size.height))
		
		self.fontPath = font
		self.fontSize = fontSize
		self.setText(text)

	def setText(self, text):
		self.text = pygame.font.Font(self.fontPath, self.fontSize).render(text, 1, Color("black"))
		self.textPos = (self.centerx - (self.text.get_rect().width / 2), self.centery - (self.text.get_rect().height / 2))

	def draw(self, window):
		pygame.draw.rect(window, Color("black"), self, 1)
		window.blit(self.text, self.textPos)

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

