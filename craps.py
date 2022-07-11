
import random

TOTAL_ROLLS = 100
BET_AMOUNT  = 10
POINTS      = (4,5,6,8,9,10)
CRAPS       = (2,3,12)
SVN11       = (7,11)
MAX_THROW   = 12


class player():
    column_labels = ["MAX POINTS", "ODDS", "BANK"] + [i for i in range(1, TOTAL_ROLLS+1)]

    def __init__(self, max_points_in_play, odds):
        assert (max_points_in_play >= 1) and (max_points_in_play <= 6)
        assert odds in ("NO", "1x", "2x", "345x", "10x")
        self.max_points = max_points_in_play
        self.odds = odds
        self.bank = 0
        self.history = [self.max_points, self.odds, self.bank]     # initialize history with player configuration, bank at shooter zero
        self.place_bet = [0] * (MAX_THROW+1)    # include all dice rolls 0-12 but only use place numbers
        self.odds_bet  = [0] * (MAX_THROW+1)
        self.come_bet  = 0

    def makeComeBet(self):
        assert BET_AMOUNT == 10
        if self.max_points > sum(1 for i in self.place_bet if i):   # fewer than max_points riding
            self.come_bet = BET_AMOUNT
            self.bank    -= BET_AMOUNT
    
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
        self.bank -= self.odds_bet[throw]

    def payTable(self, throw):
        if throw in CRAPS:
            pass       # lose come bet
        if throw in SVN11:
            self.bank += 2 * self.come_bet
        if throw in POINTS:
            # bet off and on
            self.bank += 2 * self.place_bet[throw]  # pay even money bet
            self.bank += 3 * self.odds_bet[throw] if (throw == 4 or throw == 10) else \
                         4 * self.odds_bet[throw] if (throw == 5 or throw == 9)  else \
                         5 * self.odds_bet[throw]
            self.place_bet[throw] = self.come_bet
            self.placeOddsBet(throw)
        if point and throw == 7:        # shooter out, clear table
            self.place_bet = [0] * (MAX_THROW+1)
            self.odds_bet  = [0] * (MAX_THROW+1)
        self.come_bet = 0               # no new action until new bet placed
        self.history.append(self.bank)  # record bank balance 



def rollDice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    return (die1 + die2)

#
# Main
#

random.seed(314)
rolls   = 0
shooter = 1
point   = None
column_labels = ["MAX POINTS", "ODDS", "BANK"] + [i for i in range(1, TOTAL_ROLLS+1)]
throw_history = [0,0,0]


# configure players
p1 = player(1, "10x")

while rolls < TOTAL_ROLLS:      
    p1.makeComeBet()
    throw = rollDice()
    throw_history.append(throw)
    rolls += 1
    p1.payTable(throw)
    if throw in POINTS and not point:   # shooter has a point now
        point = throw
    if throw == 7 and point:            # shooter out
        point = None
        shooter += 1  

print(player.column_labels)
print(throw_history)
print(p1.history)
