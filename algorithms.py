#!/usr/bin/python

def calc_status(grid):
	
	#variables
	totalAliveNeighbors = 0
	populationLimit = 3
	populationMin = 2
	gridLength = len(grid)
	gridHeight = len(grid[0])
	
    #create temporary array based on grid size
	tempGrid = [[False for x in range(gridHeight)] for x in range(gridLength)]
	
	#iterate through grid
	for x in range(gridLength):
		for y in range(gridHeight):
			totalAliveNeighbors = 0
			
			#add neighbors of each cell
			for z in range (len(grid[x][y].neighbors)):	
				if grid[x][y].neighbors[z].alive == True:
					totalAliveNeighbors += 1
					if totalAliveNeighbors > populationLimit:
						break
				
			#decide if cell is alive or dead	
			if totalAliveNeighbors < populationMin:
				tempGrid[x][y] = False
			elif totalAliveNeighbors == populationMin:
				if grid[x][y].alive == True:
					tempGrid[x][y] = True
				else:
					tempGrid[x][y] = False
			elif totalAliveNeighbors == populationLimit:
				tempGrid[x][y] = True
			else:
				tempGrid[x][y] = False
				
	#iterate through tempgrid and update grid			
	for x in range(gridLength):
		for y in range(gridHeight):
			grid[x][y].alive = tempGrid[x][y]
	  