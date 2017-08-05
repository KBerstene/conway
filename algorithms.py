#!/usr/bin/python

def calc_status(interface):
	# Declare variables
	cells = interface.grid.cells
	cellsToCalc = interface.grid.cellsToCalc
	neighborsToCalc = []

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
	
	# Iterate through list of cells to add neighbors to temp list
	for cell in cellsToCalc:
		for z in range (len(cells[cell.gridx][cell.gridy].neighbors)):
			neighborsToCalc.append(cells[cell.gridx][cell.gridy].neighbors[z])
			
	# Iterate through temp list to check for duplicates and add cells to cellsToCalc
	for cell in neighborsToCalc:
		if cell.added == False:
			cell.added = True
			cellsToCalc.append(cell)
	
	# Iterate through cells to see what needs to be changed
	for cell in cellsToCalc:
		cell.added = False # Reset cells added attribute
	
		totalAliveNeighbors = 0

		# Add neighbors of each cell
		for z in range (len(cells[cell.gridx][cell.gridy].neighbors)):		
			if cells[cell.gridx][cell.gridy].neighbors[z].alive == True:
				totalAliveNeighbors += 1
				if totalAliveNeighbors > interface.populationLimit:
					break
			
		# Decide if cell is alive or dead	
		if totalAliveNeighbors < interface.populationMin:
			tempGrid[cell.gridx][cell.gridy] = False
		elif totalAliveNeighbors >= interface.populationMin and totalAliveNeighbors < interface.populationLimit:
			tempGrid[cell.gridx][cell.gridy] = cells[cell.gridx][cell.gridy].alive
		elif totalAliveNeighbors == interface.populationLimit:
			tempGrid[cell.gridx][cell.gridy] = True
		else:
			tempGrid[cell.gridx][cell.gridy] = False
				
	cellsToCalc.clear()
	
	# Iterate through tempgrid and update grid			
	for x in range(gridLength):
		for y in range(gridHeight):
			if cells[x][y].alive != tempGrid[x][y]:
				cells[x][y].alive = tempGrid[x][y]
			# Add cells to update lists
				interface.grid.cellsToRedraw.append(cells[x][y])
			if cells[x][y].alive:
				cellsToCalc.append(cells[x][y])
				cells[x][y].added = True
				
	#Increase generation and update display
	interface.generation += 1
	interface.controls.updateGenerationDisplay(interface.generation)
