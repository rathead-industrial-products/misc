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
        # more data for wager algorithm
        self.running_loss_come = 0
        self.running_loss_dont = 0
        self.running_loss_dont_history = []
        # self.maxComeWager -- set in _makeWagers
        # self.maxDontWager
        self.cumComeWager = []  # set in _makeWagers
        self.cumDontWager = []
        self.f_in_seq = False
        self._makeWagers()
        self.cfit = []      # running win/loss tally at each roll
        self.dfit = []
        self._fitness()     # calculate cfit, dfit


    def _comeWager(self, i):
        MAX_WAGER_COME = 1e6
        if self.roll.prev(idx=i) in (7, 11):    # restart betting sequence
            w = 1
        elif self.roll.prev(idx=i) in CRAP:     # double wager on loss
            w = 2 * self.cwager.prev(idx=i)
        w = 1
        return (min(w, MAX_WAGER_COME))

    def _dontWager(self, i):
        def _consec711(i):
            # return number of consecutive 7-11 rolls starting from i
            n = 0
            while i < len(self.roll):
                if self.roll[i] in (7, 11):
                    n += 1
                    i += 1
                else:
                    break
            return (n)

        # bet everything except a 7-11 to explore return percentage (analytically should be 24.4% 66.7% x 0.2 + 11.11%) (26.46% after 1M rolls)
        # bet the first non-7-11 roll after a 7-11 to explore return percentage (analytically should be 24.4% 66.7% x 0.2 + 11.11%) (26.77% after 1M rolls)
        # bet 1 on a 7-11 roll followed by a non 7-11 roll. bet x on the following non 7-11. (-15.5% x=2, -4.9% x=3, +1.4% x=4, +5.6% x=5,+12.7% x=8 after 1M rolls )
        # bet 1 on a 7-11 followed by either another 7-11 or a non 7-11. escalate bet until the non 7-11 is bet. (-2.7% bets=(1,2,4), +7.8% bets=(1,3,9), +13.0% bets=(1,4,16))
        # bet (bet_seq) on a string of consecutive 7-11s followed by a non 7-11
        # results after 1M rolls:
        # bet_seq = (1,2) -15.5%, (1,3) -4.9%, (1,4) 1.4% (1,5) +5.6%, (1,8) 12.7%
        # ??? from prev algorithm bet_seq = (1,2,4) -2.7%, (1,3,9) +7.8%, (1,4,16) +13.0%
        # bet_seq (ALL)  = (1,2,4) -20.3%, (1,3,9)  -8.4%, (1,4,16) -1.1%, (1,4,20) +1.6%
        # bet_seq (ONLY) = (1,2,4) -27.3%, (1,3,9) -11.9%, (1,4,16) -3.1%, (1,4,20) +1.8%
        # bet_seq (ALL)  = (1,4,20,100) +1.7%
        # bet_seq (ONLY) = (1,4,20,100) +1.9%
        # bet_seq (ALL)  = (1,4,20,100,500) +2.2%
        # bet_seq (ALL)  = (1,4,20,100,500,2500) +2.0%
        # bet_seq (ALL)  = (1,4,20,100,1)  -8.3%         # give up after 4 losses in a row
        # bet_seq (ONLY) = (1,4,20,100,1) -99.0%
        # bet_seq (ALL)  = (1,4,20,100,1,4,20,100)  -8.2%
        # bet_seq (ONLY) = (1,4,20,100,1,4,20,100) -47.4%
        # bet_seq (ALL)  = (1,4,20,1,4,20,1,4,20) -11.6%
        # bet_seq (ALL)  = (1,4,20,100,1,4,20,100,1,4,20,100) -8.3%
        # bet_seq (ALL)  = (1,4,20,100,500,1,4,20,100,500,1,4,20,100,500) -5.8%
        # bet_seq (ALL)  = (1,4,20,100,500,2500,1,4,20,100,500,2500,1,4,20,100,500,2500) -4.3%
        # bet_seq (ALL)  = (1,5,25,1,5,25,1,5,25,1,5,25) -9.75%
        #
        # Now change the nominal bet on everything except the 7-11 series to 1
        # bet_seq (ALL)  = (0,0,0,0) -1.4%
        # bet_seq (ALL)  = (1,4,20,100,1,4,20,100,1,4,20,100) -1.5%
        # bet_seq (ALL)  = (1,4,20,100,500,2500,1,4,20,100,500,2500,1,4,20,100,500,2500) -0.6%
        # bet_seq (ALL)  = (1,4,20,1,4,20,1,4,20,1,4,20) -1.32%

        # nominal bet
        nominal = 0
        w = nominal

        SEQ_LEN_ONLY = False     # only do strings of 7-11's equal to seq_len - 1. Otherwise do all shorter 7-11 sequences as well
        bet_seq = (1,5,25,1,5,25,1,5,25,1,5,25)
        seq_len = len(bet_seq)
        pw = self.dwager.prev(idx=i)    # previous wager on last roll
        if self.f_in_seq:      # currently in a betting sequence
            if self.roll.prev(idx=i) in (7,11):        # last roll was a 7-11, continue with betting sequence
                pw_idx = bet_seq.index(pw)
                w = bet_seq[pw_idx+1]
            else:
                w = nominal        # prev roll was a non 7-11, betting sequence over, restart wager
                self.f_in_seq = False
        if not self.f_in_seq and _consec711(i):  # not currently in a betting sequence but starting a string of 7-11s
            if ((SEQ_LEN_ONLY and _consec711(i) == seq_len - 1) or   # bet only sequences of 7-11 that are exactly seq_Len-1 long
                (not SEQ_LEN_ONLY and _consec711(i) < seq_len)):     # bet all sequences of 7-11 that are seq_len -1 or shorter
                w = bet_seq[0]
                self.f_in_seq = True
        w = 1
        return (w)

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
        # come roll point winnings are recognized when the point is rolled again
        # come roll point losses are recognized when a 7 is rolled
        # and vice-versa for dont winnings/losses
        deferred_come = [0] * 11
        deferred_dont = [0] * 11
        win_loss = 0
        for i, decision in enumerate(self.come):
            r = self.roll[i]
            if r in POINT:  # realize win if point made previously, otherwise defer decision on win/loss
                if deferred_come[r]:
                    win_loss += deferred_come[r]
                deferred_come[r] = self.cwager[i]
            else:   # any roll other than a point is won/lost immediately
                win_loss += decision * self.cwager[i]
            if self.roll[i] == 7:   # realize loss from points still riding
                win_loss -= sum(deferred_come)
                deferred_come = [0] * 11
            self.cfit.append(win_loss)
        win_loss = 0
        for i, decision in enumerate(self.dont):
            r = self.roll[i]
            if r in POINT:  # realize loss if point made previously, otherwise defer decision on win/loss
                if deferred_dont[r]:
                    win_loss -= deferred_dont[r]
                deferred_dont[r] = self.dwager[i]
            else:   # any roll other than a point is won/lost immediately
                win_loss += decision * self.dwager[i]
            if self.roll[i] == 7:   # realize loss from points still riding
                win_loss += sum(deferred_dont)
                deferred_dont = [0] * 11
            self.dfit.append(win_loss)

    def pointsCovered(self, idx):
        # find first 7 in roll_seq before i (or beginning of list)
        # count unique points between that 7 and i
        start = idx
        while start != 0 and self.roll[start-1] != 7:
            start -= 1
        return (len(set(self.roll[start:idx])))
    
    def playerAdvantagePoints(self, span, idx, come_dont="DONT"):
        # for the last span points rolled before idx, return %won - %lost
        outcome = self.dont if come_dont=="DONT" else self.come
        win = 0
        lose = 0
        end = idx
        while idx > 0:
            idx -= 1
            if self.roll[idx] in POINT:
                if outcome[idx] == 1: win  += 1
                else:                 lose += 1
            if win + lose >= span: break
        win_adv = (win - lose)/(win + lose + 0.001)     # in case win + lose == 0
        return (win_adv)
    
    def playerAdvMovingAvg(self, span, come_dont="DONT"):
        mavg = []
        for i in range(len(self.roll)):
            mavg.append(self.playerAdvantagePoints(span, i))
        return (mavg)
            



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
