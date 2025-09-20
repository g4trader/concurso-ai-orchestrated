"""
Serviço de health check para IA-0
"""

import time
import httpx
from typing import List
from src.models.response import HealthResponse
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class HealthCheckService:
    """Serviço para verificação de saúde da aplicação"""
    
    def __init__(self):
        self.start_time = time.time()
        self.client = httpx.AsyncClient(timeout=5)
    
    async def check_health(self) -> HealthResponse:
        """Verificar saúde da aplicação"""
        try:
            # Verificar conexão com Ollama
            response = await self.client.get(f"{settings.OLLAMA_HOST}/api/tags")
            ollama_connected = response.status_code == 200
            
            if ollama_connected:
                models_data = response.json()
                models_available = [model["name"] for model in models_data.get("models", [])]
            else:
                models_available = []
            
            status = "healthy" if ollama_connected else "degraded"
            
            return HealthResponse(
                status=status,
                ollama_connected=ollama_connected,
                models_available=models_available,
                uptime=time.time() - self.start_time
            )
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return HealthResponse(
                status="unhealthy",
                ollama_connected=False,
                models_available=[],
                uptime=time.time() - self.start_time
            )
    
    async def get_metrics(self) -> dict:
        """Obter métricas da aplicação"""
        return {
            "uptime": time.time() - self.start_time,
            "ollama_host": settings.OLLAMA_HOST,
            "default_model": settings.DEFAULT_MODEL,
            "available_models": settings.AVAILABLE_MODELS,
            "timestamp": time.time()
        }
