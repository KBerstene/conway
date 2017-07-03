#!/usr/bin/python

import pygame
from namedtuples import *

# Main control panel
class Controls():
	# Constructor
	def __init__(self, dimensions, location, interface):
		# Create surface and static rect
		self.surface = pygame.Surface(dimensions)
		self.rect = self.surface.get_rect(left=location.left, top=location.top)
		
		# Set font
		self.fontPath = "res/trebuc.ttf"
		
		# Link interface
		self.interface = interface
		
		# Create buttons and labels
		self.controlItems = {}
		self.controlItems['startButton'] = RectWithText(Position(self.rect.left + 39, 60), Dimensions(120,41), "Start", self.fontPath)
		self.controlItems['resetButton'] = RectWithText(Position(self.rect.left + 39, 140), Dimensions(120,41), "Reset", self.fontPath)
		self.controlItems['speedText'] = Label("Speed", Position(self.rect.left + 43, 200), self.fontPath, 20)
		self.controlItems['speedDisplayBox'] = RectWithText(Position(self.rect.left + 69,230), Dimensions(61, 31), "2", self.fontPath)
		self.controlItems['speedUpButton'] = TriButton(Coordinates(self.rect.left + 158,245),Coordinates(self.rect.left + 134,230),Coordinates(self.rect.left + 134,260))
		self.controlItems['speedDownButton'] = TriButton(Coordinates(self.rect.left + 39,245),Coordinates(self.rect.left + 64,230),Coordinates(self.rect.left + 64,260))
		
	def draw(self, surface):
		# Draw control items
		for item in self.controlItems:
			self.controlItems[item].draw(surface)
		
	def updateSpeedDisplay(self, speed):
		self.controlItems['speedDisplayBox'].setText(str(speed))
	
	def collidepoint(self, pos):
		if self.rect.collidepoint(pos):
			if self.controlItems['startButton'].collidepoint(pos):
				if self.interface.simRunning:
					self.interface.simRunning=False
					self.controlItems['startButton'].setText("Start")
				else:
					self.interface.simRunning=True
					self.controlItems['startButton'].setText("Pause")
			elif self.controlItems['resetButton'].collidepoint(pos):
				self.interface.reset()
			elif self.controlItems['speedUpButton'].collidepoint(pos):
				if (self.interface.calcThread.speed < 9):
					self.interface.calcThread.speed +=1
					self.controlItems['speedDisplayBox'].setText(str(self.interface.calcThread.speed))
			elif self.controlItems['speedDownButton'].collidepoint(pos):
				if (self.interface.calcThread.speed > 1):
					self.interface.calcThread.speed -=1
					self.controlItems['speedDisplayBox'].setText(str(self.interface.calcThread.speed))
	
	def resize(self, size, position):
		# Resize surface
		self.surface = pygame.transform.scale(self.surface, size)
		self.rect = self.surface.get_rect(left=position.left, top=position.top)
		
		# Regenerate control items
		self.controlItems['startButton'] = RectWithText(Position(self.rect.left + 39, 60), Dimensions(120,41), "Start", self.fontPath)
		self.controlItems['resetButton'] = RectWithText(Position(self.rect.left + 39, 140), Dimensions(120,41), "Reset", self.fontPath)
		self.controlItems['speedText'] = Label("Speed", Position(self.rect.left + 43, 200), self.fontPath, 20)
		self.controlItems['speedDisplayBox'] = RectWithText(Position(self.rect.left + 69,230), Dimensions(61, 31), "2", self.fontPath)
		self.controlItems['speedUpButton'] = TriButton(Coordinates(self.rect.left + 158,245),Coordinates(self.rect.left + 134,230),Coordinates(self.rect.left + 134,260))
		self.controlItems['speedDownButton'] = TriButton(Coordinates(self.rect.left + 39,245),Coordinates(self.rect.left + 64,230),Coordinates(self.rect.left + 64,260))
		

# Rectangular Buttons
class RectWithText(pygame.Rect):
	# Constructor
	def __init__(self, pos=Position(0, 0), size=Dimensions(120,41), text = "", font = None, fontSize = 20):
		super().__init__((pos.left, pos.top), (size.width, size.height))
		
		self.fontPath = font
		self.fontSize = fontSize
		self.setText(text)

	def setText(self, text):
		self.text = pygame.font.Font(self.fontPath, self.fontSize).render(text, 1, pygame.Color("black"))
		self.textPos = (self.centerx - (self.text.get_rect().width / 2), self.centery - (self.text.get_rect().height / 2))

	def draw(self, window):
		pygame.draw.rect(window, pygame.Color("black"), self, 1)
		window.blit(self.text, self.textPos)

# Triangle Buttons
class TriButton():
	# Constructor
	def __init__(self, coords1, coords2, coords3):
		self.x = (coords1.x, coords2.x, coords3.x)
		self.y = (coords1.y, coords2.y, coords3.y)

	def draw(self, surface):
		pygame.draw.polygon(surface, pygame.Color("black"), self.getPoints(), 1)
	
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

class Label():
	# Constructor
	def __init__(self, text, pos = Position(0, 0), fontPath = None, size = 20):
		self.pos = pos
		self.labelSurface = pygame.font.Font(fontPath, 20).render("Speed", 1, pygame.Color("black"))
	
	def draw(self, surface):
		surface.blit(self.labelSurface, self.pos)
	