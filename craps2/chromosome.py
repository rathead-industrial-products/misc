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

MAX_WAGER   = 1e6


class chromosome():
    def __init__(self):
        pass

class gene():
    def __init__(self):
        pass


# An occurrence that influences a wager
# pass True for a come-bet event or False for a don't come-bet event
class event():
    def __init__(self, come=True):
        self.way = 'COME' if come else 'DONT'
        self.type = ''      # one of R(oll) or W(in) or L(oss)
        self.roll = []      # the set of dice rolls any one of which will qualify the event
        self.win  = []      # the set of dice rolls any one of which precipitated a win or loss
        self.when = when()  # the time(s) in the past which are searched for event occurrence
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

    # encode all class variables into a bitstring for crossover and mutation
    def toBitstring(self):
        pass

    # decode a bitstring back into class variables
    def fromBitstring(self):
        pass

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


# Time window(s) in the past to search for an event occurrence
class when():
    def __init__(self):
        self.prev_roll = []      # list of previous rolls (1-max) to examine

    # encode all class variables into a bitstring for crossover and mutation
    def toBitstring(self):
        pass

    # decode a bitstring back into class variables
    def fromBitstring(self):
        pass

# Control the types of wager made
class wager():
    def __init__(self):
        self.base = []              # the next wager is a function of [prev, bank, recent loss]
        self.limit = MAX_WAGER      # max bet allowed
        self.inc_dec = 1            # one of [+1, -1] (increment or decrement wager)
        self.growth = 'L'           # one of L(inear) or M(ultiplicitive)
        self.factor = 1.0           # either linear increment or multipication factor






#
# Initialization
#
seed()



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