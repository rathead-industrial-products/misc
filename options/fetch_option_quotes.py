#
# Fetch an options quote from Yahoo Finance
# Using Selenium, scrape data of interest
# Create an historical record by saving to a set of files
#

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
import threading
import os.path

PRINT_DEBUG = False
TICKER = 'RMBS'
ACTIVE = ('TSLA', 'AAPL', 'F')
DATA_DIR = "/home/mitchell/stock_options/data"
COLUMN_HEADINGS = ['Contract Name', 'Last Trade Date (EDT)', 'Strike', 'Last Price', 'Bid', 'Ask', 'Change', '% Change', 'Volume', 'Open Interest', 'Implied Volatility']

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
def marketOpen(quote_page):
    open_f = False
    market_status = quote_page.find_element(By.CSS_SELECTOR, 'div[slot="marketTimeNotice"]').text
    if PRINT_DEBUG: print (market_status)
    if "open" in market_status.lower():
        if PRINT_DEBUG: print ("Market Open")
        open_f = True
    if "close" in market_status.lower():
        if PRINT_DEBUG: print ("Market Closed")
    return (open_f)





# store a single quote in a file arranged by expiration date
# files are named 'SYMBYYMMDD.json' where 'SYMBYYMMDD' is an option
# symbol and expiration date extracted from the contract name
def store(quote: dict):
    contract = quote['Contract Name'][:10]
    fname = contract + ".json"
    #fname = os.path.join(DATA_DIR, fname)
    with open(fname, 'a') as f:
        json.dump(quote, f)
        f.write('\n')

# return an options quote page from yahoo finance
def OptionsQuotePage(ticker_symbol, date='', result=None, index=None):
    OPTION_URL = "https://finance.yahoo.com/quote/" + ticker_symbol + "/options"
    DATE_SUFFIX = "?date=" + date
    url = OPTION_URL
    if date: url += DATE_SUFFIX
    if PRINT_DEBUG: print (url)
    driver = webdriver.Chrome()
    if PRINT_DEBUG: print ("driver loaded")
    driver.get(url)
    if PRINT_DEBUG: print ("web page fetched")
    if result:
        result[index] = driver
    return (driver)

# return the underlying stock price
def underlying(quote_page):
    price = quote_page.find_element(By.CSS_SELECTOR, 'fin-streamer[data-testid="qsp-price"]')
    if PRINT_DEBUG: print ("Price", price.text)
    return (price)

# return all options expiration dates as linux timestamps
def expirationDates(quote_page):
    dropdown = quote_page.find_element(By.CSS_SELECTOR, 'div[role="listbox"]')
    dates = dropdown.find_elements(By.CSS_SELECTOR, 'div[role="option"]')
    expiration_dates = []
    for d in dates:
        exp = d.get_attribute("data-value")
        if PRINT_DEBUG: print (exp)
        expiration_dates.append(exp)
    return (expiration_dates)

# return True column headings have not changed from what is expected
def columnHeadingsValid(headings_from_website):
    if headings_from_website == COLUMN_HEADINGS: return (True)
    else: return (False)

# scrape all out and call contracts at all strike prices
def allContracts(quote_page):
    contracts = []
    tables = quote_page.find_elements(By.CSS_SELECTOR, 'table[class="svelte-12t6atp"]')
    for t in tables:
        rows = t.find_elements(By.CSS_SELECTOR, 'tr')
        hdg = []
        headings = rows[0].find_elements(By.CSS_SELECTOR, 'th')
        for h in headings:
            hdg.append(h.text)
        if PRINT_DEBUG: print (hdg)
        if columnHeadingsValid(hdg):
            for r in rows[1:]:
                values = []
                cells = r.find_elements(By.CSS_SELECTOR, 'td')
                for c in cells:
                    values.append(c.text)
                if PRINT_DEBUG: print (values)
                contracts.append(values)
    return (contracts)


#
# Main
#
# Fetch Options Quotes
#

from selenium import webdriver
from selenium.webdriver.common.by import By


if __name__ == "__main__":
    ticker_symbol = 'RMBS'
    qp = OptionsQuotePage(ticker_symbol)
    underlying = underlying(qp)
    expiration_dates = expirationDates(qp)
    mkt_open = marketOpen(qp)
    threads = [None] * len(expiration_dates)
    pages = [None] * len(expiration_dates)
    for i, exp in enumerate(expiration_dates):
        threads[i] = threading.Thread(target=OptionsQuotePage, args=('ticker_symbol', exp, pages, i))
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()
    for qp in pages:
        contracts = allContracts(qp)
        for c in contracts:
            quote = dict(zip(COLUMN_HEADINGS, c))
            if PRINT_DEBUG: print (quote)
            store(quote)
    




