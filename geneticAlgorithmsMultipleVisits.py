import numpy as np
import random
from getGraphFromExcel import ExcelFinder

# Create a random route starting with the start node
def create_route():
    route = [start_node]  # Start at the specified start node
    remaining_nodes = list(range(num_nodes))
    remaining_nodes.remove(start_node)
    random.shuffle(remaining_nodes)
    route.extend(remaining_nodes)
    return route

# Calculate total distance of a route
def route_distance(route):
    total_distance = 0
    for i in range(len(route) - 1):
        start, end = route[i], route[i + 1]
        distance = adj_matrix[start][end]
        if np.isinf(distance):
            return float('inf')  # Penalize routes with no connection
        total_distance += distance
    return total_distance

# Fitness function (inverse of route distance)
def fitness(route):
    total_distance = route_distance(route)
    return 1 / total_distance if total_distance != float('inf') else 1e-6  # Small fitness for invalid routes

# Select parents based on fitness
def selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    selection_probs = [f / total_fitness for f in fitness_scores]
    return population[np.random.choice(range(len(population)), p=selection_probs)]

# Crossover (Ordered Crossover)
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(1, size), 2))  # Skip the start node (index 0)
    child = [-1] * size
    child[start:end] = parent1[start:end]

    pos = end
    for city in parent2:
        if city not in child:
            while pos < size and child[pos] != -1:
                pos = (pos + 1) % size
            child[pos] = city

    child[0] = start_node  # Ensure the start node remains fixed
    return child

# Mutation (swap two cities, excluding the start node)
def mutate(route, mutation_rate=0.05):
    for i in range(1, len(route)):  # Skip the start node
        if random.random() < mutation_rate:
            j = random.randint(1, len(route) - 1)
            route[i], route[j] = route[j], route[i]

# Genetic Algorithm
def genetic_algorithm(population_size=100, generations=500, mutation_rate=0.05):
    population = [create_route() for _ in range(population_size)]

    for gen in range(generations):
        fitness_scores = [fitness(route) for route in population]

        next_population = []
        for _ in range(population_size):
            parent1 = selection(population, fitness_scores)
            parent2 = selection(population, fitness_scores)
            child = crossover(parent1, parent2)
            mutate(child, mutation_rate)
            next_population.append(child)

        population = next_population

        best_fitness = max(fitness_scores)
        if gen % 100 == 0:
            best_route = population[fitness_scores.index(best_fitness)]
            best_distance = 1 / best_fitness if best_fitness != 0 else float('inf')
            print(f"Generation {gen}: Best route distance: {best_distance:.2f}")

    best_fitness = max(fitness_scores)
    best_route = population[fitness_scores.index(best_fitness)]
    best_distance = 1 / best_fitness if best_fitness != 0 else float('inf')
    return best_route, best_distance

# Example adjacency matrix (inf represents no direct connection)

e = ExcelFinder()
adj_matrix = e.getDistanceMatrixWithNoDirectConnections()

num_nodes = len(adj_matrix)

# Allow setting a start node (fixed in all routes)
start_node = 4

# Run the genetic algorithm
best_route, best_distance = genetic_algorithm(population_size=100, generations=1000, mutation_rate=0.05)
stationNames = e.getStationNames()

pathByStations = []
for elem in best_route:
    pathByStations.append(stationNames[elem])
print("Best route:", best_route)
print("Best distance:", best_distance)
print(pathByStations)
