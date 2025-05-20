# Chainlit Chatbot 
A Chatbot which analyzes stock analysts' forecast on the stock market
<br/>
The chatbot can store stock articles found online, and extract information such as market outlook from the articles.

</br></br>
![chat_image](images/chat_image_1.jpg)
</br></br>
![chat_image](images/chat_image_2.jpg)
</br>


### Copy the code
Run the following command in your local folder after logging in with your Github account:
```
git clone https://github.com/madzai/chatbot_llm.git
```

### Install required Python packages
Create and activate a virtual environment. Then run the following code in the parent folder:
```
pip install -r requirements.txt
```

### Update the variables in .env file
Update variable KEY_TOGETHERAI (you need a Together AI account) for the Chatbot to run.
</br>
Update variable SERPER_API_KEY (you need a Serper account) for the Chatbot to be able to do web search for new stock articles.

### Run the code
Run the chatbot with the following code in the parent folder:
```
chainlit run app.py
```
The chatbot will be available in http://localhost:8000/

### Update the data
Search for newest stock articles in order to get the most updated market information.
<br />
Use function Update_all_data() and run the code in webSearch.py to search for new stock articles and store for use.
```
python webSearch.py
```

### About the stock article data
The stock articles are stored in guru_urls.json. 
<br />
File guru_source.json defines the data source and stock analysts to search for when updating the data.
<br />
