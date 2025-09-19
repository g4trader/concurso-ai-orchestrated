"""
Configurações da aplicação IA-2
"""

import os
from typing import List

class Settings:
    """Configurações da aplicação"""
    
    # LLM Configuration
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama-3.1-8b")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2048"))
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "30"))
    
    # Generation Configuration
    MAX_QUESTIONS_PER_BATCH: int = int(os.getenv("MAX_QUESTIONS_PER_BATCH", "10"))
    MAX_PARALLEL_GENERATIONS: int = int(os.getenv("MAX_PARALLEL_GENERATIONS", "5"))
    GENERATION_TIMEOUT: int = int(os.getenv("GENERATION_TIMEOUT", "30"))
    
    # Validation Configuration
    VALIDATION_LEVEL: str = os.getenv("VALIDATION_LEVEL", "strict")  # strict, medium, loose
    CONSISTENCY_THRESHOLD: float = float(os.getenv("CONSISTENCY_THRESHOLD", "0.8"))
    PLAGIARISM_THRESHOLD: float = float(os.getenv("PLAGIARISM_THRESHOLD", "0.3"))
    QUALITY_THRESHOLD: float = float(os.getenv("QUALITY_THRESHOLD", "0.9"))
    
    # Self-Consistency Configuration
    CONSISTENCY_CHECKS: int = int(os.getenv("CONSISTENCY_CHECKS", "2"))
    CONSISTENCY_TIMEOUT: int = int(os.getenv("CONSISTENCY_TIMEOUT", "10"))
    
    # Anti-Plagiarism Configuration
    PLAGIARISM_CHECK_ENABLED: bool = os.getenv("PLAGIARISM_CHECK_ENABLED", "true").lower() == "true"
    PLAGIARISM_TIMEOUT: int = int(os.getenv("PLAGIARISM_TIMEOUT", "5"))
    
    # Quality Assessment Configuration
    QUALITY_METRICS: List[str] = ["plausibility", "consistency", "clarity", "difficulty"]
    QUALITY_WEIGHTS: dict = {
        "plausibility": 0.4,
        "consistency": 0.3,
        "clarity": 0.2,
        "difficulty": 0.1
    }
    
    # Prompt Configuration
    PROMPT_CACHE_ENABLED: bool = os.getenv("PROMPT_CACHE_ENABLED", "true").lower() == "true"
    PROMPT_CACHE_TTL: int = int(os.getenv("PROMPT_CACHE_TTL", "3600"))
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8002"))
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
    PROMPTS_DIR: str = os.getenv("PROMPTS_DIR", "./prompts")
    CACHE_DIR: str = os.getenv("CACHE_DIR", "./cache")
    
    # Ollama Configuration
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "60"))

settings = Settings()
