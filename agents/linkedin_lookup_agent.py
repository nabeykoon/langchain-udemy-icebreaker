import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from tools.tools import get_profile_url_tavily


def lookup(name: str) -> str:
    llm = AzureChatOpenAI(
        temperature=0, model_name="gpt-4o-mini", api_version="2025-01-01-preview"
    )

    linkedinUrl_template = """
    given the full name {name_of_person} I want you to generate me a link to their Linkedin profile page. 
    Your response should contain only a URL.
    """
    linkedinUrl_prompt_template = PromptTemplate(
        input_variables="name_of_person", template=linkedinUrl_template
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google for Linkedin profile page",
            func= get_profile_url_tavily,
            description="Useful for when you need to get the Linkedin profile page URL of a person",
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    result = agent_executor.invoke(
        input={"input": linkedinUrl_prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url


if __name__ == "__main__":
    name = "Nadeera Abeykoon"
    linkedin_profile_url = lookup(name)
    print(f"Linkedin profile URL for {name}: {linkedin_profile_url}")
    # linkedin_profile_url = "https://www.linkedin.com/in/nadeera-abeykoon-40a991b8/"
