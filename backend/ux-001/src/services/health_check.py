"""
Serviço de Health Check para UX-001
"""

import structlog
from typing import Dict, Any, Optional
from datetime import datetime
from src.models.request import HealthCheckRequest
from src.models.response import HealthResponse, MetricsResponse

logger = structlog.get_logger(__name__)

class HealthCheckService:
    """
    Serviço responsável por fornecer informações de saúde e métricas da aplicação.
    """

    def __init__(self):
        self.start_time = datetime.now()
        self.request_count = 0
        self.error_count = 0
        logger.info("HealthCheckService inicializado.")

    async def check_health(self, request: Optional[HealthCheckRequest] = None) -> HealthResponse:
        """
        Verifica a saúde da aplicação.
        """
        self.request_count += 1
        status = "healthy"
        details: Dict[str, Any] = {
            "uptime": str(datetime.now() - self.start_time),
            "timestamp": datetime.now().isoformat(),
            "service_name": "UX-001 Sistema de Feedback do Usuário"
        }

        logger.info("Health check realizado.", status=status, details=details)
        return HealthResponse(status=status, details=details)

    async def get_metrics(self) -> MetricsResponse:
        """
        Retorna métricas básicas da aplicação.
        """
        uptime_duration = datetime.now() - self.start_time
        metrics = {
            "uptime_seconds": uptime_duration.total_seconds(),
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "requests_per_second": self.request_count / uptime_duration.total_seconds() if uptime_duration.total_seconds() > 0 else 0
        }
        logger.info("Métricas solicitadas.", metrics=metrics)
        return MetricsResponse(metrics=metrics)
