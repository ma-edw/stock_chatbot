# Chainlit Chatbot 
A Chatbot which analyzes stock analysts' forecast on the stock market
<br/>
The chatbot can store stock articles found online (based on a list of pre-defined websites and stock analysts)
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

### Run the code
Run the chatbot with the following code in the parent folder:
```
chainlit run app.py
```
The chatbot will be available in http://localhost:8000/

### Update the data
In order to get the most updated market information, search for newer stock articles is needed.
<br />
Use function Update_all_data() and run the code in webSearch.py to search for new stock articles and store for use.
```
python run webSearch.py
```

### Expand data search
The stock articles are stored in guru_urls.json. 
<br />
File guru_source.json defines the data source and stock analysts to search for when updating the data.
<br />

### Languages and Tools:

[<img align="left" alt="Visual Studio Code" width="39px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/visual-studio-code/visual-studio-code.png" />][website]
[<img align="left" alt="HTML5" width="39px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/html/html.png" />][website]
[<img align="left" alt="CSS3" width="39px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/css/css.png" />][website]
[<img align="left" alt="JavaScript" width="39px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/javascript/javascript.png" />][website]
[<img align="left" alt="React" width="39px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/react/react.png" />][website]
[<img align="left" alt="Node.js" width="39px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/nodejs/nodejs.png" />][website]
[<img align="left" alt="SQL" width="39px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/sql/sql.png" />][website]
[<img align="left" alt="MySQL" width="39px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/mysql/mysql.png" />][website]
[<img align="left" alt="MongoDB" width="39px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/mongodb/mongodb.png" />][website]
[<img align="left" alt="Git" width="39px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/git/git.png" />][website]
[<img align="left" alt="GitHub" width="39px" src="https://raw.githubusercontent.com/github/explore/78df643247d429f6cc873026c0622819ad797942/topics/github/github.png" />][website]
[<img align="left" alt="Terminal" width="39px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/terminal/terminal.png" />][website]

<br />
<br />
<br />

### Stats and others:
![Github Stats](https://github-readme-stats.dipanjanpanja6.vercel.app/api?username=madzai&show_icons=true&hide_border=true&count_private=true&theme=dark&hide=issues)
![Top Langs](https://github-readme-stats.dipanjanpanja6.vercel.app/api/top-langs/?username=madzai&layout=compact&theme=dark&show_icons=true&hide_border=true)


[website]: https://www.google.com/
