"""
Configurações da aplicação UX-001
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
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./feedback.db")
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "false").lower() == "true"
    
    # Celery Configuration
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # Elasticsearch Configuration
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    ELASTICSEARCH_ENABLED: bool = os.getenv("ELASTICSEARCH_ENABLED", "false").lower() == "true"
    
    # Feedback Configuration
    MAX_FEEDBACK_LENGTH: int = int(os.getenv("MAX_FEEDBACK_LENGTH", "1000"))
    MIN_FEEDBACK_LENGTH: int = int(os.getenv("MIN_FEEDBACK_LENGTH", "10"))
    FEEDBACK_CATEGORIES: List[str] = [
        "error_in_question",
        "typo_in_question", 
        "unclear_question",
        "wrong_answer",
        "suggestion",
        "compliment",
        "other"
    ]
    
    # Draft Configuration
    DRAFT_TTL_HOURS: int = int(os.getenv("DRAFT_TTL_HOURS", "24"))
    MAX_DRAFTS_PER_USER: int = int(os.getenv("MAX_DRAFTS_PER_USER", "10"))
    
    # Analytics Configuration
    ANALYTICS_RETENTION_DAYS: int = int(os.getenv("ANALYTICS_RETENTION_DAYS", "365"))
    BULK_FEEDBACK_LIMIT: int = int(os.getenv("BULK_FEEDBACK_LIMIT", "50"))
    
    # Notification Configuration
    NOTIFICATION_ENABLED: bool = os.getenv("NOTIFICATION_ENABLED", "false").lower() == "true"
    EMAIL_NOTIFICATIONS: bool = os.getenv("EMAIL_NOTIFICATIONS", "false").lower() == "true"
    
    # Cache Configuration
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
    
    # Security
    ALLOWED_HOSTS: List[str] = ["*"]
    SECURE_COOKIES: bool = os.getenv("SECURE_COOKIES", "false").lower() == "true"

settings = Settings()
