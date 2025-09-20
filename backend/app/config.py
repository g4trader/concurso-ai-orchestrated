from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./concurso_ai.db"
    database_url_test: str = "sqlite:///./concurso_ai_test.db"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    frontend_url: str = "http://localhost:3000"
    
    # Environment
    environment: str = "development"
    
    # Railway/Production settings
    port: int = 8000
    host: str = "0.0.0.0"
    
    # Production database (Railway/PostgreSQL)
    railway_database_url: Optional[str] = None
    
    class Config:
        env_file = ".env"


settings = Settings()
