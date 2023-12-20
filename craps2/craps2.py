#
# 
#

import roll, itertools
from wager import wager
import matplotlib.pyplot as plt

CRAP        = (2, 3, 12)
CRAP_BAR_12 = (2, 3)
POINT       = (4, 5, 6, 8, 9, 10)

N_ROLLS = 1000

class xlist(list):
    # extend the built-in list type to add a .prev() method
    # return a list of the n previous rolls before idx
    # return outofrange for rolls out of range
    # return a scaler if n == 1
    # default with no parameters returns the last item in the list
    def prev(self, n=1, idx=None, outofrange=0):
        if idx is None: idx = len(self)
        assert idx >= 0 and idx <= len(self)
        if idx - n < 0:
            prelist = [outofrange] * abs(idx-n)
            prev = prelist + self[:idx]
        else:
            prev = self[idx-n: idx]
        if n == 1: prev = prev[0]
        return (prev)

def _plotSeries(**series):
    # _plotSeries(('label1':[d1, d2], 'label2:[d3.d4], ... ))
    fig, ax = plt.subplots()
    for label, data in series.items():
        ax.plot(data, label=label)
    plt.legend()
    plt.show()

def _printList(l):  # print a list seperating items with tabs
    for item in l:
        print ("%s\t" % (str(item)), end='')
    print ()




trial = roll.trial(N_ROLLS, outcome=True, flat=True) #[430:450]
(roll_seq, c_outcome, d_outcome) = [xlist(t) for t in zip(*trial)]
cwager = xlist([])
dwager = xlist([])

w = wager(roll_seq, c_outcome, d_outcome, cwager, dwager)

# roll stats
# total rolls
# % of 7-11's
# % of Craps
# % of Points
# longest roll
# max consecutive 7-11's
from collections import Counter
total_rolls = len(roll_seq)
counts = Counter(roll_seq)
svn11_rolled = 0
craps_rolled = 0
points_rolled = 0
for key in (7, 11): svn11_rolled += counts[key]
for key in CRAP: craps_rolled += counts[key]
for key in POINT: points_rolled += counts[key]
# longest roll
idx7 = [i for i, roll in enumerate(roll_seq) if roll == 7]
longest_roll = idx7[0]
for i in range(len(idx7)-1):
    longest_roll = max(longest_roll, idx7[i+1] - idx7[i])
# consecutive 7-11's
no_11 = [x if x!=11 else 7 for x in roll_seq]   # replace 11s with 7s
max_consecutive_7_11 = max([len(list(g)) if k==7 else 0 for k, g in itertools.groupby(no_11)])
print ("Total Rolls", total_rolls)
print ("Longest Roll", longest_roll)
print ("Max Consecutive 7-11's", max_consecutive_7_11)
print ("Roll Distribution: 7-11 %0.2f%%, Crap %0.2f%%, Point %0.2f%%" % (
     100*svn11_rolled/total_rolls,
    -100*craps_rolled/total_rolls,
     100*points_rolled/total_rolls))

'''
print ("roll\t", end=''); _printList (roll_seq)
print ("outcome\t", end=''); _printList (w.dont)
print ("loss\t", end=''); _printList ([round(x, 2) for x in w.running_loss_dont_history])
print ("bet\t", end=''); _printList ([round(x, 2) for x in w.dwager])
print ("bank\t", end=''); _printList ([round(x, 2) for x in w.dfit])
'''

print ("Player come advantage %0.2f%%\nPlayer don't advantage %0.2f%%\nMax come bet %.0f\nMax don't bet %.0f" % (100*w.fitnessCome()/w.totalBetCome(), 100*w.fitnessDont()/w.totalBetDont(), w.maxBetCome(), w.maxBetDont()))
_plotSeries(come=w.fitnessArrayCome(), dont_come=w.fitnessArrayDont())
#print (roll_seq[841600:841620])
#print (dwager[841600:841620])
#_plotSeries(w.fitnessArrayDont()[841600:841620])
#


#
# Main  --  Unit Test
#
import unittest

class TestCraps(unittest.TestCase):
    def test_xListPrev(self):
        xl = xlist([])
        self.assertEqual(xl.prev(), 0)
        self.assertEqual(xl.prev(2), [0, 0])
        xl.append(1)
        self.assertEqual(xl, [1])
        xl.append(2)
        self.assertEqual(xl, [1, 2])
        xl += [3, 4]
        self.assertEqual(xl, [1, 2, 3, 4])
        self.assertEqual(xl.prev(), 4)
        self.assertEqual(xl.prev(2), [3, 4])
        self.assertEqual(xl.prev(idx=0), 0)
        self.assertEqual(xl.prev(2, 1), [0, 1])

'''
if __name__ == '__main__':
    unittest.main(verbosity=2)
'''

