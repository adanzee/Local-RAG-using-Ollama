import logging
import os
from app.config import DatabaseConfig, EmbeddingConfig
from app.database import DatabaseHandler
from app.logging_config import configure_logging
from app.services.embedding_service import EmbeddingService
from app.services.chunking_service import ChunkingService
from app.services.ingestion_service import IngestionService


def main():
    configure_logging()
    logger = logging.getLogger(__name__)
    db = None

    try:
        db = DatabaseHandler(DatabaseConfig())
        embedding_service = EmbeddingService(EmbeddingConfig())
        chunking_service = ChunkingService(EmbeddingConfig())
        ingestion_service = IngestionService(db, embedding_service, chunking_service)

        file_path = input("Enter the path to the document: ").strip()

        # Validate file path
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"File does not exist: {abs_path}")
        if not os.path.isfile(abs_path):
            raise ValueError(f"Path is not a file: {abs_path}")
        # Prevent path traversal
        if ".." in abs_path or not abs_path.startswith(os.getcwd()):
            raise ValueError(f"Invalid path: {abs_path}")

        chunk_count = ingestion_service.ingest_file(abs_path)

        if chunk_count == 0:
            print("Document already exists in the database.")
        else:
            print(f"Successfully ingested {chunk_count} chunks.")

    except Exception as exc:
        logger.exception("Failed to ingest document")
        print(f"Error during ingestion: {exc}")
    finally:
        if db is not None:
            db.close_connection()


if __name__ == "__main__":
    main()
