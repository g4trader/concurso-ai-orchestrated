"""
Modelos de response para IA-0
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class QuestionResponse(BaseModel):
    """Response para geração de questão"""
    question: str = Field(..., description="Enunciado da questão")
    alternatives: List[str] = Field(..., description="Alternativas de resposta")
    correct_answer: str = Field(..., description="Resposta correta")
    explanation: str = Field(..., description="Explicação da resposta")
    model_used: str = Field(..., description="Modelo utilizado")
    processing_time: float = Field(..., description="Tempo de processamento")
    timestamp: datetime = Field(..., description="Timestamp da geração")

class HealthResponse(BaseModel):
    """Response para health check"""
    status: str = Field(..., description="Status da aplicação")
    ollama_connected: bool = Field(..., description="Conexão com Ollama")
    models_available: List[str] = Field(..., description="Modelos disponíveis")
    uptime: float = Field(..., description="Tempo de atividade")

class ModelInfo(BaseModel):
    """Informações do modelo"""
    name: str = Field(..., description="Nome do modelo")
    size: str = Field(..., description="Tamanho do modelo")
    modified_at: str = Field(..., description="Data de modificação")
    digest: str = Field(..., description="Digest do modelo")

class ErrorResponse(BaseModel):
    """Response de erro"""
    error: str = Field(..., description="Mensagem de erro")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalhes do erro")
    timestamp: datetime = Field(..., description="Timestamp do erro")
