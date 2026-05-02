import logging
import requests
from requests.exceptions import RequestException, Timeout
from app.config import OllamaConfig

logger = logging.getLogger(__name__)


class OllamaService:
    def __init__(self, config: OllamaConfig):
        self.config = config

    def build_prompt(self, question: str, context: str, history: str) -> str:
        return f"""You are a helpful assistant. Use the following context and chat history to answer the user's question.
If the answer is not in the context, say you don't know. Be concise.

Chat History:
{history}

Context:
{context}

Question: {question}
AI Response:"""

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": self.config.num_ctx,
                "temperature": self.config.temperature,
            },
        }

        try:
            response = requests.post(
                f"{self.config.endpoint}/api/generate",
                json=payload,
                timeout=self.config.timeout,
            )
            response.raise_for_status()
            result = response.json()
            answer = result.get("response")
            if answer is None:
                raise ValueError(f"Unexpected Ollama response: {result}")
            return answer.strip()
        except (RequestException, Timeout) as exc:
            logger.error("Ollama request failed: %s", exc)
            raise
