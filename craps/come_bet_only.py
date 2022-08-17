#
# Make only come bets, no odds bets.
#

import sys, table


def get_shooters():
    shooters = []
    for line in sys.stdin:
        lstr = line.strip()[1:-1].split(',')
        l = tuple([int(i) for i in lstr])
        shooters.append(l)
    return (tuple(shooters))


#
# Main
#

t = table.table()
shooters = get_shooters()

for s in shooters:
    bank = 0
    win_loss = []  # track cumulative win/loss on every roll, not including bets on the table
    for throw in s:
        if (not t.comeout and throw in table.CRAPS_PLUS_11): continue   # threw a 2, 3, 11, or 12 after shooter point established
        t.comeBet(1)
        bank -= 1
        t.roll(throw)
        (come, place, odds) = t.payoff()
        bank += (t.collect())    # net win/loss = table payoff minus amount bet
        win_loss.append(bank + t.working())
    print (s, win_loss)



