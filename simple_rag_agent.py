from dotenv import load_dotenv
from griptape.drivers.embedding.openai import OpenAiEmbeddingDriver
from griptape.drivers.vector.pgvector_vector_store_driver import (
    PgVectorVectorStoreDriver,
)
from griptape.structures import Agent
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
    "Provide only the material contained in the DB about the judgement in providing your answers.",
    tools=[tool],
    stream=True,
)

# Run the agent
Chat(agent).start()
