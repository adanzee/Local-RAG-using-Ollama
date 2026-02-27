# the orchestrator of the entire RAG pipeline, responsible for coordinating the ingestion, chunking
# , and retrieval processes. It will also handle interactions with the LLM and vector database.
from ingestion import extract_text_from_file
from chunking import chunk_text


def load_and_process_document(file_path):
    # extract text from document
    text = extract_text_from_file(file_path)
    print("Extracted text length:", len(text))
    # chunk the text
    chunks = chunk_text(text)
    print("Number of chunks created:", len(chunks))
    return chunks
