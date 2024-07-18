from langchain_community.utilities import GoogleSerperAPIWrapper
import os
from dotenv import load_dotenv
load_dotenv()  

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

