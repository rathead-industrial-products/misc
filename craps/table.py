#
# Maintain the state of a craps table.
# Perform the actions of the boxmen.
#

DIE_FACE    = (1,2,3,4,5,6)
POINTS      = (4,5,6,8,9,10)
CRAPS       = (2,3,12)
MAX_THROW   = 12
MAX_ODDS    = ("1x", "2x", "345x", "10x")


class wager():
    def __init__(self, max_odds="10x"):
        self.come  = 0                  # come bet
        self.place = [0] * MAX_THROW    # place bets. Only (4,5,6,8,9,10) are used
        self.odds  = [0] * MAX_THROW    # odds bets. Only (4,5,6,8,9,10) are used
        assert max_odds in MAX_ODDS
        self.max_odds = max_odds

    def _clearPlaceOdds(self, place_or_odds, throw):
        amount = place_or_odds[throw]
        place_or_odds[throw] = 0
        return (amount)

    def clearPlace(self, throw):
        return (self._clearPlaceOdds(self.place, throw))
        
    def clearOdds(self, throw):
        return (self._clearPlaceOdds(self.odds, throw))

    def clearCome(self):
        amount = self.come
        self.come = 0
        return (amount)

    def clearAll(self):
        amount  = self.clearCome()
        amount += sum([self.clearPlace(n) for n in POINTS])
        amount += sum([self.clearOdds(n) for  n in POINTS])
        return (amount)

    def comeBet(self, amount):
        assert not self.come            # cannot already be a come bet working
        self.come = amount

    def placeBet(self, amount, num):
        assert num in POINTS            # must be one of (4,5,6,8,9,10)
        assert not self.place[num]      # no existing place bet
        self.place[num] = amount

    def oddsBet(self, amount, num):
        assert num in POINTS            # must be one of (4,5,6,8,9,10)
        assert self.place[num]          # must be a current place bet
        assert not self.odds[num]       # no existing odds bet
        # must be able to evenly pay off 3:2 and 6:5 odds
        if num == 5 or num == 9: assert not amount % 2           
        if num == 6 or num == 8: assert not amount % 5
        # odds bet can't exceed max allowed
        if self.max_odds == "1x":  assert amount <= self.place[num]
        if self.max_odds == "2x":  assert amount <= (2 * self.place[num])
        if self.max_odds == "10x": assert amount <= (10 * self.place[num])
        if self.max_odds == "345x":
            if num == 4 or num == 10: assert amount <= (3 * self.place[num])
            if num == 5 or num == 9:  assert amount <= (4 * self.place[num])
            if num == 6 or num == 8:  assert amount <= (5 * self.place[num])
        self.odds[num] = amount

    def moveComeToPlace(self, roll):
        self.placeBet(self.clearCome(), roll)


class table():
    def __init__(self):
        self.comeout                 = True # true if this is a comeout roll.
        self.point                   = None # the shooter's point. One of None (OFF), 4, 5, 6, 8, 9, or 10.
        self.odds_working_on_comeout = True # place numbers with odds have the odds working on the comeout roll (casino default = False)
        self.odds_off_and_on         = True # when a place number is made with a come bet riding, the odds are paid but not returned (they stay working)
        self.bet    = wager()
        self.payout = wager()
        self.shooter_rolls = 0

    def roll(self, die1_or_total, die2=None):
        if die2 != None:
            assert die1_or_total in DIE_FACE
            assert die2 in DIE_FACE
            throw = die1_or_total + die2
        else:
            assert die1_or_total >= 1 and die1_or_total <= MAX_THROW
            throw = die1_or_total
        self.shooter_rolls += 1
        self._action(throw)

    def comeBet(self, amount):
        self.bet.comeBet(amount)

    def oddsBet(self, amount, num):
        self.bet.oddsBet(amount, num)

    def bets(self):
        '''Return the status of all bets in the form (come, (place4, place5, ..., place10), (odds4, odds5, ..., odds10)).'''
        come  = self.bet.come
        place = tuple(self.bet.place[4:7] + self.bet.place[8:11])
        odds  = tuple(self.bet.odds[4:7]  + self.bet.odds[8:11])
        return (come, place, odds)

    def action(self):
        '''Return the sum off all bets currently on the table.'''
        (come, place, odds) = self.bets()
        total = come + sum(place) + sum(odds)
        return (total)

    def payoff(self):
        '''Return everything in the payout in the form (come, (place4, place5, ..., place10), (odds4, odds5, ..., odds10)).'''
        come  = self.payout.come
        place = tuple(self.payout.place[4:7] + self.payout.place[8:11])
        odds  = tuple(self.payout.odds[4:7]  + self.payout.odds[8:11])
        return (come, place, odds)

    def collect(self):
        '''Return and clear the entire payout.'''
        (come, place, odds) = self.payoff()
        total = come + sum(place) + sum(odds)
        self.payout.clearAll()
        return (total)

    def _correctOdds(self, throw, amount):
        '''Return the correct odds for this amount and the throw.'''
        if throw == 4 or throw == 10: return (2 * amount)
        if throw == 5 or throw == 9:  return ((3 * amount) / 2)
        if throw == 6 or throw == 8:  return ((6 * amount) / 5)

    def _action(self, throw):
        # be the boxman
        if throw == 7:
            self.payoff.come = 2 * self.bet.clearCome()
            if self.comeout and not self.odds_working_on_comeout:
                for p in POINTS: self.payoff.odds[p] = self.bet.odds(p)
            self.bet.clearAll()
            if not self.comeout:
                self.shooter_rolls = 0  # new shooter
            self.comeout = True         # even if this was a comeout roll, it's still True

        if throw in POINTS:    
            # pay any place bets and odds working. Shooter has point if comeout roll.
            # if the odds are off and on or working on the comeout, the come bet must be the same or greater as the place bet
            # to reuse the same odds bet      
            self.payout.odds[throw] = self._correctOdds(throw, self.bet.odds[throw])   # pay odds
            odds_stay_working = (self.comeout and self.odds_working_on_comeout) or (self.bet.come and self.odds_off_and_on)
            if not odds_stay_working:
                self.payout.odds[throw] += self.bet.clearOdds(throw)            # return odds
            else:
                assert self.bet.come >= self.bet.place[throw]                   # odds off and on, verify new bet is >= old bet
            self.payout.place[throw] = 2 * self.bet.clearPlace(throw)           # pay place bet
            self.bet.moveComeToPlace(throw)

        if self.comeout:
            if throw == 11:                                                     # winner on comeout, otherwise no action
                self.payout.come = 2 * self.bet.clearCome()
            if throw in CRAPS:                                                  # loser on comeout, otherwise no action
                self.bet.clearCome()
            if throw in POINTS:
                self.point = throw                                              # comeout roll, shooter has point
            self.comeout = False





#
# Main  --  Unit Test
#

import unittest

class TestWager(unittest.TestCase):
    def test_wager_init(self):
        w = wager()
        self.assertEqual(w.max_odds, "10x")         # default odds
        self.assertRaises(Exception, wager, "12x")  # odds error check

    def test_wager_comeBet(self):
        w = wager()
        self.assertEqual(w.come, 0) 
        w.comeBet(5)
        self.assertEqual(w.come, 5)
        self.assertRaises(Exception, w.comeBet, 2)     # come bet already established

    def test_wager_placeBet(self):
        w = wager()
        self.assertRaises(Exception, w.placeBet, (5, 1))    # 1 is not a point
        w.placeBet(5, 6)
        self.assertRaises(Exception, w.placeBet, (5, 6))    # 6 already established

    def test_wager_oddsBet(self):
        w = wager()
        self.assertRaises(Exception, w.oddsBet, (5, 1))     # 1 is not a point
        self.assertRaises(Exception, w.oddsBet, (5, 6))     # no place bet on 6
        w.placeBet(5, 6)
        w.oddsBet(5, 6)
        self.assertEqual(w.odds[6], 5)
        self.assertRaises(Exception, w.oddsBet, (5, 6))     # odds bet on 6 already established
        w.odds[6] = 0
        self.assertRaises(Exception, w.oddsBet, (2, 6))     # odds bet on 6 must be multiple of 5
        self.assertRaises(Exception, w.oddsBet, (55, 6))    # odds bet can't exceed 10x place bet

    def test_wager_clearCome(self):
        w = wager()
        self.assertEqual(w.come, 0)
        w.comeBet(1)
        self.assertEqual(w.come, 1)
        amount = w.clearCome()
        self.assertEqual(w.come, 0)
        self.assertEqual(amount, 1)

    def test_wager_moveComeToPlace(self):
        w = wager()
        w.comeBet(1)
        w.moveComeToPlace(4)
        self.assertEqual(w.come, 0)
        self.assertEqual(w.place[4], 1)


class TestTable(unittest.TestCase):
    def test_table_init(self):
        t = table()
        self.assertEqual(t.comeout, True)

    def test_table_roll(self):
        t = table()
        self.assertRaises(Exception, t.roll, 0)     # one die (throw) must be >= 1 and <= 12
        self.assertRaises(Exception, t.roll, 13)
        self.assertRaises(Exception, t.roll, 0, 1)  # two die, each die must be 1<= die <=6
        self.assertRaises(Exception, t.roll, 7, 1)
        self.assertRaises(Exception, t.roll, 1, 0)
        self.assertRaises(Exception, t.roll, 1, 7)

    def test_table_bets(self):
        t = table()
        (come, place, odds) = t.bets()
        self.assertEqual(come, 0)
        self.assertEqual(place, (0,0,0,0,0,0))
        self.assertEqual(odds, (0,0,0,0,0,0))


if __name__ == '__main__':
    unittest.main(verbosity=2)



