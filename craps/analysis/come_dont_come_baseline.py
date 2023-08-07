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

table = simple_table.table()

roll.seq(); roll.seq(); roll.seq(); roll.seq()
shooters = [roll.seq() for i in range(N_SHOOTERS)]

right_bet = 1
wrong_bet = 1

# [[shooter1-roll1 balance, shooter2-roll1 balance, ..], [shooter1-roll2 balance, shooter2-roll2 balance, ..], ..]
hist_interim_right = []     # array as described above for rolls that are still in progress
hist_interim_wrong = []
hist_completed_right = []   # array as described above for rolls that have 7'ed-out
hist_completed_wrong = []
stats_interim_right = []
stats_completed_right = []
stats_interim_wrong = []
stats_completed_wrong = []

for i in range(longestSeq(shooters)+1): # initialize arrays
    hist_interim_right.append([])
    hist_interim_wrong.append([])
    hist_completed_right.append([])
    hist_completed_wrong.append([])
    stats_interim_right.append([])
    stats_completed_right.append([])
    stats_interim_wrong.append([])
    stats_completed_wrong.append([])

for s in shooters:
    bank_right = 0
    bank_wrong = 0
    n_throws = 0
    for throw in s:
        table.comeBet(right_bet)
        bank_right -= right_bet
        table.dontComeBet(wrong_bet)
        bank_wrong -= wrong_bet

        table.action(throw)
        n_throws += 1
      
        bank_right += table.collectPayoutRight()
        bank_wrong += table.collectPayoutWrong()

        if n_throws != len(s):  # not a 7-out, collect interim bank balance data
            hist_interim_right[n_throws].append(bank_right + table.workingAmountRight())  # working bets are in play and haven't been lost
            hist_interim_wrong[n_throws].append(bank_wrong + table.workingAmountWrong())

    # shooter has 7'd-out
    hist_completed_right[n_throws].append(bank_right)
    hist_completed_wrong[n_throws].append(bank_wrong)

for i in range(longestSeq(shooters)+1): # calculate statistics on multiple results in each histogram bin
    if hist_interim_right[i]:   stats_interim_right[i]   = roll.meanMedianModeStdDev(hist_interim_right[i])
    if hist_completed_right[i]: stats_completed_right[i] = roll.meanMedianModeStdDev(hist_completed_right[i])
    if hist_interim_wrong[i]:   stats_interim_wrong[i]   = roll.meanMedianModeStdDev(hist_interim_wrong[i])
    if hist_completed_wrong[i]: stats_completed_wrong[i] = roll.meanMedianModeStdDev(hist_completed_wrong[i])

avg_interim_right = [s[0] if len(s) else 0 for s in stats_interim_right]
avg_completed_right = [s[0] if len(s) else 0 for s in stats_completed_right]
avg_interim_wrong = [s[0] if len(s) else 0 for s in stats_interim_wrong]
avg_completed_wrong = [s[0] if len(s) else 0 for s in stats_completed_wrong]

print (avg_interim_right)
print (avg_completed_right)
print (avg_interim_wrong)
print (avg_completed_wrong)

writeCSV("come_baseline.csv", (avg_interim_right, avg_interim_wrong, avg_completed_right, avg_completed_wrong), ("interim come", "interim don't come", "come", "don't come"))
