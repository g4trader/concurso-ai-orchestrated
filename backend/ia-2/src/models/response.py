"""
Modelos de response para IA-2
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class QuestionGenerationResponse(BaseModel):
    """Response para geração de questão"""
    question_id: str = Field(..., description="ID da questão")
    question: str = Field(..., description="Texto da questão")
    alternatives: Dict[str, str] = Field(..., description="Alternativas A-E")
    correct_answer: str = Field(..., description="Resposta correta")
    justification: str = Field(..., description="Justificativa")
    source_chunks: List[str] = Field(..., description="IDs dos chunks fonte")
    metadata: Dict[str, Any] = Field(..., description="Metadados da questão")
    generation_time: float = Field(..., description="Tempo de geração")
    timestamp: datetime = Field(..., description="Timestamp da geração")

class QuestionMetadata(BaseModel):
    """Metadados da questão"""
    banca: str = Field(..., description="Banca organizadora")
    ano: int = Field(..., description="Ano do edital")
    topico: str = Field(..., description="Tópico/área")
    dificuldade: str = Field(..., description="Nível de dificuldade")
    estilo: str = Field(..., description="Estilo da questão")
    plausibilidade_score: float = Field(..., description="Score de plausibilidade")
    consistency_score: float = Field(..., description="Score de consistência")
    plagiarism_score: float = Field(..., description="Score de plágio")

class BatchGenerationResponse(BaseModel):
    """Response para geração em lote"""
    batch_id: str = Field(..., description="ID do lote")
    status: str = Field(..., description="Status do lote")
    total_requests: int = Field(..., description="Total de requests")
    successful: int = Field(..., description="Questões geradas com sucesso")
    failed: int = Field(..., description="Questões que falharam")
    questions: List[QuestionGenerationResponse] = Field(..., description="Questões geradas")
    failed_requests: List[Dict[str, Any]] = Field(..., description="Requests que falharam")
    processing_time: float = Field(..., description="Tempo total de processamento")
    timestamp: datetime = Field(..., description="Timestamp do processamento")

class ValidationResponse(BaseModel):
    """Response para validação de questão"""
    validation_id: str = Field(..., description="ID da validação")
    is_valid: bool = Field(..., description="Se a questão é válida")
    scores: Dict[str, float] = Field(..., description="Scores de validação")
    checks: Dict[str, Dict[str, Any]] = Field(..., description="Resultados dos checks")
    recommendations: List[str] = Field(..., description="Recomendações")
    validation_time: float = Field(..., description="Tempo de validação")
    timestamp: datetime = Field(..., description="Timestamp da validação")

class ValidationScores(BaseModel):
    """Scores de validação"""
    plausibility: float = Field(..., description="Score de plausibilidade")
    consistency: float = Field(..., description="Score de consistência")
    plagiarism: float = Field(..., description="Score de plágio")
    quality: float = Field(..., description="Score de qualidade")

class ValidationChecks(BaseModel):
    """Resultados dos checks de validação"""
    uniqueness: Dict[str, Any] = Field(..., description="Check de unicidade")
    consistency: Dict[str, Any] = Field(..., description="Check de consistência")
    plagiarism: Dict[str, Any] = Field(..., description="Check de plágio")
    quality: Dict[str, Any] = Field(..., description="Check de qualidade")

class HealthResponse(BaseModel):
    """Response para health check"""
    status: str = Field(..., description="Status geral")
    services: Dict[str, Dict[str, Any]] = Field(..., description="Status dos serviços")
    uptime: float = Field(..., description="Tempo de atividade")
    timestamp: datetime = Field(..., description="Timestamp do check")

class ServiceStatus(BaseModel):
    """Status de um serviço"""
    name: str = Field(..., description="Nome do serviço")
    status: str = Field(..., description="Status do serviço")
    response_time: Optional[float] = Field(None, description="Tempo de resposta")
    error: Optional[str] = Field(None, description="Erro se houver")
    last_check: datetime = Field(..., description="Última verificação")

class MetricsResponse(BaseModel):
    """Response para métricas"""
    uptime: float = Field(..., description="Tempo de atividade")
    total_questions_generated: int = Field(..., description="Total de questões geradas")
    total_validations: int = Field(..., description="Total de validações")
    avg_generation_time: float = Field(..., description="Tempo médio de geração")
    avg_validation_time: float = Field(..., description="Tempo médio de validação")
    success_rate: float = Field(..., description="Taxa de sucesso")
    quality_scores: Dict[str, float] = Field(..., description="Scores de qualidade médios")
    timestamp: datetime = Field(..., description="Timestamp das métricas")

class ErrorResponse(BaseModel):
    """Response de erro"""
    error: str = Field(..., description="Mensagem de erro")
    code: str = Field(..., description="Código do erro")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalhes do erro")
    timestamp: datetime = Field(..., description="Timestamp do erro")

class QuestionInfo(BaseModel):
    """Informações de uma questão"""
    question_id: str = Field(..., description="ID da questão")
    question: str = Field(..., description="Texto da questão")
    alternatives: Dict[str, str] = Field(..., description="Alternativas")
    correct_answer: str = Field(..., description="Resposta correta")
    justification: str = Field(..., description="Justificativa")
    source_chunks: List[str] = Field(..., description="Chunks fonte")
    metadata: Dict[str, Any] = Field(..., description="Metadados")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data de atualização")

class BatchInfo(BaseModel):
    """Informações de um lote"""
    batch_id: str = Field(..., description="ID do lote")
    status: str = Field(..., description="Status do lote")
    total_requests: int = Field(..., description="Total de requests")
    successful: int = Field(..., description="Sucessos")
    failed: int = Field(..., description="Falhas")
    processing_time: float = Field(..., description="Tempo de processamento")
    created_at: datetime = Field(..., description="Data de criação")
    completed_at: Optional[datetime] = Field(None, description="Data de conclusão")
