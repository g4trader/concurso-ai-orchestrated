"""
Configurações da aplicação IA-0
"""

import os
from typing import List

class Settings:
    """Configurações da aplicação"""
    
    # Ollama
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "30"))
    OLLAMA_MAX_RETRIES: int = int(os.getenv("OLLAMA_MAX_RETRIES", "3"))
    
    # Modelos
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "qwen2:7b")
    AVAILABLE_MODELS: List[str] = [
        "qwen2:7b",
        "llama3.1:8b",
        "mistral:7b"
    ]
    
    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_RELOAD: bool = os.getenv("API_RELOAD", "true").lower() == "true"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://vercel.app"
    ]

settings = Settings()
