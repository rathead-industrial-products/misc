#
#
#


TRIAL_LEN    = 10000000
BET_MULTIPLE = 3

import roll, simple_table

roll.seed(1)
trial = roll.trial(TRIAL_LEN, True)

table = simple_table.table()
bank = 0
base_bet = 1
last_roll = 0
last_bet  = 1
max_bet = 1

for roll in trial:
    bet = base_bet
    if last_roll in (7,11): bet = BET_MULTIPLE * last_bet 
    max_bet = max(bet, max_bet)
    table.dontComeBet(bet)
    bank -= bet
    table.action(roll)
    bank += table.collectPayoutWrong()
    last_roll = roll
    last_bet = bet
    #print ("%d\t%d\t%s\t%2d" % (roll, bet, table.betsWrong()[1], bank+table.workingAmountWrong()))

print (bank, max_bet)


