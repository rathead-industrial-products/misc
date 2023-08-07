#
# Analyze dice rolls
# Definitions:
#   Sequence: A series of rolls ending with a 7. The length of a sequence
#       can be as short as one roll.
#   Trial(n): A collection of sequences totaling at least n rolls. A trial
#       is complete on the first 7 rolled after n-1 rolls.
#
#

import sys
import statistics
import sys; sys.path.append('../modules')
import roll


POINTS      = (4,5,6,8,9,10)
CRAPS       = (2,3,12)
SVN11       = (7,11)
MAX_THROW   = 12
TRIAL_LEN   = 100



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

def rollLength(trial):
    n_rolls = [len(s) for s in trial]
    return (n_rolls, meanMedianModeStdDev(n_rolls))

def pointsCovered(trial):    # for each sequence calculate maximum number of points covered, assuming continuous come line betting
    '''Returns ((seq1_pts_covered, seq2_pts_covered, ...), (mean, median, mode))'''
    points_covered = []
    n_shooters = 0
    for s in trial:
        points_covered.append(0)
        points = [False] * MAX_THROW
        for throw in s:
            if throw in POINTS:
                points[throw] = True
            if throw == 7:      # all points 7-out
                points_covered[-1] = max(points_covered[-1], points.count(True))
                points = [False] * MAX_THROW
    return (points_covered, meanMedianModeStdDev(points_covered))

def pointsMade(trial):    # for each sequence calculate total number of points made, assuming continuous come betting
    '''Returns ((seq1_pts_made, seq2_pts_made, ...), (mean, median, mode))'''
    points_made = []
    n_shooters = 0
    for s in trial:
        points_made.append(0)
        points = [False] * MAX_THROW
        for throw in s:
            if throw in POINTS:
                if points[throw]: points_made[-1] += 1
                points[throw] = True
            if throw == 7:      # all points 7-out
                points = [False] * MAX_THROW
    return (points_made, meanMedianModeStdDev(points_made))

def pointsMadeVsRollLength(trial):
    # for each roll of length (1-max) construct a histogram of number of points made
    seqs_roll_length = rollLength(trial)[0]         # list of roll lengths
    seqs_points_made = pointsMade(trial)[0]         # number of points made on each roll aligned with seq_roll_length
    n_seqs = len(trial)
    longest_roll = max(seqs_roll_length)
    total_points_made = [0] * (longest_roll+1)          # total number of points made for each roll length across all sequences
    roll_length_occurrances = [0] * (longest_roll+1)    # number of times each roll length happens
    points_made_vs_roll_length = [0] * (longest_roll+1) # array to contain final results
    for i in range(n_seqs):                             # for each sequence
        rl = seqs_roll_length[i]                        # .. of length rl
        total_points_made[rl] += seqs_points_made[i]    # accumulate points made for a roll of length rl
        roll_length_occurrances[rl] += 1                # keep track of number of times this roll length has occurred
    for i in range(2, (longest_roll+1)):                # normalize points made - rolls of length 0 and 1 never occur
        if roll_length_occurrances[i]:                  # avoid divide-by-zero if roll length never occurred
            points_made_vs_roll_length[i] = round((total_points_made[i] / roll_length_occurrances[i]), 1)
    return(points_made_vs_roll_length)
       

def pointsMadePerPointCovered(trial):
    '''For each number of points covered (1-6) in a sequence, construct a histogram of points made.'''
    seqs_points_covered = pointsCovered(trial)[0]
    seqs_points_made    = pointsMade(trial)[0]
    n_seqs = len(trial)
    points_covered_hist = [None]                                # 0 points covered never occurs
    for p in range(1,7):                                        # from 1 to 6 points covered
        points_made = []                                        # list of points made for this number of points covered
        for i in range(n_seqs):                             # search all sequences for this number of points covered
            if seqs_points_covered[i] == p:
                points_made.append(seqs_points_made[i])
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
trial = roll.trial(TRIAL_LEN)

# print(trial)   # source data 
(rolls_per_seq, roll_stats) = rollLength(trial)
(points_made_per_seq, points_made_stats) = pointsMade(trial)
(points_covered_per_seq, points_covered_stats) = pointsCovered(trial)
points_made_per_point_covered = pointsMadePerPointCovered(trial)
rps_hist = histogram(rolls_per_seq, True)
pmps_hist = histogram(points_made_per_seq, True)
pcps_hist = histogram(points_covered_per_seq, True)
pmvrl_hist = pointsMadeVsRollLength(trial)
pmppc_hist = pointsMadePerPointCovered(trial)


print("rolls per sequence", roll_stats, rps_hist)
print("points made per sequence", points_made_stats, pmps_hist)
print("points covered per sequence", points_covered_stats, pcps_hist)
print("points made vs roll length", pmvrl_hist)
print("points made per point covered", pmppc_hist)

'''
writeCSV("roll_histogram.csv", (rps_hist, pmps_hist, pcps_hist, pmvrl_hist, pmppc_hist), 
                               ("rolls per sequence", 
                                "points made per sequence",
                                "points covered per sequence",
                                "points made vs roll length",
                                "points made per point covered"))
'''
