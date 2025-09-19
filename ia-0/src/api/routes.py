"""
Rotas da API IA-0
"""

from fastapi import APIRouter, HTTPException
from typing import List
from src.models.request import QuestionRequest, BatchQuestionRequest
from src.models.response import QuestionResponse, HealthResponse, ModelInfo
from src.services.ollama_service import OllamaService
from src.services.health_check import HealthCheckService

router = APIRouter(prefix="/api/v1", tags=["ia-0"])

# Dependências
ollama_service = OllamaService()
health_service = HealthCheckService()

@router.get("/", response_model=dict)
async def root():
    """Endpoint raiz"""
    return {
        "service": "IA-0 Ollama Service",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check da aplicação"""
    return await health_service.check_health()

@router.get("/models", response_model=List[ModelInfo])
async def list_models():
    """Listar modelos disponíveis"""
    return await ollama_service.list_models()

@router.post("/generate", response_model=QuestionResponse)
async def generate_question(request: QuestionRequest):
    """Gerar questão de concurso"""
    return await ollama_service.generate_question(request)

@router.post("/generate/batch")
async def generate_questions_batch(request: BatchQuestionRequest):
    """Gerar múltiplas questões em lote"""
    return await ollama_service.generate_questions_batch(request.requests)

@router.get("/metrics")
async def get_metrics():
    """Métricas da aplicação"""
    return await health_service.get_metrics()
