from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_ollama import ChatOllama
from langchain.schema import StrOutputParser

from third_parties.linkedin import scrape_linkedin_profile

load_dotenv()
import os


if __name__ == "__main__":
    print("Hello World!")
    print(os.environ["AZURE_OPENAI_API_KEY"])

    summary_template = """
    given the Linkedin information {information} about a person from I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables="information", template=summary_template
    )
    # llm = AzureChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", api_version="2025-01-01-preview")
    llm = ChatOllama(model="mistral")


    chain = summary_prompt_template | llm | StrOutputParser() #StrOutputParser() will convert the output to a string, otherwise we have to parse the output ourselves like res.content
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/nadeera-abeykoon-40a991b8/")
    res = chain.invoke(input={"information": linkedin_data})
    print(res)
    
