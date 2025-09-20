"""
Configurações da aplicação IA-1
"""

import os
from typing import List

class Settings:
    """Configurações da aplicação"""
    
    # Pipeline Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "512"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    SUPPORTED_FORMATS: List[str] = ["pdf", "txt", "docx", "png", "jpg", "jpeg"]
    
    # Embedding Configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", "1024"))
    EMBEDDING_BATCH_SIZE: int = int(os.getenv("EMBEDDING_BATCH_SIZE", "32"))
    
    # Reranker Configuration
    RERANKER_MODEL: str = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-large")
    RERANKER_TOP_K: int = int(os.getenv("RERANKER_TOP_K", "10"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    
    # FAISS Configuration
    FAISS_INDEX_TYPE: str = os.getenv("FAISS_INDEX_TYPE", "IndexFlatIP")
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "./data/faiss_index")
    FAISS_METADATA_PATH: str = os.getenv("FAISS_METADATA_PATH", "./data/metadata")
    
    # Parser Configuration
    PYMUPDF_TIMEOUT: int = int(os.getenv("PYMUPDF_TIMEOUT", "30"))
    TESSERACT_TIMEOUT: int = int(os.getenv("TESSERACT_TIMEOUT", "60"))
    OCR_LANGUAGE: str = os.getenv("OCR_LANGUAGE", "por")
    
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
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    BACKUP_DIR: str = os.getenv("BACKUP_DIR", "./backups")

settings = Settings()
