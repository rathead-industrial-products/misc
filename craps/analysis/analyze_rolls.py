#
# Analyze dice rolls
# Read lines of shooter rolls from stdin
#

import sys
import statistics
import sys; sys.path.append('../modules')
import roll


POINTS      = (4,5,6,8,9,10)
CRAPS       = (2,3,12)
SVN11       = (7,11)
MAX_THROW   = 12
N_SHOOTERS  = 100000


def get_shooters(n_shooters=N_SHOOTERS):
    shooters = []
    while n_shooters:
        shooters.append(roll.seq())
        n_shooters -= 1
    return (shooters)

def meanMedianModeStdDev(data, incl_sd=False):
    '''statistics.mode (version < 3.8) will generate an exception if no unique mode found.'''
    try:    mode = statistics.mode(data)                             # returns first mode found
    except: mode = max([p[0] for p in statistics._counts(data)])    # returns largest if no unique mode
    return (round(statistics.mean(data), 1), statistics.median(data), mode, round(statistics.stdev(data), ))

def histogram(data, normalize=False):
    '''Given a list of non-negative integers, return a tuple of the number of occurances of each integer.
       If normalize is True, convert each bin to a percentage of the total number of occurrances. '''
    DECIMALS = None
    if not data: return (None)  # return None if empty data set input
    largest_int = max(data)     # number of bins in histogram
    hist = [0] * (largest_int+1)
    for d in data:
        hist[d] += 1            # increment bin
    if normalize:
        total = sum(hist)
        hist = [round(100.0*bin/total, DECIMALS) for bin in hist]
    return (tuple(hist))

def rollLength(shooters):
    n_rolls = [len(s) for s in shooters]
    return (n_rolls, meanMedianModeStdDev(n_rolls))

def pointsCovered(shooters):    # for each shooter calculate maximum number of points covered, assuming continuous come line betting
    '''Returns ((shooter1_pts_covered, shooter2_pts_covered, ...), (mean, median, mode))'''
    points_covered = []
    n_shooters = 0
    for s in shooters:
        points_covered.append(0)
        points = [False] * MAX_THROW
        for throw in s:
            if throw in POINTS:
                points[throw] = True
            if throw == 7:      # all points 7-out
                points_covered[-1] = max(points_covered[-1], points.count(True))
                points = [False] * MAX_THROW
    return (points_covered, meanMedianModeStdDev(points_covered))

def pointsMade(shooters):    # for each shooter calculate total number of points made, assuming continuous come betting
    '''Returns ((shooter1_pts_made, shooter2_pts_made, ...), (mean, median, mode))'''
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
    return (points_made, meanMedianModeStdDev(points_made))

def pointsMadePerPointCovered(shooters):
    '''For each number of points covered (1-6) in a shooter's roll, construct a histogram of points made.'''
    shooters_points_covered = pointsCovered(shooters)[0]
    shooters_points_made    = pointsMade(shooters)[0]
    n_shooters = len(shooters)
    points_covered_hist = [None]                                # 0 points covered never occurs
    for p in range(1,7):                                        # from 1 to 6 points covered
        points_made = []                                        # list of points made for this number of points covered
        for i in range(n_shooters):                             # search all shooters for this number of points covered
            if shooters_points_covered[i] == p:
                points_made.append(shooters_points_made[i])
        points_covered_hist.append(histogram(points_made, True))
    return (points_covered_hist)

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

roll.seed()
shooters = get_shooters()

# print(shooters)   # source data 
(rolls_per_shooter, roll_stats) = rollLength(shooters)
(points_made_per_shooter, points_made_stats) = pointsMade(shooters)
(points_covered_per_shooter, points_covered_stats) = pointsCovered(shooters)
points_made_per_point_covered = pointsMadePerPointCovered(shooters)
rps_hist = histogram(rolls_per_shooter, True)
pmps_hist = histogram(points_made_per_shooter, True)
pcps_hist = histogram(points_covered_per_shooter, True)
pmppc_hist = pointsMadePerPointCovered(shooters)


print("rolls per shooter", roll_stats, rps_hist)
print("points made per shooter", points_made_stats, pmps_hist)
print("points covered per shooter", points_covered_stats, pcps_hist)
print("points made per point covered", pmppc_hist)

writeCSV("roll_histogram.csv", (rps_hist, pmps_hist, pcps_hist, pmppc_hist), ("rolls per shooter", "points made per shooter", "points covered per shooter", "points made per point covered"))
