
"""
Create a json database from example csv files in /db

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

import csv
import datetime

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


