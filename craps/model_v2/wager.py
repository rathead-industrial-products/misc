#
# Make a wager on a craps table.
# Only come and don't come wagers are supported.
#

class wager():
    history    = []
    unresolved = []

    def __init__(self, bet=1, come=True):
        # default to a single unit come bet
        self.bet        = bet  
        self.come       = come          # true if come bet, false if don't come bet
        self.point      = 0             # nonzero if a point has been established
        self.resolved   = False         # True if wager resolved, False if deferred
        self.resolution = 0             # roll that resolved wager (win or lose)
        self.win        = None          # if resolved, True if win, False if lose. None if unresolved
        wager.unresolved.append(self)

    def roll(self, throw):
        # wager has already been resolved
        if self.resolved: return (True) 

        # first roll after wager (i.e. come-out roll), wager will not resolve
        if self.point == 0 and throw in (4, 5, 6, 8, 9, 10):    # establish point
            self.point = throw
            return (False)
        
        # point previously made but wager still unresolved
        if self.point and throw not in (self.point, 7):
            return (False)

        # don't come bar 12 is a no-op if there is a point established
        # and like it never happened if it is a come-out roll
        if not self.come and throw == 12:
            if not self.point: wager.unresolved.remove(self)
            return (False)   

        # all following throws will resolve wager    
        # point previously established                   
        if throw == self.point:
            if self.come: self.win = True   # come bet a winner
            else:         self.win = False  # don't come bet a loser
        if throw == 7 and self.point:
            if self.come: self.win = False  # come bet a loser
            else:         self.win = True   # don't come bet a winner

        # 7-11
        elif throw in (7, 11):
            if self.come: self.win = True   # come bet a winner
            else:         self.win = False  # don't come bet a loser

        # crap
        if throw in (2, 3) or (throw == 12 and self.come):  # crap
            if self.come: self.win = False  # come bet a loser
            else:         self.win = True   # don't come bet a winner
       
        self.resolution = throw
        self.resolved = True
        print ("appending to history, deleting from unresolved, pt/resolved = %d / %d" % (self.point, self.resolution))
        wager.history.append(self)
        wager.unresolved.remove(self)
        return (True)                       # wager resolved


#
# Main  --  Unit Test
#

import unittest

class TestWager(unittest.TestCase):
    def setUp(self):
        wager.history    = []
        wager.unresolved = []

    def tearDown(self):
        pass

    def _dumpWager(self, w):
        print (w.bet, w.come, w.point, w.resolved, w.resolution, w.win)

    def _dumpWagerQueueLen(self):
        hl = []
        ul = []
        for h in wager.history:
            hl.append("%s/%s" % (h.point, h.resolution))
        for u in wager.unresolved:
            ul.append("%s/%s" % (u.point, u.resolution))
        print (hl, ul)

    def test_wager_init(self):
        w = wager()
        self.assertFalse(w.point or w.resolved or w.resolution or w.win)
        self.assertTrue(w.come and w.bet == 1)
        self.assertTrue(w in wager.unresolved)

    def test_wager_come_7_11(self):
        w7 = wager()
        w7.roll(7)
        self.assertTrue(w7.point==0 and w7.resolved and w7.resolution==7 and w7.win)
        w11 = wager()
        w11.roll(11)
        self.assertTrue(w11.point==0 and w11.resolved and w11.resolution==11 and w7.win)
        self.assertTrue(w7 in wager.history and w11 in wager.history)
        self.assertTrue(len(wager.unresolved) == 0)

    def test_wager_dont_come_7_11(self):
        w7 = wager(come=False)
        w7.roll(7)
        self.assertTrue(w7.point==0 and w7.resolved and w7.resolution==7 and not w7.win)
        w11 = wager(come=False)
        w11.roll(11)
        self.assertTrue(w11.point==0 and w11.resolved and w11.resolution==11 and not w7.win)
        self.assertTrue(w7 in wager.history and w11 in wager.history)
        self.assertTrue(len(wager.unresolved) == 0)

    def test_wager_come_crap(self):
        w2 = wager()
        w2.roll(2)
        self.assertTrue(w2.point==0 and w2.resolved and w2.resolution==2 and not w2.win)
        w3 = wager()
        w3.roll(3)
        self.assertTrue(w3.point==0 and w3.resolved and w3.resolution==3 and not w3.win)
        w12 = wager()
        w12.roll(12)
        self.assertTrue(w12.point==0 and w12.resolved and w12.resolution==12 and not w3.win)
        self.assertTrue(w2 in wager.history and w3 in wager.history and w12 in wager.history)
        self.assertTrue(len(wager.unresolved) == 0)

    def test_wager_dont_come_crap(self):
        w2 = wager(come=False)
        w2.roll(2)
        self.assertTrue(w2.point==0 and w2.resolved and w2.resolution==2 and w2.win)
        w3 = wager(come=False)
        w3.roll(3)
        self.assertTrue(w3.point==0 and w3.resolved and w3.resolution==3 and w3.win)
        w12 = wager(come=False)
        w12.roll(12)
        self.assertTrue(w12.point==0 and not w12.resolved and w12.resolution==0 and w12.win==None)
        self.assertTrue(w2 in wager.history and w3 in wager.history and w12 not in wager.history)
        self.assertTrue(len(wager.unresolved) == 0)

    def test_wager_come_point_made(self):
        w = wager()
        w.roll(4)
        self.assertTrue(w.point==4 and not w.resolved and w.resolution==0 and w.win==None)
        self.assertTrue(len(wager.unresolved) == 1)
        w.roll(4)
        self.assertTrue(w.point==4 and w.resolved and w.resolution==4 and w.win==True)
        self.assertTrue(w in wager.history)
        self.assertTrue(len(wager.unresolved) == 0)

    def test_wager_come_point_lost(self):
        w = wager()
        w.roll(4)
        self.assertTrue(w.point==4 and not w.resolved and w.resolution==0 and w.win==None)
        self.assertTrue(len(wager.unresolved) == 1)
        w.roll(7)
        self.assertTrue(w.point==4 and w.resolved and w.resolution==7 and w.win==False)
        self.assertTrue(w in wager.history)
        self.assertTrue(len(wager.unresolved) == 0)

    def test_Wager_come_sequence(self):
        trial = [5, 4, 6, 8, 8, 4, 10, 7, 7, 10]
        n_unresolved = [1, 2, 3, 4, 4, 4, 5, 0, 0, 1]
        for i in  range(len(trial)):
            w = wager()
            for u in wager.unresolved:
                u.roll(trial[i])
                self._dumpWager(u)
                self._dumpWagerQueueLen()
            self.assertTrue(len(wager.unresolved) == n_unresolved[i])

'''
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
'''


if __name__ == '__main__':
    unittest.main(verbosity=2)



