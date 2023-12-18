#
# 
#

import roll
from wager import wager
import matplotlib.pyplot as plt

N_ROLLS = 1000000

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


def _plotSeries(y1, y2=[], label1='', label2=''):
    fig, ax = plt.subplots()
    ax.plot(y1, label=label1)
    if y2:
        ax.plot(y2, label=label2)
    plt.legend()
    plt.show()

def _runningSum(l):
    # Return a list where element n is the sum of all elements [0:n] of l
    s = [l[0]]
    for e in l[1:]:
        s.append(s[-1]+e)
    return (s)


trial = roll.trial(N_ROLLS, outcome=True, flat=True)
(roll_seq, c_outcome, d_outcome) = xlist(zip(*trial))
cwager = xlist([])
dwager = xlist([])

w = wager(roll_seq, c_outcome, d_outcome, wager, dwager)


print (wager.fitnessCome()/N_ROLLS, wager.fitnessDont/N_ROLLS, wager.maxBetCome, wager.maxBetDont)
_plotSeries(wager.fitnessArrayCome(), wager.fitnessArrayDont, 'come', 'dont come')


#
# Main  --  Unit Test
#
import unittest

class TestxListPrev(unittest.TestCase):
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

