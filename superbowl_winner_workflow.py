from dotenv import load_dotenv

from griptape.structures import Workflow
from griptape.tasks import PromptTask
from griptape.drivers.prompt.openai import OpenAiChatPromptDriver
from griptape.drivers.prompt.ollama import OllamaPromptDriver
from griptape.tools import DateTimeTool, WebSearchTool
from griptape.drivers.web_search.google import GoogleWebSearchDriver
from griptape.utils import StructureVisualizer
from griptape.rules import Rule
import os

load_dotenv()

websearchdriver = GoogleWebSearchDriver(
    api_key=os.environ["GOOGLE_API_KEY"], search_id=os.environ["GOOGLE_API_SEARCH_ID"]
)

get_todays_date_task = PromptTask(
    "What is today's date?",
    prompt_driver=OllamaPromptDriver(model="llama3.2"),
    tools=[DateTimeTool()],
    id="get_todays_date",
)

who_won_the_superbowl_task = PromptTask(
    "Who won the Super Bowl this year: {{ parent_outputs['get_todays_date'] }}",
    prompt_driver=OllamaPromptDriver(model="llama3.2"),
    tools=[WebSearchTool(web_search_driver=websearchdriver)],
    id="who_won_the_superbowl",
    parent_ids=["get_todays_date"],
)

workflow = Workflow(tasks=[get_todays_date_task, who_won_the_superbowl_task])

print(StructureVisualizer(workflow).to_url())

workflow.run()
