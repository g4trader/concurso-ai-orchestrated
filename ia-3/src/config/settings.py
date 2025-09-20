"""
Configurações da aplicação IA-3
"""

import os
from typing import List

class Settings:
    """Configurações da aplicação"""
    
    # Evaluation Configuration
    EVALUATION_TIMEOUT: int = int(os.getenv("EVALUATION_TIMEOUT", "300"))
    MAX_CONCURRENT_EVALUATIONS: int = int(os.getenv("MAX_CONCURRENT_EVALUATIONS", "5"))
    EVALUATION_BATCH_SIZE: int = int(os.getenv("EVALUATION_BATCH_SIZE", "10"))
    
    # Metrics Configuration
    TOPIC_HIT_RATE_THRESHOLD: float = float(os.getenv("TOPIC_HIT_RATE_THRESHOLD", "0.8"))
    STYLE_MATCH_THRESHOLD: float = float(os.getenv("STYLE_MATCH_THRESHOLD", "0.7"))
    ANSWERABILITY_THRESHOLD: float = float(os.getenv("ANSWERABILITY_THRESHOLD", "0.9"))
    
    # Benchmark Configuration
    BENCHMARK_TIMEOUT: int = int(os.getenv("BENCHMARK_TIMEOUT", "600"))
    BENCHMARK_DATASET_PATH: str = os.getenv("BENCHMARK_DATASET_PATH", "./data/benchmark")
    
    # Report Configuration
    REPORT_FORMATS: List[str] = ["json", "csv", "html"]
    REPORT_TEMPLATE_PATH: str = os.getenv("REPORT_TEMPLATE_PATH", "./templates")
    
    # Cache Configuration
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    
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
    
    # Storage
    DATA_DIR: str = os.getenv("DATA_DIR", "./data")
    REPORTS_DIR: str = os.getenv("REPORTS_DIR", "./reports")
    CACHE_DIR: str = os.getenv("CACHE_DIR", "./cache")

settings = Settings()
