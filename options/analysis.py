
"""
Analyze behavior of RMBS call options

All times are Eastern in datetime naive format

"""
#
# Database Record
#
# Raw data from Yahoo Finance
# 'Contract Name'       : str       'RMBS240419C00055000'
# 'Last Trade Date'     : str       '2024-03-19 9:55AM EDT'
# 'Strike'              : float     52.5
# 'Last Price''         : float     20.82
# 'Bid''                : float     19.7
# 'Ask''                : float     24.5
# 'Change'              : float     0.0
# '% Change'            : str       '-'
# 'Volume'              : str       '-'
# 'Open Interest'       : int       8
# 'Implied Volatility'  : str       '106.64%'
#
# Add when quote fetched
# 'type'                : str       'PUT' | 'CALL'
# 'time'                : str       '2024-03-28 15:55:53'
# 'underlying'          : float     61.810001373291016
#


import datetime
import json
import os
from   fetch_option_quotes import *

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

# return the file as a list of quotes
def recall(fname):
    fname = os.path.join(DATA_DIR, fname)
    quotes = []
    with open(fname, 'r') as f:
        for line in f:
            quotes.append(json.loads(line))
    return (quotes)

# return decimal days until expiration where
# the decimal portion is hours/(6.5 hours in a trading day)
def timeToExpiration(quote : dict):
    quote_dt = destringifyDT(quote['time'])             # time of quote
    market_close = quote_dt.replace(hour=16, minute=00) # 4:30 day of quote
    print (quote_dt)
    print (market_close)
    sec_to_close = (market_close - quote_dt).seconds    # seconds from quote until 4:30
    exp_dt = expiration_dt(quote['Contract Name'])
    print (quote_dt)
    print (exp_dt)
    days_to_close = (exp_dt - quote_dt).days
    dec_days = (sec_to_close / 3600 / 6.5)
    print (days_to_close)
    print (dec_days)
    return (days_to_close + dec_days)

# return (TimeValue(bid), TimeValue(ask))
def timeValue(quote : dict):
    if quote['Strike'] < quote['underlying']: 
        if quote['type'] == 'PUT':  # out of the money
            tv = (quote['Bid'], quote['Ask'])
        else: # 'CALL'              # in the money
            tv = (quote['Bid'] - (quote['underlying'] - quote['Strike']), quote['Ask'] - (quote['underlying'] - quote['Strike']))
    else:
        if quote['type'] == 'CALL':  # out of the money
            tv = (quote['Bid'], quote['Ask'])
        else: # 'PUT'              # in the money
            tv = (quote['Bid'] - (quote['underlying'] - quote['Strike']), quote['Ask'] - (quote['underlying'] - quote['Strike']))
    tv = [round(x, 2) for x in tv]
    return (tv)

# return how far out of the money an option is
# this can be a positive or negative number
def outOfTheMoney(quote : dict):
    oom = quote['Strike'] - quote['underlying']
    oom = round(oom, 2)
    return (oom)



quotes = recall("240517.json")
for q in quotes[-5:]:
    print (q)
    print (timeValue(q), outOfTheMoney(q), timeToExpiration(q))
    print ()
