#
# Optimize predicting a coin flip using a genetic algorithm
#
#
# A gene controls the prediction for each coin flip.
# 10 coin flips requires a chromosome with 10 genes.
#
# 

import random


POPULATION_SIZE = 30        # 20 - 40
CROSSOVER_RATE  = 0.95      # the chance that two chromosomes exchange some of their parts
MUTATION_RATE   = 0.05      # how many chromosomes are mutated in one generation ( < 0.05 )

RANDOM_SEED     = 314

def init_population(pop_size, n_genes):
    population = []
    for c in range(pop_size):
        c = []
        for g in range(n_genes):
            c.append(random.randint(0,1))
        population.append(c)
    return (population)

def selection(ranked_population):
    pairs = []
    half = len(ranked_population)//2
    for i in range(half):
        partner = random.randint(i, half-1)  # partner the most fit with a random individual in the top half
        pairs.append([ranked_population[i], ranked_population[partner]])
    return (pairs)

def crossover(parent1, parent2, crossover_rate):
    if random.randint(1, 100) <= int(100 * crossover_rate):
        x = random.randint(1,len(parent1)-1)    # always crossover at least one gene
        child1 = parent1[:x] + parent2[x:]
        child2 = parent2[:x] + parent1[x:]
        return ([child1, child2])
    else:
        return ([parent1, parent2])

def mutate(population, mutation_rate):
    for individual in population:
        if random.randint(1, 100) <= int(100 * mutation_rate):
            gene = random.randint(0,len(individual)-1)
            print("mutate", individual, gene)
            individual[gene] = (1 - individual[gene])

def fitness(individual):
    fit = 0
    for f in range(len(COIN_FLIP)):
        if individual[f] == COIN_FLIP[f]:
            fit += 1
        else:
            fit -= 1
    return (fit)

def rankPopulation(population):
    rp = sorted(population, key=fitness, reverse=True)
    return (rp)


#
# Main 
#

GENERATIONS = 50

COIN_FLIP = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1]
random.seed(RANDOM_SEED)

pop = init_population(4, len(COIN_FLIP))

for g in range(GENERATIONS):

    pop = rankPopulation(pop)
    print ("Generation", g)
    for p in pop: print (p, fitness(p))
    print()

    pairs = selection(pop)
    pop = []

    for parent in pairs:
        for p in parent: print (p, fitness(p))
        print ()

        children = crossover(parent[0], parent[1], CROSSOVER_RATE)
        for c in children:
            pop.append(c)
            print (c, fitness(c))
        print ()

    mutate(pop, MUTATION_RATE)

