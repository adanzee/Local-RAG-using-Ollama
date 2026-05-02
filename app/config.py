import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

@dataclass
class DatabaseConfig:
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "5432"))
    name: str = os.getenv("DB_NAME", "rag_db")
    user: str = os.getenv("DB_USER", "postgres")
    password: str = os.getenv("DB_PASSWORD", "")
    min_connections: int = int(os.getenv("DB_MIN_CONNECTIONS", "1"))
    max_connections: int = int(os.getenv("DB_MAX_CONNECTIONS", "10"))

@dataclass
class OllamaConfig:
    endpoint: str = os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434")
    model: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    temperature: float = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))
    timeout: int = int(os.getenv("OLLAMA_TIMEOUT", "60"))
    num_ctx: int = int(os.getenv("OLLAMA_NUM_CTX", "4096"))

@dataclass
class EmbeddingConfig:
    model_name: str = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
    batch_size: int = int(os.getenv("EMBEDDING_BATCH_SIZE", "4"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "500"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    top_k: int = int(os.getenv("TOP_K", "5"))
