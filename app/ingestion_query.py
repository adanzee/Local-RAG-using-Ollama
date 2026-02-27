from model import ModelHandler
from database import DatabaseHandler


def retrieve_relevant_chunks():
    query_model = ModelHandler()
    db = DatabaseHandler(
        dbname="db_name", port="port", password="password", host="hos", user="user"
    )

    # Getting the user query and embedding it
    user_query = input("\n💬 What would you like to know from the PDF? ")
    embedquery = query_model.embed_text([user_query])[
        0
    ]  # Get the embedding for the user query

    # Finding the distance between embeddings
    search_query = """SELECT content, embedding <=> %s AS distance
    FROM docs
    ORDER BY distance ASC
    LIMIT 5;
    """
    db.cur.execute(search_query, (embedquery,))
    results = db.cur.fetchall()

    print("\n📄 Top 3 relevant chunks from the PDF:")
    for i, (content, distance) in enumerate(results):
        print(f"Chunk {i + 1} (Distance: {distance:.4f}): {content}\n{'---' * 40}")

    db.close_connection()


if __name__ == "__main__":
    retrieve_relevant_chunks()
