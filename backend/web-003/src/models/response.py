"""
Modelos de Response para WEB-003
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Banca(BaseModel):
    """Modelo de banca"""
    id: str = Field(..., description="ID único da banca")
    name: str = Field(..., description="Nome da banca")
    code: str = Field(..., description="Código da banca")
    description: Optional[str] = Field(None, description="Descrição da banca")
    website: Optional[str] = Field(None, description="Site da banca")
    is_active: bool = Field(True, description="Se a banca está ativa")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data de atualização")

class Edital(BaseModel):
    """Modelo de edital"""
    id: str = Field(..., description="ID único do edital")
    banca_id: str = Field(..., description="ID da banca")
    title: str = Field(..., description="Título do edital")
    year: int = Field(..., description="Ano do edital")
    description: Optional[str] = Field(None, description="Descrição do edital")
    total_questions: int = Field(..., description="Número total de questões")
    time_limit: int = Field(..., description="Tempo limite em minutos")
    topics: List[str] = Field(..., description="Tópicos do edital")
    is_active: bool = Field(True, description="Se o edital está ativo")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data de atualização")

class Question(BaseModel):
    """Modelo de questão"""
    id: str = Field(..., description="ID único da questão")
    question: str = Field(..., description="Enunciado da questão")
    alternatives: List[Dict[str, str]] = Field(..., description="Alternativas")
    correct_answer: str = Field(..., description="Resposta correta")
    justification: str = Field(..., description="Justificativa")
    topic: str = Field(..., description="Tópico da questão")
    difficulty: str = Field(..., description="Dificuldade")
    source_chunks: List[str] = Field(..., description="Chunks de origem")

class Simulado(BaseModel):
    """Modelo de simulado"""
    id: str = Field(..., description="ID único do simulado")
    banca_id: str = Field(..., description="ID da banca")
    edital_id: str = Field(..., description="ID do edital")
    total_questions: int = Field(..., description="Número total de questões")
    time_limit: int = Field(..., description="Tempo limite em minutos")
    difficulty: str = Field(..., description="Dificuldade")
    topics: List[str] = Field(..., description="Tópicos")
    status: str = Field(..., description="Status do simulado")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data de atualização")

class SimuladoGenerationResponse(BaseModel):
    """Response para geração de simulado"""
    simulado: Simulado = Field(..., description="Dados do simulado criado")
    questions: List[Question] = Field(..., description="Lista de questões geradas")
    estimated_time: int = Field(..., description="Tempo estimado em minutos")
    generation_id: str = Field(..., description="ID da geração para tracking")

class GenerationStatusResponse(BaseModel):
    """Response para status de geração"""
    generation_id: str = Field(..., description="ID da geração")
    status: str = Field(..., description="Status da geração")
    progress: int = Field(..., description="Progresso em percentual")
    message: str = Field(..., description="Mensagem de status")
    estimated_completion: Optional[datetime] = Field(None, description="Estimativa de conclusão")

class SimuladoSubmitResponse(BaseModel):
    """Response para submissão de simulado"""
    simulado_id: str = Field(..., description="ID do simulado")
    score: float = Field(..., description="Pontuação obtida")
    correct_answers: int = Field(..., description="Número de respostas corretas")
    total_questions: int = Field(..., description="Número total de questões")
    time_spent: int = Field(..., description="Tempo gasto em segundos")
    submitted_at: datetime = Field(..., description="Data/hora de submissão")
    results: List[Dict[str, Any]] = Field(..., description="Resultados detalhados")

class SimuladoResultsResponse(BaseModel):
    """Response para resultados de simulado"""
    simulado_id: str = Field(..., description="ID do simulado")
    score: float = Field(..., description="Pontuação obtida")
    correct_answers: int = Field(..., description="Número de respostas corretas")
    total_questions: int = Field(..., description="Número total de questões")
    time_spent: int = Field(..., description="Tempo gasto em segundos")
    completed_at: datetime = Field(..., description="Data/hora de conclusão")
    results: List[Dict[str, Any]] = Field(..., description="Resultados detalhados")
    recommendations: List[str] = Field(..., description="Recomendações")

class BancaListResponse(BaseModel):
    """Response para lista de bancas"""
    bancas: List[Banca] = Field(..., description="Lista de bancas")
    total: int = Field(..., description="Total de bancas")
    page: int = Field(..., description="Página atual")
    page_size: int = Field(..., description="Tamanho da página")

class EditalListResponse(BaseModel):
    """Response para lista de editais"""
    editais: List[Edital] = Field(..., description="Lista de editais")
    total: int = Field(..., description="Total de editais")
    page: int = Field(..., description="Página atual")
    page_size: int = Field(..., description="Tamanho da página")

class HealthResponse(BaseModel):
    """Response para health check"""
    status: str = Field(..., description="Status da aplicação")
    details: Dict[str, Any] = Field(..., description="Detalhes do status")

class MetricsResponse(BaseModel):
    """Response para métricas"""
    metrics: Dict[str, Any] = Field(..., description="Métricas do sistema")

class ErrorResponse(BaseModel):
    """Response para erros"""
    error: str = Field(..., description="Descrição do erro")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalhes do erro")
