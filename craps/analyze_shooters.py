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
    '''statistics.mode (version < 3.8) will generate an exception if no unique mode found.'''
    mode = max([p[0] for p in statistics._counts(data)]) # returns largest if no unique mode
    return (statistics.mean(data), statistics.median(data), mode)

def histogram(data):
    '''Given a list of non-negative integers, return a tuple of the number of occurances of each integer.'''
    largest_int = max(data)     # number of bins in histogram
    hist = [0] * (largest_int+1)
    for d in data:
        hist[d] += 1            # increment bin
    return (tuple(hist))

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

def writeCSV(file_name, data_series=[(),(),()], column_headers= ()):
    '''Excel columns are limited to 16K and rows to 1M, so data sets are organized by columns to allow the max number of entries.'''
    '''Data series is a collection of data sets.'''
    f = open(file_name, 'w')
    for hdr in column_headers:
        f.write("%s," % (hdr)) 
    f.write('\n')
    n_series = len(data_series)
    n_rows = 0
    for series in data_series:
        n_rows = max(n_rows, len(series))
    for i in range(n_rows):
        for s in range(n_series):
            if i < len(data_series[s]): f.write("%s," % (str(data_series[s][i])))
            else:                       f.write(",")
        f.write('\n')
    f.close()

#
# Main
#

shooters = get_shooters()

# print(shooters)   # source data from file
(rolls_per_shooter, roll_stats) = rollLength(shooters)
(points_made_per_shooter, points_made_stats) = pointsMade(shooters)
rps_hist = histogram(rolls_per_shooter)
pmps_hist = histogram(points_made_per_shooter)
#print(roll_stats, rps_hist)
#print(points_made_stats, pmps_hist)

writeCSV("roll_histogram.csv", (rps_hist, pmps_hist), ("rolls per shooter", "points made per shooter"))

