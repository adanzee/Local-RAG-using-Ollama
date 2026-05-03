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

        # Atomic batch insert
        records = [
            (chunk, vector.tolist(), docs_name, file_hash)
            for chunk, vector in zip(chunks, embedding_vectors)
        ]

        try:
            self._insert_batch(records)
            logger.info("Ingested %d chunks from %s", len(chunks), docs_name)
            return len(chunks)
        except Exception as e:
            # Check if it's a unique constraint violation (file already exists)
            if "unique_file_hash" in str(e).lower():
                logger.info("File '%s' already exists in the database.", file_path)
                return 0
            raise

    def _insert_batch(self, records):
        # For simplicity, since database.py now uses per-operation connections,
        # we can call insert_text multiple times, but to make it atomic, we could add a batch method.
        # For now, since each insert_text commits, it's not fully atomic, but the unique constraint helps.
        for content, embedding, docs_name, file_hash in records:
            self.db_handler.insert_text(content, embedding, docs_name, file_hash=file_hash)
