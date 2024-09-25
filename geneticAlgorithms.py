import random
import numpy as np
from numpy import genfromtxt
from getGraphFromExcel import ExcelFinder

import random
import numpy as np

# Function to calculate total distance, without returning to the start
def calculate_total_distance_no_return(path, distance_matrix):
    total_distance = 0
    for i in range(len(path) - 1):
        distance = distance_matrix[path[i], path[i + 1]]
        if np.isinf(distance):
            return 1e7
        total_distance = total_distance + distance
    return total_distance

    # return sum(distance_matrix[path[i], path[i + 1]] for i in range(len(path) - 1))

# Create initial population (random permutations of nodes, with a fixed starting node)
def create_population(population_size, num_nodes, start_node):
    population = []
    for _ in range(population_size):
        remaining_nodes = list(set(range(num_nodes)) - {start_node})  # Nodes excluding the start node
        random.shuffle(remaining_nodes)  # Randomize the order of the remaining nodes
        population.append([start_node] + remaining_nodes)  # Add the start node at the beginning
    return population

# Fitness function (inverse of total distance, without return)
def fitness(path, distance_matrix):
    return 1 / calculate_total_distance_no_return(path, distance_matrix)

# Tournament selection for choosing parents
def tournament_selection(population, fitnesses, k=5):
    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1], reverse=True)
    return selected[0][0]

# Ordered crossover with a fixed starting node
def crossover(parent1, parent2, start_node):
    size = len(parent1)
    start, end = sorted(random.sample(range(1, size), 2))  # Start from index 1 (since index 0 is fixed)
    child = [None] * size
    child[0] = start_node  # Ensure the starting node stays fixed
    child[start:end] = parent1[start:end]
    pointer = 1
    for node in parent2:
        if node not in child:
            while child[pointer] is not None:
                pointer += 1
            child[pointer] = node
    return child

# Mutation (swapping two cities, excluding the starting node)
def mutate(path, mutation_rate):
    for i in range(1, len(path)):  # Skip index 0 (starting node)
        if random.random() < mutation_rate:
            j = random.randint(1, len(path) - 1)
            path[i], path[j] = path[j], path[i]

# Main genetic algorithm with a fixed starting node and no return to start
def genetic_algorithm(distance_matrix, population_size, mutation_rate, generations, start_node):
    num_nodes = len(distance_matrix)
    population = create_population(population_size, num_nodes, start_node)
    
    for generation in range(generations):
        # Evaluate fitness for each individual
        fitnesses = [fitness(individual, distance_matrix) for individual in population]
        
        # Create new population using selection, crossover, and mutation
        new_population = []
        for _ in range(population_size // 2):
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child1 = crossover(parent1, parent2, start_node)
            child2 = crossover(parent2, parent1, start_node)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.extend([child1, child2])
        
        population = new_population
    
    # Find and return the best solution from the final population
    best_individual = max(population, key=lambda x: fitness(x, distance_matrix))
    best_distance = calculate_total_distance_no_return(best_individual, distance_matrix)
    return best_individual, best_distance

# Example Usage
# Load your distance matrix here (should be a 98x98 NumPy array)
e = ExcelFinder()
# distance_matrix = genfromtxt('distanceMatrix.csv', delimiter=',')
# distance_matrix = e.getDistanceMatrixWithNoDirectConnections()
distance_matrix = np.array(e.getDistanceMatrix())
# Set parameters
population_size = 500
mutation_rate = 0.01
generations = 500
start_node = 4

# Run the genetic algorithm
best_path, best_distance = genetic_algorithm(distance_matrix, population_size, mutation_rate, generations, start_node)
stationNames = e.getStationNames()

pathByStations = []
for elem in best_path:
    pathByStations.append(stationNames[elem])

print("Best Path:", best_path)
print(pathByStations)
print("Best Distance:", best_distance)
