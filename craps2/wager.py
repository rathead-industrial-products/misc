#
# Given a sequence of rolls with outcomes ([roll, come w/l, dont come w/l/d], [..], ..)
# calculate a come and don't come wager for each roll and determine the overall win/loss
# of the entire sequence.
#

CRAP        = (2, 3, 12)
CRAP_BAR_12 = (2, 3)
POINT       = (4, 5, 6, 8, 9, 10)

class wager():
    def __init__(self, roll_seq, come_outcome, dont_outcome, come_wager, dont_wager):
        self.roll = roll_seq
        self.come = come_outcome
        self.dont = dont_outcome
        self.cwager = come_wager
        self.dwager = dont_wager
        # self.maxComeWager -- set in _makeWagers
        # self.maxDontWager
        self.cumComeWager = []  # set in _makeWagers
        self.cumDontWager = []
        self._makeWagers()
        self.cfit = []      # running win/loss tally at each roll
        self.dfit = []
        self._fitness()     # calculate cfit, dfit

    def _comeWager(self, i):
        MAX_WAGER_COME = 1024
        if self.roll.prev(idx=i) in (7, 11):    # restart betting sequence
            w = 1
        elif self.roll.prev(idx=i) in CRAP:     # double wager on loss
            w = 2 * self.cwager.prev(idx=i)
        else: w = 2 * self.cwager.prev(idx=i)
        return (min(w, MAX_WAGER_COME))

    def _dontWager(self, i):
        MAX_WAGER_DONT = 100000
        w = 1
        return (min(w, MAX_WAGER_DONT))

    def _makeWagers(self):
        # cwager & dwager are empty xlists
        cum_come = 0
        cum_dont = 0
        for i, _ in enumerate(self.roll):
            cw = self._comeWager(i)     # compute come wager based on history up to i
            self.cwager.append(cw)
            cum_come += cw
            self.cumComeWager.append(cum_come)
            dw = self._dontWager(i)     # dont come wager
            self.dwager.append(dw)
            cum_dont += dw
            self.cumDontWager.append(cum_dont)  
        self.maxComeWager = max(self.cwager)
        self.maxDontWager = max(self.dwager)
        return ()
            
    def _fitness(self):
        # create a running account of win/loss at every roll
        win_loss = 0
        for i, item in enumerate(self.come):
            win_loss += item * self.cwager[i]
            self.cfit.append(win_loss)
        win_loss = 0
        for i, item in enumerate(self.dont):
            win_loss += item * self.dwager[i]
            self.dfit.append(win_loss)

    def maxBetCome(self):
        return (self.maxComeWager)
    
    def maxBetDont(self):
        return (self.maxDontWager)
    
    def fitnessArrayCome(self):
        return (self.cfit)
    
    def fitnessArrayDont(self):
        return (self.dfit)
    
    def fitnessCome(self):
        return (self.cfit[-1])
    
    def fitnessDont(self):
        return (self.dfit[-1])

    def totalBetCome(self):
        return (self.cumComeWager[-1])

    def totalBetDont(self):
        return (self.cumDontWager[-1])
