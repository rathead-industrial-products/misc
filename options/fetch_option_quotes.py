
"""
Create a json database from example csv files in /db

Use as a function library for analysis programs

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
import os.path
# suppress FutureWarnings from pandas
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from   yahoo_fin import stock_info, options
import yfinance as yf

TICKER = 'RMBS'
ACTIVE = ('TSLA', 'AAPL', 'F')
DATA_DIR = "/home/mitchell/stock_options/data"

#
# File Management
#
# Database records are individual lines in a json file
# Files are organized by expiration date, one per month
#

# return a datetime object with the current East Coast time
def nowET():
    et = datetime.datetime.now() + datetime.timedelta(hours=3)
    return (et)

# convert a datetime to a string of the form '2024-03-28 15:55:53'
def stringifyDT(dt):
    s = dt.strftime('%Y-%m-%d %H:%M:%S')
    return (s)
    
# convert a string of the form '2024-03-28 15:55:53' to a datetime
def destringifyDT(s):
    dt = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    return (dt)

# convert a contract name to an expiration date in the form a datetime
def expiration_dt(contract_name):
    yymmdd = contractExpiration(contract_name)
    s = "20%s-%s-%s 00:00:00" % (yymmdd[:2], yymmdd[2:4], yymmdd[4:])
    dt = destringifyDT(s)
    return (dt)

# extract the expiration date in the form 'YYMMDD' from the contract name
def contractExpiration(contract_name):
    exp = contract_name[:10][4:]
    return (exp)

# return true if the market is open
def marketOpen():
    # see if any of very actively traded stocks have traded in the last minute
    # if one or more have traded, infer that the market is open
    # stock_info.get_market_status()    # should return (“PRE”), (“OPEN”), (“POST”), or (“CLOSED”) but is broken
    # use yfinance to get a current quote as a pandas dataframe with pandas timestamps
    open_f = False
    for ticker in ACTIVE:
        last_trade_dt = list(yf.Ticker(ticker).history(period="1d").to_dict()['Volume'].keys())[0].to_pydatetime()
        last_trade_dt_naive = last_trade_dt.replace(tzinfo=None)    # to compare with naive nowET
        if nowET() < last_trade_dt_naive + datetime.timedelta(minutes=1):
            open_f = True
    return (open_f)

# store a single quote in a file arranged by expiration date
# files are named 'YYMMDD.json' where 'YYMMDD' is an option
# expiration date extracted from the contract name
def store(quote: dict):
    exp = contract_name[:10][4:]
    fname = exp + ".json"
    fname = os.path.join(DATA_DIR, fname)
    with open(fname, 'a') as f:
        json.dump(quote, f)
        f.write('\n')



#
# Main
#
# Fetch Options Quotes
#

if __name__ == "__main__":

    if not marketOpen():
        print ("fetch_option_quotes.py - Market Closed")
    # exit()        ** Until marketOpen is verified **
    else:
        print ("fetch_option_quotes.py - Market Open")


    exp_dates = options.get_expiration_dates(TICKER)
    for ex in exp_dates:
        all = options.get_options_chain(TICKER, ex)
    calls = all['calls']
    puts = all['puts']
    underlying = stock_info.get_live_price(TICKER)
    time = nowET().strftime('%Y-%m-%d %H:%M:%S')
    for _, row in calls.iterrows():
        record = dict(row.to_dict(), **{'type': 'CALL', 'time': time, 'underlying': underlying})
        store(record)
    for _, row in puts.iterrows():
        record = dict(row.to_dict(), **{'type': 'PUT', 'time': time, 'underlying': underlying})
        store(record)



