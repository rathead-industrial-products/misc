#
# Gemerate baseline data set for pass/come don't pass/don't come betting.
#
# For each shooter, bet 1 unit on come (don't come) every roll.
# After shooter 7s-out, calculate total shooter's payout.
# Aggregate data across ** many ** shooters.
#
# Summarize data:
# For each roll of length n, calculate:
# 	payout					            (mean, median, mode, and std dev)
#	Number of points made	 		    (mean, median, mode, and std dev)
#	Number of points riding at 7-out	(mean, median, mode, and std dev)
#
# For all rolls of length l > n, calculate:
#   bankroll after the lth roll         (mean, median, mode, and std dev)
#
# Plot number of rolls n vs:
#	mean payout or bankroll with std dev error bars for:
#       rolls of length n
#       bankroll at n for rolls of lenght > n
#

import sys; sys.path.append('../modules')
import roll, simple_table

N_SHOOTERS = 100000
 
def longestSeq(shooters):
    # find the longest roll sequence out of all the shooters
    longest = 0
    for s in shooters:
        if len(s) > longest: longest = len(s)
    return (longest)


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

shooters = [roll.seq() for i in range(N_SHOOTERS)]

hist_right = []
hist_wrong = []
stats_right = []
stats_wrong = []
for i in range(longestSeq(shooters)+1): # create an empty histogram of arrays to hold payouts
    hist_right.append([])
    hist_wrong.append([])
    stats_right.append([])
    stats_wrong.append([])
for s in shooters:  # create histogram of payouts vs length of roll sequence
    hist_right[roll.rollLength(s)].append(roll.payoutRight(s))
    hist_wrong[roll.rollLength(s)].append(roll.payoutWrong(s))
for i in range(longestSeq(shooters)+1): # calculate statistics on multiple results in each histogram bin
    if hist_right[i]: stats_right[i] = roll.meanMedianModeStdDev(hist_right[i])
    if hist_wrong[i]: stats_wrong[i] = roll.meanMedianModeStdDev(hist_wrong[i])

avg_right = [s[0] if len(s) else 0 for s in stats_right]
avg_wrong = [s[0] if len(s) else 0 for s in stats_wrong]

writeCSV("come_baseline.csv", (avg_right, avg_wrong), ("come payout vs roll length", "don't come payout vs roll length"))

"""
roll_length = []
payout_right = []
payout_wrong = []
pts_made = []
pts_riding = []
for shooter in range(SHOOTERS):
    seq = roll.seq()
    roll_length.append(roll.rollLength(seq))
    payout_right.append(roll.payoutRight(seq))
    payout_wrong.append(roll.payoutWrong(seq))
    pts_made.append(roll.pointsMade(seq))
    pts_riding.append(roll.pointsRiding(seq))

    #print (seq, pts_made[-1], pts_riding[-1], payout_right[-1], payout_wrong[-1])

print ("roll length", roll.meanMedianModeStdDev(roll_length))
print ("payout right", roll.meanMedianModeStdDev(payout_right))
print ("payout wrong", roll.meanMedianModeStdDev(payout_wrong))
print ("points made", roll.meanMedianModeStdDev(pts_made))
print ("points riding", roll.meanMedianModeStdDev(pts_riding))
"""