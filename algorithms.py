#!/usr/bin/python

def calc_status(grid, interface):
	
	# Declare variables
	totalAliveNeighbors = 0
	gridLength = len(grid)
	gridHeight = len(grid[0])
	
    # Create temporary array based on grid size
	tempGrid = [[False for x in range(gridHeight)] for x in range(gridLength)]
	
	# Iterate through grid
	for x in range(gridLength):
		for y in range(gridHeight):
			totalAliveNeighbors = 0
			
			# Add neighbors of each cell
			for z in range (len(grid[x][y].neighbors)):	
				if grid[x][y].neighbors[z].alive == True:
					totalAliveNeighbors += 1
					if totalAliveNeighbors > interface.populationLimit:
						break
				
			# Decide if cell is alive or dead	
			if totalAliveNeighbors < interface.populationMin:
				tempGrid[x][y] = False
			elif totalAliveNeighbors >= interface.populationMin and totalAliveNeighbors < interface.populationLimit:
				tempGrid[x][y] = grid[x][y].alive
			elif totalAliveNeighbors == interface.populationLimit:
				tempGrid[x][y] = True
			else:
				tempGrid[x][y] = False
				
	# Iterate through tempgrid and update grid			
	for x in range(gridLength):
		for y in range(gridHeight):
			grid[x][y].alive = tempGrid[x][y]
	  