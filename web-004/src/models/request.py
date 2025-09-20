"""
Modelos de Request para WEB-004
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class AnalyzeResultsRequest(BaseModel):
    """Request para análise de resultados"""
    include_performance: bool = Field(True, description="Incluir análise de performance")
    include_weak_points: bool = Field(True, description="Incluir identificação de pontos fracos")
    include_recommendations: bool = Field(True, description="Incluir recomendações")
    custom_thresholds: Optional[Dict[str, float]] = Field(None, description="Limiares customizados")

class ExportResultsRequest(BaseModel):
    """Request para exportação de resultados"""
    format: str = Field(..., description="Formato de exportação", pattern="^(pdf|excel|csv|json)$")
    include_charts: bool = Field(True, description="Incluir gráficos")
    include_detailed_analysis: bool = Field(True, description="Incluir análise detalhada")
    custom_sections: Optional[List[str]] = Field(None, description="Seções customizadas")

class SaveDraftRequest(BaseModel):
    """Request para salvar rascunho"""
    title: str = Field(..., description="Título do rascunho", min_length=1)
    notes: Optional[str] = Field(None, description="Notas do usuário")
    tags: Optional[List[str]] = Field(None, description="Tags do rascunho")

class ShareResultsRequest(BaseModel):
    """Request para compartilhar resultados"""
    share_type: str = Field(..., description="Tipo de compartilhamento", pattern="^(public|private|link)$")
    expiry_hours: Optional[int] = Field(24, description="Horas até expiração", ge=1, le=168)
    password: Optional[str] = Field(None, description="Senha para acesso privado")

class GetChartsRequest(BaseModel):
    """Request para dados de gráficos"""
    chart_types: List[str] = Field(..., description="Tipos de gráficos solicitados")
    time_range: Optional[str] = Field("all", description="Período de tempo")
    granularity: Optional[str] = Field("daily", description="Granularidade dos dados")

class HealthCheckRequest(BaseModel):
    """Request para health check"""
    check_components: Optional[bool] = Field(False, description="Verificar componentes")

class MetricsRequest(BaseModel):
    """Request para métricas"""
    time_range: Optional[str] = Field("1h", description="Período das métricas")
