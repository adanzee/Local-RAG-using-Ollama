import os
import tempfile
import uuid
import streamlit as st
from app.config import DatabaseConfig, EmbeddingConfig, OllamaConfig
from app.database import DatabaseHandler
from app.logging_config import configure_logging
from app.services.embedding_service import EmbeddingService
from app.services.ingestion_service import IngestionService
from app.services.llm_service import OllamaService
from app.services.query_service import QueryService
from app.services.chunking_service import ChunkingService

configure_logging()

@st.cache_resource
def create_db_handler():
    db_config = DatabaseConfig()
    return DatabaseHandler(db_config)

@st.cache_resource
def create_embedding_service():
    return EmbeddingService(EmbeddingConfig())

@st.cache_resource
def create_llm_service():
    return OllamaService(OllamaConfig())

@st.cache_resource
def create_chunking_service():
    return ChunkingService(EmbeddingConfig())

@st.cache_resource
def create_services():
    db_handler = create_db_handler()
    return {
        "db_handler": db_handler,
        "ingestion_service": IngestionService(
            db_handler,
            create_embedding_service(),
            create_chunking_service(),
        ),
        "query_service": QueryService(
            db_handler,
            create_embedding_service(),
            create_llm_service(),
            EmbeddingConfig(),
        ),
    }

services = create_services()

def show_sidebar():
    st.sidebar.title("Local RAG using Ollama")
    st.sidebar.markdown("Built with Streamlit, Postgres, and local Ollama.")
    return st.sidebar.selectbox("Choose a page", ["Ingest Document", "Chat"])


def save_uploaded_file(uploaded_file):
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.read())
        return temp_file.name


def ingestion_page():
    st.header("Document Ingestion")
    st.write("Upload a PDF or DOCX file and ingest it into the RAG database.")

    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx"])
    file_path = st.text_input("Or enter a local file path:")

    if st.button("Ingest Document"):
        try:
            if uploaded_file is not None:
                path = save_uploaded_file(uploaded_file)
                try:
                    count = services["ingestion_service"].ingest_file(path)
                    if count == 0:
                        st.info("This document is already ingested.")
                    else:
                        st.success(f"Ingested {count} chunks successfully.")
                finally:
                    os.unlink(path)  # Clean up temp file
            else:
                path = file_path.strip()
                if not path:
                    st.error("Please upload a file or provide a valid path.")
                    return
                count = services["ingestion_service"].ingest_file(path)
                if count == 0:
                    st.info("This document is already ingested.")
                else:
                    st.success(f"Ingested {count} chunks successfully.")
        except Exception as exc:
            st.error(f"Ingestion failed: {exc}")

    st.markdown("---")
    st.subheader("Documents in database")
    documents = services["query_service"].list_documents()
    if documents:
        for doc in documents:
            st.write(f"- {doc}")
    else:
        st.info("No documents have been ingested yet.")


def chat_page():
    st.header("Chat with your documents")
    documents = services["query_service"].list_documents()
    if not documents:
        st.info("Ingest a document first on the Ingest Document page.")
        return

    selected_doc = st.selectbox("Select a document", documents)
    question = st.text_input("Ask a question about the selected document:")

    if st.button("Ask"):
        if not question.strip():
            st.error("Ask a non-empty question.")
            return

        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

        try:
            answer = services["query_service"].answer_question(
                selected_doc,
                question,
                st.session_state.session_id,
            )
            st.markdown("**Answer:**")
            st.write(answer)
        except Exception as exc:
            st.error(f"Query failed: {exc}")

    st.markdown("---")
    st.subheader("Recent history")
    if "session_id" in st.session_state:
        history_rows = services["query_service"].db_handler.get_recent_history(
            st.session_state.session_id, limit=10
        )
        if history_rows:
            for role, message in history_rows:
                st.write(f"**{role.title()}:** {message}")
        else:
            st.info("No chat history for this session yet.")
    else:
        st.info("Start a chat session by asking a question.")


def main():
    page = show_sidebar()
    if page == "Ingest Document":
        ingestion_page()
    else:
        chat_page()


if __name__ == "__main__":
    main()
