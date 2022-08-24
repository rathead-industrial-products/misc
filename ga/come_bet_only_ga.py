#
# Optimize craps win (loss) betting only the come (pass) line
#
#
# A gene controls the wager for each come bet.
#  Gene     Controls
#   0       First bet after 7-out (0 bets working)
#   1       Bet when there is 1 bet working
#   2       Bet when there are 2 bets working
#   3       Bet when there are 3 bets working
#   4       Bet when there are 4 bets working
#   5       Bet when there are 5 bets working
#   6       Bet when there are 6 bets working
#   7       Incremental +/- bet after rolling a CRAP (2, 3, 12) - add to normal bet
#   8       Incremental +/- bet after rolling an 11 - add to normal bet
#
# 

from inspect import GEN_RUNNING
import random


POPULATION_SIZE = 30        # 20 - 40
CROSSOVER_RATE  = 0.95      # the chance that two chromosomes exchange some of their parts
MUTATION_RATE   = 0.05      # how many chromosomes are mutated in one generation ( < 0.05 )
GENES           = 9

RANDOM_SEED     = 314

INC_BET_CRAP = 7
INC_BET_11   = 8

MIN_BET = 1
MAX_BET = 5

def init_population(pop_size, n_genes):
    population = []
    for c in range(pop_size):
        c = []
        for g in range(n_genes):
            c.append(random.randint(MIN_BET, MAX_BET))
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
        if random.randint(1, 100) <= int(100 * mutation_rate):  # randomly select an individual to mutate
            gene = random.randint(0,len(individual)-1)          # select a gene to mutate
            print("mutate", individual, gene)
            individual[gene] = random.randint(MIN_BET, MAX_BET) # mutate the gene

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

random.seed(RANDOM_SEED)

pop = init_population(POPULATION_SIZE, GENES)

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

