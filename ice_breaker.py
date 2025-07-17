from typing import Tuple
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_ollama import ChatOllama
from langchain.schema import StrOutputParser
from output_parsers import Summary, summary_parser

from third_parties.linkedin_scrapin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

load_dotenv()
import os

def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)

    summary_template = """
    given the Linkedin information {information} about a person from I want you to create:
    1. A short summary
    2. two interesting facts about them
    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], 
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()},
    )

    llm = AzureChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", api_version="2025-01-01-preview")
    # llm = ChatOllama(model="mistral")

    #chain = summary_prompt_template | llm | StrOutputParser() #StrOutputParser() will convert the output to a string, otherwise we have to parse the output ourselves like res.content
    chain = summary_prompt_template | llm | summary_parser
    #linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/nadeera-abeykoon-40a991b8/") 
    res: Summary = chain.invoke(input={"information": linkedin_data})
    print(res)
    print(linkedin_data.get("photoUrl"))
    return res, linkedin_data.get("photoUrl")



if __name__ == "__main__":
    print("Ice Breaker Enter")
    print(os.environ["AZURE_OPENAI_API_KEY"])
    ice_break_with(name="Nadeera Abeykoon")
   
    
