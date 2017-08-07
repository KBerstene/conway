#!/usr/bin/python

def calc_status(interface):
	# Declare variables
	cellsToCalc = interface.grid.cellsToCalc
	neighborsToCalc = []
	tempList = []
	
	
	# Iterate through list of cells to add neighbors to temp list if they are not in either list
	for cell in cellsToCalc:
		for neighbor in cell.neighbors:
			if neighbor.added == False:
				neighbor.added = True
				neighborsToCalc.append(neighbor)
	
	# Iterate through temp list to add cells to cellsToCalc
	for cell in neighborsToCalc:
		cellsToCalc.append(cell)
	
	# Iterate through cells to see what needs to be changed
	for cell in cellsToCalc:
		cell.added = False # Reset cells added attribute
		
		totalAliveNeighbors = 0
		
		# Add neighbors of each cell
		for neighbor in cell.neighbors:		
			if neighbor.alive == True:
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
	
	# Clear calc list
	cellsToCalc.clear()
	
	# Iterate through tempList and update cells
	for cell in tempList:
		if cell.alive != cell.tempAlive:
			cell.alive = cell.tempAlive
			
			# Create neighbors if the cell hasn't fully populated yet
			interface.grid.createNeighbors(cell)
			
			# Add cells to update lists
			interface.grid.cellsToRedraw.append(cell)
		if cell.alive:
			cellsToCalc.append(cell)# Add cells to update lists
			cell.added = True
		# Reset temp status
		cell.tempAlive = False			
	
	#Increase generation and update display
	interface.generation += 1
	interface.controls.updateGenerationDisplay(interface.generation)
