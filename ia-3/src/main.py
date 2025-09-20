#!/usr/bin/env python3
"""
IA-3 Avaliação Offline - Main Application
Sistema de avaliação offline para medir qualidade de simulados gerados
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.config.settings import settings
from src.api.routes import router
from src.utils.logger import setup_logging

# Configurar logging
setup_logging()

# Inicializar FastAPI
app = FastAPI(
    title="IA-3 Avaliação Offline",
    description="Sistema de avaliação offline para medir qualidade de simulados gerados usando métricas objetivas",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
