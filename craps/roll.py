#
# Module
# Roll the dice for a craps game.
# Create a single shooter sequence of rolls, ending with shooter's 7-out
# Analyze roll sequences
#

import random

POINTS          = (4,5,6,8,9,10)


def seed(val=314159):
    random.seed(val)
    
def dice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    return (die1, die2)

def throw():
    return (sum(dice()))

def _seqEnd(seq):
    # return True if the last roll of seq is a 7-out
    point = 0   # point off
    for i in range(len(seq)):
        roll = seq[i]
        if not point and roll in POINTS:
            point = roll    # point on
        elif roll == point:
            point = 0       # point off
        elif point and roll == 7:   # 7-out
            assert(i == len(seq) - 1)   # 7-out must be final roll of sequence
            return (True)
    return (False)

def seq():
    # return a single shooter's roll sequence, ending on shooters 7-out.
    seq = [throw(), throw()]
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
    def test_sequence_end(self):
        s = (8,7)
        self.assertTrue(_seqEnd(s))
        s = (7,4,11,8)
        self.assertFalse(_seqEnd(s))
        s = (7,4,11,8,4)
        self.assertFalse(_seqEnd(s))
        s = (7,4,11,8,4,7)
        self.assertFalse(_seqEnd(s))
        s = (7,3,10,5)
        self.assertFalse(_seqEnd(s))
        s = (7,3,10,5,5)
        self.assertFalse(_seqEnd(s))
        s = (7,3,10,5,5,7)
        self.assertTrue(_seqEnd(s))
        s = (8,4,6,6,10,9,8)
        self.assertFalse(_seqEnd(s))
        s = (8,4,6,6,10,9,8,7)
        self.assertFalse(_seqEnd(s))
        s = (7, 8)
        self.assertFalse(_seqEnd(s))
        s = (8,7,10)
        self.assertRaises(Exception, _seqEnd, s)
        s = (8,4,6,8,7,9,8,7)
        self.assertTrue(_seqEnd(s))
        s = (3,11,12,2,6,7)
        self.assertTrue(_seqEnd(s))
        s = (8,4,6,6,10,9,7)
        self.assertTrue(_seqEnd(s))
        s = (8,)
        self.assertFalse(_seqEnd(s))
        s = (4,5,6,7,2,10,10,8,7)
        self.assertRaises(Exception, _seqEnd, s)

    def test_seq(self):
        seed()
        seq1 = [5, 4, 6, 8, 8, 4, 10, 7]
        self.assertEqual(seq(), seq1)


if __name__ == '__main__':
    unittest.main(verbosity=2)



