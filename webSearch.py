from langchain_community.utilities import GoogleSerperAPIWrapper
from beautiful_soup import extract_article, extract_title, extract_author, extract_date, extract_stocks
import json
from pathlib import Path
import os
import schedule
import time

# from dotenv import load_dotenv
# load_dotenv()  

def Serper_Search(to_search):
    search = GoogleSerperAPIWrapper(gl='hk', hl='zh-tw', serper_api_key=os.environ["SERPER_API_KEY"])

    results = search.results(to_search)    
    num_of_results = len(results['organic'])
    
    result_links = []
    result_titles = []
    result_snippets = []

    for r in results['organic']:
        result_links.append(r['link'])
        result_titles.append(r['title'])
        result_snippets.append(r['snippet'])
    
    return (num_of_results, result_links, result_titles, result_snippets)

# search for a keyword, i.e. author in a url source
def Search_and_Update(source, keyword, file_path="guru_urls.json"):
    # Google search results
    if source == "aastocks":
        str_url = "http://www.aastocks.com/tc/stocks/news/aafn/analysts-views"
    elif source == "etnet":
        str_url = "https://www.etnet.com.hk/www/tc/news/commentary_category.php?category=stocks"
    elif source == "hk01":
        str_url = "https://www.hk01.com/channel/396/%E8%B2%A1%E7%B6%93%E5%BF%AB%E8%A8%8A"
    else:
        str_url = ""
        
    str_source = "site: " + str_url
    str_url = keyword + " " + str_source
    num_of_results, result_links, result_titles, result_snippets = Serper_Search(str_url)
    
    # Extract article from the website
    articles = []    
    for i in range(num_of_results):
        articles.append(extract_article(source=source, url=result_links[i]))

    # Existing data
    existing_data = json.loads(Path(file_path).read_text())
    
    # Check new data before combining with existing data
    data_to_add = []
    for i in range(num_of_results):
        date = extract_date(source=source, url=result_links[i])
        author = extract_author(source=source, url=result_links[i])
        title = extract_title(url=result_links[i])
        url = result_links[i]
        article = extract_article(source=source, url=result_links[i])
        stocks = extract_stocks(article=article)
    
        # check if URL is already included in existing data, or if some fields cannot be found in article
        new_data_duplicate = any(data.get("url") == url for data in existing_data)
        new_data_invalid = any(x == "not found" for x in [date, author, title, article])
        
        if not (new_data_duplicate or new_data_invalid):
            new_data = {
                "date": date,
                "author": author,
                "title": title,
                "url": url,
                "article": article,
                "stocks": stocks
            }
            data_to_add.append(new_data) 
    
    # Combine new data (if any) with existing data
    if (len(data_to_add) > 0):
        existing_data.extend(data_to_add)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data,  file, ensure_ascii=False, indent=4)
            
def Update_all_data(filename="guru_source.json"):
    with open(filename, "r", encoding="utf-8") as file:
        source_data = json.load(file) 

    for data in source_data:
        source = data["source"]
        authors = data["authors"]
        
        for author in authors:
            Search_and_Update(source=source, keyword=author)


def scheduled_update():
    schedule.every(1).day.at("00:00").do(Update_all_data)  # run at 12:00 AM every day
    while True:
        schedule.run_pending()
        time.sleep(1)


