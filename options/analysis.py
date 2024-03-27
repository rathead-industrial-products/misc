
"""
Analyze behavior of RMBS call options

All times are Eastern in datetime naive format

"""

# Database contents
# quote : dict = {
# 'type;       : string     ('PUT' | 'CALL')
# 'time'       : datetime.datetime
# 'strike'     : float
# 'expiration' : datetime.date
# 'underlying' : float
# 'bid'        : float
# 'ask'        : float
# }

import datetime

# Market
MARKET_OPEN   = datetime.time(09, 30)
MARKET_CLOSE  = datetime.time(16, 30)
MARKET_SAMPLE = [datetime.time(dt) for dt in ((09, 35), (11, 00), (13, 00), (15, 00), (16, 25))]



#
# Analyze
#
'''
Time until expiration (ttx) in (days, hours, mins), where hours, min is the time until the market closes on this day
     e.g. at 1:15 on Wednesday before expiriation, ttx = (2, 3, 15)

Time value (tv) is bid/ask quote minus the underlying stock value if in the money, else it is the bid/ask quote

Out of the money (oom) is the strike minus the underlying stock value

Plot:
tv vs ttx vs oom (probably most interesting near expiration)
d(tv) vs ttx vx oom
tv vs oom vs ttx


'''

# return (days, hours, minutes) until expiration
def timeUntilExpiration(quote : dict):
    exp = datetime.datetime.combine(quote['expiration'], MARKET_CLOSE)
    ttx = exp - quote['time']
    return (ttx.days, ttx.hours, ttx.mins)

# return (TimeValue(bid), TimeValue(ask))
def timeValue(quote : dict):
    if quote['strike'] < quote['underlying']: 
        if quote['type'] == 'PUT':  # out of the money
            tv = (quote['bid'], quote['ask'])
        else: # 'CALL'              # in the money
            tv = (quote['bid'] - quote['underlying'], quote['ask'] - quote['underlying'])
    else:
        if quote['type'] == 'CALL':  # out of the money
            tv = (quote['bid'], quote['ask'])
        else: # 'PUT'              # in the money
            tv = (quote['bid'] - quote['underlying'], quote['ask'] - quote['underlying'])
    tv = [round(x, 2) for x in tv]
    return (tv)

# return how far out of the money an option is
# this can be a positive or negative number
def outOfTheMoney(quote : dict):
    oom = quote['strike'] - quote['underlying']
    oom = round(oom, 2)
    return (oom)





