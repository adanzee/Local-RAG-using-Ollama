import logging
from app.config import EmbeddingConfig

logger = logging.getLogger(__name__)


def _find_split_boundary(text: str, start: int, end: int) -> int:
    for separator in ["\n\n", "\n", ". ", " "]:
        split_at = text.rfind(separator, start, end)
        if split_at > start:
            return split_at + len(separator)
    return end


class ChunkingService:
    def __init__(self, config: EmbeddingConfig):
        self.chunk_size = config.chunk_size
        self.overlap = config.chunk_overlap

    def chunk_text(self, text: str):
        text = text.strip()
        if not text:
            return []

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + self.chunk_size, text_length)

            if end < text_length:
                end = _find_split_boundary(text, start, end)

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            if end >= text_length:
                break

            start = max(0, end - self.overlap)
            if start >= end:
                start = end - 1  # Ensure forward progress

        logger.info("Chunked text into %d pieces", len(chunks))
        return chunks
