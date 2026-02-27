import psycopg2
from pgvector.psycopg2 import register_vector


class DatabaseHandler:
    def __init__(self, dbname, port, password, user, host):
        # establishing the connection to db
        self.connection = psycopg2.connect(
            dbname=dbname, port=port, password=password, host=host, user=user
        )

        # registering pgvector
        register_vector(self.connection)
        self.cur = self.connection.cursor()

    def insert_text(self, context, embedding, docs_name):
        # inserting the text and embedding into the db
        insert_query = (
            " INSERT INTO docs (content, embedding, docs_name) VALUES (%s, %s, %s)"
        )
        self.cur.execute(insert_query, (context, embedding, docs_name))
        self.connection.commit()

    def save_history(self, session_id, role, message):
        insert_chat = """
            INSERT INTO chat_history (session_id, role, message)
            VALUES (%s, %s, %s)
        """
        self.cur.execute(insert_chat, (session_id, role, message))
        self.connection.commit()

    def get_recent_history(self, session_id, limit=3):
        # the recent change
        get_history = """
            SELECT role, message
            FROM chat_history
            WHERE session_id = %s
            ORDER BY created_at DESC
            LIMIT %s
            """

        params = (str(session_id), (limit))

        self.cur.execute(get_history, params)
        rows = self.cur.fetchall()
        # reversing the order
        return rows[::-1]

    def close_connection(self):
        # closing the connection to db
        self.cur.close()
        self.connection.close()
