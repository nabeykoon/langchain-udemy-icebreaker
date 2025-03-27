from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_ollama import ChatOllama
from langchain.schema import StrOutputParser

load_dotenv()
import os

information = """Elon Reeve Musk (/ˈiːlɒn/ EE-lon; born June 28, 1971) is a businessman known for his key roles in Tesla, SpaceX, and Twitter (which he rebranded as X). Since 2025, he has been a senior advisor to United States president Donald Trump and the de facto head of the Department of Government Efficiency (DOGE). Musk is the wealthiest person in the world; as of March 2025, Forbes estimates his net worth to be $320 billion USD."""


if __name__ == "__main__":
    print("Hello World!")
    print(os.environ["AZURE_OPENAI_API_KEY"])

    summary_template = """
    given the information {information} about a person from I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables="information", template=summary_template
    )
    # llm = AzureChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", api_version="2025-01-01-preview")
    llm = ChatOllama(model="mistral")


    chain = summary_prompt_template | llm | StrOutputParser() #StrOutputParser() will convert the output to a string, otherwise we have to parse the output ourselves like res.content
    res = chain.invoke(input={"information": information})
    print(res)
    
