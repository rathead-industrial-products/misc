#
# Generate a sequence of rolls
# Each roll is starts when a point is established, and ends on the first 7,
# even if the shooter made his point and the 7 was during a comeout
# Index [0] is an empty sequence, so index [1] corresponds to sequence 1, etc
# The output is directed to stdout

import random
import sys

RANDOM_SEED      = 314
TOTAL_SEQUENCESS = 10

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

if len(sys.argv) > 1:
    total_sequences = int(sys.argv[1])
else:
    total_sequences = TOTAL_SEQUENCESS

random.seed(RANDOM_SEED)
sequence = 0
sequence_rolls   = []
sequence_history = []
point_established = False
throw = 0

while sequence < total_sequences:
    while not (throw == 7 and point_established):
        throw = rollDice()
        sequence_rolls.append(throw)
        if throw in POINTS:
            point_established = True
    point_established = False
    sequence_history.append(tuple(sequence_rolls))
    sequence_rolls = []
    sequence += 1

for s in sequence_history:
    print(tuple(s))
