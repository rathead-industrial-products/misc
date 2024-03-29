#
# Module
# Roll the dice for a craps game.
# A sequence is defined as a series of rolls ending with a 7.
# A trial(n) is collection of sequences totaling at least n rolls.
#
# For come and don't come, individually, each roll can be determined
# to be a win, loss, or draw with no additional information other
# than the roll sequence.
#
# Analyze roll sequences.
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

def seq():
    # return a series of rolls ending with a 7.
    # a sequence may be as short as one roll
    seq = [throw()]
    while not seq[-1] == 7:
        seq.append(throw())
    return (seq)

def seqOutcome():
    # return a series of 3-tuples: (roll, come_outcome, dont_outcome)
    # where roll is the throw of the dice and *_outcome is +1/0/-1 reflecting whether the
    # roll, now or in the future, is a win, loss, or draw.
    BAR = 12        # don't come bar 12
    rslt = []
    s = seq()
    for i in range(len(s)):
        # determine if roll is a win/lose/draw  outcome = +1 | 0 | -1
        # don't come is opposite of come outcome unless BAR is rolled, than it's a draw
        roll = s[i]
        if roll in (7, 11) or roll in (s[i+1:]): c_outcome = +1 # 7 winner or point made
        else: c_outcome = -1
        d_outcome = 0 if roll == BAR else -c_outcome
        rslt.append((roll, c_outcome, d_outcome))
    return (rslt)

def trial(n, outcome=False, flat=False):
    # return a seris of sequences totalling at least n rolls:
    # if outcome == true return a series of seqOutcome(s)
    # if flat == True return a single flat list instead of a list of sequences
    l = 0
    s = seq if not outcome else seqOutcome
    trial = [s()]
    l += len(trial[-1])
    while l < n:
        trial.append(s())
        l += len(trial[-1])
    if flat:
        trial = [item for sublist in trial for item in sublist]
    return (trial)

    c_win = sum([item[1] for item in list])


def meanMedianModeStdDev(data):
    # statistics.mode (version < 3.8) will generate an exception if no unique mode found.
    try:    mode = statistics.mode(data)                             # returns first mode found
    except: mode = max([p[0] for p in statistics._counts(data)])    # returns largest if no unique mode
    if len(data) > 1: sd = round(statistics.stdev(data),1)
    else:             sd = None
    return (round(statistics.mean(data),1), statistics.median(data), mode, sd)



def rollLength(seq):
    return (len(seq))

def trialLength(trial):
    l = 0
    for s in trial: l += len(s)
    return (l)

def pointsMade(seq):
    # return the number of points made during sequence
    # assuming continuous come betting
    points_covered = []
    points_made = 0
    for roll in seq:
        if roll in points_covered: points_made += 1
        elif roll in POINTS: points_covered.append(roll)
    return (points_made)

def pointsRiding(seq):
    # return the number of points still riding when sequence ends
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
    # return number of 3s and 2s rolled - bar 12
    c = 0
    for roll in seq:
        if roll == 3 or roll == 2: c += 1
    return (c)    

def payoutRight(seq):
    # assuming continuous come betting compute the payout for the entire sequence
    return (pointsMade(seq) -pointsRiding(seq) + svn11(seq) - crapsRight(seq))

def payoutWrong(seq):
    # assuming continuous don't come betting compute the payout for the entire sequence
    return (-pointsMade(seq) +pointsRiding(seq) - svn11(seq) + crapsWrong(seq))




#
# Initialization
#
seed()



#
# Main  --  Unit Test
#

#seed(); print (trial(10))
#seed(); print (trial(10, flat=True))

seed(); l = trial(10000000, True)
#print (l)
c_win = sum([item[1] for sublist in l for item in sublist])
d_win = sum([item[2] for sublist in l for item in sublist])
print (c_win, d_win)
#seed(); print (trial(10, True))
#seed(); print (trial(10, True, True))
#
import unittest

class TestSeqEnd(unittest.TestCase):
    def test_seq(self):
        seed()
        seq1 = [5, 4, 6, 8, 8, 4, 10, 7]
        self.assertEqual(seq(), seq1)

    def test_rollLength(self):
        s = [5, 4, 6, 8, 8, 4, 10, 7]
        self.assertEqual(rollLength(s), 8)

    def test_pointsMade(self):
        s = (8,4,6,8,9,8,7)
        self.assertEqual(pointsMade(s), 2)
        s = (3,11,12,2,6,7)
        self.assertEqual(pointsMade(s), 0)
        s = (8,4,6,6,10,9,8,4,7)
        self.assertEqual(pointsMade(s), 3)

    def test_pointsRiding(self):
        s = (8,4,6,8,9,8,7)
        self.assertEqual(pointsRiding(s), 4)
        s = (3,11,12,2,6,7)
        self.assertEqual(pointsRiding(s), 1)
        s = (8,4,6,6,10,9,8,4,7)
        self.assertEqual(pointsRiding(s), 5)

    def test_svn11(self):
        s = (8,4,6,8,9,8,7)
        self.assertEqual(svn11(s), 1)
        s = (3,11,12,2,6,7)
        self.assertEqual(svn11(s), 2)
        s = (8,4,6,6,10,9,8,4,7)
        self.assertEqual(svn11(s), 1)

    def test_crapsRight(self):
        s = (8,4,6,8,9,8,7)
        self.assertEqual(crapsRight(s), 0)
        s = (3,11,12,2,6,7)
        self.assertEqual(crapsRight(s), 3)
        s = (8,4,6,6,10,9,8,4,7)
        self.assertEqual(crapsRight(s), 0)

    def test_crapsWrong(self):
        s = (8,4,6,8,9,8,7)
        self.assertEqual(crapsWrong(s), 0)
        s = (3,11,12,2,6,7)
        self.assertEqual(crapsWrong(s), 2)
        s = (8,4,6,6,10,9,8,4,7)
        self.assertEqual(crapsWrong(s), 0)

    def test_payoutRight(self):
        s = (8,4,6,8,9,8,7)
        self.assertEqual(payoutRight(s), -1)
        s = (3,11,12,2,6,7)
        self.assertEqual(payoutRight(s), -2)
        s = (8,4,6,6,10,9,8,4,7)
        self.assertEqual(payoutRight(s), -1)

    def test_payoutWrong(self):
        s = (8,4,6,8,9,8,7)
        self.assertEqual(payoutWrong(s), 1)
        s = (3,11,12,2,6,7)
        self.assertEqual(payoutWrong(s), 1)
        s = (8,4,6,6,10,9,8,4,7)
        self.assertEqual(payoutWrong(s), 1)

    def test_trial_and_trialLength(self):
        t = trial(1)
        self.assertEqual(len(t), 1)
        t = trial(100)
        l = 0
        for s in t[:-1]: l += len(s)
        self.assertTrue(l < 100)
        l += len(t[-1])
        self.assertTrue(l >= 100)
        self.assertEqual(l, trialLength(t))
                  


if __name__ == '__main__':
    unittest.main(verbosity=2)



