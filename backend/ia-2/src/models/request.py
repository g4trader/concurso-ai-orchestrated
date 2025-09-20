"""
Modelos de request para IA-2
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class ValidationLevel(str, Enum):
    """Níveis de validação"""
    STRICT = "strict"
    MEDIUM = "medium"
    LOOSE = "loose"

class DifficultyLevel(str, Enum):
    """Níveis de dificuldade"""
    FACIL = "facil"
    INTERMEDIARIA = "intermediaria"
    DIFICIL = "dificil"

class QuestionStyle(str, Enum):
    """Estilos de questão"""
    CONCEITUAL = "conceitual"
    APLICACAO = "aplicacao"
    INTERPRETACAO = "interpretacao"
    CALCULO = "calculo"

class QuestionGenerationRequest(BaseModel):
    """Request para geração de questão"""
    contexts: List[Dict[str, Any]] = Field(..., description="Contextos para geração")
    edital_summary: Dict[str, Any] = Field(..., description="Resumo do edital")
    topic: str = Field(..., description="Tópico da questão")
    generation_config: Optional[Dict[str, Any]] = Field(None, description="Configurações de geração")

class EditalSummary(BaseModel):
    """Resumo do edital"""
    banca: str = Field(..., description="Banca organizadora")
    ano: int = Field(..., description="Ano do edital")
    cargo: str = Field(..., description="Cargo/área")
    orgao: Optional[str] = Field(None, description="Órgão responsável")
    topico: str = Field(..., description="Tópico/área")
    dificuldade: DifficultyLevel = Field(DifficultyLevel.INTERMEDIARIA, description="Nível de dificuldade")
    estilo: QuestionStyle = Field(QuestionStyle.CONCEITUAL, description="Estilo da questão")

class GenerationConfig(BaseModel):
    """Configurações de geração"""
    num_questions: int = Field(1, description="Número de questões a gerar")
    difficulty: DifficultyLevel = Field(DifficultyLevel.INTERMEDIARIA, description="Nível de dificuldade")
    style: QuestionStyle = Field(QuestionStyle.CONCEITUAL, description="Estilo da questão")
    validation_level: ValidationLevel = Field(ValidationLevel.STRICT, description="Nível de validação")

class BatchGenerationRequest(BaseModel):
    """Request para geração em lote"""
    batch_id: Optional[str] = Field(None, description="ID do lote")
    requests: List[QuestionGenerationRequest] = Field(..., description="Lista de requests")
    batch_config: Optional[Dict[str, Any]] = Field(None, description="Configurações do lote")

class BatchConfig(BaseModel):
    """Configurações do lote"""
    max_parallel: int = Field(5, description="Máximo de gerações paralelas")
    timeout_per_question: int = Field(30, description="Timeout por questão")
    quality_threshold: float = Field(0.9, description="Threshold de qualidade")
    validation_level: ValidationLevel = Field(ValidationLevel.STRICT, description="Nível de validação")

class ValidationRequest(BaseModel):
    """Request para validação de questão"""
    question: str = Field(..., description="Texto da questão")
    alternatives: Dict[str, str] = Field(..., description="Alternativas A-E")
    correct_answer: str = Field(..., description="Resposta correta")
    justification: str = Field(..., description="Justificativa")
    source_chunks: List[str] = Field(..., description="IDs dos chunks fonte")
    validation_config: Optional[Dict[str, Any]] = Field(None, description="Configurações de validação")

class ValidationConfig(BaseModel):
    """Configurações de validação"""
    check_consistency: bool = Field(True, description="Verificar consistência")
    check_plagiarism: bool = Field(True, description="Verificar plágio")
    check_quality: bool = Field(True, description="Verificar qualidade")
    consistency_threshold: float = Field(0.8, description="Threshold de consistência")
    plagiarism_threshold: float = Field(0.3, description="Threshold de plágio")
    quality_threshold: float = Field(0.9, description="Threshold de qualidade")

class HealthCheckRequest(BaseModel):
    """Request para health check"""
    check_services: Optional[List[str]] = Field(None, description="Serviços para verificar")
    deep_check: Optional[bool] = Field(False, description="Verificação profunda")

class MetricsRequest(BaseModel):
    """Request para métricas"""
    time_range: Optional[str] = Field("1h", description="Período de tempo")
    metrics: Optional[List[str]] = Field(None, description="Métricas específicas")
