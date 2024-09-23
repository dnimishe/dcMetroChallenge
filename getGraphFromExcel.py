import pandas as pd


class ExcelFinder:

    def __init__(self):
        graphDf = pd.read_excel("Graph.xlsx", sheet_name="Refined matrix")
        self.adjacency_matrix_as_list = graphDf.values.tolist()
        distanceMatrixDf = pd.read_excel("Distance matrix.xlsx", sheet_name="Distance matrix")
        self.distance_matrix_as_list = distanceMatrixDf.values.tolist()

    def getAdjacencyMatrix(self):
        refinedMatrix = [i[1:] for i in self.adjacency_matrix_as_list]
        return refinedMatrix

    def getStationNames(self):
        stationNames = [i[0] for i in self.adjacency_matrix_as_list]
        return stationNames
    
    def exportDistanceMatrix(self, matrix):
        df = pd.DataFrame(matrix)
        df.to_excel(excel_writer="Distance matrix.xlsx", sheet_name="Distance matrix")
    
    def getDistanceMatrix(self):
        refinedMatrix = [i[1:] for i in self.distance_matrix_as_list]
        return refinedMatrix