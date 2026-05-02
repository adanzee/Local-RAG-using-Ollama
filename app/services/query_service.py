import logging
from app.config import EmbeddingConfig
from app.services.llm_service import OllamaService

logger = logging.getLogger(__name__)


class QueryService:
    def __init__(self, db_handler, embedding_service, llm_service: OllamaService, config: EmbeddingConfig):
        self.db_handler = db_handler
        self.embedding_service = embedding_service
        self.llm_service = llm_service
        self.top_k = config.top_k

    def list_documents(self):
        return self.db_handler.list_documents()

    def answer_question(self, document_name: str, question: str, session_id: str):
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        history_rows = self.db_handler.get_recent_history(session_id, limit=5)
        formatted_history = "\n".join(
            f"{role}: {message}" for role, message in history_rows
        )
        embed_query = self.embedding_service.embed_text([question])[0]
        results = self.db_handler.search_nearest(
            embed_query.tolist(), docs_name=document_name, top_k=self.top_k
        )

        if not results:
            return "No relevant context was found for this document."

        combined_context = "\n---\n".join(item["content"] for item in results)
        prompt = self.llm_service.build_prompt(question, combined_context, formatted_history)
        answer = self.llm_service.generate(prompt)

        self.db_handler.save_history(session_id, "user", question)
        self.db_handler.save_history(session_id, "assistant", answer)

        return answer
