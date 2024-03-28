
"""
Create a json database from example csv files in /db

"""

#
# Raw data from Yahoo Finance
# Contract Name
# 'Last Trade Date'     : str
# 'Strike'              : str
# 'Last Price''         : float
# 'Bid''                : float
# 'Ask''                : float
# 'Change'              : float
# '% Change'            : str
# 'Volume'              : str
# 'Open Interest'       : int
# 'Implied Volatility'  : str
#


# Database contents
# quote : dict = {
# 'type;       : string     ('PUT' | 'CALL')
# 'time'       : datetime.datetime
# 'strike'     : float
# 'expiration' : datetime.datetime
# 'underlying' : float
# 'bid'        : float
# 'ask'        : float
# }

import csv
import datetime
import json
from yahoo_fin import stock_info, options


#
# File Management
#
# Database records are individual lines in a json file
# Files are organized by expiration date, one per month
#

def nextExpirationDate(date: datetime.date):
    # The 15th is the earliest third day in the month
    third = datetime.date(date.year, date.month, 15)
    third_friday = third.replace(day=(15 + ((4 - third.weekday()) % 7))) # Friday is weekday 4
    if date > third_friday:
        # find next month's expiration date
        next_month = (date.replace(day=1) + datetime.timedelta(days=31)).replace(day=1)    # first of next month
        third_friday = nextExpirationDate(next_month)
    return (third_friday)

def datetimeToStr(dt):
    dt = dt.replace(microsecond=0)
    return (str(dt))

def datetimeFromStr(s):
    dt = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    return (dt)

# store a single quote in the proper file by expiration date
def store(quote):
    fname = nextExpirationDate(quote['time'].date()).strftime("%Y%m%d")
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
    fname = nextExpirationDate(date).strftime("%Y%m%d")
    quotes = []
    with open(fname, 'r') as f:
        for line in f:
            quotes.append(json.loads(line))
    for q in quotes:
        q['time'] = datetimeFromStr(q['time'])
        q['expiration'] = datetimeFromStr(q['expiration'])
    return (quotes)

c = options.get_calls("rmbs")
for col in c.columns.values:
    print (col)
print (c.loc[0].to_dict())


'''
chain = options.get_options_chain("rmbs")
now = datetime.datetime.now()
now = now.replace(hour=now.hour+3)  # convert to Eastern time
exp = chain['calls']['Contract Name'][0][:10][4:]   # extract expiriration date from contract name
q = {}
q['type']       = 'CALL'
q['time']       = now
q['strike']     = chain['calls']['Strike'][0]
q['expiration'] = datetime.datetime.strptime(exp, '%y%m%d')
q['underlying'] = round(stock_info.get_live_price('rmbs'), 2)
q['bid']        = chain['calls']['Bid'][0]
q['ask']        = chain['calls']['Ask'][0]    

store(q)
qa = recall(now)
print ("Recalled quote Array", qa)


#stock_info.get_market_status() != "OPEN"
'''

if False:
    quote = []
    with open(r'C:\Users\mitchell\Desktop\github\misc\options\db\Sample_L2_2019_August\L2_options_20190801.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['UnderlyingSymbol'] == 'RMBS':
                q = {}
                q['type']       = row['Type'].upper()
                q['time']       = datetime.datetime.strptime(row['DataDate'], "%m/%d/%Y")
                q['strike']     = row['Strike']
                q['expiration'] = datetime.datetime.strptime(row['Expiration'], "%m/%d/%Y").date()
                q['underlying'] = row['UnderlyingPrice']
                q['bid']        = row['Bid']
                q['ask']        = row['Ask']        
                quote.append(q)
        for row in quote[:1]:
            print (row)
