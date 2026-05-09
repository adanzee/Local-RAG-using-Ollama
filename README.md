# Local RAG using Ollama

A local AI-powered retrieval-augmented generation (RAG) system that allows you to ask questions over your PDF and DOCX documents using embeddings and a local LLM (Ollama / Llama 3).

---

## Features

- Chunking of documents into manageable pieces  
- Storage of embeddings in **PostgreSQL + pgvector**  
- Vector similarity search for context retrieval  
- Chat history storage  
- Answer generation using local LLM (Ollama)
- Command-line interface and Streamlit web GUI

---

## Supported File Types

- PDF (`.pdf`)  
- Word Document (`.docx`)  

> Note: Only these formats are currently supported for document ingestion.

---

## Requirements

- Python 3.12+  
- PostgreSQL with pgvector extension  
- Packages listed in `requirements.txt`

Install Python packages:

```bash
pip install -r requirements.txt
```

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
│   ├── config.py
│   ├── database.py
│   ├── llm_query.py
│   ├── logging_config.py
│   ├── main.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chunking_service.py
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── ingestion_service.py
│   │   ├── llm_service.py
│   │   └── query_service.py
│   └── streamlit_app.py
├── data/               # Store your PDF and DOCX files here
├── venv/               # Virtual environment (ignored in Git)
├── .env.example        # Environment example
├── .env                # Environment variables (ignored in Git)
├── .gitignore
├── requirements.txt
└── setup_db.sql        # Database schema and setup
```

---

## Usage

### 1. Upload / Ingest Documents

Run the ingestion command:

```bash
python app/main.py
```

This will:

* Split documents into chunks
* Generate embeddings
* Store chunks and embeddings in the Postgres database

---

### 2. Run Chatbot

Continue asking questions about ingested documents:

```bash
python app/llm_query.py
```

Follow the prompts:

1. Select the document you want answers from
2. Ask questions in a loop (type `quit` or `exit` to stop)

---

### 3. Run Streamlit GUI

Start the new web interface:

```bash
streamlit run app/streamlit_app.py
```

Use the sidebar to switch between ingesting documents and chatting with them.

---

## License

This project is open source and free to use for learning, portfolio, or personal purposes.

```

