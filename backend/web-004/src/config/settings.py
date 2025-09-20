"""
Configurações da aplicação WEB-004
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
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./results.db")
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "false").lower() == "true"
    
    # Celery Configuration
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # Analytics Configuration
    MIN_SCORE_THRESHOLD: float = float(os.getenv("MIN_SCORE_THRESHOLD", "60.0"))
    MAX_TIME_PER_QUESTION: int = int(os.getenv("MAX_TIME_PER_QUESTION", "300"))
    WEAK_POINT_THRESHOLD: float = float(os.getenv("WEAK_POINT_THRESHOLD", "0.5"))
    
    # Export Configuration
    MAX_EXPORT_SIZE: int = int(os.getenv("MAX_EXPORT_SIZE", "10000"))
    EXPORT_FORMATS: List[str] = ["pdf", "excel", "csv", "json"]
    EXPORT_TTL_HOURS: int = int(os.getenv("EXPORT_TTL_HOURS", "24"))
    
    # Share Configuration
    SHARE_TOKEN_LENGTH: int = int(os.getenv("SHARE_TOKEN_LENGTH", "32"))
    SHARE_TOKEN_EXPIRY_HOURS: int = int(os.getenv("SHARE_TOKEN_EXPIRY_HOURS", "168"))  # 7 days
    
    # Cache Configuration
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
    
    # Security
    ALLOWED_HOSTS: List[str] = ["*"]
    SECURE_COOKIES: bool = os.getenv("SECURE_COOKIES", "false").lower() == "true"

settings = Settings()
