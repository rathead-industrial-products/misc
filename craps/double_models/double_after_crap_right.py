#
#
#


TRIAL_LEN    = 1000000
BET_MULTIPLE = 1

import roll, simple_table

roll.seed()
trial = roll.trial(TRIAL_LEN, True)

table = simple_table.table()
bank = 0
last_roll = 0
last_bet  = 1
max_bet = 1

for roll in trial:
    bet = 1
    if last_roll in (2, 3, 12): bet = BET_MULTIPLE * last_bet 
    max_bet = max(bet, max_bet)
    table.comeBet(bet)
    bank -= bet
    table.action(roll)
    bank += table.collectPayoutRight()
    last_roll = roll
    last_bet = bet
    #print ("%d\t%d\t%d" % (roll, bet, bank+table.workingAmountRight()))

print (bank, max_bet)


