"""
Modelos de Request para IA-3
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class Simulado(BaseModel):
    """Modelo de simulado"""
    simulado_id: str = Field(..., description="ID único do simulado")
    banca: str = Field(..., description="Banca organizadora")
    ano: int = Field(..., description="Ano do edital")
    topico: str = Field(..., description="Tópico do simulado")
    questoes: List[Dict[str, Any]] = Field(..., description="Lista de questões")

class HeldOutDataset(BaseModel):
    """Modelo de dataset de validação"""
    banca: str = Field(..., description="Banca do dataset")
    ano: int = Field(..., description="Ano do dataset")
    topico: str = Field(..., description="Tópico do dataset")
    questoes_reais: List[Dict[str, Any]] = Field(..., description="Questões reais para comparação")

class EvaluationConfig(BaseModel):
    """Configurações de avaliação"""
    metrics: List[str] = Field(..., description="Métricas a serem calculadas")
    thresholds: Dict[str, float] = Field(..., description="Thresholds das métricas")

class EvaluationRequest(BaseModel):
    """Request para avaliação de simulados"""
    evaluation_id: str = Field(..., description="ID único da avaliação")
    generated_simulados: List[Simulado] = Field(..., description="Simulados gerados para avaliação")
    held_out_dataset: HeldOutDataset = Field(..., description="Dataset de validação")
    evaluation_config: EvaluationConfig = Field(..., description="Configurações de avaliação")

class BenchmarkRequest(BaseModel):
    """Request para benchmark de avaliação"""
    benchmark_id: str = Field(..., description="ID único do benchmark")
    evaluation_config: EvaluationConfig = Field(..., description="Configurações de avaliação")
    dataset_path: Optional[str] = Field(None, description="Caminho do dataset")

class HealthCheckRequest(BaseModel):
    """Request para health check"""
    check_components: Optional[bool] = Field(False, description="Verificar componentes")

class MetricsRequest(BaseModel):
    """Request para métricas"""
    time_range: Optional[str] = Field("1h", description="Período das métricas")
