# Chainlit Chatbot 
A Chatbot which analyzes stock analysts' forecast on the stock market
<br/>
The chatbot can store stock articles found online.
<br/>
You can ask the chatbot about outlook on the stock market. The chatbot will answer based on the stock articles stored.


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
Update variable KEY_TOGETHERAI for the Chatbot to run.
</br>
Update variable SERPER_API_KEY for the Chatbot to be able to web search for new stock articles.

### Run the code
Run the chatbot with the following code in the parent folder:
```
chainlit run app.py
```
The chatbot will be available in http://localhost:8000/
</br>
### Example
</br>
![chat image](images/chat_image_1.jpg)
</br>
</br>
</br>
</br>
![chat image](images/chat_image_2.jpg)
</br>
</br>

### Update the data
In order to get the most updated market information, search for newer stock articles is needed.
<br />
Use function Update_all_data() and run the code in webSearch.py to search for new stock articles and store for use.
```
python webSearch.py
```

### About the stock article data
The stock articles are stored in guru_urls.json. 
<br /><br/>
File guru_source.json defines the data source and stock analysts to search for when updating the data.
<br />


