import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
lib_path = r"path_to_your_project"
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)


from model import ModelHandler
from database import DatabaseHandler
from engine import load_and_process_document


if __name__ == "__main__":
    file_path = input("Enter the path to the document: ")
    chunks = load_and_process_document(file_path)
    print("Generating embeddings for chunk!")
    modelhandler = ModelHandler()

    print("opening a db connection")
    db = DatabaseHandler(
        dbname="dbname", port=port, password="password", host="host", user="user"
    )
    outer_batch_size = 8
    for i in range(0, len(chunks), outer_batch_size):
        batch_chunks = chunks[i : i + outer_batch_size]
        embeddings = modelhandler.embed_text(batch_chunks)

        print("Embeddings for the first chunk:", embeddings.shape)
        print("Chunks created from the document:")

        # Storing the chunks and embeddings in db
        docs_name = os.path.basename(file_path)
        for txt, vec in zip(batch_chunks, embeddings):
            db.insert_text(txt, vec.tolist(), docs_name)

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}: {chunk} \n {'---' * 40}")

    print("All chunks and embeddings stored successfully in the database!")
    db.close_connection()
    print("RAG pipeline executed successfully!")
