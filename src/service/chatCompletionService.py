import abc
import openai
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from model.OPENAIResponseModel import OPENAICompletionResponse


class BaseChatCompletion(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def completion(self, messages: list) -> str:
        pass


class AzureNormalChatCompletion(BaseChatCompletion):
    """Azure Normal Chat Completion"""

    def __init__(
        self,
        engine: str,
        max_tokens: int = 4000,
        temperature: float = 0.5,
        top_p: float = 1.0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        system_prompt: str = "You are ChatGPT, a large language model trained by OpenAI. Respond conversationally",
    ) -> None:
        self.engine = engine
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.system_prompt = system_prompt

    def completion(self, messages):
        """call openai liberary to get completion"""
        response = openai.ChatCompletion.create(
            engine=self.engine,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
            messages=messages,
        )
        # conver to data model
        openAICompletionResponse = OPENAICompletionResponse.parse_obj(response)
        # return content
        if len(openAICompletionResponse.choices) == 0:
            return ""
        else:
            return openAICompletionResponse.choices[0].message.content


class AzureStreamChatCompletion(BaseChatCompletion):
    """
    A stream chat completion return chat in chunks
    """

    def __init__(
        self,
        engine: str,
        max_tokens: int = 4000,
        temperature: float = 0.5,
        top_p: float = 1.0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        system_prompt: str = "You are ChatGPT, a large language model trained by OpenAI. Respond conversationally",
    ) -> None:
        self.engine = engine
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.system_prompt = system_prompt

    def completion(self, messages):
        """call openai liberary to get completion"""
        response = openai.ChatCompletion.create(
            engine=self.engine,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
            messages=messages,
            stream=True,
        )
        # iterate through the stream of events
        for chunk in response:
            # extract message
            chunk_message = chunk["choices"][0]["delta"]
            yield chunk_message.get("content", "")



class LangChainStreamCompletionService(BaseChatCompletion):

    def __init__(self,
                 deployment_name: str,
                 model_name: str,):
        self.llm = AzureOpenAI(deployment_name=deployment_name, model_name=model_name)

    def completion(self, messages):

        # create tools
        tools = load_tools(["serpapi", "llm-math"], llm=self.llm)

        # init agent with tools
        agent = initialize_agent(tools, self.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

        response = agent.run("What was the high temperature in SF yesterday in Fahrenheit? What is that number raised to the .023 power?")

        return response


