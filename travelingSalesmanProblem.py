# Python3 program to implement traveling salesman 
# problem using naive approach. 

from getGraphFromExcel import ExcelFinder

from sys import maxsize 
from itertools import permutations
V = 98

# implementation of traveling Salesman Problem 
def travellingSalesmanProblem(graph, s): 

	# store all vertex apart from source vertex 
	vertex = [] 
	for i in range(V): 
		if i != s: 
			vertex.append(i) 

	# store minimum weight Hamiltonian Cycle 
	min_path = maxsize 
	next_permutation=permutations(vertex)
	for i in next_permutation:
		# store current Path weight(cost) 
		current_pathweight = 0

		# compute current path weight 
		k = s 
		for j in i: 
			current_pathweight += graph[k][j] 
			k = j 
		current_pathweight += graph[k][s] 

		# update minimum 
		min_path = min(min_path, current_pathweight)
		print(min_path)
		
	return min_path 


# Driver Code 
if __name__ == "__main__": 

	e = ExcelFinder()
	distanceMatrix = e.getDistanceMatrix()
	allStations = e.getStationNames()
	startingNode = 4
	print(allStations[startingNode])
	print(travellingSalesmanProblem(distanceMatrix, startingNode))