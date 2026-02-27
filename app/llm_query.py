import os
import sys
import requests
import uuid

# Fixing the path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
lib_path = r"path_to_your_project"
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

from model import ModelHandler
from database import DatabaseHandler

# --- CONFIG ---
# Ensure these variables are defined or imported
DB_CONFIG = {
    "dbname": "dbname",
    "port": "port",
    "password": "password",
    "host": "host",
    "user": "user",
}


def get_llm_response(query, context, history_text):
    url = "http://localhost:11434/api/generate"

    # 1. BUILD THE PROMPT HERE (Inside the function where it has access to variables)
    query_prompt = f"""You are a helpful assistant. Use the following context and chat history to answer.
If the answer is not in the context, say you don't know. Be concise.

Chat History:
{history_text}

Context:
{context}

Question: {query}
AI Response:"""

    payload = {
        "model": "llama3.2:3b",
        "prompt": query_prompt,
        "stream": False,
        "options": {
            "num_ctx": 4096,  # Increased to accommodate history + context
            "temperature": 0.7,
        },
    }

    try:
        response = requests.post(url, json=payload)
        return response.json().get("response")
    except Exception as e:
        return f"Could not connect to Ollama. Error: {str(e)}"


def run_rag_pipeline(session_id, model_tool, db_tool, user_file):
    """This function handles one question-answer cycle for a specific document."""

    try:
        user_input = input("\n💬 Ask a question (type 'quit' to exit): ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Shutting down...")
            sys.exit()

        # 1️⃣ FETCH HISTORY
        raw_history = db_tool.get_recent_history(session_id, limit=3)
        formatted_history = ""
        for q, a in raw_history:
            formatted_history += f"User: {q}\nAI: {a}\n"

        # 2️⃣ RETRIEVE CONTEXT
        embed_query = model_tool.embed_text([user_input])[0]
        search_query = """
            SELECT content 
            FROM docs 
            WHERE docs_name = %s 
            ORDER BY embedding <=> %s::vector 
            LIMIT 5;
        """

        print("🔍 Searching database...")
        db_tool.cur.execute(search_query, (user_file, embed_query.tolist()))
        results = db_tool.cur.fetchall()

        if not results:
            print("❌ No matching chunks found.")
            return

        combined_context = "\n---\n".join([row[0] for row in results])

        # 3️⃣ GENERATE RESPONSE
        print("🔍 AI is thinking...")
        final_response = get_llm_response(
            user_input, combined_context, formatted_history
        )

        print("\n" + "=" * 60)
        print(f"💡 AI Response:\n{final_response}")
        print("=" * 60)

        # 4️⃣ SAVE THIS INTERACTION TO HISTORY
        db_tool.save_history(session_id, "user", user_input)
        db_tool.save_history(session_id, "assistant", final_response)

    except Exception as e:
        print("❌ Error in pipeline:", e)


if __name__ == "__main__":
    current_session_id = str(uuid.uuid4())
    model_tool = ModelHandler()
    db_tool = DatabaseHandler(**DB_CONFIG)

    try:
        print("\n" + "=" * 60)
        print("--- 🤖 Local RAG System Ready ---")

        # Ask for document ONCE
        user_file = input("From which document to get answers? ").strip()

        # Check if doc exists
        db_tool.cur.execute(
            "SELECT COUNT(*) FROM docs WHERE docs_name = %s", (user_file,)
        )
        if db_tool.cur.fetchone()[0] == 0:
            print(f"❌ Error: Document '{user_file}' not found.")
            sys.exit()

        # Main question-answer loop
        while True:
            run_rag_pipeline(current_session_id, model_tool, db_tool, user_file)

    finally:
        db_tool.close_connection()
