
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
# Added when quote fetched
# 'type'                : str       'PUT' | 'CALL'
# 'time'                : str       '2024-03-28 15:55:53'
# 'underlying'          : float     61.810001373291016
#


import datetime
import json
from yahoo_fin import stock_info, options

TICKER = 'RMBS'

#
# File Management
#
# Database records are individual lines in a json file
# Files are organized by expiration date, one per month
#

def datetimeToStr(dt):
    s = dt.strftime("%y%m%d")
    return (s)

def strToDatetime(s):
    dt = datetime.datetime.strptime(s, '%y%m%d')
    return (dt)

# Return the next option expiration Friday (in the form 'YYMMDD') after date (in the form 'YYMMDD')
# date is in the form 'YYMMDD'
def nextExpirationDate(date: str):
    dt = strToDatetime(date)
    # The 15th is the earliest third day in the month
    third = datetime.date(date.year, date.month, 15)
    third_friday = third.replace(day=(15 + ((4 - third.weekday()) % 7))) # Friday is weekday 4
    if dt > third_friday:
        # find next month's expiration date
        next_month = (date.replace(day=1) + datetime.timedelta(days=31)).replace(day=1)    # first of next month
        third_friday = nextExpirationDate(next_month)
    return (third_friday.strftime('%y%m%d'))

# extract the expiration date in the form 'YYMMDD' from the contract name
def contractExpiration(contract_name):
    exp = contract_name[:10][4:]
    return (exp)

# store a single quote in a file arranged by expiration date
# files are named 'YYMMDD.json' where 'YYMMDD' is an option expiration Friday
def store(quote):
    fname = nextExpirationDate(quote['time']) + ".json"
    with open(fname, 'a') as f:
        dts = datetimeToStr(quote['time'])
        datetimeFromStr(dts)
        quote['time'] = datetimeToStr(quote['time'])    # allow it to be json serializable
        quote['expiration'] = datetimeToStr(quote['expiration'])
        json.dump(quote, f)
        f.write('\n')

# return the entire file of the next expiration date as a list of quotes
def recall(date):
    date = date.date()  # convert from datetime to date
    fname = nextExpirationDate(date).strftime("%y%m%d")
    quotes = []
    with open(fname, 'r') as f:
        for line in f:
            quotes.append(json.loads(line))
    for q in quotes:
        q['time'] = datetimeFromStr(q['time'])
        q['expiration'] = datetimeFromStr(q['expiration'])
    return (quotes)


def addDictFields(type, time, underlying):
    d = {}
    d['type'] = type
    d['time'] = time
    d['underlying'] = underlying
    return (d)


exp_dates = options.get_expiration_dates(TICKER)
for ex in exp_dates:
    calls = options.get_calls(TICKER, ex)
    puts  = options.get_puts(TICKER, ex)
    underlying = stock_info.get_live_price(TICKER)
    fetch_et = datetimeToStr(datetime.datetime.now() - datetime.timedelta(hours=3))
    for _, row in calls.iterrows():
        record = dict(row.to_dict(), **addDictFields('CALL', fetch_et, underlying))
        print (record)
        store(record)
    for p in puts:
        pass
        #record = dict(p.to_dict, **addDictFields('PUT', fetch_time, underlying))
        #store(record)



