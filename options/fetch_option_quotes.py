
"""
Create a json database from example csv files in /db

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
from yahoo_fin import stock_info, options

TICKER = 'RMBS'
DATA_DIR = "/home/mitchell/stock_options/data"

#
# File Management
#
# Database records are individual lines in a json file
# Files are organized by expiration date, one per month
#

# str in the form 'YYMMDD'
def datetimeToStr(dt):
    s = dt.strftime("%y%m%d")
    return (s)

# str in the form 'YYMMDD'
def strToDatetime(s):
    dt = datetime.datetime.strptime(s, '%y%m%d')
    return (dt)

# convert time in the form '2024-03-28 15:55:53' to 'YYMMDD'
def timeToYYMMDD(time):
    s = time[2:4] + time[5:7] + time[8:10]
    return (s)

# extract the expiration date in the form 'YYMMDD' from the contract name
def contractExpiration(contract_name):
    exp = contract_name[:10][4:]
    return (exp)

# store a single quote in a file arranged by expiration date
# files are named 'YYMMDD.json' where 'YYMMDD' is an option expiration Friday
def store(quote: dict):
    fname = contractExpiration(quote['Contract Name']) + ".json"
    fname = os.path.join(DATA_DIR, fname)
    with open(fname, 'a') as f:
        json.dump(quote, f)
        f.write('\n')

# return the file as a list of quotes
def recall(fname):
    fname = os.path.join(DATA_DIR, fname)
    quotes = []
    with open(fname, 'r') as f:
        for line in f:
            quotes.append(json.loads(line))
    return (quotes)


exp_dates = options.get_expiration_dates(TICKER)
for ex in exp_dates:
    all = options.get_options_chain(TICKER, ex)
    calls = all['calls']
    puts = all['puts']
    underlying = stock_info.get_live_price(TICKER)
    time = (datetime.datetime.now() - datetime.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
    for _, row in calls.iterrows():
        record = dict(row.to_dict(), **{'type': 'CALL', 'time': time, 'underlying': underlying})
        store(record)
    for _, row in puts.iterrows():
        record = dict(row.to_dict(), **{'type': 'PUT', 'time': time, 'underlying': underlying})
        store(record)



