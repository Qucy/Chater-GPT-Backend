import os
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

deployment_name = 'text-davinci-003'
model_nane = 'text-davinci-003'

# Create an instance of Azure OpenAI text-davinci-003
llm = AzureOpenAI(deployment_name=deployment_name, model_name=model_nane)

def chainLLMWithPrompt():
    # create a prompt template
    prompt = PromptTemplate(
        input_variables=["product"],
        template="What is a good name for a company that makes {product}?",
    )
    # create LLMChain
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run("colorful socks")
    print(response)


def LLMAgentWithSearchAndCalcTools():

    from langchain.agents import load_tools
    from langchain.agents import initialize_agent
    from langchain.agents import AgentType

    # create tools
    tools = load_tools(["serpapi", "llm-math"], llm=llm)

    # init agent with tools
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    agent.run("What was the highest temperature in SF yesterday in Fahrenheit ? What is that number raised to the .023 power?")


def LLMAgentWithPythonREPLTool():

    from langchain.agents.agent_toolkits import create_python_agent
    from langchain.tools.python.tool import PythonREPLTool

    # create python agent
    agent_executor = create_python_agent(
        llm=llm,
        tool=PythonREPLTool(),
        verbose=True
    )

    agent_executor.run("What is the 10th fibonacci number?")

    print(agent_executor)





if __name__ == '__main__':

    # chainLLMWithPrompt()

    # LLMAgentWithSearchAndCalcTools()

    # LLMAgentWithPythonREPLTool()

    llm('what is machine learning?')