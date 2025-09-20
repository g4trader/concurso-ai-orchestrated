"""
Configurações da aplicação OPS-002
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
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./observability.db")
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "false").lower() == "true"
    
    # Elasticsearch Configuration
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    ELASTICSEARCH_ENABLED: bool = os.getenv("ELASTICSEARCH_ENABLED", "false").lower() == "true"
    
    # Prometheus Configuration
    PROMETHEUS_ENABLED: bool = os.getenv("PROMETHEUS_ENABLED", "true").lower() == "true"
    PROMETHEUS_PORT: int = int(os.getenv("PROMETHEUS_PORT", "9090"))
    
    # Logging Configuration
    LOG_RETENTION_DAYS: int = int(os.getenv("LOG_RETENTION_DAYS", "30"))
    LOG_BATCH_SIZE: int = int(os.getenv("LOG_BATCH_SIZE", "100"))
    LOG_FLUSH_INTERVAL: int = int(os.getenv("LOG_FLUSH_INTERVAL", "5"))
    
    # Metrics Configuration
    METRICS_RETENTION_DAYS: int = int(os.getenv("METRICS_RETENTION_DAYS", "90"))
    METRICS_COLLECTION_INTERVAL: int = int(os.getenv("METRICS_COLLECTION_INTERVAL", "60"))
    
    # Health Check Configuration
    HEALTH_CHECK_INTERVAL: int = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))
    HEALTH_CHECK_TIMEOUT: int = int(os.getenv("HEALTH_CHECK_TIMEOUT", "10"))
    
    # Alerting Configuration
    ALERT_WEBHOOK_URL: str = os.getenv("ALERT_WEBHOOK_URL", "")
    ALERT_EMAIL_ENABLED: bool = os.getenv("ALERT_EMAIL_ENABLED", "false").lower() == "true"
    ALERT_SLACK_ENABLED: bool = os.getenv("ALERT_SLACK_ENABLED", "false").lower() == "true"
    
    # Service Discovery
    SERVICE_DISCOVERY_ENABLED: bool = os.getenv("SERVICE_DISCOVERY_ENABLED", "false").lower() == "true"
    CONSUL_URL: str = os.getenv("CONSUL_URL", "http://localhost:8500")
    
    # Security
    ALLOWED_HOSTS: List[str] = ["*"]
    SECURE_COOKIES: bool = os.getenv("SECURE_COOKIES", "false").lower() == "true"
    API_KEY: str = os.getenv("API_KEY", "observability-api-key")

settings = Settings()
