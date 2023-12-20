#
# 
#

import random
import matplotlib.pyplot as plt


N_FLIPS = 1000000


def _plotSeries(y1, y2=[], label1='', label2=''):
    fig, ax = plt.subplots()
    ax.plot(y1, label=label1)
    if y2:
        ax.plot(y2, label=label2)
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

MAX_WAGER = 100

for i in range(N_FLIPS):
    if loss < 0:
        if coin_prev == 0:      # added to loss, recalculate wager
            wager = -loss/4
            if wager > MAX_WAGER:
                wager = 16      # reset, start over
                loss = 0
        else: pass              # maintain previous wager until loss is recovered
    else:
        wager = 16              # default wager
#    wager = min(wager, MAX_WAGER)
    coin = random.randint(0,1)
    if coin == 1:       # win
        loss += wager
        if loss > 0: loss = 0
        bank += wager
    else:               # loss
        loss -= wager
        bank -= wager
    coin_prev = coin
    hist_coin.append(coin)
    hist_wager.append(int(wager))
    hist_loss.append(int(loss))
    hist_bank.append(int(bank))
#    print (coin, wager, loss, bank)

#_printList (hist_coin[1675:1690])
#_printList (hist_wager[1675:1690])
#_printList (hist_loss[1675:1690])
#_printList (hist_bank[1675:1690])
print ("max bet", max(hist_wager))
_plotSeries(hist_loss, hist_bank, 'loss', 'bank')

