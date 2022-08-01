#
# Generate a sequence of rolls
# Each roll is an individual craps shooter and is a valid craps roll
# The sequence ends when the shooter 7-outs
# Index [0] is an empty sequence, so index [1] corresponds to shooter 1, etc
# The output is directed to stdout

import random
import sys

RANDOM_SEED    = 314
TOTAL_SHOOTERS = 10

POINTS      = (4,5,6,8,9,10)
CRAPS       = (2,3,12)
SVN11       = (7,11)
MAX_THROW   = 12


def rollDice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    return (die1 + die2)

#
# Main
#

if len(sys.argv):
    total_shooters = int(sys.argv[1])
else:
    total_shooters = TOTAL_SHOOTERS

random.seed(RANDOM_SEED)
shooters = 0
point    = None
shooter_rolls   = []
shooter_history = []

while shooters < total_shooters:
    throw = rollDice()
    shooter_rolls.append(throw)
    if not point and throw in POINTS:   # shooter has a point now
        point = throw
    elif point:
        if throw == point:              # shooter made point, comeout roll now
            point = None
        if throw == 7:                  # shooter out
            point = None
            shooter_history.append(tuple(shooter_rolls))
            shooter_rolls = []
            shooters += 1

for s in shooter_history:
    print(tuple(s))