#
#
#


TRIAL_LEN   = 10

import roll, wager
from wager import wager

roll.seed()
trial = [roll.throw() for i in range(TRIAL_LEN)]

for t in trial:
    w = wager()
    for u in wager.unresolved:
        u.roll(t)

print (trial)
for h in wager.history:
    print (h.point, h.resolution, h.win)
print ("------")
for u in wager.unresolved:
    print (u.point, u.resolution, u.win)
    
