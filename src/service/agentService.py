import os
import requests
import json
from langchain.llms import AzureOpenAI
from langchain.tools import BaseTool
from langchain.agents import create_sql_agent, initialize_agent, AgentType, load_tools
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.memory import ConversationBufferWindowMemory
from langchain.sql_database import SQLDatabase
from model.NewsModel import Article



class SQLAgentService:

    def __init__(self, deployment_name: str, model_name: str, db_link: str) -> None:
        self.llm = AzureOpenAI(deployment_name=deployment_name, model_name=model_name)
        self.db = SQLDatabase.from_uri(db_link)
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.agent = create_sql_agent(
            llm=self.llm, 
            toolkit=self.toolkit, 
            verbose=True,
            max_iterations=5
        )


    def run(self, message: str) -> str:
        response = self.agent.run(message)
        return response
    

class NewsRetrievalTool(BaseTool):
    
    # set the proxy server address
    proxy_address = 'http://127.0.0.1:7890'

    # set the environment variables
    os.environ['http_proxy'] = proxy_address
    os.environ['https_proxy'] = proxy_address
    
    name = "News Retrieval Tool"
    description = "useful when you need to retrieve latest news"
    
    def _run(self, query:str):
        articles_all = ''
        # loading news from API
        try:
            url = (f'https://newsapi.org/v2/everything?q={query}&from=2023-05-17&pageSize=3&sortBy=popularity&apiKey=')
            r = requests.get(url)
            j_news = r.json()
            j_articles = j_news['articles']
            for a in j_articles:
                article = Article.parse_raw(json.dumps(a))
                articles_all += str(article)
        except Exception as e:
            print(e)
            articles_all = 'Sorry, we cannot find any news for you.'
            
        return articles_all
        
    
    def _arun(self, query: str):
        raise NotImplementedError("Async operation not supported yet.")


class NewsAgentService:

    def __init__(self, deployment_name: str, model_name: str) -> None:
        self.llm = AzureOpenAI(deployment_name=deployment_name, model_name=model_name)
        self.tools = [NewsRetrievalTool()]
        self.agent = initialize_agent(
            agent='zero-shot-react-description',
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            max_iterations=3,
            early_stopping_method='generate'
        )

    def run(self, message: str) -> str:
        response = self.agent.run(message)
        return response
    

class SearchAgentService:

    def __init__(self, deployment_name: str, model_name: str) -> None:
        self.llm = AzureOpenAI(deployment_name=deployment_name, model_name=model_name)
        self.tools = load_tools(["serpapi"], llm=self.llm)
        self.agent = initialize_agent(self.tools, 
                                      self.llm, 
                                      agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                                      verbose=True, 
                                      max_iterations=5)


    def run(self, message: str) -> str:
        try:
            response = self.agent.run(message)
        except Exception as e:
            print(e)
            response = 'Sorry, we cannot find any information for you.'
        return response