#!/usr/bin/python

def calc_status(interface):
	# Declare variables
	totalAliveNeighbors = 0
	cells = interface.grid.cells

	try:
		gridLength = len(cells)
		gridHeight = len(cells[0])
	except IndexError:
		# Grid length or height is 0
		# because screen size is too small
		# Don't do any calculations
		return
	
	# Create array of new alive/dead stats
	tempGrid = [[False for x in range(gridHeight)] for x in range(gridLength)]
	
	# Iterate through cells to see what needs to be changed
	for x in range(gridLength):
		for y in range(gridHeight):
			totalAliveNeighbors = 0

			# Add neighbors of each cell
			for z in range (len(cells[x][y].neighbors)):	
				if cells[x][y].neighbors[z].alive == True:
					totalAliveNeighbors += 1
					if totalAliveNeighbors > interface.populationLimit:
						break
				
			# Decide if cell is alive or dead	
			if totalAliveNeighbors < interface.populationMin:
				tempGrid[x][y] = False
			elif totalAliveNeighbors >= interface.populationMin and totalAliveNeighbors < interface.populationLimit:
				tempGrid[x][y] = cells[x][y].alive
			elif totalAliveNeighbors == interface.populationLimit:
				tempGrid[x][y] = True
			else:
				tempGrid[x][y] = False
				
	# Iterate through tempgrid and update grid			
	for x in range(gridLength):
		for y in range(gridHeight):
			if cells[x][y].alive != tempGrid[x][y]:
				cells[x][y].alive = tempGrid[x][y]
				interface.grid.cellsToRedraw.append(cells[x][y])
				
	#Increase generation and update display
	interface.generation += 1
	interface.controls.updateGenerationDisplay(interface.generation)
