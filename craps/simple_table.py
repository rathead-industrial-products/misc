#
# Maintain the state of a craps table.
# Wagers are on the come (pass) line only
# Perform the actions of the boxmen.
#

from ctypes.wintypes import POINT


DIE_FACE        = (1,2,3,4,5,6)
POINTS          = (4,5,6,8,9,10)
CRAPS           = (2,3,12)
SVN_11          = (7, 11)
MAX_THROW       = 12


class table():
    def __init__(self):
        self.come   = 0                  # come bet
        self.place  = {}                 # place bets. self.place[4|5|6|8|9|10] = bet
        self.payout = 0

    def roll(self, die1_or_total, die2=None):
        if die2 != None:
            assert die1_or_total in DIE_FACE
            assert die2 in DIE_FACE
            throw = die1_or_total + die2
        else:
            assert die1_or_total >= 1 and die1_or_total <= MAX_THROW
            throw = die1_or_total
        self._action(throw)

    def comeBet(self, amount):
        self.come = amount

    def bets(self):
        '''Return the status of all bets in the form (come, (place4, place5, ..., place10)).'''
        come  = self.come
        place = [self.place.get(p, 0) for p in POINTS]
        return (come, place)

    def workingPoints(self):
        '''Return the points that have a bet on them.'''
        return (sorted(self.place.keys()))

    def workingAmount(self):
        '''Return the sum of all bets currently on the table.'''
        (come, place) = self.bets()
        total = come + sum(place)
        return (total)

    def collectPayout(self):
        '''Return payout and clear it.'''
        payout = self.payout
        self.payout = 0
        return(payout)

    def _action(self, throw):
        # be the boxman 
        if throw in self.place.keys():
            self.payout += 2 * self.place[throw]
        if throw in POINTS: 
            self.place[throw] = self.come
        if throw in SVN_11:
            self.payout += 2 * self.come
        if throw == 7:
            self.place = {}     # clear the table
        self.come = 0



#
# Main  --  Unit Test
#

import unittest

class TestTable(unittest.TestCase):
    def test_table_init(self):
        t = table()
        self.assertFalse(t.come or t.place or t.payout)

    def test_table_roll(self):
        t = table()
        self.assertRaises(Exception, t.roll, 0)     # one die (throw) must be >= 1 and <= 12
        self.assertRaises(Exception, t.roll, 13)
        self.assertRaises(Exception, t.roll, 0, 1)  # two die, each die must be 1<= die <=6
        self.assertRaises(Exception, t.roll, 7, 1)
        self.assertRaises(Exception, t.roll, 1, 0)
        self.assertRaises(Exception, t.roll, 1, 7)

    def test_table_comeBet(self):
        t = table()
        t.comeBet(5)
        self.assertEqual(t.come, 5)

    def test_table_bets(self):
        t = table()
        t.come = 1
        t.place[4]  = 4
        t.place[5]  = 5
        t.place[6]  = 6
        t.place[8]  = 8
        t.place[9]  = 9
        t.place[10] = 10
        self.assertEqual(t.bets(), (1, [4, 5, 6, 8, 9, 10]))

    def test_table_workingPoints(self):
        t = table()
        self.assertEqual(t.workingPoints(), [])
        t.place[4]  = 4
        t.place[8]  = 8
        t.place[10] = 10
        self.assertEqual(t.workingPoints(), [4, 8, 10])

    def test_table_workingAmount(self):
        t = table()
        t.come = 1
        t.place[4]  = 4
        t.place[8]  = 8
        t.place[10] = 10
        self.assertEqual(t.workingAmount(), 23)

    def test_table_collectPayout(self):
        t = table()
        t.payout = 4
        payout = t.collectPayout()
        self.assertEqual(payout, 4)
        self.assertEqual(t.payout, 0)

    def test_table_action_2roll(self):
        t = table()
        t.comeBet(1)
        t._action(6)                        # establish point
        t.comeBet(1)
        t._action(7)                        # seven-out
        self.assertEqual(t.payout, 2)    # come bet paid

    def test_table_action_crap_roll(self):
        t = table()
        for c in CRAPS:     # shooter has not established a point yet
            t.comeBet(1)
            t._action(c)
            self.assertEqual(t.come, 0)     # come bet is lost
            self.assertEqual(t.payout, 0)
        t.comeBet(1)
        t._action(6)                        # establish point
        self.assertEqual(t.come, 0)         # come bet moved to point
        for c in CRAPS:
            t.comeBet(1)
            t._action(c)
            self.assertEqual(t.come, 0)     # come bet is lost
            self.assertEqual(t.payout, 0)

    def test_table_action_3roll_incr_bet(self):
        t = table()
        t.comeBet(1)
        t._action(6)                        # establish point
        t.comeBet(1)
        t._action(4)                        # another number working
        t.comeBet(2)                        # double come bet to cover potential 7-out
        t._action(7)                        # seven-out
        self.assertEqual(t.payout, 4)       # come payout + returned bet

    def test_table_action_make_point(self):
        t = table()
        t.comeBet(1)
        t._action(6)                        # establish point
        t.comeBet(1)
        t._action(6)                        # make point
        self.assertEqual(t.payout, 2)       # point paid, bet returned
        self.assertEqual(t.place[6], 1)     # place bet off/on
        self.assertEqual(t.workingPoints(), [6])    # only the 6 is working

    def test_table_action_7_out(self):
        t = table()
        t.comeBet(1)
        t._action(6)                        # establish point
        t.comeBet(1)
        t._action(4)                        # another point
        t.comeBet(1)
        t._action(7)                        # 7-out
        self.assertEqual(t.payout, 2)       # come bet paid
        self.assertEqual(t.workingPoints(), [])    # no place bets working


if __name__ == '__main__':
    unittest.main(verbosity=2)



