from dotenv import load_dotenv
from griptape.drivers.embedding.openai import OpenAiEmbeddingDriver
from griptape.drivers.vector.pgvector_vector_store_driver import (
    PgVectorVectorStoreDriver,
)
from griptape.structures import Agent
from griptape.drivers.prompt.anthropic import AnthropicPromptDriver
from griptape.rules import Rule
from griptape.tools import VectorStoreTool
import os
from griptape.utils import Chat


# Get environment variables
load_dotenv()
DB_PASSWORD = os.environ.get("DB_PASSWORD")

# Set pgvector variables
db_user = "ian"
db_pass = DB_PASSWORD
db_host = "localhost"
db_port = "5432"
db_name = "postgres"

# Create the connetion string
db_connection_string = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# Create the PgVectorVectorStoreDriver
vector_store_driver = PgVectorVectorStoreDriver(
    connection_string=db_connection_string,
    embedding_driver=OpenAiEmbeddingDriver(),
    table_name="vectors",
)

# Create the tool
tool = VectorStoreTool(
    vector_store_driver=vector_store_driver,
    description="This DB has information about the judgement",
)

# Create the agent
agent = Agent(
    prompt_driver=AnthropicPromptDriver(
        model="claude-3-7-sonnet-20250219"  # , stream=True
    ),
    tools=[tool],
    rules=[
        Rule(
            "Use only the information contained in the DB about the judgement in providing your answers.",
        ),
        Rule("You are a legal assistant."),
        Rule(
            "Never provide the names of any individuals including witnesses in your responses. Rather than using names, use job titles or roles"
        ),
        Rule(
            "Check your answers to ensure that you have completely removed the names of any individuals before giving your final response."
        ),
        Rule("Always respect the privacy of individuals."),
        Rule("Keep your answers concise. Only answer the question asked."),
    ],
)

# Run the agent
Chat(agent).start()
