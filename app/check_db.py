# testing the db to see which things are working and which are not
import numpy as np
from database import DatabaseHandler


def test_handshake():
    print("Connecting to database...")
    try:
        # intilialize the database handler
        db = DatabaseHandler(
            dbname="rag_db",
            port=5432,
            password="@123",
            host="localhost",
            user="postgres",
        )

        print("Connection successful!")

        # before attaching the pdf file testing the dummy
        test_text = (
            "This is a test text to check the database connection and insertion."
        )
        # using dummy with numpy to create a vector representation of the text also the model output is this and further
        # to feed this to db convert into list and then to string
        test_vector = (
            np.random.rand(384).astype(np.float32).tolist()
        )  # creating a random vector of size 384 for testing

        print("Inserting dummy text into the database...")
        # inserting the dummy text and vector into the database
        db.insert_text(test_text, test_vector)
        print("Dummy text inserted successfully!")
    except Exception as e:
        print("Error connecting to database:", e)
        print("Error details:", {e})


if __name__ == "__main__":
    test_handshake()
