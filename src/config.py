import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM
    OLLAMA_CHAT_MODEL: str = "llama3.1:8b"
    OLLAMA_CHAT_BASE_URL: str = "http://localhost:11434"

    # Embedding
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    # ou pour Ollama : "nomic-embed-text"

    # Base de données
    DATABASE_URL: str = "sqlite:///data/processed/sportsee.db"

    # Observabilité
    LOGFIRE_TOKEN: str | None = None
    LOGFIRE_SERVICE_NAME: str = "sportsee-rag"
    ENVIRONMENT: str = "local"


settings = Settings()