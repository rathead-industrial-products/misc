#
# Module
# Roll the dice for a craps game.
# Created sequences of rolls.
# Analyze roll sequences
#

import random

POINTS          = (4,5,6,8,9,10)
SEQUENCE_LEN    = 10


def seed(val=314159):
    random.seed(val)
    
def dice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    return (die1, die2)

def throw():
    return (sum(dice()))

def _seqEnd(seq):
    # iterate through seq finding all shooters
    # return True if the next roll after seq is a come-out roll
    come_out = True
    point = 0   # point off
    for i in range(len(seq)):
        roll = seq[i]
        if come_out and roll in POINTS:
            come_out = False
            point = roll
        elif not come_out and roll == point: come_out = True   # shooter made point
        elif not come_out and roll == 7:  # shooter out
            come_out = True
    return (come_out)

def seq(len=SEQUENCE_LEN):
    # return a roll sequence of at least len rolls, ending when shooter 7s-out or makes his point
    seq = [throw() for i in range(len)]
    while not _seqEnd(seq):
        seq.append(throw())
    return (seq)


#
# Initialization
#
seed()



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
        s = (8,4,6,6,10,9,8)
        self.assertTrue(_seqEnd(s))
        s = (7, 8)
        self.assertFalse(_seqEnd(s))
        s = (8,7,10)
        self.assertFalse(_seqEnd(s))
        s = (8, 4, 6, 8, 7, 9, 8, 7, 11, 7, 5, 9)
        self.assertFalse(_seqEnd(s))

    def test_no_7_sequence(self):
        s = (3,11,12,2)
        self.assertTrue(_seqEnd(s))
        s = (8,4,6,6,10,9,8)
        self.assertTrue(_seqEnd(s))
        s = (8,)
        self.assertFalse(_seqEnd(s))

    def test_come_out_roll(self):
        s = (7,3,11)
        self.assertTrue(_seqEnd(s))
        s = (7,3,11,6)
        self.assertFalse(_seqEnd(s))
        s = (7,3,9,10,7)
        self.assertTrue(_seqEnd(s))


if __name__ == '__main__':
    unittest.main(verbosity=2)



