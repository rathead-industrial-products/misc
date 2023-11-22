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

import multiprocessing as mp
import random, sys, time
import simple_table

DICE_SEQUENCES = "../craps/sequence7/sequence7_10K.txt"

POPULATION_SIZE     = 20         # 20 - 40
CROSSOVER_RATE      = 0.95      # the chance that two chromosomes exchange some of their parts
MUTATION_RATE       = 0.05      # how many chromosomes are mutated in one generation ( < 0.05 )
GENERATIONS         = 50
N_GENES             = 9
N_GENE_BETS_WORKING = 6
GENE_CRAP           = 7
GENE_11             = 8

RANDOM_SEED     = 314

MIN_BET = 1
MAX_BET = 5

def randomGeneValue(gene):
    if gene == GENE_CRAP or gene == GENE_11:
        return(random.randint(-MAX_BET, MAX_BET))
    else:
        return(random.randint(MIN_BET, MAX_BET))

def initPopulation(pop_size, N_GENES):
    population = []
    for c in range(pop_size):
        c = []
        for g in range(N_GENES):
            c.append(randomGeneValue(g))
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
            #print("mutate", individual, gene)
            individual[gene] = randomGeneValue(gene) # mutate the gene

class fitness:
    def __init__(self, roll_seq):
        self.roll_seq = roll_seq

    def __call__(self, individual):
        t = simple_table.table()
        last_throw = 0
        bank = 0
        for s in self.roll_seq:
            for throw in s:
                # bet is dictated by genes
                bet = individual[len(t.workingPointsRight())]
                if last_throw in simple_table.CRAPS:
                    bet += individual[GENE_CRAP]
                    bet = max(0, bet)       # can't bet < 0
                if last_throw == 11:
                    bet += individual[GENE_11]
                    bet = max(0, bet)       # can't bet < 0
                t.comeBet(bet)
                bank -= bet
                t.action(throw)
                payout = t.collectPayoutRight()    # table payoff including amount bet
                bank += payout    # table payoff including amount bet
                # bank += t.collectPayoutRight()    # table payoff including amount bet
                # print (bet, throw, payout, bank)
                last_throw = throw
            # print (s, bank)
        return (bank)

def rankPopulation(population):
    with mp.Pool() as p:
        fit = p.map(fitness(roll_seq), population)      # fit order is same as population order (map preserves order)
    rp_ranked_by_fit = sorted(zip(fit, population), reverse=True)
    (fit, rp) = zip(*rp_ranked_by_fit)

    #print ("d", rp_ranked_by_fit)
    #print ("d", population)
    #print ("d", rp)

    #rp = sorted(population, key=fitness(roll_seq), reverse=True)
    return (rp)

def getRollSequences():
    sequence = []
    with open(DICE_SEQUENCES) as f:
        for line in f.readlines():
            lstr = line.strip()[1:-1].split(',')
            l = tuple([int(i) for i in lstr])
            sequence.append(l)
        return (tuple(sequence))
#
# Main 
#
if __name__ == '__main__':
    start_time = time.time()
    random.seed(RANDOM_SEED)
    pop = initPopulation(POPULATION_SIZE, N_GENES)
    roll_seq = getRollSequences()

    for g in range(GENERATIONS):
        pop = rankPopulation(pop)
        print ("Generation", g)

        if g % 10 == 0:
            print (pop[0], fitness(roll_seq)(pop[0]))
            #print()

        pairs = selection(pop)
        pop = []
        for parent in pairs:
            #for p in parent: print (p, fitness(p))
            #print ()

            children = crossover(parent[0], parent[1], CROSSOVER_RATE)
            for c in children:
                pop.append(c)
                #print (c, fitness(c))
            #print ()

        mutate(pop, MUTATION_RATE)

    pop = rankPopulation(pop)
    print ("Generation", g)
    for p in pop: print (p, fitness(roll_seq)(p))

    print('Execution time = %0.1f sec ' % (time.time() - start_time))