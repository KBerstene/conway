#!/usr/bin/python

from interface import Interface
from threads import *

if __name__ == "__main__":
	#total = 0
	# Initialize the interface
	interface = Interface()

	# Initialize the calculations thread
	calculations = CalcThread(interface)
	
	# Let interface know about calc thread so it can display speed
	interface.setCalcThread(calculations)

	# Start the calc thread
	calculations.start()
	
	# Run the interface updates
	while (interface.update()):
		pass
		
	exit()