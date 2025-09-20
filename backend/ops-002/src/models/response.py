"""
Modelos de Response para OPS-002
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

class LogEntryResponse(BaseModel):
    """Response para entrada de log"""
    id: str = Field(..., description="ID único do log")
    timestamp: datetime = Field(..., description="Timestamp do log")
    level: LogLevel = Field(..., description="Nível do log")
    message: str = Field(..., description="Mensagem do log")
    service: str = Field(..., description="Nome do serviço")
    version: str = Field(..., description="Versão do serviço")
    environment: str = Field(..., description="Ambiente")
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

class LogQueryResponse(BaseModel):
    """Response para consulta de logs"""
    logs: List[LogEntryResponse] = Field(..., description="Lista de logs")
    total: int = Field(..., description="Total de logs encontrados")
    page: int = Field(..., description="Página atual")
    page_size: int = Field(..., description="Tamanho da página")
    has_next: bool = Field(..., description="Tem próxima página")

class MetricResponse(BaseModel):
    """Response para métrica"""
    id: str = Field(..., description="ID único da métrica")
    name: str = Field(..., description="Nome da métrica")
    value: float = Field(..., description="Valor da métrica")
    service: str = Field(..., description="Nome do serviço")
    environment: str = Field(..., description="Ambiente")
    labels: Optional[Dict[str, str]] = Field(None, description="Labels da métrica")
    timestamp: datetime = Field(..., description="Timestamp da métrica")

class MetricQueryResponse(BaseModel):
    """Response para consulta de métricas"""
    metrics: List[MetricResponse] = Field(..., description="Lista de métricas")
    total: int = Field(..., description="Total de métricas encontradas")
    aggregated_data: Optional[Dict[str, Any]] = Field(None, description="Dados agregados")

class HealthCheckResponse(BaseModel):
    """Response para health check"""
    status: str = Field(..., description="Status do serviço")
    timestamp: datetime = Field(..., description="Timestamp da verificação")
    uptime: float = Field(..., description="Tempo de atividade em segundos")
    version: str = Field(..., description="Versão do serviço")
    environment: str = Field(..., description="Ambiente")
    checks: Dict[str, Any] = Field(..., description="Resultados dos checks")
    dependencies: Optional[Dict[str, Any]] = Field(None, description="Status das dependências")

class AlertResponse(BaseModel):
    """Response para alerta"""
    id: str = Field(..., description="ID único do alerta")
    name: str = Field(..., description="Nome do alerta")
    description: str = Field(..., description="Descrição do alerta")
    severity: str = Field(..., description="Severidade do alerta")
    service: str = Field(..., description="Serviço relacionado")
    condition: str = Field(..., description="Condição do alerta")
    threshold: float = Field(..., description="Limiar do alerta")
    current_value: Optional[float] = Field(None, description="Valor atual")
    status: str = Field(..., description="Status do alerta")
    enabled: bool = Field(..., description="Se o alerta está ativo")
    created_at: datetime = Field(..., description="Data de criação")
    last_triggered: Optional[datetime] = Field(None, description="Última vez que foi disparado")

class ServiceRegistrationResponse(BaseModel):
    """Response para registro de serviço"""
    id: str = Field(..., description="ID único do serviço")
    name: str = Field(..., description="Nome do serviço")
    version: str = Field(..., description="Versão do serviço")
    environment: str = Field(..., description="Ambiente")
    health_check_url: str = Field(..., description="URL do health check")
    metrics_url: Optional[str] = Field(None, description="URL das métricas")
    tags: Optional[List[str]] = Field(None, description="Tags do serviço")
    registered_at: datetime = Field(..., description="Data de registro")
    last_heartbeat: Optional[datetime] = Field(None, description="Último heartbeat")

class ServiceListResponse(BaseModel):
    """Response para lista de serviços"""
    services: List[ServiceRegistrationResponse] = Field(..., description="Lista de serviços")
    total: int = Field(..., description="Total de serviços")

class BulkLogResponse(BaseModel):
    """Response para logs em lote"""
    processed: int = Field(..., description="Número de logs processados")
    failed: int = Field(..., description="Número de logs que falharam")
    log_ids: List[str] = Field(..., description="IDs dos logs criados")
    errors: List[Dict[str, Any]] = Field(..., description="Erros encontrados")
    processing_time: float = Field(..., description="Tempo de processamento")

class BulkMetricResponse(BaseModel):
    """Response para métricas em lote"""
    processed: int = Field(..., description="Número de métricas processadas")
    failed: int = Field(..., description="Número de métricas que falharam")
    metric_ids: List[str] = Field(..., description="IDs das métricas criadas")
    errors: List[Dict[str, Any]] = Field(..., description="Erros encontrados")
    processing_time: float = Field(..., description="Tempo de processamento")

class DashboardResponse(BaseModel):
    """Response para dashboard"""
    total_services: int = Field(..., description="Total de serviços")
    active_alerts: int = Field(..., description="Alertas ativos")
    total_logs_today: int = Field(..., description="Total de logs hoje")
    avg_response_time: float = Field(..., description="Tempo médio de resposta")
    error_rate: float = Field(..., description="Taxa de erro")
    uptime_percentage: float = Field(..., description="Percentual de uptime")
    recent_logs: List[LogEntryResponse] = Field(..., description="Logs recentes")
    recent_metrics: List[MetricResponse] = Field(..., description="Métricas recentes")
    active_alerts_list: List[AlertResponse] = Field(..., description="Lista de alertas ativos")

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
