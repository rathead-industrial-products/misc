#
# Standard 1 unit bet on Pass/Come and Dont Pass / Dont Come
#
# Compute variance from straight-line 1.4% house advantage
# to help determine required bankroll
#
# Min, max, avg (should == 0) and std dev of bankroll vs straight-line
#

TRIAL_LEN    = 10000   # number of dice rolls in each trial
TRIALS       = 1

# probabilities from https://wizardofodds.com/games/craps/appendix/1/
HOUSE_ADVANTAGE_COME      = 0.01414
HOUSE_ADVANTAGE_DONT_COME = 0.01364

import roll, simple_table

table = simple_table.table()
trial_results_come      = []
trial_results_dont_come = []
for seed in range(TRIALS):   # reseed with 0, 1, ..., 9
    roll.seed(seed)
    trial = roll.trial(TRIAL_LEN, True)
    total_bet_come      = 0
    total_bet_dont_come = 0
    bank_come      = 0.0
    bank_dont_come = 0.0
    roll_results_come       = []
    roll_results_dont_come  = []
    for throw in trial:
        bet = 1
        table.comeBet(bet)
        total_bet_come += bet
        table.dontComeBet(bet)
        if throw != 12: total_bet_dont_come += bet
        table.action(throw)    
        bank_come      += table.collectPayoutRight() - bet
        bank_dont_come += table.collectPayoutWrong() - bet
        roll_results_come.append(bank_come)
        roll_results_dont_come.append(bank_dont_come)
    trial_results_come.append(roll_results_come)
    trial_results_dont_come.append(roll_results_dont_come)

for i in range(TRIALS):
    print ((100 * trial_results_come[i][-1])/total_bet_come)
    print ((100 * trial_results_dont_come[i][-1])/total_bet_dont_come)

'''
for i in range(TRIALS):
    (mean, median, mode, sd) = roll.meanMedianModeStdDev(trial_results_come[i])
    bank_min = min(trial_results_come[i])
    bank_max = max(trial_results_come[i])
    bank_last = trial_results_come[i][-1]
    print ("Come trial %d: mean = %.1f, median = %.1f, mode = %.1f, sd = %.1f, min = %.1f, max = %.1f, ending bank = %.0f" %
           (i+1, mean, median, mode, sd, bank_min, bank_max, bank_last))
    
print ()
for i in range(TRIALS):
    (mean, median, mode, sd) = roll.meanMedianModeStdDev(trial_results_dont_come[i])
    bank_min = min(trial_results_dont_come[i])
    bank_max = max(trial_results_dont_come[i])
    bank_last = trial_results_dont_come[i][-1]
    print ("Dont Come trial %d: mean = %.1f, median = %.1f, mode = %.1f, sd = %.1f, min = %.1f, max = %.1f, ending bank = %.0f" %
           (i, mean, median, mode, sd, bank_min, bank_max, bank_last))
'''
