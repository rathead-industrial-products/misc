#
# 
#

import roll, random, itertools
import matplotlib.pyplot as plt
from collections import Counter


N_FLIPS = 10000


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
hist_bank  = []
random.seed(1)

# accumulate losses, wager 1/4 of recent losses
# When a win offsets recent losses, continue betting
# the previous wager until losses are recovered

# starting with a unit bet, bet 4 times or until 4 ones in a row
# after 4 bets, increase bet by one
# repeat until 4 ones in a row or bet reaches 7 (don't bet 7)
# after a one (win), leave bet + win riding until 4 wins in a row

MAX_WAGER = 1000

def circuitBreaker(coin_hist):
    return (False)
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

wager       = 1
zero_wager  = 1
zeros_bet   = 0
consec_ones = 0
for i, coin in enumerate(hist_coin):
    if coin == 1:       # win
        bank += wager
    else:               # loss
        bank -= wager
    last_wager = wager

    hist_wager.append(int(wager))
    hist_bank.append(int(bank))

    # nominal wager after any zeros is 1111,2222,...,6666
    # after 4 consecutive ones, reset wager sequence to 1111
    # on any one, double wager until either a zero or 4 ones in a row
    four_ones = not i < 3 and hist_coin[i-3:i+1] == [1,1,1,1]
    if coin == 0:
        consec_ones = 0
        if zeros_bet >= 4:
            zero_wager = zero_wager + 1 if zero_wager != 6 else 1
            zeros_bet = 0
        wager = zero_wager
        zeros_bet += 1
    else:   # coin == 1
        consec_ones += 1
        if consec_ones < 4:
            wager *= 2  # wager + win riding
        else:   # won 4 times, reset wager
            wager = 1
            zero_wager = 1


#    print (coin, wager, bank)


'''
# create list of run lengths of 0/1, separated by 1/0
runs_zero = [len(list(g)) for k, g in itertools.groupby(hist_coin) if k==0]
runs_one  = [len(list(g)) for k, g in itertools.groupby(hist_coin) if k==1]

# make a list of number of flips (of head or tail) between runs of 4 or more heads
# for each span between runs of heads, compute the pct of heads
run_groups = itertools.groupby(hist_coin)
group1_spacing = []
frac_ones = []
span = 0
ones = 0
zeros = 0
for k, g in run_groups:
    len_g = len(list(g))
    if k==1 and len_g >= 4:
        group1_spacing.append(span)
        frac_ones.append(ones/(ones+zeros))
        span = 0
        ones = 0
        zeros = 0
    else:
        span += len_g
        if k==1: ones += len_g
        else:    zeros += len_g
# calculate absolute number of 0s in each span that we must survive
abs0 = []
for i, span in enumerate(group1_spacing):
    abs0.append(int(span * (1 - frac_ones[i])))

#print (hist_coin)
#print (group1_spacing)
#print (abs0)
print (roll.meanMedianModeStdDev(abs0))


bins = max(max(runs_zero), max(runs_one))
plt.hist([runs_zero, runs_one], bins=bins, label=['0', '1'])
plt.legend(loc='upper right')
plt.show()


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


'''
start=0; end=None
start=5620; end=5640
if end and (end-start<=20):
    _printList (hist_coin[start:end])
    _printList (hist_wager[start:end])
    _printList (hist_bank[start:end])


print ("max bet", max(hist_wager))
_plotSeries(coin=hist_coin[start:end], wager=hist_wager[start:end], bank=hist_bank[start:end])
