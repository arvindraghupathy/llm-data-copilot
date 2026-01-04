import ollama
from typing import List
from app.core.config import settings

def embed_text(text: str) -> List[float]:
    """
    Generate an embedding vector for a query.
    """
    response = ollama.embeddings(
        model=settings.embedding_model,
        prompt=text,
    )

    return response["embedding"]
