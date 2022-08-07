import random, statistics, sys

RANDOM_SEED     = 314
N_TRIALS        = 10
FLIPS_PER_TRIAL = 100

def meanMedianMode(data):
    '''statistics.mode (version < 3.8) will generate an exception if no unique mode found.'''
    try:    mode = statistics.mode(data)                             # returns first mode found
    except: mode = max([p[0] for p in statistics._counts(data)])    # returns largest if no unique mode
    return (statistics.mean(data), statistics.median(data), mode)

#
# Main
#

print (sys.argv)
try:    n_trials = int(sys.argv[1])
except: n_trials = N_TRIALS
try:    flips_per_trial = int(sys.argv[2])
except: flips_per_trial = FLIPS_PER_TRIAL

random.seed(RANDOM_SEED)

flip = []
for f in range(n_trials):
    total = 0
    for t in range(flips_per_trial):
        total += random.randint(0,1)
    total -= flips_per_trial // 2
    flip.append(total)

print (meanMedianMode(flip), round(statistics.stdev(flip), 1), (min(flip), max(flip)))

