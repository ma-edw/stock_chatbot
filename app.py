from langchain_google_vertexai.model_garden import ChatAnthropicVertex
from langchain_google_vertexai import VertexAI
from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

from langchain import hub
from langchain_chroma import Chroma
# from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.embeddings import HuggingFaceEmbeddings

import chainlit as cl
import os
import json
from langchain_community.document_loaders import JSONLoader
from pathlib import Path

import datetime

from dotenv import load_dotenv
load_dotenv()  
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'chainlit-class.json'

def current_date(_):
    td = datetime.date.today()
    td_str = str(td.strftime("%d %B %Y"))
    return td_str

def get_stock_codes(filename="hk_stocks.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            stock_data = json.load(file)
            stock_codes = []
            for stock in stock_data:
                stock_codes.append(stock["Stock_Code"])
            return stock_codes
    except:
        return []


model_choice = "Mistral"

@cl.on_chat_start
async def on_chat_start():    

    if model_choice == "Qwen":
        # Use TogetherAI
        model = ChatTogether(
            api_key=os.environ["KEY_TOGETHERAI"],
            model="Qwen/Qwen1.5-72B-Chat",
            streaming=True,
        )
    
    elif model_choice == "Gemini":
        # use Gemini-Pro
        model = VertexAI(
            model_name="gemini-pro",
            project='vtxclass',
            location='asia-southeast1',
            streaming=True
        )
    
    elif model_choice == "Mistral":
        # use Mistral AI
        model = ChatOpenAI(
            base_url="https://api.together.xyz/v1",
            api_key=os.environ["KEY_TOGETHERAI"],
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            streaming=True
        )
    
    elif model_choice == "Sonnet":
        # use Claude 3 - no connection
        model = ChatAnthropicVertex(
            model_name="claude-3-sonnet@20240229",
            project='vtxclass',
            location='asia-southeast1',
            streaming=True
        )
       
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                ''' 
                            
                ROLE: You're a stock market expert who is very knowledgeable in stock markets. 
                You analyze stock articles in Traditional Chinese very well, and can interpret how the author forecasts the market. 
                
                For stock forecast articles, please only refer to the stock_guru_data variable (unless user asks you to search for external sources as well). 
                It is a list of dictionaries with fields date, author, title, url and article.
                The article field contains the article written by the author field on date field.
                The url field is the website of the article.
                User may ask you about a particular author e.g. 郭家耀. Then you filter out 'author': '郭家耀' in the list of dictionaries, and find the author's articles.
                User may ask you to focus on articles in a date range e.g. from 1 July 2024 to 5 July 2024. 
                Then you filter the values of the "date" field and find the filtered articles
                
                Please always speak in Traditional Chinese (do not speak in simplified chinese or english).
                Please answer in markdown format.                
                In your answers, please always quote the web site, author, title and date which your answer is based on
                Please answer based on the prompt
                Please answer using only the information from context
                
                Here is an example for the format of your answer:
                Question: 近期推介什麼股票？
                Answer:
                近期推介股票：
                以下為幾篇股評文章中專家近期推介的股票，以及推介原因的概括：

                植耀輝 - 2024-07-05:
                中特股: 持續受到追捧，預期下半年有機會跑出，業務相對穩定估值合理，未來可能加大分紅及回購。
                中海油 (00883.HK): 估值合理，油價持續看升，集團2025年產油目標進取，預計息率將回升至吸引水平。
                資料來源：http://www.aastocks.com/tc/stocks/news/aafn-con/.HK.240705_095740/analysts-views/AAFN
                
                羅國森 - 2024-05-24:
                四大內銀: 市場預期在新國九條的推動下，內地資本市場走向"高質量"的發展，上市公司分紅比率將提高，建議四大內銀增加派息以提高市值。
                資料來源：https://www.etnet.com.hk/www/tc/news/home_categorized_news_detail.php?newsid=ETN34052470
                
                陳永陸 - 2024-07-12:
                港股: 受益於美國減息和中國刺激經濟措施，特別是三中全會可能推出的新政策，港股有望持續攀升。
                資料來源：https://www.etnet.com.hk/www/tc/news/commentary_expert_detail.php?category=stocks&expert=chanwingluk&from=latest&newsid=ETN340712881
                
                
                                   
                stock codes
                ---
                Please search which of the {stock_codes} can be found in the article your answer is based on, and include those stock codes in your answer.
                
                current date
                ---
                Today's date is {current_date}.
                
                context
                ---                         
                {context}
                '''
            ),
            ("human", "{question}"),
        ]
    )
    
    ########################################################################################
    # Document Loader
    file_path = "guru_urls.json"

    loader = JSONLoader(
        file_path=file_path,
        jq_schema='.[].article',
        text_content=False)

    docs = loader.load()

    ########################################################################################
    # VectorStore
    hfe = HuggingFaceEmbeddings(model_name="BAAI/bge-base-zh-v1.5")

    vectorstore = Chroma.from_documents(documents=docs, embedding=hfe)

    retriever = vectorstore.as_retriever(search_kwargs={'k': 6})
    
    ########################################################################################
    # rag chain  
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)    
       
    runnable = (
        {"stock_codes": RunnableLambda(get_stock_codes), "current_date": RunnableLambda(current_date), "context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    
    cl.user_session.set("runnable", runnable)
    

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable") 

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        message.content,
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)
    
    await msg.stream_token(chunk)

    await msg.send()
