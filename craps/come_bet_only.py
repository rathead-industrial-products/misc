#
# Make only come bets, no odds bets.
#

import sys, simple_table


def get_sequence():
    sequence = []
    for line in sys.stdin:
        lstr = line.strip()[1:-1].split(',')
        l = tuple([int(i) for i in lstr])
        sequence.append(l)
    return (tuple(sequence))

def histogram(data, normalize=False):
    '''Given a list of integers, return the smallest value plus a tuple of the number of occurences of each integer.
       Bin 0 holds the occurence count for the smallest integer, bin (largest - smallest) holds the largest value.
       If normalize is True, convert each bin to a percentage of the total number of occurrences. '''
    if not data: return (None)      # return None if empty data set input
    smallest = min(data)
    largest  = max(data)     
    bins = largest - smallest + 1   # number of bins in histogram
    hist = [0] * bins
    for d in data:
        hist[d-smallest] += 1       # increment bin, bin 0 is smallest integer
    if normalize:
        total = sum(hist)
        hist = [round(100.0*bin/total, 1) for bin in hist]
    return (smallest, tuple(hist))


#
# Main
#

BET_SEQUENCE = (1, 1, 1, 1, 1, 1, 1)        # amount to bet when there are already (0,1,2,3,4,5,6) place bets working
AFTER_CRAP_RIGHT = 0                        # increment bet this amount after rolling a 2, 3, or 12
AFTER_11_RIGHT   = 0                        # increment bet this amount after rolling an 11
AFTER_CRAP_WRONG = 0                        # increment bet this amount after rolling a 2 or 3 (but not 12)
AFTER_11_WRONG   = 0                        # increment bet this amount after rolling an 11

roll_length_vs_payoff_right = {}     # [trial1_payoff, trial2_payoff, ..., trialn_payoff]
roll_length_vs_payoff_wrong = {}

t = simple_table.table()
sequence = get_sequence()


for s in sequence:
    stop_wrong_betting = False
    bank_right = 0
    bank_wrong = 0
    last_throw = 0
    throws     = 0
    win_loss_right = []  # track cumulative win/loss on every roll, not including bets on the table
    win_loss_wrong = []  # track cumulative win/loss on every roll, not including bets on the table
    for throw in s:
        working_right = len(t.workingPointsRight())
        come_bet = BET_SEQUENCE[working_right]
        working_wrong = len(t.workingPointsWrong())
        dont_come_bet = BET_SEQUENCE[working_wrong]

        if bank_wrong <= -6:
            dont_come_bet = 0
            if throws > 20:
                bank_wrong = working_wrong
                t.dont_place = {}

        if last_throw in simple_table.CRAPS:
            come_bet += AFTER_CRAP_RIGHT
            come_bet = max(0, come_bet)
            if last_throw != simple_table.BAR:
                dont_come_bet += AFTER_CRAP_WRONG
                dont_come_bet = max(0, dont_come_bet)
        if last_throw == 11:
            come_bet += AFTER_11_RIGHT
            come_bet = max(0, come_bet)
            dont_come_bet += AFTER_11_WRONG
            dont_come_bet = max(0, dont_come_bet)
        t.comeBet(come_bet)
        bank_right -= come_bet
        t.dontComeBet(dont_come_bet)
        bank_wrong -= dont_come_bet
        t.roll(throw)
        bank_right += t.collectPayoutRight()    # table payoff including amount bet
        win_loss_right.append(bank_right + t.workingAmountRight())
        bank_wrong += t.collectPayoutWrong()    # table payoff including amount bet
        win_loss_wrong.append(bank_wrong + t.workingAmountWrong())
        last_throw = throw
        throws += 1
    # print (s, win_loss_right)
    # print (s, win_loss_wrong)
    if len(s) in roll_length_vs_payoff_right.keys():
        roll_length_vs_payoff_right[len(s)].append(win_loss_right[-1])
    else:
        roll_length_vs_payoff_right[len(s)] = [win_loss_right[-1],]
    if len(s) in roll_length_vs_payoff_wrong.keys():
        roll_length_vs_payoff_wrong[len(s)].append(win_loss_wrong[-1])
    else:
        roll_length_vs_payoff_wrong[len(s)] = [win_loss_wrong[-1],]
    
# right betting histograms
total_for_all_sequences = 0
for k in sorted(roll_length_vs_payoff_right.keys()):
    (offset, hist) = histogram(roll_length_vs_payoff_right[k])
    total = 0
    mult = offset
    for h in hist:
        total += mult * h
        mult += 1
    total_for_all_sequences += total
    print (k, offset, hist, total)
print (total_for_all_sequences)
    
# wrong betting histograms
total_for_all_sequences = 0
for k in sorted(roll_length_vs_payoff_wrong.keys()):
    (offset, hist) = histogram(roll_length_vs_payoff_wrong[k])
    total = 0
    mult = offset
    for h in hist:
        total += mult * h
        mult += 1
    total_for_all_sequences += total
    print (k, offset, hist, total)
print (total_for_all_sequences)



