import os
import logging
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

logger = logging.getLogger(__name__)

def parse_int_env(var_name: str, default: int) -> int:
    value = os.getenv(var_name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        logger.warning(f"Invalid {var_name} value '{value}', using default {default}")
        return default

def parse_float_env(var_name: str, default: float) -> float:
    value = os.getenv(var_name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        logger.warning(f"Invalid {var_name} value '{value}', using default {default}")
        return default

@dataclass
class DatabaseConfig:
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = parse_int_env("DB_PORT", 5432)
    name: str = os.getenv("DB_NAME", "rag_db")
    user: str = os.getenv("DB_USER", "postgres")
    password: str = os.getenv("DB_PASSWORD", "")
    min_connections: int = parse_int_env("DB_MIN_CONNECTIONS", 1)
    max_connections: int = parse_int_env("DB_MAX_CONNECTIONS", 10)

    def __post_init__(self):
        if not (1 <= self.port <= 65535):
            raise ValueError(f"DB_PORT must be between 1 and 65535, got {self.port}")
        if self.min_connections <= 0:
            raise ValueError(f"DB_MIN_CONNECTIONS must be positive, got {self.min_connections}")
        if self.max_connections <= 0:
            raise ValueError(f"DB_MAX_CONNECTIONS must be positive, got {self.max_connections}")
        if self.min_connections > self.max_connections:
            raise ValueError(f"DB_MIN_CONNECTIONS ({self.min_connections}) cannot be greater than DB_MAX_CONNECTIONS ({self.max_connections})")

@dataclass
class OllamaConfig:
    endpoint: str = os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434")
    model: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    temperature: float = parse_float_env("OLLAMA_TEMPERATURE", 0.7)
    timeout: int = parse_int_env("OLLAMA_TIMEOUT", 60)
    num_ctx: int = parse_int_env("OLLAMA_NUM_CTX", 4096)

    def __post_init__(self):
        if not (0.0 <= self.temperature <= 2.0):
            raise ValueError(f"OLLAMA_TEMPERATURE must be between 0.0 and 2.0, got {self.temperature}")
        if self.timeout <= 0:
            raise ValueError(f"OLLAMA_TIMEOUT must be positive, got {self.timeout}")
        if self.num_ctx <= 0:
            raise ValueError(f"OLLAMA_NUM_CTX must be positive, got {self.num_ctx}")

@dataclass
class EmbeddingConfig:
    model_name: str = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
    batch_size: int = parse_int_env("EMBEDDING_BATCH_SIZE", 4)
    chunk_size: int = parse_int_env("CHUNK_SIZE", 500)
    chunk_overlap: int = parse_int_env("CHUNK_OVERLAP", 50)
    top_k: int = parse_int_env("TOP_K", 5)

    def __post_init__(self):
        if self.batch_size <= 0:
            raise ValueError(f"EMBEDDING_BATCH_SIZE must be positive, got {self.batch_size}")
        if self.chunk_size <= 0:
            raise ValueError(f"CHUNK_SIZE must be positive, got {self.chunk_size}")
        if self.chunk_overlap <= 0:
            raise ValueError(f"CHUNK_OVERLAP must be positive, got {self.chunk_overlap}")
        if self.top_k <= 0:
            raise ValueError(f"TOP_K must be positive, got {self.top_k}")
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(f"CHUNK_OVERLAP ({self.chunk_overlap}) must be less than CHUNK_SIZE ({self.chunk_size})")
