import logging
import openai
import os


class Config(object):
    
    # open configuration
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_version = '2023-03-15-preview'
    openai.api_type = 'azure'
    openai.api_base = ''
    api_deployment_name = 'chatGPTAzure'

    # langChain configuration
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"
    os.environ["OPENAI_API_BASE"] = ""
    os.environ["SERPAPI_API_KEY"] = ""
    langChain_deployment_name = 'text-davinci-003'
    langChain_model_name = 'text-davinci-003'

    number_workers = 20

class DevelopmentConfig(Config):
    """Development configuration"""

    # logging
    logger_name = "chatGPT"
    logger_level = logging.DEBUG
    logger_path =  "../logs/chatGPT.log"

    # database config for sqlite
    SQLALCHEMY_DATABASE_URI = 'sqlite:////mnt/disk1/python-projects/Chater-GPT-Backend/db/gpt-demo.db'
    SQL_AGENT_DB = "sqlite:////mnt/disk1/python-projects/LangChainDemo/demo.db"


class ProductionConfig(Config):
    """Production configuration"""

    # logging
    logger_name = "chatGPT"
    logger_level = logging.INFO
    logger_path =  "../logs/chatGPT.log"

    # database config for sqlite
    SQLALCHEMY_DATABASE_URI = '../../db/gpt-demo.db'
    SQL_AGENT_DB = "sqlite:////mnt/disk1/python-projects/LangChainDemo/demo.db"