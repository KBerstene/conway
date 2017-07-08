#!/usr/bin/python


def calc_status(grid):
	#variables
	totalAliveNeighbors = 0
	populationLimit = 3
	gridLength = len(grid.cells)
	gridHeight = len(grid.cells[0])
	
    #create temporary array
	tempGrid = [[False for x in range(gridHeight)] for x in range(gridLength)]
			 
	#1337 maths
	for x in range(gridLength):
		for y in range(gridHeight):
			totalAliveNeighbors = 0
			for z in range (len(grid.cells[x][y].neighbors)):	
				if grid.cells[x][y].neighbors[z].alive == True:
					totalAliveNeighbors += 1
			if totalAliveNeighbors < populationLimit-1:
				tempGrid[x][y] = False
				
			elif totalAliveNeighbors == populationLimit-1:
				
				if grid.cells[x][y].alive == True:
					tempGrid[x][y] = True
				else:
					tempGrid[x][y] = False
			elif totalAliveNeighbors == populationLimit:
				tempGrid[x][y] = True
				
			else:
				tempGrid[x][y] = False
				
	for x in range(gridLength):
		for y in range(gridHeight):
			grid.cells[x][y].alive = tempGrid[x][y]
	  
	  