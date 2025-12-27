from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False

    # OpenAI Settings
    openai_api_key: str

    # Qdrant Settings
    qdrant_url: str
    qdrant_api_key: Optional[str] = None

    # Database Settings
    database_url: str

    # Application Settings
    app_name: str = "RAG Chatbot API"
    version: str = "1.0.0"
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()