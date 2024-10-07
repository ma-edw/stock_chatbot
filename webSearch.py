from langchain_community.utilities import GoogleSerperAPIWrapper
from beautiful_soup import extract_article, extract_title, extract_author, extract_date, extract_stocks
import json
from pathlib import Path
import os
import shutil
import schedule
import time
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()  

from filepaths import *

def Serper_Search(to_search):
    search = GoogleSerperAPIWrapper(gl='hk', hl='zh-tw', serper_api_key=os.environ["SERPER_API_KEY"])

    results = search.results(to_search)    
    num_of_results = len(results['organic'])
    
    result_links = []
    for r in results['organic']:
        result_links.append(r['link'])
    
    return (num_of_results, result_links)

# search for a keyword, i.e. author in a url source
def Search_and_Update(source, keyword, file_path=FILEPATH_GURU_ARTICLES):
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
    num_of_results, result_links = Serper_Search(str_url)
    print(f"No. of search results: {num_of_results}")
    print()

    # Existing data
    existing_data = json.loads(Path(file_path).read_text())
    
    # Check new data before combining with existing data
    data_to_add = []
    for i in range(num_of_results):
        print(f"Processing {result_links[i]}")
        
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
                "source": source,
                "date": date,
                "author": author,        
                "title": title,
                "url": url,        
                "article": article,
                "stocks": stocks,
            }
            data_to_add.append(new_data) 
            print(f"Article saved: {title}")
        else:
            reason_to_reject_article = "duplicate" if new_data_duplicate else "invalid" if new_data_invalid else None
            print(f"Article not saved: {reason_to_reject_article}")
        print()
        
    print(f"No. of new articles to add: {len(data_to_add)}")
    print()
    
    # Combine new data (if any) with existing data
    if (len(data_to_add) > 0):
        existing_data.extend(data_to_add)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data,  file, ensure_ascii=False, indent=4)      

def Update_all_data(guru_source_filename=FILEPATH_GURU_SOURCES, articles_filename=FILEPATH_GURU_ARTICLES, articles_backup=FOLDER_GURU_ARTICLES_BACKUP):
    # add date string (current date) to backup of stock articles file
    date_str = datetime.now().strftime('%Y-%m-%d') # e.g. 2024-09-16
    # ensure backup folder exists
    os.makedirs(articles_backup, exist_ok=True)
    articles_backup_file = f'{articles_filename[:-5]}_{date_str}.json'
    articles_backup_dir = os.path.join(articles_backup, articles_backup_file)
    shutil.copy(articles_filename, articles_backup_dir)

    with open(articles_filename, "r", encoding="utf-8") as file:
        articles_data = json.load(file)
    num_of_articles = len(articles_data) 
    print(f"No. of articles before update: {num_of_articles}")
    print()

    with open(guru_source_filename, "r", encoding="utf-8") as file:
        source_data = json.load(file) 
    for data in source_data:
        
        source = data["source"]
        authors = data["authors"]
        
        for author in authors:
            print(f"Searching for {author} in {source}")
            print()
            Search_and_Update(source=source, keyword=author)
    
    with open(articles_filename, "r", encoding="utf-8") as file:
        source_data = json.load(file) 
        
    # newly added data
    new_data = source_data[num_of_articles:]
        
    print()       
    print("Search complete.")
    print(f"No. of articles after update: {len(source_data)}")
    print()
    print("Newly added articles:")
    print()    
    for d in new_data:
        author = d["author"]
        title = d["title"]
        url = d["url"]
        print(f"Author: {author}, Title: {title}")
        print(f"{url}")
        print()
    
    # Sort the data after addition of new articles
    sorted_data = sorted(source_data, key=lambda x: (x.get('source', ''), x.get('author', ''), x.get('date', ''))) 
    
    with open(articles_filename, "w", encoding="utf-8") as file:
        json.dump(sorted_data,  file, ensure_ascii=False, indent=4)    


def scheduled_update():
    schedule.every(1).day.at("00:00").do(Update_all_data)  # run at 12:00 AM every day
    while True:
        schedule.run_pending()
        time.sleep(1)


# Use either options to update the article database
# Keep running the code to update article database regularly
# scheduled_update() 

# or manually update article database     
# Update_all_data()
