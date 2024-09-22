import requests
from bs4 import BeautifulSoup
import re
import datetime
import json
from filepaths import *

def clean_string(text):
    try:
        char_remove = r'[^\u3000\u4e00-\u9fff\u3400-\u4dbf\uff00-\uffef\u2e80-\u2eff\u3000-\u303f\u31c0-\u31ef\u2f00-\u2fdf\u2ff0-\u2fff\u3040-\u309f\u30a0-\u30ff\u31f0-\u31ff\u4dc0-\u4dff\u31a0-\u31bf]'
        cleaned_text = re.sub(char_remove, '', text)
        return cleaned_text
    except:
        return "not found"

def extract_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title_element = soup.find('title')
        
        if title_element:
            return clean_string(title_element.text)
        else:
            return "not found"
    except:
        return "not found"

def extract_author(source, url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if source == "aastocks" or source == "hk01":
            title_element = soup.find('title')
            
            if title_element:
                if source == "aastocks":
                    author = title_element.text.split("：")[0]
                    return clean_string(author)
                elif source == "hk01":
                    author = title_element.text.split("｜")[-1]
                    return clean_string(author)
            else:
                return "not found"
        elif source == "etnet":
            div_element = soup.find('div', style="font-size:40px; display: flex;align-items: flex-end; padding-bottom:10px;")
            if div_element:
                return clean_string(div_element.text) 
            else:
                return "not found"
        else:
            return "not found"
    except:
        return "not found"

def adjust_date_string(dt, source):    
    try:
        if source == "aastocks":
            try:
                year = int("20" + dt[0:2])
                month = int(dt[2:4])
                day = int(dt[4:6])
                dt2 = datetime.date(year, month, day)
                return str(dt2)
            except:
                return "not found"
        elif source == "etnet":
            try:
                # extract e.g. "29/07/2024" from "29/07/2024 13:37"
                dt = dt[:10]
                year = int(dt[-4:])
                month = int(dt[3:5])
                day = int(dt[0:2])
                dt2 = datetime.date(year, month, day)
                return str(dt2)
            except:
                return "not found"
        else:
            return "not found"
    except:
        return "not found"

def extract_date(source, url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if source == "aastocks":
            # extract date string from URL
            dt = url[52:58]
            
            if all(char.isdigit() for char in dt):
                # return generate_date(dt)
                return adjust_date_string(dt, source)
            else:
                return "not found"

        elif source == "etnet":
            date_paragraph = soup.find('p', class_='date')
            if date_paragraph:
                # return date_paragraph.text.strip() 
                dt = date_paragraph.text.strip()
                return adjust_date_string(dt, source)
            else:
                return "not found"
        else:
            return "not found"
    except:
            return "not found"

def extract_article(source, url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # additional string for author, date, title
        str_author = "筆者：" + extract_author(source, url)
        str_date = "。日期：" + extract_date(source, url)
        str_title = "。標題：" + extract_title(url) + "。"
        str_addl = str_author + str_date + str_title

        if source == "aastocks" or source == "hk01":
            if source == "aastocks":
                div_element = soup.find('div', class_='newscontent5 fLevel3', id='spanContent')
            elif source == "hk01":
                div_element = soup.find('div', class_='article-grid__content-section')        

            if div_element:
                p_elements = div_element.find_all('p')
                if p_elements:
                    p_combined = ""
                    for p in p_elements:
                        p_combined += p.text
                        
                    p_combined = str_addl + p_combined + "。網址：" + url
                    return p_combined    
                else:
                    return "not found"        
            else:
                return "not found"
            
        elif source == "etnet":
            article_paragraph = soup.find('p', itemprop='articleBody')
            if article_paragraph:
                return str_addl + article_paragraph.text.strip() + "。網址：" + url
            else:
                return "not found"  
        
        else:
            return "not found"
    except:
        return "not found"

def extract_stocks(article, filename=FILEPATH_STOCK_CODES):
    try:
        # open stock list file
        with open(filename, "r", encoding="utf-8") as file:
            stock_data = json.load(file)
            stock_codes = []
            stock_names = []
            
            # find in article matches for stock codes and stock names
            for stock in stock_data:
                if stock["Stock_Code"] in article:
                    stock_codes.append(stock["Stock_Code"])
                if stock["Stock_Name"] in article:
                    stock_names.append(stock["Stock_Name"])
            
            # add stock codes based on stock names found (if not included already)
            for stock_name in stock_names:
                for stock in stock_data:
                    # find the stock code for each stock name found in article
                    if stock["Stock_Name"] == stock_name:                    
                        stock_code_match = stock["Stock_Code"]
                        # add to stock code list if not duplicate
                        if stock_code_match not in stock_codes:
                            stock_codes.append(stock_code_match)
                            
        return stock_codes
    except:
        return "not found"