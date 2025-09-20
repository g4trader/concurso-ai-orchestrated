"""
Rotas da API IA-3
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
import time
from datetime import datetime
from src.models.request import (
    EvaluationRequest, BenchmarkRequest, HealthCheckRequest, MetricsRequest
)
from src.models.response import (
    EvaluationResponse, BenchmarkResponse, HealthResponse, MetricsResponse, ErrorResponse
)
from src.services.health_check import HealthCheckService

router = APIRouter(prefix="/api/v1", tags=["ia-3"])

# Dependências
health_service = HealthCheckService()

@router.get("/", response_model=dict)
async def root():
    """Endpoint raiz"""
    return {
        "service": "IA-3 Avaliação Offline",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@router.get("/health", response_model=HealthResponse)
async def health_check(request: HealthCheckRequest = None):
    """Health check da aplicação"""
    return await health_service.check_health(request)

@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(request: MetricsRequest = None):
    """Métricas da aplicação"""
    return await health_service.get_metrics(request)

@router.post("/evaluate/simulados", response_model=EvaluationResponse)
async def evaluate_simulados(
    background_tasks: BackgroundTasks,
    request: EvaluationRequest
):
    """Avaliar simulados gerados"""
    try:
        start_time = time.time()
        
        # Mock evaluation - em produção seria avaliação real
        evaluation_response = EvaluationResponse(
            evaluation_id=request.evaluation_id,
            status="completed",
            metrics={
                "topic_hit_rate": {
                    "metric_name": "topic_hit_rate",
                    "value": 0.85,
                    "threshold": request.evaluation_config.thresholds.get("topic_hit_rate", 0.8),
                    "passed": True,
                    "details": {"matched_topics": 17, "total_topics": 20}
                },
                "style_match": {
                    "metric_name": "style_match",
                    "value": 0.78,
                    "threshold": request.evaluation_config.thresholds.get("style_match", 0.7),
                    "passed": True,
                    "details": {"consistency_score": 0.78}
                },
                "answerability": {
                    "metric_name": "answerability",
                    "value": 0.92,
                    "threshold": request.evaluation_config.thresholds.get("answerability", 0.9),
                    "passed": True,
                    "details": {"answerable_questions": 92, "total_questions": 100}
                }
            },
            gap_analysis={
                "gaps_found": ["Algumas questões podem ter dificuldade inconsistente"],
                "severity": "medium",
                "recommendations": ["Revisar critérios de dificuldade", "Padronizar estilo de questões"]
            },
            recommendations=[
                "Melhorar consistência de estilo",
                "Revisar critérios de dificuldade",
                "Aumentar cobertura de tópicos"
            ],
            processing_time=time.time() - start_time,
            timestamp=datetime.now()
        )
        
        return evaluation_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/benchmark/evaluation", response_model=BenchmarkResponse)
async def benchmark_evaluation(
    background_tasks: BackgroundTasks,
    request: BenchmarkRequest
):
    """Benchmark de avaliação"""
    try:
        start_time = time.time()
        
        # Mock benchmark - em produção seria benchmark real
        benchmark_response = BenchmarkResponse(
            benchmark_id=request.benchmark_id,
            status="completed",
            results={
                "overall_score": 0.85,
                "metrics_performance": {
                    "topic_hit_rate": 0.85,
                    "style_match": 0.78,
                    "answerability": 0.92
                },
                "recommendations": [
                    "Sistema atende aos critérios básicos",
                    "Oportunidade de melhoria na consistência de estilo"
                ]
            },
            processing_time=time.time() - start_time,
            timestamp=datetime.now()
        )
        
        return benchmark_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/evaluations")
async def list_evaluations(
    skip: int = 0,
    limit: int = 100
):
    """Listar avaliações"""
    try:
        # Mock list - em produção seria busca real
        return {"evaluations": [], "total": 0}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/benchmarks")
async def list_benchmarks(
    skip: int = 0,
    limit: int = 100
):
    """Listar benchmarks"""
    try:
        # Mock list - em produção seria busca real
        return {"benchmarks": [], "total": 0}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
