import logging
import threading
from app.config import DatabaseConfig
from pgvector.psycopg2 import register_vector
from psycopg2 import pool

logger = logging.getLogger(__name__)


class DatabaseHandler:
    _pool = None
    _pool_lock = threading.Lock()

    def __init__(self, config: DatabaseConfig):
        with DatabaseHandler._pool_lock:
            if DatabaseHandler._pool is None:
                self.initialize_pool(config)

        self.config = config

    @classmethod
    def initialize_pool(cls, config: DatabaseConfig):
        if cls._pool is not None:
            return

        cls._pool = pool.ThreadedConnectionPool(
            minconn=config.min_connections,
            maxconn=config.max_connections,
            dbname=config.name,
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
        )
        logger.info("Initialized Postgres connection pool")

    def _get_connection(self):
        return DatabaseHandler._pool.getconn()

    def _return_connection(self, conn):
        DatabaseHandler._pool.putconn(conn)

    def insert_text(self, content, embedding, docs_name, file_hash=None, metadata=None):
        conn = self._get_connection()
        try:
            register_vector(conn)
            with conn.cursor() as cur:
                insert_query = """
                    INSERT INTO docs (content, embedding, docs_name, file_hash, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cur.execute(insert_query, (content, embedding, docs_name, file_hash, metadata))
            conn.commit()
        finally:
            self._return_connection(conn)

    def delete_by_file_hash(self, file_hash):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM docs WHERE file_hash = %s", (file_hash,))
            conn.commit()
        finally:
            self._return_connection(conn)

    def save_history(self, session_id, role, message):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                insert_chat = """
                    INSERT INTO chat_history (session_id, role, message)
                    VALUES (%s, %s, %s)
                """
                cur.execute(insert_chat, (session_id, role, message))
            conn.commit()
        finally:
            self._return_connection(conn)

    def get_recent_history(self, session_id, limit=3):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                get_history = """
                    SELECT role, message
                    FROM chat_history
                    WHERE session_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                """
                cur.execute(get_history, (str(session_id), limit))
                rows = cur.fetchall()
                return rows[::-1]
        finally:
            self._return_connection(conn)

    def list_documents(self):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT docs_name FROM docs ORDER BY docs_name")
                return [row[0] for row in cur.fetchall()]
        finally:
            self._return_connection(conn)

    def document_exists(self, docs_name=None, file_hash=None):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                if file_hash is not None:
                    cur.execute("SELECT 1 FROM docs WHERE file_hash = %s LIMIT 1", (file_hash,))
                elif docs_name is not None:
                    cur.execute("SELECT 1 FROM docs WHERE docs_name = %s LIMIT 1", (docs_name,))
                else:
                    return False
                return cur.fetchone() is not None
        finally:
            self._return_connection(conn)

    def search_nearest(self, embedding, docs_name=None, top_k=5):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                if docs_name:
                    query = """
                        SELECT content, docs_name, embedding <=> %s::vector AS score
                        FROM docs
                        WHERE docs_name = %s
                        ORDER BY score
                        LIMIT %s
                    """
                    params = (embedding, docs_name, top_k)
                else:
                    query = """
                        SELECT content, docs_name, embedding <=> %s::vector AS score
                        FROM docs
                        ORDER BY score
                        LIMIT %s
                    """
                    params = (embedding, top_k)

                cur.execute(query, params)
                return [
                    {"content": row[0], "docs_name": row[1], "score": float(row[2])}
                    for row in cur.fetchall()
                ]
        finally:
            self._return_connection(conn)

    def close_connection(self):
        # No-op since we use per-operation connections now
        pass
