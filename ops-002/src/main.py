#!/usr/bin/env python3
"""
OPS-002 Observabilidade Básica - Main Application
Sistema de observabilidade com logs, métricas e health checks
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
    title="OPS-002 Observabilidade Básica",
    description="Sistema de observabilidade com logs, métricas, health checks e alertas para monitoramento de aplicações",
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
