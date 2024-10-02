import numpy as np
import random
from getGraphFromExcel import ExcelFinder


# Generate a random route that starts at the START_NODE
def generate_individual(n_nodes):
    route = list(range(n_nodes))
    route.remove(START_NODE)  # Start node is fixed
    random.shuffle(route)
    return [START_NODE] + route

# Calculate the fitness (total distance) of the route
def fitness(individual):
    total_distance = 0
    for i in range(len(individual) - 1):
        total_distance += distance_matrix[individual[i]][individual[i+1]]
    return total_distance

# Create the initial population
def create_population(pop_size, n_nodes):
    return [generate_individual(n_nodes) for _ in range(pop_size)]

# Selection: Tournament selection
def select(population, fitnesses):
    tournament_size = 5
    tournament = random.sample(list(zip(population, fitnesses)), tournament_size)
    tournament = sorted(tournament, key=lambda x: x[1])
    return tournament[0][0]

# Crossover: Ordered crossover (OX)
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted([random.randint(1, size - 1) for _ in range(2)])

    child = [-1] * size
    child[start:end] = parent1[start:end]

    p2_pointer = 0
    for i in range(size):
        if child[i] == -1:
            while parent2[p2_pointer] in child:
                p2_pointer += 1
            child[i] = parent2[p2_pointer]

    return child

# Mutation: Swap mutation
def mutate(individual):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(1, len(individual)), 2)  # Don't mutate the start node
        individual[i], individual[j] = individual[j], individual[i]

# Genetic algorithm
def genetic_algorithm():
    n_nodes = len(distance_matrix)
    population = create_population(POPULATION_SIZE, n_nodes)
    
    for generation in range(GENERATIONS):
        fitnesses = [fitness(ind) for ind in population]
        new_population = []
        
        for _ in range(POPULATION_SIZE // 2):
            # Selection
            parent1 = select(population, fitnesses)
            parent2 = select(population, fitnesses)
            
            # Crossover
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            
            # Mutation
            mutate(child1)
            mutate(child2)
            
            new_population.append(child1)
            new_population.append(child2)
        
        population = new_population
    
    # Get the best solution after all generations
    fitnesses = [fitness(ind) for ind in population]
    best_individual = population[np.argmin(fitnesses)]
    
    return best_individual, min(fitnesses)

if __name__ == "__main__":
    # Sample distance matrix (NxN) where N is the number of nodes
    # You should replace this with your actual distance matrix after using Floyd-Warshall.
    e = ExcelFinder()
    distance_matrix = np.array(e.getDistanceMatrixFromCsv())

    # Parameters for the genetic algorithm
    POPULATION_SIZE = 1000
    MUTATION_RATE = 0.02
    GENERATIONS = 5000
    START_NODE = 4  # You can change this to start from any other node
    stationNames = e.getStationNames()

    # Run the genetic algorithm
    best_route, best_distance = genetic_algorithm()
    pathByStations = []
    for elem in best_route:
        pathByStations.append(stationNames[elem])

    print("Best route:", best_route)
    print(pathByStations)
    print("Best distance:", best_distance)