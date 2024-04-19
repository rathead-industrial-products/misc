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
import time
import json
import threading
import os.path

PRINT_DEBUG = True
RETRY_ATTEMPTS = 3
TICKER = 'RMBS'
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


# store a single quote in a file arranged by expiration date
# files are named 'SYMBYYMMDD.json' where 'SYMBYYMMDD' is an option
# symbol and expiration date extracted from the contract name
def store(quote: dict):
    contract = quote['Contract Name'][:10]
    fname = contract + ".json"
    fname = os.path.join(DATA_DIR, fname)
    with open(fname, 'a') as f:
        json.dump(quote, f)
        f.write('\n')


# return the underlying stock price, quote time, and market open status
def underlying(quote_page):
    price = quote_page.find_element(By.CSS_SELECTOR, 'fin-streamer[data-testid="qsp-price"]').text
    market_status = quote_page.find_element(By.CSS_SELECTOR, 'div[slot="marketTimeNotice"]').text   # As of 1:18 PM EDT. Market Open.
    quote_time = market_status.strip("As of.MarketOpen:close:") 
    open_f = True if "open" in market_status.lower() else False       
    if PRINT_DEBUG: print ("Price", price)
    if PRINT_DEBUG: print ("Market Status", market_status)
    if PRINT_DEBUG: print ("Quote Time", quote_time)
    return ((price, quote_time, open_f))


# return true if the market is open
def marketOpen(quote_page):
    return (underlying(quote_page)[2])

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
        #if PRINT_DEBUG: print (hdg)
        if columnHeadingsValid(hdg):
            for r in rows[1:]:
                values = []
                cells = r.find_elements(By.CSS_SELECTOR, 'td')
                for c in cells:
                    values.append(c.text)
                #if PRINT_DEBUG: print (values)
                contracts.append(values)
    return (contracts)


# return an options quote page from yahoo finance
def OptionsQuotePage(ticker_symbol, date=''):
    url = "https://finance.yahoo.com/quote/" + ticker_symbol + "/options"
    date_suffix = "?date=" + date
    if date: url += date_suffix
    if PRINT_DEBUG: print (url)
    driver = webdriver.Chrome(options=options)
    if PRINT_DEBUG: print ("driver loaded")
    driver.get(url)
    if PRINT_DEBUG: print ("web page fetched")  
    return (driver)


def threadFetchContracts(ticker_symbol, date, result, idx):
    attempt = 0
    while attempt < RETRY_ATTEMPTS:
        try:    # cannot find elements occasionally, perhaps page isn't loaded?  
            qp = OptionsQuotePage(ticker_symbol, date)         
            result[idx] = (underlying(qp), allContracts(qp))
            if PRINT_DEBUG: print ("contracts fetched for exp", date)
            break
        except:
            attempt += 1
            if PRINT_DEBUG: print (attempt, "failure(s) to find element for exp", date)
    qp.quit()


#
# Main
#
# Fetch Options Quotes
#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
 
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


#from selenium import webdriver
#from selenium.webdriver.common.by import By


if __name__ == "__main__":
    start = time.time()
    ticker_symbol = 'RMBS'
    attempt = 0
    while attempt < RETRY_ATTEMPTS:
        try:    # cannot find elements occasionally, perhaps page isn't loaded?  
            qp = OptionsQuotePage(ticker_symbol)         
            expiration_dates = expirationDates(qp)
            mkt_open = marketOpen(qp)
            break
        except:
            attempt += 1
            if PRINT_DEBUG: print (attempt, "failure(s) to find element for expiration date query")
    qp.quit()
    print ("Market Open") if mkt_open else print ("Market Closed")
    
    if mkt_open or True:
        threads = [None] * len(expiration_dates)
        expirations = [None] * len(expiration_dates)
        for i, exp in enumerate(expiration_dates):
            threads[i] = threading.Thread(target=threadFetchContracts, args=(ticker_symbol, exp, expirations, i))
            threads[i].start()
        for i in range(len(threads)):
            threads[i].join()
        for i, scraped_data in enumerate(expirations):
            try:
                ((price, quote_time, open_f), contracts) = scraped_data
                m = nowET().strftime("%m").lstrip('0')      # month without a leading zero
                d = nowET().strftime("%d").lstrip('0')      # day without a leading zero
                y = nowET().strftime("%Y")
                quote_time = m + '/' + d + '/' + y + ' ' + quote_time[:-4]    # format like 'Last Trade Date (EDT)' in contract
                print (quote_time)
                for c in contracts:
                    quote = dict(zip(COLUMN_HEADINGS, c))
                    quote.update({'time': quote_time, 'underlying': price})
                    #if PRINT_DEBUG: print (quote)
                    store(quote)
            except TypeError:
                if PRINT_DEBUG: print ("Nonexistant contracts for expiration", expiration_dates[i])
    if PRINT_DEBUG: print("Execution time %d seconds" % (int(time.time() - start)))
