#
# Maintain the state of a craps table.
# Wagers are on the come (pass) line or don't come (don't pass) line only.
# Perform the actions of the boxmen.
#


DIE_FACE        = (1,2,3,4,5,6)
POINTS          = (4,5,6,8,9,10)
CRAPS           = (2,3,12)
BAR             = 12
SVN_11          = (7, 11)
MAX_THROW       = 12


class table():
    def __init__(self):
        self.come        = 0                  # come bet
        self.dont_come   = 0                  # dont come bet
        self.place       = {}                 # place bets. self.place[4|5|6|8|9|10] = bet
        self.dont_place  = {}
        self.payout      = 0
        self.dont_payout = 0

    def roll(self, die1_or_total, die2=None):
        if die2 != None:
            assert die1_or_total in DIE_FACE
            assert die2 in DIE_FACE
            throw = die1_or_total + die2
        else:
            assert die1_or_total >= 1 and die1_or_total <= MAX_THROW
            throw = die1_or_total
        return(throw)

    def comeBet(self, amount):
        self.come = amount

    def dontComeBet(self, amount):
        self.dont_come = amount

    def betsRight(self):
        '''Return the status of all bets in the form (come, (place4, place5, ..., place10))'''
        come  = self.come
        place = [self.place.get(p, 0) for p in POINTS]
        return (come, place)

    def betsWrong(self):
        '''Return the status of all bets in the form (dont_come, (dont_place4, dont_place5, ..., dont_place10)'''
        dont_come  = self.dont_come
        dont_place = [self.dont_place.get(p, 0) for p in POINTS]
        return (dont_come, dont_place)

    def takeDownWrong(self):
        '''Remove and return all the dont place bets'''
        bets = self.betsWrong()
        self.dont_place = {}
        return (sum(bets[1]))

    def workingPointsRight(self):
        '''Return the come/place points that have a bet.'''
        return (sorted(self.place.keys()))

    def workingPointsWrong(self):
        '''Return the dont_come/dont_place points that have a bet.'''
        return (sorted(self.dont_place.keys()))

    def workingAmountRight(self):
        '''Return the sum of all come + place bets currently on the table.'''
        (come, place) = self.betsRight()
        total = come + sum(place)
        return (total)

    def workingAmountWrong(self):
        '''Return the sum of all dont_come + dont_place bets currently on the table.'''
        (dont_come, dont_place) = self.betsWrong()
        total = dont_come + sum(dont_place)
        return (total)

    def collectPayoutRight(self):
        '''Return come/place payout and clear it.'''
        payout = self.payout
        self.payout = 0
        return(payout)

    def collectPayoutWrong(self):
        '''Return dont_come/dont_place payout and clear it.'''
        payout = self.dont_payout
        self.dont_payout = 0
        return(payout)

    def action(self, throw):
        # be the boxman 

        # right player
        if throw in self.place.keys():
            self.payout += 2 * self.place[throw]
            del(self.place[throw])
        if throw in POINTS and self.come: 
            self.place[throw] = self.come
        if throw in SVN_11:
            self.payout += 2 * self.come
        if throw == 7:
            self.place = {}     # clear the table
        self.come = 0

        # wrong player
        if throw in self.dont_place.keys():
            del(self.dont_place[throw])
        if throw in POINTS and self.dont_come: 
            self.dont_place[throw] = self.dont_come
        if throw in CRAPS and throw != BAR:
            self.dont_payout += 2 * self.dont_come
        if throw == BAR:
            self.dont_payout += self.dont_come  # push, return bet
        if throw == 7:
            for p in self.dont_place.keys():
                self.dont_payout += 2 * self.dont_place[p]
            self.dont_place = {}
        # no need to test against 7 or 11 for don't come bet, it is lost automatically
        self.dont_come = 0



#
# Main  --  Unit Test
#

import unittest

class TestTable(unittest.TestCase):
    def test_table_init(self):
        t = table()
        self.assertFalse(t.come or t.place or t.payout)
        self.assertFalse(t.dont_come or t.dont_place or t.dont_payout)

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

    def test_table_dontComeBet(self):
        t = table()
        t.dontComeBet(5)
        self.assertEqual(t.dont_come, 5)

    def test_table_betsRight(self):
        t = table()
        t.come = 1
        t.place[4]  = 4
        t.place[5]  = 5
        t.place[6]  = 6
        t.place[8]  = 8
        t.place[9]  = 9
        t.place[10] = 10
        self.assertEqual(t.betsRight(), (1, [4, 5, 6, 8, 9, 10]))

    def test_table_betsWrong(self):
        t = table()
        t.dont_come = 1
        t.dont_place[4]  = 4
        t.dont_place[5]  = 5
        t.dont_place[6]  = 6
        t.dont_place[8]  = 8
        t.dont_place[9]  = 9
        t.dont_place[10] = 10
        self.assertEqual(t.betsWrong(), (1, [4, 5, 6, 8, 9, 10]))

    def test_table_takeDownWrong(self):
        t = table()
        t.dont_come = 1
        t.dont_place[4]  = 4
        t.dont_place[5]  = 5
        t.dont_place[6]  = 6
        self.assertEqual(t.betsWrong(), (1, [4, 5, 6, 0, 0, 0]))
        working_bets_returned = t.takeDownWrong()
        self.assertEqual(t.betsWrong(), (1, [0, 0, 0, 0, 0, 0]))
        self.assertEqual(working_bets_returned, 15)

    def test_table_workingPointsRight(self):
        t = table()
        self.assertEqual(t.workingPointsRight(), [])
        t.place[4]  = 4
        t.place[8]  = 8
        t.place[10] = 10
        self.assertEqual(t.workingPointsRight(), [4, 8, 10])

    def test_table_workingPointsWrong(self):
        t = table()
        self.assertEqual(t.workingPointsWrong(), [])
        t.dont_place[4]  = 4
        t.dont_place[8]  = 8
        t.dont_place[10] = 10
        self.assertEqual(t.workingPointsWrong(), [4, 8, 10])

    def test_table_workingAmountRight(self):
        t = table()
        self.assertEqual(t.workingAmountRight(), 0)
        t.come = 1
        t.place[4]  = 4
        t.place[8]  = 8
        t.place[10] = 10
        self.assertEqual(t.workingAmountRight(), 23)

    def test_table_workingAmountWrong(self):
        t = table()
        self.assertEqual(t.workingAmountWrong(), 0)
        t.dont_come = 1
        t.dont_place[4]  = 4
        t.dont_place[8]  = 8
        t.dont_place[10] = 10
        self.assertEqual(t.workingAmountWrong(), 23)

    def test_table_collectPayoutRight(self):
        t = table()
        t.payout = 4
        payout = t.collectPayoutRight()
        self.assertEqual(payout, 4)
        self.assertEqual(t.payout, 0)

    def test_table_collectPayoutWrong(self):
        t = table()
        t.dont_payout = 4
        payout = t.collectPayoutWrong()
        self.assertEqual(payout, 4)
        self.assertEqual(t.dont_payout, 0)

    def test_table_action_2roll(self):
        t = table()
        t.comeBet(1)
        t.dontComeBet(1)
        t.action(6)                        # establish point
        t.comeBet(1)
        t.dontComeBet(1)
        t.action(7)                        # seven-out
        self.assertEqual(t.payout, 2)       # come bet paid
        self.assertEqual(t.dont_payout, 2)  # dont place bet paid

    def test_table_action_roll_crap(self):
        t = table()
        for c in CRAPS:     # shooter has not established a point yet
            t.comeBet(1)
            t.dontComeBet(1)
            t.action(c)
            self.assertEqual(t.come, 0)     # come bet is lost
            self.assertEqual(t.payout, 0)
            if c != BAR:
                self.assertEqual(t.dont_come, 0)
                self.assertEqual(t.dont_payout, 2)  # don't come bet pays off
                t.dont_payout = 0
            else:
                self.assertEqual(t.dont_come, 0)
                self.assertEqual(t.dont_payout, 1)  # push, return dont come bet

    def test_table_action_roll_crap_after_point(self):
        t = table()
        t.comeBet(1)
        t.dontComeBet(1)
        t.action(6)                        # establish point
        self.assertEqual(t.come, 0)         # come bet moved to point
        self.assertEqual(t.dont_come, 0)
        for c in CRAPS:
            t.comeBet(1)
            t.dontComeBet(1)
            t.action(c)
            self.assertEqual(t.come, 0)     # come bet is lost
            self.assertEqual(t.payout, 0)
            if c != BAR:
                self.assertEqual(t.dont_come, 0)
                self.assertEqual(t.dont_payout, 2)  # don't come bet pays off
                t.dont_payout = 0
            else:
                self.assertEqual(t.dont_come, 0)
                self.assertEqual(t.dont_payout, 1)  # push, return dont come bet
  
    def test_table_action_3roll_incr_bet(self):
        t = table()
        t.comeBet(1)
        t.dontComeBet(1)
        t.action(6)                        # establish point
        t.comeBet(1)
        t.dontComeBet(1)
        t.action(4)                        # another number working
        t.comeBet(2)                        # double come bet to cover potential 7-out
        t.dontComeBet(2)
        t.action(7)                        # seven-out
        self.assertEqual(t.payout, 4)       # come payout + returned bet
        self.assertEqual(t.dont_payout, 4)  # lost dont come, points paid off

    def test_table_action_make_point(self):
        t = table()
        t.comeBet(1)
        t.dontComeBet(1)
        t.action(6)                        # establish point
        t.comeBet(1)
        t.dontComeBet(1)
        t.action(6)                        # make point
        self.assertEqual(t.payout, 2)       # point paid, bet returned
        self.assertEqual(t.dont_payout, 0)  # dont point lost
        self.assertEqual(t.place[6], 1)     # place bet off/on
        self.assertEqual(t.dont_place[6], 1)
        self.assertEqual(t.workingPointsRight(), [6])    # only the 6 is working
        self.assertEqual(t.workingPointsWrong(), [6])
        
    def test_table_action_7_out(self):
        t = table()
        t.comeBet(1)
        t.dontComeBet(1)
        t.action(6)                        # establish point
        t.comeBet(1)
        t.dontComeBet(1)
        t.action(4)                        # another point
        t.comeBet(1)
        t.dontComeBet(1)
        t.action(7)                        # 7-out
        self.assertEqual(t.payout, 2)       # come bet paid
        self.assertEqual(t.dont_payout, 4)  # points paid, dont come bet lost
        self.assertEqual(t.workingPointsRight(), [])    # no place bets working
        self.assertEqual(t.workingPointsWrong(), [])    # no place bets working

    def test_table_action_dont_come_sequence_1(self):
        SEQUENCE = (11, 7, 7, 7, 11, 5, 7)
        t = table()
        for s in SEQUENCE:
            t.dontComeBet(1)
            t.action(s)
        self.assertEqual(t.collectPayoutWrong(), 2)

    def test_table_action_establish_point_no_come_dont_come(self):
        t = table()
        # no come or don't come bet
        t.action(6)
        self.assertEqual(t.workingPointsWrong(), [])
        self.assertEqual(t.workingPointsRight(), [])

    def test_table_action_remove_bet_after_point(self):
        t = table()
        t.comeBet(1)
        t.action(5)                        # establish point
        t.action(5)                        # make point
        self.assertEqual(t.collectPayoutRight(), 2)
        t.action(5)
        self.assertEqual(t.collectPayoutRight(), 0)



if __name__ == '__main__':
    unittest.main(verbosity=2)



