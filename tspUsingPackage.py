import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming
from getGraphFromExcel import ExcelFinder

if __name__ == "__main__": 

	e = ExcelFinder()
	distanceMatrix = np.array(e.getDistanceMatrix())
	allStations = e.getStationNames()
	startingNode = 4
	print(allStations[startingNode])
	print(e.getDistanceMatrix())
	# permutation, distance = solve_tsp_dynamic_programming(distanceMatrix)
	# print(permutation)
	# print(distance)