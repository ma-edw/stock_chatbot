from futu import *
from datetime import date, datetime, timedelta
from pathlib import Path
import json
from filepaths import FILEPATH_STOCK_PRICES, FILEPATH_GURU_ARTICLES

# Dates
def get_current_day():
    ''' Get the current day in string format: yyyy-mm-dd, e.g. 2024-07-06 '''
    current_date = date.today()
    current_date_str = str(current_date) 
    return current_date_str # str

def get_latest_day(stock, stock_prices_file_path=FILEPATH_STOCK_PRICES):
    ''' Get the latest date of the closing prices of a specific stock in stock_prices.json '''
    # open the stock price file
    with open(stock_prices_file_path, "r", encoding="utf-8") as file:
       stock_prices_data = json.load(file)
        
    # find the date list by locating the stock code in the data
    for data in stock_prices_data:
        if data["stock_code"] == stock: 
            # latest date is the last entry in date
            latest_day =  data["dates"][-1]
    
    return latest_day # str

# get price from futu API
def get_price_api(stock, dt):
    ''' get price for a specific stock code on a specific date via Futu API '''
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # futu API uses format e.g. 'HK.00700'
    stock_str = "HK." + stock
    ret, data, page_req_key = quote_ctx.request_history_kline(stock_str, start=dt, end=dt, max_count=1000)
    if ret == RET_OK:
        close_prices = data['close'].values.tolist()  
        quote_ctx.close() 
        return close_prices[0] # <class 'float'> 
    else:       
        quote_ctx.close()
        return None

# get price from json file
def get_price(stock, dt, file_path=FILEPATH_STOCK_PRICES):
    ''' get price from json file for a specific stock code on a specific date '''
    with open(file_path, "r", encoding="utf-8") as file:
        stock_price_data = json.load(file) 
    # locate the stock code dictionary in json data
    for data in stock_price_data:
        if data["stock_code"] == stock: 
            # get the close price based on the index of date in the dates field
            index = data["dates"].index(dt)
            return data["close_prices"][index]

def get_latest_price(stock, dt, file_path=FILEPATH_STOCK_PRICES):
    latest_day = get_latest_day(stock=stock, stock_prices_file_path=file_path)
    latest_price = get_price(stock=stock, dt=latest_day, file_path=file_path)
    return latest_price
    

def get_price_list(stock, dt_start, dt_end):
    ''' Given a list of stock codes, date start and date end, get the trading dates and stock close prices via Futu API  '''
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # futu API uses format e.g. 'HK.00700'
    stock_str = "HK." + stock
    ret, data, page_req_key = quote_ctx.request_history_kline(stock_str, start=dt_start, end=dt_end, max_count=1000)
    if ret == RET_OK:
        datetimes = data['time_key'].values.tolist()
        close_prices = data['close'].values.tolist()  
        quote_ctx.close() 
        # extract dates (the first 10 characters) from each datetime string, e.g. convert '2024-07-24 00:00:00' to '2024-07-24'
        dates = []
        for t in datetimes:
            dates.append(t[:10])
        return dates, close_prices # <class 'float'> 
    else:       
        quote_ctx.close()
        return None   

# stock price history (list of prices within date range)
def store_stock_prices(stocks, dt_start, dt_end, file_path=FILEPATH_STOCK_PRICES):
    ''' store stock price history (list of prices within date start and date end) in stock prices json file'''
    data_to_add = []
    for stock in stocks:
        # get dates and close prices for each stock
        dates, close_prices = get_price_list(stock, dt_start, dt_end)  
        # create a dictionary for the stock   
        stock_to_add = {
            "stock_code": stock,
            "dates": [],
            "close_prices": []
        }
        # add dates and close prices to dictionary
        for i in range(len(dates)):
            stock_to_add["dates"].append(dates[i])
            stock_to_add["close_prices"].append(close_prices[i])
        # add stock dictionary to list of stocks
        data_to_add.append(stock_to_add)

    # create new json file with empty list
    with open(file_path, 'w') as file:
        json.dump([], file)

    # store data into json file
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data_to_add,  file, ensure_ascii=False, indent=4)
    
def store_all_stock_prices(dt_from="2023-01-01", dt_to=get_current_day(), stock_articles_file_path=FILEPATH_GURU_ARTICLES, stock_prices_file_path=FILEPATH_STOCK_PRICES):
    ''' store stock prices (Dates: 1 January 2023 to current day) for all stocks in guru articles json file '''
    # get all stocks from stock lists in articles file
    stock_list = []
    with open(stock_articles_file_path, "r", encoding="utf-8") as file:
        guru_article_data = json.load(file)
    for article in guru_article_data:
        stock_list.extend(article["stocks"])
    # remove duplicates and sort -> sorted stock list with unique values
    stock_list = sorted(set(stock_list))
    
    # for each stock, get price history from dt_form to current date
    store_stock_prices(stocks=stock_list, dt_start=dt_from, dt_end=dt_to, file_path=stock_prices_file_path)

def get_stock_growth(stock, d1, d2):
    ''' get stock prices on two different dates, and calculate the price difference and price percentage gain '''
    p1 = get_price(stock, d1)
    p2 = get_price(stock, d2)
    p_diff = round(p2 - p1, 2)
    p_gain = round(p_diff / p1 * 100, 2)
    return p_diff, p_gain

