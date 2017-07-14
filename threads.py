#!/usr/bin/python

from threading import Thread
from algorithms import calc_status
from time import sleep,time

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
				self.calc()
				sleep(1.0/self.speed)

	def calc(self):
		start = time()
		calc_status(self.interface.grid, self.interface)
		end = time()
		print ("Calculations: " + str((end - start)*1000) + "ms")
