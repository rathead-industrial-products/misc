#
# Gemerate baseline data set for pass/come don't pass/don't come betting.
#
# For each shooter, bet 1 unit on come (don't come) every roll.
# After shooter 7s-out, calculate total shooter's payout.
# Aggregate data across ** many ** shooters.
#
# Summarize data:
# For each roll of length n, calculate:
# 	payout					(mean, median, mode, and std dev)
#	Number of points made	 		(mean, median, mode, and std dev)
#	Number of points riding at 7-out	(mean, median, mode, and std dev)
# Plot number of rolls vs:
#	mean payout with std dev error bars
#

import sys; sys.path.append('../modules')
import roll

N_SHOOTERS = 10
 
def longestSeq(shooters):
    # find the longest roll sequence out of all the shooters
    longest = 0
    for s in shooters:
        if len(s) > longest: longest = len(s)
    return (longest)


#
# Main
#

shooters = [roll.seq() for i in range(N_SHOOTERS)]
hist_right = []
hist_wrong = []
for i in range(longestSeq(shooters)+1): # create an empty histogram of arrays to hold payouts
    hist_right.append([])
    hist_wrong.append([])
for s in shooters:  # create histogram of payouts vs length of roll sequence
    hist_right[roll.rollLength(s)].append(roll.payoutRight(s))
    hist_wrong[roll.rollLength(s)].append(roll.payoutWrong(s))
for i in range(longestSeq(shooters)+1): # calculate statistics on multiple results in each histogram bin
    if hist_right[i]: pass
    if hist_wrong[i]: pass


print (hist_right)
print (hist_wrong)

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