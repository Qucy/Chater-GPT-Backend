import logging
import openai
import os


class Config(object):
    
    # open configuration
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_version = '2023-03-15-preview'
    openai.api_type = 'azure'
    openai.api_base = 'https://qucy-openai-test.openai.azure.com/'

    # langChain configuration
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"
    #os.environ["OPENAI_API_BASE"] = "your api base"
    #os.environ["SERPAPI_API_KEY"] = "your search api key"
    llm_deployment_name = 'chatGPTAzure'
    llm_model_name = 'gpt-35-turbo'

    # azure speech configuration
    speech_service_key = os.getenv("SPEECH_KEY")
    speech_service_region = os.getenv("SPEECH_REGION")
    speech_synthesis_voice_name = 'en-US-JennyNeural' 
    speech_recognition_language = 'en-US'


    # number of workers
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