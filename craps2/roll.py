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
    # return three series of 3-tuples: (roll, come_outcome, dont_outcome)
    # where roll is the throw of the dice and *_outcome is +1/0/-1 reflecting whether the
    # roll, now or in the future, is a win, loss, or draw.
    BAR   = 12        # don't come bar 12
    rslt = []
    s = seq()
    for i in range(len(s)):
        # determine if roll is a win/lose/draw  outcome = +1 | 0 | -1
        # don't come is opposite of come outcome unless BAR is rolled, than it's a draw
        roll = s[i]
        if roll in (2, 3, 12):  c_outcome = -1      # crap a loser
        elif roll in (7, 11):   c_outcome = +1      # 7 winner
        elif roll in (s[i+1:]): c_outcome = +1      # point made
        else:                   c_outcome = -1      # point not made
        d_outcome = 0 if roll == BAR else -c_outcome
        rslt.append((roll, c_outcome, d_outcome))
    return (rslt)

def trial(n, outcome=False, flat=False):
    # return a series of sequences totalling at least n rolls:
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

def meanMedianModeStdDev(data):
    # statistics.mode (version < 3.8) will generate an exception if no unique mode found.
    try:    mode = statistics.mode(data)                             # returns first mode found
    except: mode = max([p[0] for p in statistics._counts(data)])    # returns largest if no unique mode
    if len(data) > 1: sd = round(statistics.stdev(data),1)
    else:             sd = None
    return (min(data), max(data), round(statistics.mean(data),1), statistics.median(data), mode, sd)


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
    seed(); l = trial(10, True, True)

    c = [item[:2] for item in l]
    print (c)

    #c_win = sum([item[1] for sublist in l for item in sublist])
    #d_win = sum([item[2] for sublist in l for item in sublist])





    unittest.main(verbosity=2)



