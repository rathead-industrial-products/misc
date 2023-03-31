#
# Module
# Roll the dice for a craps game.
# Created sequences of rolls.
# Analyze roll sequences
#

import random

DIE_FACE        = (1,2,3,4,5,6)
POINTS          = (4,5,6,8,9,10)
CRAPS           = (2,3,12)
CRAPS_PLUS_11   = (2,3,11,12)
SVN_11          = (7, 11)
MAX_THROW       = 12
MAX_ODDS        = ("1x", "2x", "345x", "10x")
SEQUENCE_LEN    = 100


def dice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    return (die1, die2)

def throw():
    return (sum(dice()))

def _seqEnd(seq):
    # determine if the roll sequence is in the middle of a shooter's roll
    # return True if it the next roll after the sequence will be a come-out roll, otherwise False
    pass

def seq(len=SEQUENCE_LEN):
    # return a roll sequence of at least len rolls, ending when shooter 7s-out
    seq = [throw() for i in range(len)]
    while not _seqEnd(seq[-1]):
        seq.append(throw())

#
# Main  --  Unit Test
#

import unittest

class TestSeqEnd(unittest.TestCase):
    def test_shooters_point_made(self):
        s = (7,4,11,8)
        self.assertFalse(_seqEnd(s))
        s = (7,4,11,8,4)
        self.assertTrue(_seqEnd(s))
        s = (7,3,10,5)
        self.assertFalse(_seqEnd(s))
        s = (7,3,10,5,5)
        self.assertFalse(_seqEnd(s))
        s = (7,3,10,5,5,10)
        self.assertTrue(_seqEnd(s))
        s = (7,2,5,3)
        self.assertFalse(_seqEnd(s))
        s = (7,3,11)
        self.assertFalse(_seqEnd(s))


if __name__ == '__main__':
    unittest.main(verbosity=2)



