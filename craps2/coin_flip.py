#
# 
#

import random, itertools
import matplotlib.pyplot as plt
from collections import Counter


N_FLIPS = 10000000


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



# 0 = loss, 1 = win
loss = 0
bank = 0
hist_coin  = []
hist_wager = []
hist_loss  = []
hist_bank  = []
random.seed(1)

# accumulate losses, wager 1/4 of recent losses
# When a win offsets recent losses, continue betting
# the previous wager until losses are recovered

MAX_WAGER = 1000

def circuitBreaker(coin_hist):
    # if there have been five losses in a row anywhere in the last 6 rolls, stop betting
    consec = 5
    roll_len = 6
    if len(coin_hist) >= roll_len:
        lastseq = coin_hist[-roll_len:]
        consec_zeros = max([len(list(g)) if k==0 else 0 for k, g in itertools.groupby(lastseq)])
        if consec_zeros >= consec:
            return (True)
        return (False)

for i in range(N_FLIPS):
    hist_coin.append(random.randint(0,1))

for i, coin in enumerate(hist_coin):
    if loss < 0:
        if circuitBreaker(hist_coin):
            wager = 0       # long string of 0's, take a break for awhile
        elif coin_prev == 0:      # added to loss, recalculate wager
            wager = -loss/4
            last_lost_wager = wager
        else:               # maintain previous wager until loss is recovered
            wager = last_lost_wager
    else:
        wager = 16              # default wager
#    wager = min(wager, MAX_WAGER)

    if coin == 1:       # win
        loss += wager
        if loss > 0: loss = 0
        bank += wager
    else:               # loss
        loss -= wager
        bank -= wager
    coin_prev = coin
    hist_wager.append(int(wager))
    hist_loss.append(int(loss))
    hist_bank.append(int(bank))
#    print (coin, wager, loss, bank)

# create list of run lengths of 0/1, separated by 1/0
runs_zero = [len(list(g)) for k, g in itertools.groupby(hist_coin) if k==0]
runs_one  = [len(list(g)) for k, g in itertools.groupby(hist_coin) if k==1]

'''
bins = max(max(runs_zero), max(runs_one))
plt.hist([runs_zero, runs_one], bins=bins, label=['0', '1'])
plt.legend(loc='upper right')
plt.show()
'''

# create histogram of run length vs. occurance
h_dict = Counter(runs_zero)
h = [0]*(max(h_dict.keys())+1)
for k,v in h_dict.items():
    h[k]=v
norm = [i*item for i, item in enumerate(h)]
normpct = [int(100*round(n/N_FLIPS, 2)) for n in norm]
print (h)
print (norm)
print (normpct)


hist_bet = hist_coin[:-1]       # place a unit bet after every '1'. This is the same as the coin flip history shifted right one position
hist_bet.insert(0, 0)
win1 = 0
win0 = 0
hist_win1 = []
hist_win0 = []
for i, b in enumerate(hist_bet):
    if b: 
        if hist_coin[i]: win1 += 1
        else: win1 -= 1
    else:
        if not hist_coin[i]: win0 += 1
        else: win0 -= 1    
    hist_win1.append(win1)
    hist_win0.append(win0)  
print (win1, win0)
_plotSeries(win1=hist_win1, win0=hist_win0)

'''
start=0; end=None
start=7900; end=8200
if end and (end-start<=20):
    _printList (hist_coin[start:end])
    _printList (hist_wager[start:end])
    _printList (hist_loss[start:end])
    _printList (hist_bank[start:end])

print ("max bet", max(hist_wager))
_plotSeries(wager=hist_wager[start:end], loss=hist_loss[start:end], bank=hist_bank[start:end])
'''
