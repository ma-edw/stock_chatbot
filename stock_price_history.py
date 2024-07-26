from futu import *
from datetime import date, datetime, timedelta

def date_adjusted(source, dt):
    # aastocks: "2024-07-06"
    # etnet: "07/06/2024 09:21"
    # futu API: "2019-09-11"
    if source == "etnet":
        date_str, time_str = dt.split()
        month, day, year = date_str.split('/')
        dt_adj = f"{year}-{month}-{day}"
    else:
        dt_adj = dt
    return dt_adj        

def get_price(stock, dt):
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # futu API uses format e.g. 'HK.00700'
    stock_str = "HK." + stock
    ret, data, page_req_key = quote_ctx.request_history_kline(stock_str, start=dt, end=dt, max_count=100)
    if ret == RET_OK:
        close_prices = data['close'].values.tolist()  
        quote_ctx.close() 
        return close_prices[0] # <class 'float'> 
    else:       
        quote_ctx.close()
        return None      

def get_date_b4(dt, days):
    dt_now = datetime.strptime(dt, '%Y-%m-%d') # str of today
    dt_b4 = dt_now - timedelta(days)
    date_b4 = dt_b4.strftime('%Y-%m-%d') # str
    return date_b4

def get_stock_growth(stock, days):
    d1 = str(date.today())
    d2 = get_date_b4(d1, days)
    p1 = get_price(stock, d1)
    p2 = get_price(stock, d2)
    p_diff = round(p2 - p1, 2)
    p_gain = round(p_diff / p1 * 100, 2)
    return p_diff, p_gain   

