import hashlib
import logging
from pathlib import Path
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


def compute_file_hash(file_path: str) -> str:
    hasher = hashlib.sha256()
    path = Path(file_path)
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


class IngestionService:
    def __init__(self, db_handler, embedding_service: EmbeddingService, chunking_service: ChunkingService):
        self.db_handler = db_handler
        self.embedding_service = embedding_service
        self.chunking_service = chunking_service

    def ingest_file(self, file_path: str) -> int:
        text = DocumentService.extract_text_from_file(file_path)
        chunks = self.chunking_service.chunk_text(text)
        if not chunks:
            raise ValueError("The document did not contain any text to ingest.")

        file_hash = compute_file_hash(file_path)
        if self.db_handler.document_exists(file_hash=file_hash):
            logger.info("File '%s' already exists in the database.", file_path)
            return 0

        embedding_vectors = self.embedding_service.embed_text(chunks)
        docs_name = Path(file_path).name

        for chunk, vector in zip(chunks, embedding_vectors):
            self.db_handler.insert_text(
                chunk,
                vector.tolist(),
                docs_name,
                file_hash=file_hash,
            )

        logger.info("Ingested %d chunks from %s", len(chunks), docs_name)
        return len(chunks)
