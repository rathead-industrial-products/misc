#
# Bankroll Accounting
#   The player's bankroll is what he holds on the rail + any bets on the table.
#   Once there is a loss the bet is removed from the bankroll.
#   
#   Separate bankrolls are tracked for come bets and odds bet.
#   Over time, the come bankroll should decrease at the rate of the house advantage
#   and the odds bankroll should remain constant.
#
#   A record is kept of the balance of each bankroll, updated after every roll.
#   player.history[] = [(max bets riding, odds), (roll_bank_come roll 1, roll_bank_odds roll 1, shooter_bank_come roll 1, shooter_bank_odds roll 1), ...]
#
#   A record is also kept of the bankroll balance on a per-shooter basis.
#   It is zero'd before each shooter and updated after every roll of that shooter.
#
#
#
#


import random

TOTAL_ROLLS = 100
BET_AMOUNT  = 10
POINTS      = (4,5,6,8,9,10)
CRAPS       = (2,3,12)
SVN11       = (7,11)
MAX_THROW   = 12
ALL_ODDS    = ("NO", "1x", "2x", "345x", "10x")


class player():
    def __init__(self, max_bets_riding, odds):
        assert (max_bets_riding >= 1) and (max_bets_riding <= 7)
        assert odds in ALL_ODDS
        self.max_bets_riding = max_bets_riding
        self.odds = odds
        self.roll_bank_come = 0
        self.roll_bank_odds = 0
        self.shooter_bank_come = 0
        self.shooter_bank_odds = 0
        self.history = [(self.max_bets_riding, self.odds)]  # initialize history with player configuration
        self.place_bet = [0] * (MAX_THROW+1)                # include all dice rolls 0-12 in list but only use place numbers
        self.odds_bet  = [0] * (MAX_THROW+1)
        self.come_bet  = 0

    def makeComeBet(self):
        assert BET_AMOUNT == 10
        if self.max_bets_riding > sum(1 for i in self.place_bet if i):   # place bet if fewer than max_bets_riding
            self.come_bet = BET_AMOUNT
    
    def placeOddsBet(self, throw):
        assert BET_AMOUNT == 10
        assert throw in POINTS
        if self.odds == "NO":
            self.odds_bet[throw] = 0
        elif self.odds == "1x":
            self.odds_bet[throw] = BET_AMOUNT
        elif self.odds == "2x":
            self.odds_bet[throw] = 2 * BET_AMOUNT
        elif self.odds == "345x":
            self.odds_bet[throw] = 3 * BET_AMOUNT if (throw == 4 or throw == 10) else \
                                   4 * BET_AMOUNT if (throw == 5 or throw == 9)  else \
                                   5 * BET_AMOUNT
        elif self.odds == "10x":
            self.odds_bet[throw] = 10 * BET_AMOUNT
        else:
            assert False

    def payTable(self, throw):
        place_bets_before_roll = sum(1 for i in self.place_bet if i)
        if throw in CRAPS:
            self.roll_bank_come    -= self.come_bet                # lose come bet
            self.shooter_bank_come -= self.come_bet                # lose come bet
        if throw in SVN11:
            self.roll_bank_come    += self.come_bet                # pay even money bet
            self.shooter_bank_come += self.come_bet                # pay even money bet
        if throw in POINTS:
            # bet off and on if come bet placed
            self.roll_bank_come    += self.place_bet[throw]     # pay even money bet
            self.shooter_bank_come += self.place_bet[throw]
            self.roll_bank_odds    += oddsPayout(self.odds_bet[throw])
            self.shooter_bank_odds += oddsPayout(self.odds_bet[throw])
            self.odds_bet[throw] = 0                # remove odds
            self.place_bet[throw] = self.come_bet   # make new bet if come bet placed
            if self.place_bet[throw]: self.placeOddsBet(throw)  # place odds on bet 
        if point and throw == 7:        # shooter out, clear table
            self.roll_bank_come    -= sum(i for i in self.place_bet)
            self.shooter_bank_come -= sum(i for i in self.place_bet)
            self.roll_bank_odds    -= sum(i for i in self.odds_bet)
            self.shooter_bank_odds -= sum(i for i in self.odds_bet)
            self.place_bet = [0] * (MAX_THROW+1)
            self.odds_bet  = [0] * (MAX_THROW+1)
        self.come_bet = 0               # no new action until new bet placed
        self.history.append((self.roll_bank_come, self.roll_bank_odds, self.shooter_bank_come, self.shooter_bank_odds))  # record bank balances

        # print debugging
        # print("%1d (%1d) %4s %1d %6d %6d" % (self.max_bets_riding, place_bets_before_roll, self.odds, throw, self.roll_bank_come, self.roll_bank_odds), self.place_bet, self.odds_bet)



def rollDice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    return (die1 + die2)

def oddsPayout(bet):
    odds_payout = int(2 * bet     if (throw == 4 or throw == 10) else \
                      3 * bet / 2 if (throw == 5 or throw == 9)  else \
                      6 * bet / 5)  # throw == 6 or throw == 8
    return (odds_payout)

def playerComeBets(player):
    return (player.history[0][0])       # one of (1, 2, 3, 4, 5, 6, 7)

def playerOdds(player):
    return (player.history[0][1])       # one of ("NO", "1x", "2x", "345x", "10x")

def playerIDString(player):
    return(str(playerComeBets(player))+'_'+str(playerOdds(player)))   # i.e. "1_1x"

def dumpCSV(come_bets=(1,2,3,4,5,6,7), odds=ALL_ODDS):
    """1_NO come, 1_NO come, 1_1x come, 1_1x come, ..., 1_NO odds, 1_NO odds, 1_1x odds, 1_1x odds, ..., shooter_1, shooter_2, ..., shooter_max"""
    """roll_bank_come, shooter_bank_come, roll_bank_come, shooter_bank_come, ..., roll_bank_odds, shooter_bank_odds, roll_bank_odds, shooter_bank_odds, ..., roll 1   , roll 1   , ..., roll 1"""
    f = open("craps.csv", 'w')  
    for p in players:
        if playerComeBets(p) in come_bets and playerOdds(p) in odds:
            f.write("\"%s come\rroll\",\"%s come\nshooter\"," % (playerIDString(p), playerIDString(p)))
    for p in players:
        if playerComeBets(p) in come_bets and playerOdds(p) in odds:
            f.write("\"%s come\rroll\",\"%s come\nshooter\"," % (playerIDString(p), playerIDString(p)))
    for i in range(len(shooter_history)):
        f.write("shooter_%d," % (i+1))
    f.write('\n')

    for i in range(1,TOTAL_ROLLS):      # write rows out as columns to avoid Excel 256 column limit
        for p in players:               # players come bankroll at each roll of the dice
            if playerComeBets(p) in come_bets and playerOdds(p) in odds:
                f.write("%d,%d," % (p.history[i][0], p.history[i][2]))
        for p in players:               # players odds bankroll at each roll of the dice
            if playerComeBets(p) in come_bets and playerOdds(p) in odds:
                f.write("%d,%d," % (p.history[i][1], p.history[i][3]))
        for s in shooter_history:       # shooter's rolls in order
            if (i-1) < len(s):
                f.write("%d," % s[i-1])
            elif (i-1) == len(s):       # summarize points made and lost
                f.write("(%d %d)," % shooterPointsMadeLost(s))
            else: f.write(',')          # skip cell if shooter has already 7'd out
        f.write('\n')
    f.close()

def minMaxBank(player):
    min_bank =  1e6
    max_bank = -1e6
    for i in range(2,TOTAL_ROLLS):  # skip configuration cells
        min_roll_bank_come = min(min_bank, player.history[i][0])
        max_roll_bank_come = max(max_bank, player.history[i][0])
        min_roll_bank_odds = min(min_bank, player.history[i][1])
        max_roll_bank_odds = max(max_bank, player.history[i][1])
    print(playerIDString(player), min_roll_bank_come, max_roll_bank_come, min_roll_bank_odds, max_roll_bank_odds)

def shooterPointsMadeLost(shooter_rolls):
    points = []
    made = 0
    lost = 0
    for i in range(len(shooter_rolls)):
        throw = shooter_rolls[i]
        if throw in POINTS:
            if throw in points:
                made += 1
            else:
                points.append(throw)
    lost = len(points)  # points rolled but not made
    return (made, lost)

def rollLengthHistogram(shooter_history): # return list of number of rolls made of length n, starting with 1 rolls (excluding final 7-out)
    h = [0] * 1000      # assume no rolls longer than 1000
    for s in shooter_history:
        h[len(s)] += 1
    for i in range(len(h)):
        if h[i]: longest_roll = i
    h = h[2:longest_roll+1]        # trim list - start at 2 rolls (including final 7-out) and end at final entry, results in index being number of rolls excluding final 7-out
    return h





#
# Main
#

random.seed(314)
rolls   = 0
point   = None
throw_history = [0,0]
shooter_rolls = []
shooter_history = []


# all possible player configurations
players = []
for i in range(1,8):
    players += [player(i, "NO"), player(i, "1x"), player(i, "2x"), player(i, "345x"), player(i, "10x")]

while rolls < TOTAL_ROLLS:
    for p in players: p.makeComeBet()    
    throw = rollDice()
    throw_history.append(throw)
    shooter_rolls.append(throw)
    rolls += 1
    for p in players:
        p.payTable(throw)  
    if throw in POINTS and not point:   # shooter has a point now
        point = throw
    if throw == 7 and point:            # shooter out
        point = None
        shooter_history.append(shooter_rolls)
        shooter_rolls = []
        for p in players:
            p.shooter_bank_come = 0
            p.shooter_bank_odds = 0


#
# Write out to .csv file
#
dumpCSV((7,), ("10x",))


# 
# Analysis
#
# print(rollLengthHistogram(shooter_history))
