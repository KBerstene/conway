#!/usr/bin/python

def calc_status(interface):
	# Declare variables
	#totalAliveNeighbors = 0
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
	
	#########################################
	for cell in cellsToCalc:
		x , y = interface.grid.getCellIndex(cell)
		for z in range (len(cells[x][y].neighbors)):
			neighborsToCalc.append(cells[x][y].neighbors[z])
	
	for cell in neighborsToCalc:
		cellsToCalc.append(cell)
	
	
	#print(neighborsToCalc)
	
	
	for cell in cellsToCalc:
		x , y = interface.grid.getCellIndex(cell)
	
	
	
	
	
	
	
	
	# Iterate through cells to see what needs to be changed
	#for x in range(gridLength):
		#for y in range(gridHeight):
	#########################################
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
				
	cellsToCalc.clear()
	# Iterate through tempgrid and update grid			
	for x in range(gridLength):
		for y in range(gridHeight):
			if cells[x][y].alive != tempGrid[x][y]:
				cells[x][y].alive = tempGrid[x][y]
				# Add cells to update lists
				interface.grid.cellsToRedraw.append(cells[x][y])
				cellsToCalc.append(cells[x][y])
				
				#x,y = interface.grid.getCellIndex(cells[x][y])
				#Print(x , y)
				
	#Increase generation and update display
	interface.generation += 1
	interface.controls.updateGenerationDisplay(interface.generation)
