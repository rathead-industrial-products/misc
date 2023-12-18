#
# Given a sequence of rolls with outcomes ([roll, come w/l, dont come w/l/d], [..], ..)
# calculate a come and don't come wager for each roll and determine the overall win/loss
# of the entire sequence.
#

class wager():
    def __init__(self, roll_seq, come_outcome, dont_outcome, come_wager, dont_wager):
        self.roll = roll_seq
        self.come = come_outcome
        self.dont = dont_outcome
        self.cwager = come_wager
        self.dwager = dont_wager
        # self.maxComeWager -- set in _makeWagers
        # self.maxDontWager
        self._makeWagers()
        self.cfit = []      # running win/loss tally at each roll
        self.dfit = []
        self._fitness()     # calculate cfit, dfit

    def _comeWager(cwager, i):
        pass

    def _dontWager(dwager, i):
        pass

    def _makeWagers(self, cwager, dwager):
        # cwager & dwager are empty xlists
        for i, _ in enumerate(self.roll):
            cwager.append(self._comeWager(cwager, i))   # compute come wager based on history up to i
            dwager.append(self._dontWager(dwager, i))   # don't come wager
        self.maxComeWager = max(cwager)
        self.maxDontWager = max(dwager)
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
