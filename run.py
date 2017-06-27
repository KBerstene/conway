#!/usr/bin/python

from interface import Interface
from threads import *

if __name__ == "__main__":
	# Initialize the interface
	interface = Interface()

	# Initialize the calculations thread
	calculations = CalcThread(interface)

	# Start the calc thread
	calculations.start()
	
	# Run the interface updates
	while (True):
		interface.update()
