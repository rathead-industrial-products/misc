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

BET_SEQUENCE = (1, 1, 1, 1, 1, 4, 4)        # amount to bet when there are already (0,1,2,3,4,5,6) place bets working
AFTER_CRAP = -4                             # increment bet this amount after rolling a 2, 3, or 12
AFTER_11   = -4                             # increment bet this amount after rolling an 11

roll_length_vs_payoff = {}     # [trial1_payoff, trial2_payoff, ..., trialn_payoff]

t = simple_table.table()
shooters = get_shooters()

for s in shooters:
    bank = 0
    last_throw = 0
    win_loss = []  # track cumulative win/loss on every roll, not including bets on the table
    for throw in s:
        working = len(t.workingPoints())
        bet = BET_SEQUENCE[working]
        if last_throw in simple_table.CRAPS:
            bet += AFTER_CRAP
            bet = max(0, bet)
        if last_throw == 11:
            bet += AFTER_11
            bet = max(0, bet)
        t.comeBet(bet)
        bank -= bet
        t.roll(throw)
        bank += t.collectPayout()    # table payoff including amount bet
        win_loss.append(bank + t.workingAmount())
        last_throw = throw
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



