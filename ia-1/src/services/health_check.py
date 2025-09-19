"""
Serviço de Health Check para IA-1
"""

import structlog
from typing import Dict, Any, Optional
from datetime import datetime
from src.models.request import HealthCheckRequest
from src.models.response import HealthResponse, MetricsResponse

logger = structlog.get_logger(__name__)

class HealthCheckService:
    """
    Serviço responsável por health checks e métricas da aplicação.
    """

    def __init__(self):
        logger.info("HealthCheckService inicializado.")
        self.start_time = datetime.now()
        self.request_count = 0
        self.error_count = 0

    async def check_health(self, request: Optional[HealthCheckRequest] = None) -> HealthResponse:
        """
        Verifica a saúde da aplicação.

        Args:
            request (Optional[HealthCheckRequest]): Request de health check.

        Returns:
            HealthResponse: Resposta com status da aplicação.
        """
        logger.info("Health check solicitado.")
        
        try:
            # Verificar componentes críticos
            components_status = await self._check_components()
            
            # Determinar status geral
            overall_status = "healthy" if all(
                status["status"] == "healthy" 
                for status in components_status.values()
            ) else "unhealthy"
            
            health_response = HealthResponse(
                status=overall_status,
                timestamp=datetime.now(),
                uptime=self._get_uptime(),
                version="1.0.0",
                components=components_status
            )
            
            logger.info("Health check concluído.", status=overall_status)
            return health_response
            
        except Exception as e:
            logger.error("Erro no health check.", error=str(e))
            return HealthResponse(
                status="unhealthy",
                timestamp=datetime.now(),
                uptime=self._get_uptime(),
                version="1.0.0",
                components={"error": {"status": "unhealthy", "message": str(e)}}
            )

    async def get_metrics(self) -> MetricsResponse:
        """
        Obtém métricas da aplicação.

        Returns:
            MetricsResponse: Métricas da aplicação.
        """
        logger.info("Métricas solicitadas.")
        
        try:
            metrics = {
                "uptime_seconds": self._get_uptime(),
                "total_requests": self.request_count,
                "error_count": self.error_count,
                "success_rate": self._calculate_success_rate(),
                "memory_usage": await self._get_memory_usage(),
                "cpu_usage": await self._get_cpu_usage()
            }
            
            metrics_response = MetricsResponse(
                timestamp=datetime.now(),
                metrics=metrics
            )
            
            logger.info("Métricas obtidas com sucesso.")
            return metrics_response
            
        except Exception as e:
            logger.error("Erro ao obter métricas.", error=str(e))
            return MetricsResponse(
                timestamp=datetime.now(),
                metrics={"error": str(e)}
            )

    def increment_request_count(self):
        """Incrementa contador de requests."""
        self.request_count += 1

    def increment_error_count(self):
        """Incrementa contador de erros."""
        self.error_count += 1

    async def _check_components(self) -> Dict[str, Dict[str, Any]]:
        """
        Verifica status dos componentes da aplicação.

        Returns:
            Dict[str, Dict[str, Any]]: Status dos componentes.
        """
        components = {}
        
        try:
            # Verificar serviços principais
            components["parser_service"] = await self._check_parser_service()
            components["embedding_service"] = await self._check_embedding_service()
            components["indexing_service"] = await self._check_indexing_service()
            components["database"] = await self._check_database()
            
        except Exception as e:
            logger.error("Erro ao verificar componentes.", error=str(e))
            components["error"] = {
                "status": "unhealthy",
                "message": str(e)
            }
        
        return components

    async def _check_parser_service(self) -> Dict[str, Any]:
        """Verifica status do parser service."""
        try:
            # TODO: Implementar verificação real do parser service
            return {
                "status": "healthy",
                "message": "Parser service is running"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Parser service error: {str(e)}"
            }

    async def _check_embedding_service(self) -> Dict[str, Any]:
        """Verifica status do embedding service."""
        try:
            # TODO: Implementar verificação real do embedding service
            return {
                "status": "healthy",
                "message": "Embedding service is running"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Embedding service error: {str(e)}"
            }

    async def _check_indexing_service(self) -> Dict[str, Any]:
        """Verifica status do indexing service."""
        try:
            # TODO: Implementar verificação real do indexing service
            return {
                "status": "healthy",
                "message": "Indexing service is running"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Indexing service error: {str(e)}"
            }

    async def _check_database(self) -> Dict[str, Any]:
        """Verifica status do banco de dados."""
        try:
            # TODO: Implementar verificação real do banco de dados
            return {
                "status": "healthy",
                "message": "Database connection is active"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Database error: {str(e)}"
            }

    def _get_uptime(self) -> float:
        """Calcula uptime em segundos."""
        return (datetime.now() - self.start_time).total_seconds()

    def _calculate_success_rate(self) -> float:
        """Calcula taxa de sucesso."""
        if self.request_count == 0:
            return 100.0
        return ((self.request_count - self.error_count) / self.request_count) * 100.0

    async def _get_memory_usage(self) -> Dict[str, Any]:
        """Obtém uso de memória."""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used
            }
        except ImportError:
            return {"error": "psutil not available"}
        except Exception as e:
            return {"error": str(e)}

    async def _get_cpu_usage(self) -> Dict[str, Any]:
        """Obtém uso de CPU."""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            return {
                "percent": cpu_percent,
                "count": cpu_count
            }
        except ImportError:
            return {"error": "psutil not available"}
        except Exception as e:
            return {"error": str(e)}
