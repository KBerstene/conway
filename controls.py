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
		self.populateItems()
	
	def populateItems(self):
		self.controlItems['startButton'] = RectWithText(Position(self.rect.left + 39, 60), Dimensions(120,41), "Start", self.fontPath, click = lambda:(self.controlItems['startButton'].setText("Pause")) if self.interface.pause() else self.controlItems['startButton'].setText("Start"))
		self.controlItems['resetButton'] = RectWithText(Position(self.rect.left + 39, 140), Dimensions(120,41), "Reset", self.fontPath, click = lambda:self.interface.reset())
		self.controlItems['speedText'] = Label("Speed", Position(self.rect.left + 43, 200), self.fontPath, 20)
		self.controlItems['speedDisplayBox'] = RectWithText(Position(self.rect.left + 69,230), Dimensions(61, 31), "2", self.fontPath)
		self.controlItems['speedUpButton'] = TriButton(Position(self.rect.left + 134, 230), click = lambda:self.interface.speedUp())
		self.controlItems['speedDownButton'] = TriButton(Position(self.rect.left + 40, 230), flip = True, click = lambda:self.interface.speedDown())
	
	def draw(self, surface):
		# Draw control items
		for item in self.controlItems:
			self.controlItems[item].draw(surface)
		
	def updateSpeedDisplay(self, speed):
		self.controlItems['speedDisplayBox'].setText(str(speed))
	
	def collidepoint(self, pos):
		if self.rect.collidepoint(pos):
			for key, item in self.controlItems.items():
				if item.collidepoint(pos):
					item.clickAction()
					break
	
	def resize(self, size, position):
		# Resize surface
		self.surface = pygame.transform.scale(self.surface, size)
		self.rect = self.surface.get_rect(left=position.left, top=position.top)
		
		# Regenerate control items
		self.populateItems()
		self.updateSpeedDisplay(self.interface.calcThread.speed)
		

# Rectangular Buttons
class RectWithText(pygame.Rect):
	# Constructor
	def __init__(self, pos=Position(0, 0), size=Dimensions(120,41), text = "", font = None, fontSize = 20, click = lambda:None):
		super().__init__((pos.left, pos.top), (size.width, size.height))
		self.clickAction = click
		
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
	def __init__(self, pos = Position(0, 0), size = Dimensions(24, 30), flip = False, click = lambda:None):
		self.clickAction = click
		if (flip):
			self.x = (pos.left, pos.left + size.width, pos.left + size.width)
			self.y = (pos.top + (size.height / 2), pos.top, pos.top + size.height)
		else:
			self.x = (pos.left + size.width, pos.left, pos.left)
			self.y = (pos.top + (size.height / 2), pos.top, pos.top + size.height)
			
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
		self.labelSurface = pygame.font.Font(fontPath, 20).render(text, 1, pygame.Color("black"))
	
	def draw(self, surface):
		surface.blit(self.labelSurface, self.pos)
	
	def collidepoint(self, *args, **kwargs):
		pass