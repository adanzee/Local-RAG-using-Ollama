import logging
import sys
import uuid
from app.config import DatabaseConfig, EmbeddingConfig, OllamaConfig
from app.database import DatabaseHandler
from app.logging_config import configure_logging
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import OllamaService
from app.services.query_service import QueryService


def select_document(documents):
    print("Available documents:")
    for index, doc_name in enumerate(documents, start=1):
        print(f"{index}. {doc_name}")

    selection = input("Select a document by number or name: ").strip()
    if selection.isdigit():
        index = int(selection) - 1
        if 0 <= index < len(documents):
            return documents[index]
    if selection in documents:
        return selection
    raise ValueError("Invalid document selection.")


def run_rag_pipeline(session_id, document_name, query_service):
    question = input("\n💬 Ask a question (type 'quit' to exit): ").strip()
    if question.lower() in ["quit", "exit", "q"]:
        print("Shutting down...")
        sys.exit()

    answer = query_service.answer_question(document_name, question, session_id)
    print("\n" + "=" * 60)
    print(f"💡 AI Response:\n{answer}")
    print("=" * 60)


def main():
    configure_logging()
    logger = logging.getLogger(__name__)

    db = None
    try:
        db = DatabaseHandler(DatabaseConfig())
        embedding_service = EmbeddingService(EmbeddingConfig())
        llm_service = OllamaService(OllamaConfig())
        query_service = QueryService(db, embedding_service, llm_service, EmbeddingConfig())

        documents = query_service.list_documents()
        if not documents:
            print("No documents are available in the database. Please ingest a document first.")
            return

        document_name = select_document(documents)
        session_id = str(uuid.uuid4())

        while True:
            run_rag_pipeline(session_id, document_name, query_service)

    except Exception as exc:
        logger.exception("Error while running query loop")
        print(f"Error: {exc}")

    finally:
        if db is not None:
            db.close_connection()


if __name__ == "__main__":
    main()
