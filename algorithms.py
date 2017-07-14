#!/usr/bin/python

def calc_status(grid, interface):
	# Declare variables
	totalAliveNeighbors = 0
<<<<<<< HEAD
=======
	populationLimit = 2
>>>>>>> Added control individual redraw.  Most redrawing takes no time at all now.  Huge grids still take a long time to draw, but I don't know how much more can be optimized.
	cells = grid.cells
	gridLength = len(cells)
	gridHeight = len(cells[0])

	# Create array of new alive/dead stats
	tempGrid = [[False for x in range(gridHeight)] for x in range(gridLength)]
	
	# Iterate through grid
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
<<<<<<< HEAD
				grid.cellsToDraw.append(cells[x][y])
=======
				grid.cellsToRedraw.append(cells[x][y])
	  
>>>>>>> Added control individual redraw.  Most redrawing takes no time at all now.  Huge grids still take a long time to draw, but I don't know how much more can be optimized.
