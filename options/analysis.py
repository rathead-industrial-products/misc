
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
# 'time value ask'      : float     1.70    # option value minus intrinsic value (if any)
# 'spread'              ; float     0.35    # ask - bid
# 'dist from underlying': float     22.0    # strike price minus underlying stock price (can be pos or neg)
#


import datetime
import json
import os
import pandas as pd

HOST = 'SERVER'     # SERVER | MAC
HOST = 'MAC'
DATA_DIR = "/home/mitchell/stock_options/data"
DISPLAY_COLUMNS = ['Contract Name', 'Strike', 'Bid', 'time value bid', 'Ask', 'time value ask', 'dist from underlying']

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


# return all json files in the given directory as a list of quotes
def recall(dir):
    fnames = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    json_fnames = [os.path.join(dir, f) for f in fnames if '.json' in f]
    quotes = []
    for jf in json_fnames:
        with open(jf, 'r') as f:
            for line in f:
                quote = json.loads(line)
                try:
                    quote['Strike'] = float(quote['Strike'])
                    quote['Last Price'] = float(quote['Last Price'])             
                    quote['Bid'] = float(quote['Bid'])
                    quote['Ask'] = float(quote['Ask'])
                    quote['Change'] = float(quote['Change'])
                    quote['Open Interest'] = int(quote['Open Interest'].replace(',' , ''))
                    quote['underlying'] = float(quote['underlying'])
                    quotes.append(quote)
                except:
                    pass    # filters '-' in fields that should have valid values
    return (quotes)


# return decimal days until expiration where
# the decimal portion is hours/(6.5 hours in a trading day)
def timeToExpiration(quote : dict):
    quote_dt = destringifyDT(quote['time'])             # time of quote
    market_close = quote_dt.replace(hour=16, minute=00) # 4:00 day of quote
    sec_to_close = (market_close - quote_dt).seconds    # seconds from quote until 4:00
    exp_dt = expiration_dt(quote['Contract Name']).replace(hour=23) # midnight-ish on expiration date
    days_to_close = (exp_dt - quote_dt).days
    dec_days = (sec_to_close / 3600 / 6.5)
    ttx = days_to_close + dec_days
    ttx = round(ttx, 1)
    return (days_to_close + dec_days)

# return (TimeValue(bid), TimeValue(ask))
def timeValue(quote : dict):
    if quote['Strike'] < quote['underlying']: 
        if quote['type'] == 'PUT':  # out of the money
            tv = (quote['Bid'], quote['Ask'])
        else: # 'CALL'              # in the money
            tv = (quote['Bid'] + quote['dist from underlying'], quote['Ask'] + quote['dist from underlying'])
    else:
        if quote['type'] == 'CALL':  # out of the money
            tv = (quote['Bid'], quote['Ask'])
        else: # 'PUT'              # in the money
            tv = (quote['Bid'] - quote['dist from underlying'], quote['Ask'] - quote['dist from underlying'])
    tv = [round(x, 2) for x in tv]
    return (tv)

# return how far the strike price is from the underlying stock price
# this can be a positive or negative number
def distFromUnderlying(quote : dict):
    dfu = quote['Strike'] - quote['underlying']
    dfu = round(dfu, 1)
    return (dfu)

# return the contract type 'PUT' or 'CALL'
def contractType(quote: dict):
    try:
        if quote['Contract Name'][10] == 'C': return ('CALL')
        if quote['Contract Name'][10] == 'P': return ('PUT')
    except:
        print (quote)
    
    assert False, "Indeterminate contract type (not PUT or CALL)"

# add some parameters derived from the raw data to the quote
def addDerivedValues(quote: dict):
    quote['type'] = contractType(quote)
    quote['time to expiration'] = timeToExpiration(quote)
    quote['dist from underlying'] = distFromUnderlying(quote)
    tv = timeValue(quote)
    quote['time value bid'] = tv[0]
    quote['time value ask'] = tv[1]
    quote['spread'] = tv[1] - tv[0]

# return True if the time value is negative. [How can that ever happen??]
def negTimeValue(quote: dict):
    if quote['time value bid'] < 0 or quote['time value ask'] < 0: return (True)
    return (False)

  


if __name__ == "__main__":
    if HOST == 'SERVER':
        quotes = recall(DATA_DIR)      # get raw quote data
    else:
        quotes = recall('.')           # set working directory before running

    recent = [q for q in quotes if q['Contract Name'].startswith("RMBS240621")]
    #quotes = recent

    for quote in quotes:
        addDerivedValues(quote)              # update quote with derived values
    # filter suspicious quotes
    # bid or ask == 0
    #ba_zero = [q for q in quotes if not q['Bid'] == 0.0 or q['Ask'] == 0.0]
    # postive time value
    #neg_tv = [q for q in ba_zero if q['time value bid'] > 0 and q['time value ask'] > 0]
    #recent = [q for q in neg_tv if q['Contract Name'].startswith("RMBS240517")]
    #tv_high = [q for q in recent if q['time value bid'] > 20]
    #print (len(quotes), len(ba_zero), len(neg_tv), len(tv_high))

    
    calls  = [q for q in quotes if 'C' in q['Contract Name']]
    pos_tv = [q for q in calls if q['time value bid'] > 0]
    spread = [q for q in calls if q['spread'] < 5 and q['spread'] >= 0]
    dist   = [q for q in pos_tv if abs(q['dist from underlying']) <= 1]
    ttx    = [q for q in dist if q['time to expiration'] > 0 and q['time to expiration'] <= 30]
        
    #df = df[DISPLAY_COLUMNS]
    #print (df.sort_values(['time value bid'], ascending=False).head(10))


    if HOST == 'MAC':
        import matplotlib.pyplot as plt
        df = pd.DataFrame(ttx)
        #fig = plt.figure()
        #ax = fig.add_subplot(projection='3d')
        #ax.scatter(df["dist from underlying"], df["time to expiration"], df["spread"])
        #ax.set_xlabel('dist from underlying')
        #ax.set_ylabel('time to expiration')
        #ax.set_zlabel('spread')
        #df.plot(x="time to expiration", y="time value bid", kind="scatter")
        df.plot(x="time to expiration", y="time value bid", z="spread", kind="scatter", projection='3d')
        #fig, ax = plt.subplots()
        #ax.hist(df["time to expiration"])
        plt.show()



    #
    # sort on spread
    #       does spread correlate with any other parmeters?
    #
    # sort on time_value_bid
    #       what is the best contract to sell?
    #



