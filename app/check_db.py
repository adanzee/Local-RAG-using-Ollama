# testing the db to see which things are working and which are not
import numpy as np
from app.config import DatabaseConfig
from app.database import DatabaseHandler


def test_handshake():
    print("Connecting to database...")
    db = None
    try:
        db = DatabaseHandler(DatabaseConfig())
        print("Connection successful!")

        test_text = "This is a test text to check the database connection and insertion."
        test_vector = np.random.rand(384).astype(np.float32).tolist()

        print("Inserting dummy text into the database...")
        db.insert_text(test_text, test_vector, "test_document", file_hash="test-handshake")
        print("Dummy text inserted successfully!")

        # Clean up the test record
        db.delete_by_file_hash("test-handshake")
        print("Test record cleaned up.")

    except Exception as e:
        print("Error connecting to database:", e)

    finally:
        if db is not None:
            db.close_connection()


if __name__ == "__main__":
    test_handshake()
