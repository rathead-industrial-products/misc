
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
# Added when quote fetched
# 'time'                : str       '2024-03-28 15:55:53'   # time when quote was served
# 'underlying'          : float     61.810001373291016      # underlying stock price at 'time'
#
# Derived
# 'type'                : str       'PUT' | 'CALL'
# 'time to expiration'  : float     4.23    # time to expiration where .days = fraction of 6.5 hour day left today
# 'time value bid'      : float     1.35    # option value minus intrinsic value (if any)
# 'time value ask'      : float     1.35    # option value minus intrinsic value (if any)
# 'dist from underlying': float     22.0    # strike price minus underlying stock price (can be pos or neg)
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

"4/18/2024 2:56 PM"

# convert a contract name in the form of 'RMBS240419C00040000'
# to an expiration date in the form of a datetime
def expiration_dt(contract_name):
    exp = contract_name[:10][4:]
    exp_dt = datetime.datetime.strptime(exp, '%y%m%d')
    return (exp_dt)
    

# convert a string of the form '4/1/2024 2:56 PM' to a datetime
def destringifyDT(s):
    if s[1]  == '/': s = '0' + s                # convert month to two digits
    if s[4]  == '/': s = s[:3] + '0' + s[3:]    # convert day to two digits
    if s[12] == ':': s = s[:11] + '0' + s[11:]  # convert hour to two digits 
    dt = datetime.datetime.strptime(s, '%m/%d/%Y %I:%M %p')
    return (dt)


# return the file as a list of quotes
def recall(fname):
    #fname = os.path.join(DATA_DIR, fname)
    quotes = []
    with open(fname, 'r') as f:
        for line in f:
            quote = json.loads(line)
            quote['Strike'] = float(quote['Strike'])
            quote['Last Price'] = float(quote['Last Price'])
            quote['Bid'] = float(quote['Bid'])
            quote['Ask'] = float(quote['Ask'])
            quote['Change'] = float(quote['Change'])
            quote['Open Interest'] = int(quote['Open Interest'].replace(',' , ''))
            quote['underlying'] = float(quote['underlying'])
            quotes.append(quote)
    return (quotes)


# return decimal days until expiration where
# the decimal portion is hours/(6.5 hours in a trading day)
def timeToExpiration(quote : dict):
    quote_dt = destringifyDT(quote['time'])             # time of quote
    market_close = quote_dt.replace(hour=16, minute=00) # 4:00 day of quote
    print (quote_dt)
    print (market_close)
    sec_to_close = (market_close - quote_dt).seconds    # seconds from quote until 4:00
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

# return how far the strike price is from the underlying stock price
# this can be a positive or negative number
def distFromUnderlying(quote : dict):
    dfu = quote['Strike'] - quote['underlying']
    dfu = round(dfu, 2)
    return (dfu)

# return the contract type 'PUT' or 'CALL'
def contractType(quote: dict):
    if quote['Contract Name'][10] == 'C': return ('CALL')
    if quote['Contract Name'][10] == 'P': return ('PUT')
    assert False, "Indeterminate contract type (not PUT or CALL)"

# return the parameters derived from the raw data
def derived(quote: dict):
    quote['type'] = contractType(quote)
    quote['time to expiration'] = timeToExpiration(quote)
    tv = timeValue(quote)
    quote['time value bid'] = tv[0]
    quote['time value ask'] = tv[1]
    quote['dist from underlying'] = distFromUnderlying(quote)

'''
quotes = recall("240517.json")
for q in quotes[-5:]:
    print (q)
    print (timeValue(q), distFromUnderlying(q), timeToExpiration(q))
    print ()
    '''


if __name__ == "__main__":
    fname = 'RMBS240517.json'
    quotes = recall(fname)      # get raw quote data
    for quote in quotes[:1]:
        print (quote)
        derived(quote)              # update quote with derived values
        print (quote)
    # put quotes into panda datastore
    # do some analysis
