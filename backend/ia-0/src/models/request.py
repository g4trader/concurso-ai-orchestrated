"""
Modelos de request para IA-0
"""

from pydantic import BaseModel, Field
from typing import Optional, List

class QuestionRequest(BaseModel):
    """Request para geração de questão"""
    prompt: str = Field(..., description="Prompt para geração da questão")
    model: Optional[str] = Field(None, description="Modelo a ser usado")
    max_tokens: Optional[int] = Field(1000, description="Máximo de tokens")
    temperature: Optional[float] = Field(0.7, description="Temperatura para geração")
    context: Optional[str] = Field(None, description="Contexto adicional")

class BatchQuestionRequest(BaseModel):
    """Request para geração em lote"""
    requests: List[QuestionRequest] = Field(..., description="Lista de requests")

class ModelRequest(BaseModel):
    """Request para operações com modelos"""
    model_name: str = Field(..., description="Nome do modelo")
    action: str = Field(..., description="Ação a ser executada")
