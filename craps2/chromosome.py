#
# Define chromosome and gene classes for a genetic
# algorithm for craps wagering
#

import random

CRAP        = (2, 3, 12)
CRAP_BAR_12 = (2, 3)
SVN         = (7,)
ELVN        = (11,)
POINT       = (4, 5, 6, 8, 9, 10)
ALL_DICE    = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
COME_WIN    = (SVN, ELVN, POINT)
COME_LOSS   = (CRAP, POINT)
DONT_WIN    = (CRAP_BAR_12, POINT)
DONT_LOSS   = (SVN, ELVN, POINT)

MAX_LOOKBACK = 8    # examine no further than this many rolls back to determine wager
MAX_GROWTH_FACTOR = 10  # the most a previous wager can be incremented or multiplied
MAX_WAGER    = 1e6


class chromosome():
    def __init__(self):
        pass

# genes are an and/or combination of events plus a wager
# 
class gene():
    def __init__(self):
        self.a11 = True      # wager or True
        self.a12 = True      # wager or True
        self.a21 = True      # wager or True
        self.a22 = True      # wager or True
        self.a11Aa12_or_a21Aa22 = []       # self.and_comb | 
        pass


# An occurrence that influences a wager
# pass True for a come-bet event or False for a don't come-bet event
class event():
    def __init__(self, come=True):
        self.way = 'COME' if come else 'DONT'
        self.type = ''      # one of R(oll) or W(in) or L(oss)
        self.roll = []      # the set of dice rolls any one of which will qualify the event
        self.win  = []      # the set of dice rolls any one of which precipitated a win or loss
        self.when = []      # the previous rolls which are searched for event occurrence
        while not self.validate: self._create()     # populate class variables with random data

    def _oneOrMoreOf(self, alist):
        random.sample(alist, random.randrange(len(alist)))

    # populate an empty event with random characteristics
    def _create(self):
        self.type = random.choice('R', 'W', 'L')
        if self.type == 'R':    # specify which rolls of the dice qualify
            self.roll = self._oneOrMoreOf(ALL_DICE)
        if self.type == 'W':    # specify what precipiated a win
            self.win = self._oneOrMoreOf(COME_WIN) if self.way == 'COME' else self._oneOrMoreOf(DONT_WIN)
        if self.type == 'L':    # specify what precipiated a loss
            self.win = self._oneOrMoreOf(COME_LOSS) if self.way == 'COME' else self._oneOrMoreOf(DONT_LOSS)
        # specify which previous roll to examine for event occurrence
        self.when = [0] * MAX_LOOKBACK
        self.when[random.randint(0,MAX_LOOKBACK)] = 1

    # encode all class variables into a bitstring for crossover and mutation
    def toBitstring(self):
        bit_str = []
        cleavage_pt = []
        type_map = {'R':(0,0,1), 'W':(0,1,0), 'L':(1,0,0)}
        roll_map = [0] * len(ALL_DICE)
        for r in self.roll: roll_map[r] = 1
        win_map = [0] * len(ALL_DICE)
        for r in self.win: win_map[r] = 1
        bit_str += type_map[self.type]
        cleavage_pt.append(len(bit_str))
        bit_str += roll_map
        cleavage_pt.append(len(bit_str))
        bit_str += win_map
        return (bit_str, cleavage_pt)

    # decode a bitstring back into class variables
    def fromBitstring(self, bit_str, cleavage_pt):
        type_bit_str = bit_str[:cleavage_pt[0]]
        win_bit_str  = bit_str[cleavage_pt[0]:cleavage_pt[1]]
        loss_bit_str = bit_str[cleavage_pt[1]:]
        self.type = 'R' if type_bit_str == [0,0,1] else 'W' if type_bit_str == [0,1,0] else 'L'
        self.win  = [i for i, item in enumerate(win_bit_str) if item==1]
        self.loss = [i for i, item in enumerate(loss_bit_str) if item==1]

    # return True if this class has a legal, valid configuration
    def validate(self):
        if self.way  not in ('COME', 'DONT'): return (False)
        if self.type not in ('R', 'W', 'L'):  return (False)
        if self.way == 'COME':
            if self.type == 'W' and self.win not in COME_WIN:  return (False)
            if self.type == 'L' and self.win not in COME_LOSS: return (False)
        else: # DONT
            if self.type == 'W' and self.win not in DONT_WIN:  return (False)
            if self.type == 'L' and self.win not in DONT_LOSS: return (False)
        return (True)
    
    def occur(self, roll, outcome, bank, loss):
        if self.type == 'R':
            p = self.when.index(1) + 1      # a specific roll (i.e. 7) occurred a specific number of rolls previously
            if roll[-p] in self.roll: return (True)
            return (False)
        elif self.type == 'W':
            p =self.when.index(1) + 1
            winning_rolls = COME_WIN if self.way == 'COME' else DONT_WIN
            # a previous roll matched a potentially winning roll for this betting way
            # and the previous roll actually won
            if (roll[-p] in [r for l in winning_rolls for r in l]) \
                and outcome[-p] == 1: return (True)
            return (False)
        elif self.type == 'L':
            p =self.when.index(1) + 1
            losing_rolls = COME_LOSS if self.way == 'COME' else DONT_LOSS
            # a previous roll matched a potentially losing roll for this betting way
            # and the previous roll actually lost
            if (roll[-p] in [r for l in losing_rolls for r in l]) \
                and outcome[-p] == -1: return (True)
            return (False)
        pass


# Control the types of wager made
class wager():
    def __init__(self):
        self.limit   = MAX_WAGER    # max bet allowed
        self.base    = ''           # the next wager is a function of one of P(revious), B(ank), (recent) L(oss)
        self.inc_dec = 0            # one of +1 or -1 (increment or decrement wager)
        self.growth  = ''           # one of L(inear) or M(ultiplicitive)
        self.factor  = 1.0          # either linear increment or multiplication factor
        while not self.validate: self._create()     # populate class variables with random data

    # populate an empty wager with random characteristics
    def _create(self):
        self.base = random.choice('P', 'B', 'L')
        self.inc_dec = random.choice(-1, 1)
        self.growth = random.choice('L', 'M')
        self.factor = random.randint(1, MAX_GROWTH_FACTOR)

    # return True if this class has a legal, valid configuration
    def validate(self):
        return (True)





#
# Initialization
#
random.seed(314)



#
# Main  --  Unit Test
#

import unittest

class TestSeqEnd(unittest.TestCase):
    def test_seq(self):
        seed()
        seq1 = [5, 4, 6, 8, 8, 4, 10, 7]
        self.assertEqual(seq(), seq1)


if __name__ == '__main__':
    unittest.main(verbosity=2)