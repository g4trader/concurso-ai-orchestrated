from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import os

# Choose database URL based on environment
database_url = settings.database_url

# Check for Railway PostgreSQL URL in production
if os.getenv("RAILWAY_DATABASE_URL"):
    database_url = os.getenv("RAILWAY_DATABASE_URL")
elif os.getenv("DATABASE_URL"):
    database_url = os.getenv("DATABASE_URL")

# Create database engine
engine = create_engine(database_url)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
