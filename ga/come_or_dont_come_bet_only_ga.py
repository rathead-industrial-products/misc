#
# Optimize craps win (loss) betting only the come (pass) line or the don't come (don't pass) line
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

COME      = True     # come/don't come GLOBAL selector
DONT_COME = not COME

DICE_SEQUENCES = "../craps/sequence7/sequence7_100K.txt"

POPULATION_SIZE     = 80         # 20 - 40
CROSSOVER_RATE      = 0.95      # the chance that two chromosomes exchange some of their parts
MUTATION_RATE       = 0.10      # how many chromosomes are mutated in one generation ( < 0.05 )
GENERATIONS         = 50
N_GENES             = 9
N_GENE_BETS_WORKING = 6
GENE_CRAP           = 7
GENE_11             = 8

RANDOM_SEED     = 314

MIN_BET = 1     # must be at least 1 or solution will converge on zero
MAX_BET = 10

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
        # c = [1, 1, 1, 1, 5, 10, 10, 0, -5]
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
        self.bank = 0
        self.total_bet = 0

    def __call__(self, individual, show=False):
        t = simple_table.table()
        pointsWorking = t.workingPointsRight if COME else t.workingPointsWrong
        collectPayout = t.collectPayoutRight if COME else t.collectPayoutWrong
        placeBet = t.comeBet if COME else t.dontComeBet
        last_throw = 0
        self.bank = 0
        self.total_bet = 0
        for s in self.roll_seq:
            for throw in s:
                # bet is dictated by genes
                bet = individual[len(pointsWorking())]
                if last_throw in simple_table.CRAPS:
                    if not (DONT_COME and simple_table.BAR):
                        bet += individual[GENE_CRAP]
                if last_throw == 11:
                    bet += individual[GENE_11]
                bet = min(MAX_BET, max(MIN_BET, bet))
                placeBet(bet)
                self.bank -= bet
                self.total_bet += bet
                t.action(throw)
                payout = collectPayout()    # table payoff including amount bet
                self.bank += payout    # table payoff including amount bet
                if show: print (bet, throw, payout, self.bank)
                last_throw = throw
            if show: print (s, self.bank)
        return (self.bank/self.total_bet if self.total_bet else 0.0)

def rankPopulation(population):
    with mp.Pool() as p:
        fit = p.map(fitness(roll_seq), population)      # fit order is same as population order (map preserves order)
    rp_ranked_by_fit = sorted(zip(fit, population), reverse=True)
    (fit, rp) = zip(*rp_ranked_by_fit)
    return (rp)

def getRollSequences():
    sequence = []
    with open(DICE_SEQUENCES) as f:
        for line in f.readlines():
            lstr = line.strip()[1:-1].split(',')
            l = tuple([int(i) for i in lstr])
            sequence.append(l)
        return (tuple(sequence))
    
def showResults(generation, roll_seq, gene, show_gene=False):
    DEBUG_SHOW_INDIVIDUAL_ROLLS = False
    f = fitness(roll_seq)
    pct_rtn = f(gene, DEBUG_SHOW_INDIVIDUAL_ROLLS) * 100
    if show_gene:
        print ("Generation %d, %s, win pct = %.2f%%, bank = %d" % (generation, gene, pct_rtn, f.bank))
    else:
        print ("Generation %d, %.2f" % (generation, pct_rtn))

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
        showResults(g, roll_seq, pop[0], not g%10)

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
    showResults(GENERATIONS, roll_seq, pop[0], True)

    print('Execution time = %0.1f sec ' % (time.time() - start_time))