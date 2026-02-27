# Local RAG using Ollama

A local AI-powered retrieval-augmented generation (RAG) system that allows you to ask questions over your PDF and DOCX documents using embeddings and a local LLM (Ollama / Llama 3).

---

## Features

- Chunking of documents into manageable pieces  
- Storage of embeddings in **PostgreSQL + pgvector**  
- Vector similarity search for context retrieval  
- Chat history storage  
- Answer generation using local LLM (Ollama)
- **Command-line interface only (no GUI)**  

---

## Supported File Types

- PDF (`.pdf`)  
- Word Document (`.docx`)  

> Note: Only these formats are currently supported for document ingestion.

---

## Requirements

- Python 3.12+  
- PostgreSQL with pgvector extension  
- Packages listed in `requirements.txt.`

Install Python packages:

```bash
pip install -r requirements.txt
````

---

## Database Setup

1. Make sure PostgreSQL and pgvector are installed and running.
2. Create a database and run the setup SQL:

```bash
psql -U postgres -d your_database -f setup_db.sql
```

This will create all necessary tables and extensions for the RAG system.

---

## Project Structure

```text
project/
├── app/
│   ├── __init__.py
│   ├── check_db.py
│   ├── chunking.py
│   ├── database.py
│   ├── engine.py
│   ├── ingestion.py
│   ├── ingestion_query.py
│   ├── llm_query.py
│   ├── main.py
│   └── model.py
├── data/               # Store your PDF and DOCX files here
├── venv/               # Virtual environment (ignored in Git)
├── .env                # Environment variables (ignored in Git)
├── .gitignore
├── requirements.txt
└── setup_db.sql        # Database schema and setup
```

---

## Usage

### 1. Upload / Ingest Documents

Add your PDF or DOCX files to the `data/` folder, then run:

```bash
python main.py
```

This will:

* Split documents into chunks
* Generate embeddings
* Store chunks and embeddings in the Postgres database

---

### 2. Run Chatbot

Run the local RAG chatbot to ask questions over your documents:

```bash
python llm_query.py
```

Follow the prompts:

1. Select the document you want answers from
2. Ask questions in a loop (type `quit` or `exit` to stop)

> The chatbot retrieves the most relevant chunks from your database and generates answers using Ollama.

---

## Notes

* Ensure `.env` and `venv/` are not committed to GitHub.
* Use a virtual environment (`venv`) to avoid dependency conflicts.
* The system works fully locally — no cloud services required.
* All embeddings and chat history are stored in the database for context-aware responses.

---

## License

This project is open source and free to use for learning, portfolio, or personal purposes.

```

