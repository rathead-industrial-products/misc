#
# Make only come bets, no odds bets.
#

import sys, simple_table


def get_shooters():
    shooters = []
    for line in sys.stdin:
        lstr = line.strip()[1:-1].split(',')
        l = tuple([int(i) for i in lstr])
        shooters.append(l)
    return (tuple(shooters))

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


roll_length_vs_payoff = {}     # [trial1_payoff, trial2_payoff, ..., trialn_payoff]

t = simple_table.table()
shooters = get_shooters()

for s in shooters:
    bank = 0
    win_loss = []  # track cumulative win/loss on every roll, not including bets on the table
    for throw in s:
        # bet is the amount already on the table, up to MAX_BET, minimum of 1
        MIN_BET = 1
        MAX_BET = 4
        bet = t.workingAmount()
        bet = max(bet, MIN_BET)
        bet = min(bet, MAX_BET)
        t.comeBet(bet)
        bank -= bet
        t.roll(throw)
        bank += t.collectPayout()    # table payoff including amount bet
        win_loss.append(bank + t.workingAmount())
    # print (s, win_loss)
    if len(s) in roll_length_vs_payoff.keys():
        roll_length_vs_payoff[len(s)].append(win_loss[-1])
    else:
        roll_length_vs_payoff[len(s)] = [win_loss[-1],]
    
total_for_all_shooters = 0
for k in sorted(roll_length_vs_payoff.keys()):
    (offset, hist) = histogram(roll_length_vs_payoff[k])
    total = 0
    mult = offset
    for h in hist:
        total += mult * h
        mult += 1
    total_for_all_shooters += total
    print (k, offset, hist, total)
print (total_for_all_shooters)



