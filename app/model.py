# load and deal with model related code, such as embedding model and LLM model, and also the vector database client
from sentence_transformers import SentenceTransformer


class ModelHandler:
    def __init__(self, embedding_model_name="all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(embedding_model_name)

    def embed_text(self, text):

        # using inner batch size inorder to handle large number of chunks and avoid memory issues,
        # also showing progress bar for better user experience
        return self.embedding_model.encode(
            text,
            batch_size=4,
            convert_to_numpy=True,
            show_progress_bar=True,
            normalize_embeddings=False,
        )
