from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "dev"

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "documents"
    embedding_model: str = "mxbai-embed-large"
    embedding_dim: int = 1024

    otel_endpoint: Optional[str] = None
    openai_api_key: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
