#!/usr/bin/python

from threading import Thread
from algorithms import calc_status
from time import sleep

# Create thread class for calculation loop
class CalcThread(Thread):
	def __init__(self, interface):
		Thread.__init__(self)
		self.daemon = True
		self.interface = interface
		self.speed = 2
		
	def run(self):
		while (True):
			if self.interface.simRunning:
				calc_status(self.interface.grid)
				sleep(1.0/self.speed)
