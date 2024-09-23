import pandas as pd

def main():
    df = pd.read_excel("Distance matrix.xlsx", sheet_name="Distance matrix")
    matrix_as_list = df.values.tolist()
    # remove the first element from each array, aka the name of the station
    refinedMatrix = [i[1:] for i in matrix_as_list]
    print(refinedMatrix[0])
    return refinedMatrix

if __name__ == "__main__": 
    # var = main()
    # print(len(var))
    # print(len(var[0]))
    main()