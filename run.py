#!/usr/bin/python

from interface import Interface
import time

# Create an interface
interface = Interface()

# Start the simulation
interface.start()

# ---TESTING CODE--- #
# Wait three seconds, then change one of the squares to alive
time.sleep(3)
interface.grid[27][18]=True

# -END TESTING CODE- #
