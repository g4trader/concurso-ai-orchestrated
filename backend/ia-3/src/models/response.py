"""
Modelos de Response para IA-3
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class MetricResult(BaseModel):
    """Resultado de uma métrica"""
    metric_name: str = Field(..., description="Nome da métrica")
    value: float = Field(..., description="Valor da métrica")
    threshold: float = Field(..., description="Threshold da métrica")
    passed: bool = Field(..., description="Se passou no threshold")
    details: Dict[str, Any] = Field(default_factory=dict, description="Detalhes da métrica")

class GapAnalysis(BaseModel):
    """Análise de gaps"""
    gaps_found: List[str] = Field(..., description="Gaps identificados")
    severity: str = Field(..., description="Severidade dos gaps")
    recommendations: List[str] = Field(..., description="Recomendações")

class EvaluationResponse(BaseModel):
    """Response para avaliação de simulados"""
    evaluation_id: str = Field(..., description="ID da avaliação")
    status: str = Field(..., description="Status da avaliação")
    metrics: Dict[str, MetricResult] = Field(..., description="Resultados das métricas")
    gap_analysis: GapAnalysis = Field(..., description="Análise de gaps")
    recommendations: List[str] = Field(..., description="Recomendações")
    processing_time: float = Field(..., description="Tempo de processamento")
    timestamp: datetime = Field(..., description="Timestamp da avaliação")

class BenchmarkResponse(BaseModel):
    """Response para benchmark"""
    benchmark_id: str = Field(..., description="ID do benchmark")
    status: str = Field(..., description="Status do benchmark")
    results: Dict[str, Any] = Field(..., description="Resultados do benchmark")
    processing_time: float = Field(..., description="Tempo de processamento")
    timestamp: datetime = Field(..., description="Timestamp do benchmark")

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
