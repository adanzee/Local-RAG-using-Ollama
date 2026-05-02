import logging
from app.config import DatabaseConfig
from pgvector.psycopg2 import register_vector
from psycopg2 import pool

logger = logging.getLogger(__name__)


class DatabaseHandler:
    _pool = None

    def __init__(self, config: DatabaseConfig):
        if DatabaseHandler._pool is None:
            self.initialize_pool(config)

        self.conn = DatabaseHandler._pool.getconn()
        register_vector(self.conn)
        self.cur = self.conn.cursor()

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

    def insert_text(self, content, embedding, docs_name, file_hash=None, metadata=None):
        insert_query = """
            INSERT INTO docs (content, embedding, docs_name, file_hash, metadata)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cur.execute(insert_query, (content, embedding, docs_name, file_hash, metadata))
        self.conn.commit()

    def save_history(self, session_id, role, message):
        insert_chat = """
            INSERT INTO chat_history (session_id, role, message)
            VALUES (%s, %s, %s)
        """
        self.cur.execute(insert_chat, (session_id, role, message))
        self.conn.commit()

    def get_recent_history(self, session_id, limit=3):
        get_history = """
            SELECT role, message
            FROM chat_history
            WHERE session_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """
        self.cur.execute(get_history, (str(session_id), limit))
        rows = self.cur.fetchall()
        return rows[::-1]

    def list_documents(self):
        self.cur.execute("SELECT DISTINCT docs_name FROM docs ORDER BY docs_name")
        return [row[0] for row in self.cur.fetchall()]

    def document_exists(self, docs_name=None, file_hash=None):
        if file_hash is not None:
            self.cur.execute("SELECT 1 FROM docs WHERE file_hash = %s LIMIT 1", (file_hash,))
        elif docs_name is not None:
            self.cur.execute("SELECT 1 FROM docs WHERE docs_name = %s LIMIT 1", (docs_name,))
        else:
            return False

        return self.cur.fetchone() is not None

    def search_nearest(self, embedding, docs_name=None, top_k=5):
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

        self.cur.execute(query, params)
        return [
            {"content": row[0], "docs_name": row[1], "score": float(row[2])}
            for row in self.cur.fetchall()
        ]

    def close_connection(self):
        if hasattr(self, "cur"):
            self.cur.close()
        if hasattr(self, "conn") and DatabaseHandler._pool is not None:
            DatabaseHandler._pool.putconn(self.conn)
