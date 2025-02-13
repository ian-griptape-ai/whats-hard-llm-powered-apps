from dotenv import load_dotenv

from griptape.structures import Agent
from griptape.tools import DateTimeTool, WebSearchTool
from griptape.drivers.prompt.openai import OpenAiChatPromptDriver
from griptape.drivers.web_search.google import GoogleWebSearchDriver
from rich import print
import os

load_dotenv()

websearchdriver = GoogleWebSearchDriver(
    api_key=os.environ["GOOGLE_API_KEY"], search_id=os.environ["GOOGLE_API_SEARCH_ID"]
)

openai_agent = Agent(
    prompt_driver=OpenAiChatPromptDriver(
        model="gpt-4o-2024-08-06", temperature=0.1, seed=42
    ),
    # rules=[Rule("when getting relative time, use the get_relative_datetime activity")],
    tools=[WebSearchTool(web_search_driver=websearchdriver), DateTimeTool()],
)
openai_agent.run("Who won the most recent super bowl?")
