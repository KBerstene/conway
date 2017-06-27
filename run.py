#!/usr/bin/python

from interface import Interface
import time

# Initialize and launch the interface
interface = Interface()

while (True):
	interface.update()
	interface.fpsClock.tick(interface.fpsLimit)
