#
#
#

TRIAL_LEN    = 36    # each possible roll should appear ~10000 times
TRIALS       = 10        # must be > 1 or list operation will fail




import roll, simple_table

def stats(bank_per_trial_list, total_bets):
    mean_bank = roll.meanMedianModeStdDev(bank_per_trial_list)[0]
    mean_bets = roll.meanMedianModeStdDev(total_bets)[0]
    mean_bank_pct = 100*mean_bank/mean_bets
    bank_bet = zip(bank_per_trial_list, total_bets)
    adv_pct_per_trial = [round(100*bank/bet, 2) for (bank, bet) in bank_bet]
    sd_adv_pct = roll.meanMedianModeStdDev(adv_pct_per_trial)[3]
    player_adv = adv_pct_per_trial
    mean_adv   = mean_bank_pct
    sd_adv     = sd_adv_pct
    return (player_adv, mean_adv, sd_adv)

def profile_singleComeBet(throw, prev_throw, last_bet, table):
    bet = 1
    table.comeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutRight() - bet)

def profile_singleComeBarCraps(throw, prev_throw, last_bet, table):
    # regular come bet craps
    # 2, 3, 12 are ignored
    if throw in (2, 3, 12): return (0, 0) # pretend this throw never happened
    bet = 1
    table.comeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutRight() - bet)

def profile_singleComeDoubleCraps(throw, prev_throw, last_bet, table):
    # regular come bet craps
    # on throws of 2, 3, 12 (loser) double the next bet
    bet = 1
    if prev_throw in (2, 3, 12): bet = 2 * last_bet
    table.comeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutRight() - bet)

def profile_singleComeDoubleFirstBarCraps(throw, prev_throw, last_bet, table):
    # regular come bet craps
    # 2, 3, 12 are ignored
    # first point or single roll of 7 is doubled bet
    global come_out
    if prev_throw == 0: come_out = True
    if throw in (2, 3, 12): return (0,0)    # ignore crap
    bet = 1
    if come_out: bet = 2     # double first point
    if throw in (4, 5, 6, 8, 9, 10): come_out = False     # point established, now play to resolution
    table.comeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutRight() - bet)

def profile_singleComeAfterCraps(throw, prev_throw, last_bet, table):
    # do not bet on 7,11, or any point until craps (2, 3, 12)
    # bet on roll following craps unless it is craps, then ignore
    if throw in (2, 3, 12) and prev_throw in (2, 3, 12): return (0,0)    # ignore sequential craps
    bet = 0
    if prev_throw in (2, 3, 12): bet = 1
    table.comeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutRight() - bet)

def profile_singleComeCrapsAndNextNotCraps(throw, prev_throw, last_bet, table):
    # do not bet on 7,11, or any point until...
    # bet on craps (2, 3, 12)
    # bet on roll following craps unless it is craps, then ignore
    if throw in (2, 3, 12) and prev_throw in (2, 3, 12): return (0,0)    # ignore sequential craps
    bet = 0
    if throw in (2, 3, 12) or prev_throw in (2, 3, 12): bet = 1
    table.comeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutRight() - bet)

def profile_singleDontComeBet(throw, prev_throw, last_bet, table):
    bet = 1
    table.dontComeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutWrong() - bet)

def profile_singleDontComeBar11(throw, prev_throw, last_bet, table):
    if throw == 11: return (last_bet, 0) # pretend this throw never happened
    bet = 1
    table.dontComeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutWrong() - bet)

def profile_singleDontComeBar711(throw, prev_throw, last_bet, table):
    if throw == 11: return (last_bet, 0) # pretend this throw never happened
    bet = 1
    if throw == 7: bet = 0  # not betting the losing 7 but run it on the table to collect winnings
    table.dontComeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutWrong() - bet)

def profile_singleDontComeDouble711(throw, prev_throw, last_bet, table):
    bet = 1
    if prev_throw == 12: bet = last_bet
    if prev_throw in (7, 11): bet = 2 * last_bet
    table.dontComeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutWrong() - bet)

def profile_singleDontComeDouble711Only(throw, prev_throw, last_bet, table):
    bet = 0
    if prev_throw == 12: bet = last_bet
    if prev_throw in (7, 11): bet = 2 * last_bet
    if throw in (7, 11) and bet == 0: bet = 1
    table.dontComeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutWrong() - bet)

def profile_singleDontComePointto7OnlyBetFirstPointOnly(throw, prev_throw, last_bet, table):
    # bet first point of sequence, wait for resolution. expected win = 0.2
    if prev_throw == 0 and throw == 7: return (0,0) # ignore a single 7 sequence
    if throw in (2, 3, 11, 12): return (0,0)    # ignore crap-11
    bet = 0
    if prev_throw == 0: bet = 1     # bet first point only
    table.dontComeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutWrong() - bet)

def profile_singleDontComePointto7OnlyBetAllPoints(throw, prev_throw, last_bet, table):
    # bet all points in sequence, wait for resolution. expected win = 4 points per 7 + starting poin = 0.2 * 5 = 1.0
    global come_out
    if prev_throw == 0: come_out = True
    if throw in (2, 3, 11, 12): return (0,0)    # ignore crap-11
    if prev_throw == 0 and throw == 7: return (0,0) # ignore a single 7 sequence
    bet = 1
    if come_out and throw == 7:
        return (0,0) # ignore a single 7 sequence or 7 after sequence beginning with craps
    if throw == 7: bet = 0
    if throw in (4, 5, 6, 8, 9, 10): come_out = False     # point established, now play to resolution
    table.dontComeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutWrong() - bet)

def profile_singleDontComePointto7OnlyBetAllPointsDoubleFirst(throw, prev_throw, last_bet, table):
    # bet all points in sequence, wait for resolution. expected win = 4 points per 7 + (double) starting point = 0.2 * 4 + 0.4 = 1.2
    global come_out
    if prev_throw == 0: come_out = True
    if throw in (2, 3, 11, 12): return (0,0)    # ignore crap-11
    bet = 1
    if come_out: bet = 2     # double first point
    if come_out and throw == 7:
        return (0,0) # ignore a single 7 sequence or 7 after sequence beginning with craps
    if throw == 7: bet = 0
    if throw in (4, 5, 6, 8, 9, 10): come_out = False     # point established, now play to resolution
    table.dontComeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutWrong() - bet)

def profile_singleDontComePointto7IncludedBetAllPointsDoubleFirst(throw, prev_throw, last_bet, table):
     # bet all points in sequence, wait for resolution. expected win = 4 points per 7 + (double) starting point = 0.2 * 4 + 0.4 = 1.2
    global come_out
    if prev_throw == 0: come_out = True
    if throw in (2, 3, 11, 12): return (0,0)    # ignore crap-11
    bet = 1
    if come_out: bet = 2     # double first point
    if come_out and throw == 7:
        return (0,0) # ignore a single 7 sequence or 7 after sequence beginning with craps
    if throw in (4, 5, 6, 8, 9, 10): come_out = False     # point established, now play to resolution
    table.dontComeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutWrong() - bet)

def profile_singleDontComePointto7DoubleOn7(throw, prev_throw, last_bet, table):
     # bet all points in sequence, wait for resolution. expected win = 4 points per 7 + (double) starting point = 0.2 * 4 + 0.4 = 1.2
    bet = 1
    if prev_throw == 7:
        bet = 2 * last_bet
    table.dontComeBet(bet)
    table.action(throw)    
    return (bet, table.collectPayoutWrong() - bet)




come_out = False
def run(trials, trial_len, profile):    
    results = []
    total_bets = []
    table = simple_table.table()
    for seed in range(trials):   # reseed with 0, 1, ..., 9
        roll.seed(seed)
        trial = roll.trial(trial_len, True)
        bank = 0
        total_bet = 0
        max_bet = 0
        prev_throw = 0
        last_bet = 1
        for throw in trial:
            (last_bet, win) = profile(throw, prev_throw, last_bet, table)
            total_bet += last_bet
            max_bet = max(max_bet, last_bet)
            bank += win
            if win:
                pass
                print (throw, prev_throw, last_bet, win, bank)
            prev_throw = throw
        results.append(bank)
        total_bets.append(total_bet)
    return (total_bets, results, max_bet)

def runWrapper(profile, description):
    (total_bets, results, max_bet) = run(TRIALS, TRIAL_LEN, profile)
    (player_adv, mean_adv, sd_adv) = stats(results, total_bets)
    print (description, "\n\tplayer adv =", player_adv, "\n\tmean adv   =", round(mean_adv, 2), "\n\tstd dev    =", sd_adv, "\n\tmax bet    =", max_bet)

# Main

#runWrapper(profile_singleComeBet, "Single Come Bet:\t\t")
#runWrapper(profile_singleComeBarCraps, "Single Come Bar Craps:\t\t")
#runWrapper(profile_singleComeDoubleCraps, "Single Come Double Craps:\t\t")
#runWrapper(profile_singleComeDoubleFirstBarCraps, "Single Come Double First Bar Craps:\t\t")

runWrapper(profile_singleComeAfterCraps, "Single Come After Craps:\t\t")
#runWrapper(profile_singleComeCrapsAndNextNotCraps, "Single Come Craps and Next Not Craps:\t\t")

'''
(total_bets, results, max_bet) = run(TRIALS, TRIAL_LEN, profile_singleDontComeBet)
print ("Single Don't Come Bet:\t\t", stats(results, total_bets), "max bet =", max_bet)

(total_bets, results, max_bet) = run(TRIALS, TRIAL_LEN, profile_singleDontComeBar11)
print ("Single Don't Come Bar 11:\t", stats(results, total_bets), "max bet =", max_bet)

(total_bets, results, max_bet) = run(TRIALS, TRIAL_LEN, profile_singleDontComeBar711)
print ("Single Don't Come Bar 7-11:\t", stats(results, total_bets), "max bet =", max_bet)

(total_bets, results, max_bet) = run(TRIALS, TRIAL_LEN, profile_singleDontComeDouble711)
print ("Single Don't Come Double 7-11:\t", stats(results, total_bets), "max bet =", max_bet)

(total_bets, results, max_bet) = run(TRIALS, TRIAL_LEN, profile_singleDontComeDouble711Only)
print ("Single Don't Come Double 7-11 Only:\t", stats(results, total_bets), "max bet =", max_bet)

(total_bets, results, max_bet) = run(TRIALS, TRIAL_LEN, profile_singleDontComePointto7OnlyBetFirstPointOnly)
print ("Single Don't Come Point-7 Bet First Point Only:\tavg rtn:", stats(results, total_bets), "max bet =", max_bet)

(total_bets, results, max_bet) = run(TRIALS, TRIAL_LEN, profile_singleDontComePointto7OnlyBetAllPoints)
print ("Single Don't Come Point-7 Bet All Points:\t", stats(results, total_bets), "max bet =", max_bet)

(total_bets, results, max_bet) = run(TRIALS, TRIAL_LEN, profile_singleDontComePointto7OnlyBetAllPointsDoubleFirst)
print ("Single Don't Come Point-7 Bet All Points Double First:\tavg rtn:", stats(results, total_bets), "max bet =", max_bet)

(total_bets, results, max_bet) = run(TRIALS, TRIAL_LEN, profile_singleDontComePointto7IncludedBetAllPointsDoubleFirst)
print ("Single Don't Come Point-7 Included Bet All Points Double First:\tavg rtn:", stats(results, total_bets), "max bet =", max_bet)

(total_bets, results, max_bet) = run(TRIALS, TRIAL_LEN, profile_singleDontComePointto7DoubleOn7)
print ("Single Don't Come Point-7 Double on 7:\tavg rtn:", stats(results, total_bets), "max bet =", max_bet)
'''
               

