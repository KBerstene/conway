#!/usr/bin/python

from threading import Thread
from algorithms import calc_status
from time import sleep
from time import time

# Create thread class for calculation loop
class CalcThread(Thread):
	def __init__(self, interface):
		Thread.__init__(self)
		self.daemon = True
		self.interface = interface
		self.speed = 2
		self.speedLimit = 20
		self.killswitch = False
		
	def run(self):
		while not self.killswitch:
			if self.interface.simRunning:
				# Time how long calculations take
				start = time()
				self.calc()
				end = time()
				
				# Sleep based on the time calculations take to be a consistent calc/second
				sleeptime = (.41-(self.speed*.02))-(end-start)
				if sleeptime <= 0:
					sleeptime = .001
				sleep(sleeptime)
				
	def calc(self):
		calc_status(self.interface)
