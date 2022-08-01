#
# Analyze dice rolls
# Read lines of shooter rolls from stdin
#

import sys
import statistics


POINTS      = (4,5,6,8,9,10)
CRAPS       = (2,3,12)
SVN11       = (7,11)
MAX_THROW   = 12


def get_shooters():
    shooters = []
    for line in sys.stdin:
        lstr = line.strip()[1:-1].split(',')
        l = tuple([int(i) for i in lstr])
        shooters.append(l)
    return (tuple(shooters))

def meanMedianMode(data):
    return (statistics.mean(data), statistics.median(data), statistics.mode(data))

def rollLength(shooters):
    n_rolls = [len(s) for s in shooters]
    return (n_rolls, meanMedianMode(n_rolls))

def pointsMade(shooters):    # assume continuous come line betting
    points_made = []
    n_shooters = 0
    for s in shooters:
        points_made.append(0)
        points = [False] * MAX_THROW
        for throw in s:
            if throw in POINTS:
                if points[throw]: points_made[-1] += 1
                points[throw] = True
            if throw == 7:      # all points 7-out
                points = [False] * MAX_THROW
    return (points_made, meanMedianMode(points_made))

#
# Main
#

shooters = get_shooters()

# print(shooters)
print(rollLength(shooters)[1])
print(pointsMade(shooters)[1])

