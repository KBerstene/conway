#!/usr/bin/python

import pygame
import math
from namedtuples import *
from collections import Iterable

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
		self.controls = []
		self.populateItems()
	
	def populateItems(self):
		self.addControl([ RectWithText(text = "Start", font = self.fontPath, click = lambda:(self.controls[0].objects[0].setText("Pause")) if self.interface.pause() else self.controls[0].objects[0].setText("Start")) ])
		self.addControl([ RectWithText(text = "Reset", font = self.fontPath, click = lambda:self.interface.reset()) ])
		self.addControl([ Label(text = "Speed", font = self.fontPath, size = 20) ])
		self.addControl([ TriButton(flip = True, click = lambda:self.interface.speedDown()), RectWithText(text = "2", size = Dimensions(61, 31), font = self.fontPath), TriButton(click = lambda:self.interface.speedUp()) ])
		self.speedDisplay = self.controls[3].objects[1]
	
	def addControl(self, objectList):
		if (len(self.controls) == 0):
			self.controls.append(ControlWrapper(Position(self.rect.left, self.rect.top), self.rect.width, objectList))
		else:
			self.controls.append(ControlWrapper(Position(self.rect.left, self.controls[len(self.controls)-1].top + self.controls[len(self.controls)-1].height), self.rect.width, objectList))
	
	def draw(self, surface):
		# Draw control items
		for item in self.controls:
			item.draw(surface)
		
	def updateSpeedDisplay(self, speed):
		#self.controlItems['speedDisplayBox'].setText(str(speed))
		self.speedDisplay.setText(str(speed))
		
	def collidepoint(self, pos):
		if self.rect.collidepoint(pos):
			# for key, item in self.controlItems.items():
				# if item.collidepoint(pos):
					# item.clickAction()
					# break
			for item in self.controls:
				if item.collidepoint(pos):
					item.clickAction()
					break
	
	def resize(self, size, position):
		# Resize surface
		self.surface = pygame.transform.scale(self.surface, size)
		self.rect = self.surface.get_rect(left=position.left, top=position.top)
		
		# Regenerate control items
		self.controls.clear()
		self.populateItems()
		self.updateSpeedDisplay(self.interface.calcThread.speed)
		

# Wrapper class for all control objects
# This is here to allow for padding and dynamic sizing of control objects
class ControlWrapper():
	# Constructor
	def __init__(self, pos, width, objectList, padding = 5, click = lambda:None):
		# Create object list
		self.objects = objectList
		
		# Find surface height
		maxHeight = 0
		for obj in self.objects:
			if obj.height > maxHeight:
				maxHeight = obj.height
		
		# Create surface
		self.surface = pygame.Surface((width, maxHeight + padding + padding)) # add padding twice to cover both top and bottom padding
		self.surface.fill(pygame.Color("white"))
		
		# Create size constants
		self.pos = pos
		self.left = pos.left
		self.top = pos.top
		self.width = width
		self.height = self.surface.get_rect().height
		
		# Get amount of extra width around objects
		spareWidth = width - padding # Initial left padding
		for obj in self.objects:
			spareWidth -= obj.width # object width
			spareWidth -= padding # right padding
		leftPadding = math.floor(spareWidth / 2) # round down so it falls left
		
		# Center objects
		for i in range(len(self.objects)):
			# Center vertically
			self.objects[i].top = padding
			# Center horizontally
			self.objects[i].left = leftPadding + padding
			# Set new left
			leftPadding = self.objects[i].left + self.objects[i].width
			
		# Draw objects
		for obj in self.objects:
			obj.draw(self.surface)

	def draw(self, surface):
		# Reset surface to white
		self.surface.fill(pygame.Color("white"))
		
		# Draw objects onto control surface
		for obj in self.objects:
			obj.draw(self.surface)
		
		# Draw control surface
		surface.blit(self.surface, self.pos)
	
	def collidepoint(self, pos):
		for obj in self.objects:
			if obj.collidepoint((pos[0] - self.pos[0], pos[1] - self.pos[1])):
				self.clickAction = obj.clickAction
				return True
		return False
		

# Rectangular Buttons
class RectWithText(pygame.Rect):
	# Constructor
	def __init__(self, pos=Position(0, 0), size=Dimensions(120,41), text = "", font = None, fontSize = 20, click = lambda:None):
		super().__init__((pos.left, pos.top), (size.width, size.height))
		self.clickAction = click
		
		self.fontPath = font
		self.fontSize = fontSize
		self.text = text
		self.setText(self.text)

	def setText(self, text):
		self.text = text
		self.textSurface = pygame.font.Font(self.fontPath, self.fontSize).render(text, 1, pygame.Color("black"))
		self.textPos = (self.centerx - (self.textSurface.get_rect().width / 2), self.centery - (self.textSurface.get_rect().height / 2))

	def draw(self, window):
		self.setText(self.text)
		pygame.draw.rect(window, pygame.Color("black"), self, 1)
		window.blit(self.textSurface, self.textPos)


# Triangle Buttons
class TriButton():
	# Constructor
	def __init__(self, pos = Position(0, 0), size = Dimensions(24, 30), flip = False, click = lambda:None):
		# Create surface and set clickAction
		self.surface = pygame.Surface((size.width + 1, size.height + 1))
		self.clickAction = click
		
		# Set points
		if (flip):
			self.x = (pos.left, pos.left + size.width, pos.left + size.width)
			self.y = (pos.top + ((size.height) / 2), pos.top, pos.top + size.height)
		else:
			self.x = (pos.left + size.width, pos.left, pos.left)
			self.y = (pos.top + ((size.height) / 2), pos.top, pos.top + size.height)

		# Set constants
		self.width = size.width
		self.height = size.height
		self.left = pos.left
		self.top = pos.top

		# Draw onto surface
		self.surface.fill(pygame.Color("white"))
		pygame.draw.polygon(self.surface, pygame.Color("black"), self.getPoints(), 1)
		
	def draw(self, surface):
		surface.blit(self.surface, (self.left, self.top))
	
	def getPoints(self):
		return ((self.x[0], self.y[0]), (self.x[1], self.y[1]), (self.x[2], self.y[2]))

	def collidepoint(self, mouse_pos):
		return self.surface.get_rect(left = self.left, top = self.top).collidepoint(mouse_pos)


class Label(pygame.Surface):
	# Constructor
	def __init__(self, text, pos = Position(0, 0), font = None, size = 20):
		super().__init__(pygame.font.Font(font, 20).size(text))
		super().fill(pygame.Color("white"))
		super().blit(pygame.font.Font(font, 20).render(text, 1, pygame.Color("black")), (0,0))
		self.left = pos.left
		self.top = pos.top
		self.width = super().get_rect().width
		self.height = super().get_rect().height
	
	def draw(self, surface):
		surface.blit(self, (self.left, self.top))
	
	def collidepoint(self, *args, **kwargs):
		pass
