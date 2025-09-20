"""
Modelos de Request para WEB-003
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class SimuladoGenerationRequest(BaseModel):
    """Request para geração de simulado"""
    banca_id: str = Field(..., description="ID da banca")
    edital_id: str = Field(..., description="ID do edital")
    total_questions: int = Field(..., description="Número total de questões", ge=1, le=100)
    time_limit: int = Field(..., description="Tempo limite em minutos", ge=30, le=300)
    difficulty: str = Field(..., description="Dificuldade", regex="^(easy|medium|hard)$")
    topics: Optional[List[str]] = Field(None, description="Tópicos específicos")
    custom_instructions: Optional[str] = Field(None, description="Instruções customizadas")

class SimuladoSubmitRequest(BaseModel):
    """Request para submeter simulado"""
    answers: Dict[str, str] = Field(..., description="Respostas do usuário")
    time_spent: int = Field(..., description="Tempo gasto em segundos")
    completed_at: datetime = Field(..., description="Data/hora de conclusão")

class BancaFilterRequest(BaseModel):
    """Request para filtro de bancas"""
    active_only: bool = Field(True, description="Apenas bancas ativas")
    search: Optional[str] = Field(None, description="Termo de busca")

class EditalFilterRequest(BaseModel):
    """Request para filtro de editais"""
    banca_id: Optional[str] = Field(None, description="ID da banca")
    year: Optional[int] = Field(None, description="Ano do edital")
    active_only: bool = Field(True, description="Apenas editais ativos")
    search: Optional[str] = Field(None, description="Termo de busca")

class GenerationStatusRequest(BaseModel):
    """Request para status de geração"""
    generation_id: str = Field(..., description="ID da geração")

class HealthCheckRequest(BaseModel):
    """Request para health check"""
    check_components: Optional[bool] = Field(False, description="Verificar componentes")

class MetricsRequest(BaseModel):
    """Request para métricas"""
    time_range: Optional[str] = Field("1h", description="Período das métricas")
