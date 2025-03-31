# What's Hard with LLM-Powered App Development?
## Demo App Samples

All samples require an OpenAI API key to be set in the `OPENAI_API_KEY` environment variable. Copy [env.example](./env.example) to .env and edit it to add you your own OpenAI API key to do that quickly. The `python-dotenv` import will set the environment variable automatically from that file

* [**boooking_agent_test.py**](./boooking_agent_test.py) - Shows how to model agentic systems as Structures with the Griptape Framework. 
* [**math_multi_model.py**](./math_multi_model.py) - Very simple demo that asks three different LLMs to perform math calculations. Requires local Ollama with `mistral` and `llama3.2` models in addition to an OpenAI API key.
* [**simple_pdf_proc.py**](./simple_pdf_proc.py) - A minimal RAG pre-processor for a PDF file that will load and chunk, before calculating chunk embedding wth OpenAI's embedding model, and then upserting the embeddings and chunks into a PostgreSQL/pgvector database. Database configuration can be set by editing the values in this file. The `DBPASSWORD` variable should be set in your .env file as shown in the example in [env.example](./env.example).
* [**simple_rag_agent.py**](./simple_rag_agent.py) - A simple RAG retreival agent that uses the sample database as [simple_pdf_proc.py](./simple_pdf_proc.py) to answer natural language questions about the content of a processed PDF using vector search and RAG.
* [**superbowl_who_won.py**](./superbowl_who_won.py) - How not to get an LLM to tell you who won the 2025 Super Bowl.
* [**superbowl_winner_workflow.py**](./superbowl_winner_workflow.py) - Uses WorkFlows and Tools (DateTime and WebSearch) to relibably work out who won the most recent Super Bowl. Requires Google Search API key and Search ID to be set in your .env file.
