from dotenv import load_dotenv
from griptape.chunkers import PdfChunker
from griptape.drivers.embedding.openai import OpenAiEmbeddingDriver
from griptape.drivers.vector.pgvector import PgVectorVectorStoreDriver
from griptape.loaders import PdfLoader
import os

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

# Install required Postgres extensions and create database schema
vector_store_driver.setup()

pdf_filename = "pdfs/judgement.pdf"
pdf_namespace = "judgement"

pdf_artifact = PdfLoader().load(pdf_filename)
chunks = PdfChunker(max_tokens=500).chunk(pdf_artifact)
vector_store_driver.upsert_text_artifacts({pdf_namespace: chunks})
