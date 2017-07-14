#!/usr/bin/python

def calc_status(grid):
	# Variables
	totalAliveNeighbors = 0
	populationLimit = 3
	cells = grid.cells
	gridLength = len(cells)
	gridHeight = len(cells[0])
	
	# Create array of new alive/dead stats
	tempGrid = [[False for x in range(gridHeight)] for x in range(gridLength)]
	
	# Iterate through cells to see what needs to be changed
	for x in range(gridLength):
		for y in range(gridHeight):
			totalAliveNeighbors = 0
			for z in range (len(cells[x][y].neighbors)):	
				if cells[x][y].neighbors[z].alive == True:
					totalAliveNeighbors += 1
			if totalAliveNeighbors < populationLimit-1:
				tempGrid[x][y] = False
				
			elif totalAliveNeighbors == populationLimit-1:
				
				if cells[x][y].alive == True:
					tempGrid[x][y] = True
				else:
					tempGrid[x][y] = False
			elif totalAliveNeighbors == populationLimit:
				tempGrid[x][y] = True
				
			else:
				tempGrid[x][y] = False
				
	for x in range(gridLength):
		for y in range(gridHeight):
			if cells[x][y].alive != tempGrid[x][y]:
				cells[x][y].alive = tempGrid[x][y]
				grid.cellsToRedraw.append(cells[x][y])
	  
