import logging
from sentence_transformers import SentenceTransformer
from app.config import EmbeddingConfig

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self, config: EmbeddingConfig):
        self.config = config
        self.model = SentenceTransformer(self.config.model_name)
        logger.info("Loaded embedding model %s", self.config.model_name)

    def embed_text(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        return self.model.encode(
            texts,
            batch_size=self.config.batch_size,
            convert_to_numpy=True,
            show_progress_bar=False,
            normalize_embeddings=False,
        )
