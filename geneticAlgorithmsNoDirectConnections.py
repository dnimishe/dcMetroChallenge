import numpy as np
import random
from getGraphFromExcel import ExcelFinder


# Create a random route (individual)
def create_route(distance_matrix):
    # Number of cities (nodes)
    num_cities = len(distance_matrix)
    return random.sample(range(num_cities), num_cities)

# Calculate total distance of a route
def route_distance(route):
    total_distance = 0
    for i in range(len(route) - 1):
        start, end = route[i], route[i+1]
        distance = distance_matrix[start][end]
        if np.isinf(distance):
            return 1e7  # Penalize routes with no connection
        # if distance == 1e7:
        #     return 1e7
        total_distance += distance
    return total_distance

# Fitness function (lower distance is better)
def fitness(route):
    return 1 / route_distance(route)  # Fitness is inversely proportional to distance

# Select parents based on fitness (roulette wheel selection)
def selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    selection_probs = [f/total_fitness for f in fitness_scores]
    return population[np.random.choice(range(len(population)), p=selection_probs)]

# Crossover (Ordered Crossover)
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[start:end] = parent1[start:end]

    pos = end
    for city in parent2:
        if city not in child:
            if pos >= size:
                pos = 0
            child[pos] = city
            pos += 1

    return child

# Mutation (swap two cities in a route)
def mutate(route, mutation_rate=0.01):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]

# Genetic Algorithm
def genetic_algorithm(distance_matrix, population_size=100, generations=500, mutation_rate=0.01):
    # Create initial population
    population = [create_route(distance_matrix) for _ in range(population_size)]

    for gen in range(generations):
        fitness_scores = [fitness(route) for route in population]

        # Create the next generation
        next_population = []
        for _ in range(population_size):
            # Select two parents
            parent1 = selection(population, fitness_scores)
            parent2 = selection(population, fitness_scores)

            # Perform crossover
            child = crossover(parent1, parent2)

            # Perform mutation
            mutate(child, mutation_rate)

            next_population.append(child)

        # Replace the old population with the new one
        population = next_population

        # Print best fitness every 100 generations
        if gen % 100 == 0:
            best_fitness = max(fitness_scores)
            best_route = population[fitness_scores.index(best_fitness)]
            print(f"Generation {gen}: Best route distance: {1 / best_fitness:.2f}")

    # Return the best route and its distance
    best_fitness = max(fitness_scores)
    best_route = population[fitness_scores.index(best_fitness)]
    return best_route, 1 / best_fitness

e = ExcelFinder()

# Distance matrix with 'inf' for no direct connections
distance_matrix = e.getDistanceMatrixWithNoDirectConnections()
# Run the genetic algorithm
best_route, best_distance = genetic_algorithm(distance_matrix, population_size=500, generations=1000, mutation_rate=0.05)
stationNames = e.getStationNames()

pathByStations = []
for elem in best_route:
    pathByStations.append(stationNames[elem])

print("Best route:", best_route)
print(pathByStations)
print("Best distance:", best_distance)
