"""
Modelos de Request para OPS-002
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class LogLevel(str, Enum):
    """Níveis de log"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogEntryRequest(BaseModel):
    """Request para criar entrada de log"""
    level: LogLevel = Field(..., description="Nível do log")
    message: str = Field(..., description="Mensagem do log")
    service: str = Field(..., description="Nome do serviço")
    version: str = Field(..., description="Versão do serviço")
    environment: str = Field(..., description="Ambiente (dev, staging, prod)")
    request_id: Optional[str] = Field(None, description="ID da requisição")
    user_id: Optional[str] = Field(None, description="ID do usuário")
    session_id: Optional[str] = Field(None, description="ID da sessão")
    correlation_id: Optional[str] = Field(None, description="ID de correlação")
    trace_id: Optional[str] = Field(None, description="ID do trace")
    span_id: Optional[str] = Field(None, description="ID do span")
    duration: Optional[float] = Field(None, description="Duração em segundos")
    status_code: Optional[int] = Field(None, description="Código de status HTTP")
    method: Optional[str] = Field(None, description="Método HTTP")
    path: Optional[str] = Field(None, description="Caminho da requisição")
    user_agent: Optional[str] = Field(None, description="User agent")
    ip_address: Optional[str] = Field(None, description="Endereço IP")
    error_code: Optional[str] = Field(None, description="Código do erro")
    error_message: Optional[str] = Field(None, description="Mensagem do erro")
    stack_trace: Optional[str] = Field(None, description="Stack trace")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadados adicionais")

class BulkLogEntryRequest(BaseModel):
    """Request para criar múltiplas entradas de log"""
    logs: List[LogEntryRequest] = Field(..., max_items=1000, description="Lista de logs")

class LogQueryRequest(BaseModel):
    """Request para consultar logs"""
    service: Optional[str] = Field(None, description="Filtrar por serviço")
    level: Optional[LogLevel] = Field(None, description="Filtrar por nível")
    start_time: Optional[datetime] = Field(None, description="Data/hora inicial")
    end_time: Optional[datetime] = Field(None, description="Data/hora final")
    search_text: Optional[str] = Field(None, description="Texto de busca")
    limit: int = Field(100, ge=1, le=1000, description="Limite de resultados")
    offset: int = Field(0, ge=0, description="Offset para paginação")

class MetricRequest(BaseModel):
    """Request para criar métrica"""
    name: str = Field(..., description="Nome da métrica")
    value: float = Field(..., description="Valor da métrica")
    service: str = Field(..., description="Nome do serviço")
    environment: str = Field(..., description="Ambiente")
    labels: Optional[Dict[str, str]] = Field(None, description="Labels da métrica")
    timestamp: Optional[datetime] = Field(None, description="Timestamp da métrica")

class BulkMetricRequest(BaseModel):
    """Request para criar múltiplas métricas"""
    metrics: List[MetricRequest] = Field(..., max_items=1000, description="Lista de métricas")

class HealthCheckRequest(BaseModel):
    """Request para health check"""
    service_name: Optional[str] = Field(None, description="Nome do serviço para verificar")
    check_dependencies: bool = Field(False, description="Verificar dependências")

class AlertRequest(BaseModel):
    """Request para criar alerta"""
    name: str = Field(..., description="Nome do alerta")
    description: str = Field(..., description="Descrição do alerta")
    severity: str = Field(..., pattern="^(low|medium|high|critical)$", description="Severidade do alerta")
    service: str = Field(..., description="Serviço relacionado")
    condition: str = Field(..., description="Condição do alerta")
    threshold: float = Field(..., description="Limiar do alerta")
    enabled: bool = Field(True, description="Se o alerta está ativo")

class ServiceRegistrationRequest(BaseModel):
    """Request para registrar serviço"""
    name: str = Field(..., description="Nome do serviço")
    version: str = Field(..., description="Versão do serviço")
    environment: str = Field(..., description="Ambiente")
    health_check_url: str = Field(..., description="URL do health check")
    metrics_url: Optional[str] = Field(None, description="URL das métricas")
    tags: Optional[List[str]] = Field(None, description="Tags do serviço")

class HealthCheckRequest(BaseModel):
    """Request para health check"""
    check_components: Optional[bool] = Field(False, description="Verificar componentes")

class MetricsRequest(BaseModel):
    """Request para métricas"""
    time_range: Optional[str] = Field("1h", description="Período das métricas")
