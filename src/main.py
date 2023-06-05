
import os
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from config.configuration import DevelopmentConfig, ProductionConfig
from model.APIRequestModel import Translation, GrammerCorrection, TLDRSummarization, RestaurantReviewCreator, FriendChatModel
from service.chatCompletionService import AzureNormalChatCompletion, AzureStreamChatCompletion, LangChainStreamCompletionService
from service.promptService import TranslationPromptService, GrammerCorrectionPromptService, TLDRSummarizationPromptService, RestaruantReviewPromptService, FriendChatPromptService
from service.agentService import SQLAgentService, NewsAgentService, SearchAgentService
from service.azureSpeechService import AzureSpeechService
from dao.promptTemplateDao import PromptTemplateDao
from util.logger import GPTLogger


app = FastAPI()

# init config
config = ProductionConfig if os.getenv("ENV") == "production" else DevelopmentConfig

# init logger
logger = GPTLogger(config.logger_name, config.logger_level, config.logger_path)

# init service
normal_completion = AzureNormalChatCompletion(config.llm_deployment_name)
stream_completion = AzureStreamChatCompletion(config.llm_deployment_name)
langChain_completion = LangChainStreamCompletionService(config.llm_deployment_name, config.llm_deployment_name)
translationPromptService = TranslationPromptService()
grammerCorrectionPromptService = GrammerCorrectionPromptService()
tldrSummarizationPromptService = TLDRSummarizationPromptService()
restaurantReviewPromptService = RestaruantReviewPromptService()
friendChatPromptService = FriendChatPromptService()
sqlAgentService = SQLAgentService(config.llm_deployment_name, config.llm_model_name, config.SQL_AGENT_DB)
newsAgentService = NewsAgentService(config.llm_deployment_name, config.llm_model_name)
searchAgentService = SearchAgentService(config.llm_deployment_name, config.llm_model_name)
azureSpeechService = AzureSpeechService(config, logger)


origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
def login(form_data: dict):
    username = form_data["username"]
    password = form_data["password"]
    if username != "qucy" or password != "qucy123":
        return {"message": "failed"}
    else:
        return {"message": "success", "username": username, "token": "fake-jwt-token"}
    

#=====================================   generation apis =====================================
@app.post("/generate/translation")
def generation_translation(trans: Translation):
    # get prompts
    messages = translationPromptService.get_prompts(target_language=trans.target_language, 
                                                    style=trans.style, 
                                                    content=trans.content)
    # call openai liberary to get completion
    translation = normal_completion.completion(messages=messages)
    # return response
    return {
        "data":
        {
            "target_language": trans.target_language,
            "content": translation
        }
        ,
        "meta": {
            "message": "success",
            "status": 200
        }
    }

@app.post("/generate/gammarcorrection")
def gammer_correction(grammar: GrammerCorrection):
    # get prompts
    messages = grammerCorrectionPromptService.get_prompts(content=grammar.content)
    # call open library to get completion
    correction = normal_completion.completion(messages=messages)

    # return response
    return {
        "data": {
            "content": correction
        },
        "meta": {
            "message": "success",
            "status": 200
        }
    }

@app.post("/generate/tldr")
def tldr_summarization(tldr: TLDRSummarization):
    # get prompts
    messages = tldrSummarizationPromptService.get_prompts(target_language=tldr.target_language,
                                                          content_length=tldr.content_length,
                                                          content=tldr.content)
    # call open library to get completion
    tldr = normal_completion.completion(messages=messages)
    # return response
    return {
        "data": {
            "content": tldr
        },
        "meta": {
            "message": "success",
            "status": 200
        }
    }

@app.post("/generate/resturantreview")
def resturant_review_creator(resturant: RestaurantReviewCreator):
    # get prompts
    messages = restaurantReviewPromptService.get_prompts(
        target_language=resturant.target_language,
        content_length=resturant.content_length,
        content_category=resturant.content_category,
        content=resturant.content
    )
    # call open library to get completion
    review = normal_completion.completion(messages=messages)
    # return response
    return {
        "data": {
            "content": review
        },
        "meta": {
            "message": "success",
            "status": 200
        }
    }

@app.post("/generate/friendchat")
def friend_chat(friendchat: FriendChatModel):
    # get prompts
    messages = friendChatPromptService.get_prompts(
        contents=friendchat.contents
    )
    # call open library to get completion
    chat = normal_completion.completion(messages=messages)
    # return response
    return {
        "data": {
            "content": chat
        },
        "meta": {
            "message": "success",
            "status": 200
        }
    }

@app.post("/generate/friendchat/stream")
async def friend_chat_stream(friendchat: FriendChatModel):
    text_stream = generate_text_in_stream(friendchat)
    return StreamingResponse(text_stream, media_type="text/plain")


async def generate_text_in_stream(friendchat: FriendChatModel):
    # get prompts
    messages = friendChatPromptService.get_prompts(
        contents = friendchat.contents
    )
    # call open library to get completion
    chats = stream_completion.completion(messages=messages)
    for chat in chats:
        # return chat in stream manner
        yield chat
        await asyncio.sleep(0.01)



@app.post("/generate/langchat/stream")
async def lang_chat_stream(friendchat: FriendChatModel):
    response = langChain_completion.completion(messages='hello')
    return response

# =====================================  prompt apis =====================================
@app.get("/prompt/templates")
def get_prompt_templates():
    prompt_template_dao = PromptTemplateDao(config.SQLALCHEMY_DATABASE_URI)
    prompt_templates = prompt_template_dao.get_all()
    return {
        "data" : prompt_templates,
        "meta": {
            "message": "success",
            "status": 200
        }
    }


# =====================================  agent apis =====================================
@app.get("/agent/db/query/{message}")
def db_query(message: str):
    # get responses
    messages = sqlAgentService.run(message)
    return {
        "data": {
            "content": messages
        },
        "meta": {
            "message": "success",
            "status": 200
        }
    }

@app.get("/agent/news/query/{message}")
def news_query(message: str):
    # get responses
    messages = newsAgentService.run(message)
    return {
        "data": {
            "content": messages
        },
        "meta": {
            "message": "success",
            "status": 200
        }
    }

@app.get("/agent/search/query/{message}")
def search_query(message: str):
    # get responses
    messages = searchAgentService.run(message)
    return {
        "data": {
            "content": messages
        },
        "meta": {
            "message": "success",
            "status": 200
        }
    }



# =====================================  menu apis =====================================
@app.get("/menus")
def get_menus():
    menus = {
        "data": [  
            {
                "id": 1,
                "name": "Generation",
                "icon": "Management",
                "path": "",
                "children": [
                    {
                        "id": 101,
                        "name": "Translation",
                        "icon": "Document",
                        "path": "/generation-translation",
                        "children": []
                    },
                    {
                        "id": 102,
                        "name": "Grammar correction",
                        "icon": "Notebook",
                        "path": "/generation-grammercorr",
                        "children": []
                    },
                    {
                        "id": 103,
                        "name": "TL;DR summarization",
                        "icon": "Tickets",
                        "path": "/generation-tldr",
                        "children": []
                    },
                    {
                        "id": 104,
                        "name": "Friend chat",
                        "icon": "ChatDotRound",
                        "path": "/generation-friendchat",
                        "children": []
                    },
                    {
                        "id": 105,
                        "name": "Restaurant review creator",
                        "icon": "Food",
                        "path": "/generation-restreview",
                        "children": []
                    }
                ]
            },
            {
                "id": 2,
                "name": "Agent",
                "icon": "Platform",
                "path": "",
                "children": [
                    {
                        "id": 201,
                        "name": "Database Agent",
                        "icon": "Mug",
                        "path": "/database-agent",
                        "children": []
                    },
                    {
                        "id": 202,
                        "name": "News Agent",
                        "icon": "Cellphone",
                        "path": "/fin-data-agent",
                        "children": []
                    },
                    {
                        "id": 203,
                        "name": "Search Agent",
                        "icon": "Guide",
                        "path": "/search-agent",
                        "children": []
                    },
                    # {
                    #     "id": 204,
                    #     "name": "Code generation",
                    #     "icon": "Monitor",
                    #     "path": "/code-generation",
                    #     "children": []
                    # },
                    # {
                    #     "id": 205,
                    #     "name": "Bug fixer",
                    #     "icon": "Search",
                    #     "path": "/code-bugfixer",
                    #     "children": []
                    # }
                ]
            },
            {
                "id": 3,
                "name": "Prompt Template",
                "icon": "Monitor",
                "path": "",
                "children": [
                    {
                        "id": 301,
                        "name": "List Templates",
                        "icon": "Mug",
                        "path": "/prompt-templates",
                        "children": []
                    }
                ]
            }
        ],
        "meta": {   
            "message": "success",
            "status": 200
        }
    }
    return menus
    


