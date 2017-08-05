#!/usr/bin/python

def calc_status(interface):
	# Declare variables
	cells = interface.grid.cells
	cellsToCalc = interface.grid.cellsToCalc
	neighborsToCalc = []
	tempList = []

	try:
		gridLength = len(cells)
		gridHeight = len(cells[0])
	except IndexError:
		# Grid length or height is 0
		# because screen size is too small
		# Don't do any calculations
		return
	
	# Create array of new alive/dead stats
	#tempGrid = [[False for x in range(gridHeight)] for x in range(gridLength)]
	
	# Iterate through list of cells to add neighbors to temp list if they are not in either list
	for cell in cellsToCalc:
		for z in range (len(cell.neighbors)):
			if cell.neighbors[z].added == False:
				cell.neighbors[z].added = True
				neighborsToCalc.append(cell.neighbors[z])
			
	# Iterate through temp list to add cells to cellsToCalc
	for cell in neighborsToCalc:
		cellsToCalc.append(cell)
	
	# Iterate through cells to see what needs to be changed
	for cell in cellsToCalc:
		cell.added = False # Reset cells added attribute
	
		totalAliveNeighbors = 0

		# Add neighbors of each cell
		for z in range (len(cell.neighbors)):		
			if cell.neighbors[z].alive == True:
				totalAliveNeighbors += 1
				if totalAliveNeighbors > interface.populationLimit:
					break
		
		# Decide if cell is alive or dead	
		if totalAliveNeighbors < interface.populationMin:
			cell.tempAlive = False
		elif totalAliveNeighbors >= interface.populationMin and totalAliveNeighbors < interface.populationLimit:
			cell.tempAlive = cell.alive
		elif totalAliveNeighbors == interface.populationLimit:
			cell.tempAlive = True
		else:
			cell.tempAlive = False 
			
		# Add cells to temp list	
		tempList.append(cell)
		
		#if totalAliveNeighbors < interface.populationMin:
			#tempGrid[cell.gridx][cell.gridy] = False
		#elif totalAliveNeighbors >= interface.populationMin and totalAliveNeighbors < interface.populationLimit:
			#tempGrid[cell.gridx][cell.gridy] = cell.alive
		#elif totalAliveNeighbors == interface.populationLimit:
			#tempGrid[cell.gridx][cell.gridy] = True
		#else:
			#tempGrid[cell.gridx][cell.gridy] = False
		
	# Clear calc list
	cellsToCalc.clear()
			
	# Iterate through tempList and update cells
	for cell in tempList:
		if cell.alive != cell.tempAlive:
			cell.alive = cell.tempAlive
			interface.grid.cellsToRedraw.append(cell)# Add cells to update lists
		if cell.alive:
			cellsToCalc.append(cell)# Add cells to update lists
			cell.added = True
		# Reset temp status
		cell.tempAlive = False
	
	
	
	# Iterate through tempgrid and update grid			
	# for x in range(gridLength):
		# for y in range(gridHeight):
			# if cells[x][y].alive != tempGrid[x][y]:
				# cells[x][y].alive = tempGrid[x][y]
			# # Add cells to update lists
				# interface.grid.cellsToRedraw.append(cells[x][y])
			# if cells[x][y].alive:
				# cellsToCalc.append(cells[x][y])
				# cells[x][y].added = True
				
					
	#Increase generation and update display
	interface.generation += 1
	interface.controls.updateGenerationDisplay(interface.generation)
