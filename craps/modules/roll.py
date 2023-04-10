#
# Module
# Roll the dice for a craps game.
# Create a single shooter sequence of rolls, ending with shooter's 7-out
# Analyze roll sequences
#

import random, statistics

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


def meanMedianModeStdDev(data):
    # statistics.mode (version < 3.8) will generate an exception if no unique mode found.
    try:    mode = statistics.mode(data)                             # returns first mode found
    except: mode = max([p[0] for p in statistics._counts(data)])    # returns largest if no unique mode
    return (statistics.mean(data), statistics.median(data), mode, round(statistics.stdev(data),1))

#
# seq is a single shooter's complete tenure
# from first roll to final 7-out

def rollLength(seq):
    return (len(seq))

def pointsMade(seq):
    # return the number of points made during a shooter's tenure
    # assuming continuous come betting
    points_covered = []
    points_made = 0
    for roll in seq:
        if roll in points_covered: points_made += 1
        elif roll in POINTS: points_covered.append(roll)
    return (points_made)

def pointsRiding(seq):
    # return the number of points still riding when shooter 7s-out
    # assuming continuous come betting
    points_covered = []
    for roll in seq:
        if roll in POINTS and roll not in points_covered:
            points_covered.append(roll)
    return len(points_covered)

def svn11(seq):
    # return number of 7s and 11s rolled
    s11 = 0
    for roll in seq:
        if roll == 7 or roll == 11: s11 += 1
    return (s11)

def crapsRight(seq):
    # return number of 2s, 3s, and 12s rolled
    c = 0
    for roll in seq:
        if roll == 2 or roll == 3 or roll == 12: c += 1
    return (c)    

def crapsWrong(seq):
    # return number of 3s, and 12s rolled
    c = 0
    for roll in seq:
        if roll == 3 or roll == 12: c += 1
    return (c)    

def payoutRight(seq):
    # assuming continuous come betting compute the payout for the entire shooter's tenure
    return (pointsMade(seq) -pointsRiding(seq) + svn11(seq) - crapsRight(seq))

def payoutWrong(seq):
    # assuming continuous don't come betting compute the payout for the entire shooter's tenure
    return (-pointsMade(seq) +pointsRiding(seq) - svn11(seq) + crapsWrong(seq))




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



