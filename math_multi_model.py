from dotenv import load_dotenv

from griptape.structures import Agent
from griptape.tools import DateTimeTool, CalculatorTool, WebSearchTool
from griptape.drivers.prompt.openai import OpenAiChatPromptDriver
from griptape.drivers.prompt.ollama import OllamaPromptDriver
from rich import print
import os

prompt = "What is 10224 * 4563 / 3.4?"

ollama_mistral7B_agent = Agent(
    prompt_driver=OllamaPromptDriver(
        model="mistral",
    ),
)
ollama_mistral7B_agent_output = ollama_mistral7B_agent.run(prompt).output


ollama_llama32_agent = Agent(
    prompt_driver=OllamaPromptDriver(
        model="llama3.2",
    ),
)
ollama_llama32_agent_ouput = ollama_llama32_agent.run(prompt).output

openai_agent = Agent(
    prompt_driver=OpenAiChatPromptDriver(
        model="gpt-4o-2024-08-06", temperature=0.1, seed=42
    ),
)
openai_agent_ouput = openai_agent.run(prompt).output


print(
    f"""
Mistral 7B answer: 
        
        {ollama_mistral7B_agent_output}      

Llama 3.2 answer:

        {ollama_llama32_agent_ouput}

OpenAI gpt-4o answer:

        {openai_agent_ouput}
      """
)
