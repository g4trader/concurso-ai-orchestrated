#!/usr/bin/env python3
"""
Script para executar o backend
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    from app.config import settings
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
        log_level="info"
    )
