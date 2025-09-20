"""
Configurações da aplicação WEB-003
"""

import os
from typing import List

class Settings:
    """Configurações da aplicação"""
    
    # API Configuration
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
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./simulado.db")
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "false").lower() == "true"
    
    # Celery Configuration
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # Simulado Configuration
    MAX_QUESTIONS_PER_SIMULADO: int = int(os.getenv("MAX_QUESTIONS_PER_SIMULADO", "100"))
    MIN_QUESTIONS_PER_SIMULADO: int = int(os.getenv("MIN_QUESTIONS_PER_SIMULADO", "1"))
    MAX_TIME_LIMIT_MINUTES: int = int(os.getenv("MAX_TIME_LIMIT_MINUTES", "300"))
    MIN_TIME_LIMIT_MINUTES: int = int(os.getenv("MIN_TIME_LIMIT_MINUTES", "30"))
    
    # Generation Configuration
    GENERATION_TIMEOUT_SECONDS: int = int(os.getenv("GENERATION_TIMEOUT_SECONDS", "300"))
    MAX_CONCURRENT_GENERATIONS: int = int(os.getenv("MAX_CONCURRENT_GENERATIONS", "5"))
    
    # External Services
    IA_1_URL: str = os.getenv("IA_1_URL", "https://ia-1-ingestion-service-609095880025.us-central1.run.app")
    IA_2_URL: str = os.getenv("IA_2_URL", "https://ia-2-generation-service-609095880025.us-central1.run.app")
    IA_3_URL: str = os.getenv("IA_3_URL", "https://ia-3-evaluation-service-609095880025.us-central1.run.app")
    
    # Cache Configuration
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
    
    # Security
    ALLOWED_HOSTS: List[str] = ["*"]
    SECURE_COOKIES: bool = os.getenv("SECURE_COOKIES", "false").lower() == "true"

settings = Settings()
