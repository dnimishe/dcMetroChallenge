import pandas as pd
import csv
import numpy as np


class ExcelFinder:

    def __init__(self):
        graphDf = pd.read_excel("Graph.xlsx", sheet_name="Refined matrix")
        self.adjacency_matrix_as_list = graphDf.values.tolist()

    def getAdjacencyMatrix(self):
        refinedMatrix = [i[1:] for i in self.adjacency_matrix_as_list]
        return refinedMatrix
    
    def getDistanceMatrixWithNoDirectConnections(self):
        refinedMatrix = [i[1:] for i in self.adjacency_matrix_as_list]
        for i in range(0, len(refinedMatrix)):
            for j in range(0, len(refinedMatrix[i])):
                if refinedMatrix[i][j] == 0 and i != j:
                    refinedMatrix[i][j] = np.inf
        return np.array(refinedMatrix)
    
    def getDistanceMatrixInfinity(self):
        refinedMatrix = [i[1:] for i in self.adjacency_matrix_as_list]
        for i in range(0, len(refinedMatrix)):
            for j in range(0, len(refinedMatrix[i])):
                if refinedMatrix[i][j] == 0 and i != j:
                    refinedMatrix[i][j] = 1e7
        return refinedMatrix

    def getStationNames(self):
        stationNames = [i[0] for i in self.adjacency_matrix_as_list]
        return stationNames
    
    def exportDistanceMatrix(self, matrix):
        # df = pd.DataFrame(matrix)
        # df.to_excel(excel_writer="Distance matrix.xlsx", sheet_name="Distance matrix")
        with open("distanceMatrix.csv","w+") as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(matrix)
    
    def getDistanceMatrixFromCsv(self):
        d = list(csv.reader(open("distanceMatrix.csv")))
        distanceMatrix = [list( map(int,i) ) for i in d]
        return distanceMatrix