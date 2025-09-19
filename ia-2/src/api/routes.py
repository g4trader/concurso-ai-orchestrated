"""
Rotas da API IA-2
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from src.models.request import (
    QuestionGenerationRequest, BatchGenerationRequest, ValidationRequest,
    HealthCheckRequest, MetricsRequest
)
from src.models.response import (
    QuestionGenerationResponse, BatchGenerationResponse, ValidationResponse,
    HealthResponse, MetricsResponse, ErrorResponse
)
from src.services.prompt_engineering_service import PromptEngineeringService
from src.services.llm_generation_service import LLMGenerationService
from src.services.validation_service import ValidationService
from src.services.self_consistency_service import SelfConsistencyService
from src.services.anti_plagiarism_service import AntiPlagiarismService
from src.services.quality_assessment_service import QualityAssessmentService
from src.services.batch_processor_service import BatchProcessorService
from src.services.health_check import HealthCheckService

router = APIRouter(prefix="/api/v1", tags=["ia-2"])

# Dependências
prompt_service = PromptEngineeringService()
llm_service = LLMGenerationService()
validation_service = ValidationService()
consistency_service = SelfConsistencyService()
plagiarism_service = AntiPlagiarismService()
quality_service = QualityAssessmentService()
batch_service = BatchProcessorService()
health_service = HealthCheckService()

@router.get("/", response_model=dict)
async def root():
    """Endpoint raiz"""
    return {
        "service": "IA-2 Geração Condicionada",
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

@router.post("/generate/question", response_model=QuestionGenerationResponse)
async def generate_question(
    background_tasks: BackgroundTasks,
    request: QuestionGenerationRequest
):
    """Gerar questão única"""
    try:
        # 1. Engenharia de prompt
        prompt = await prompt_service.create_prompt(
            request.contexts,
            request.edital_summary,
            request.topic
        )
        
        # 2. Geração com LLM
        raw_question = await llm_service.generate_question(prompt)
        
        # 3. Validação
        validation_result = await validation_service.validate_question(raw_question)
        
        # 4. Self-consistency check
        consistency_result = await consistency_service.check_consistency(raw_question)
        
        # 5. Anti-plagiarism check
        plagiarism_result = await plagiarism_service.check_plagiarism(
            raw_question, request.contexts
        )
        
        # 6. Quality assessment
        quality_result = await quality_service.assess_quality(raw_question)
        
        # 7. Combinar resultados
        question_response = QuestionGenerationResponse(
            question_id=f"q_{int(time.time())}",
            question=raw_question["question"],
            alternatives=raw_question["alternatives"],
            correct_answer=raw_question["correct_answer"],
            justification=raw_question["justification"],
            source_chunks=raw_question["source_chunks"],
            metadata={
                "banca": request.edital_summary["banca"],
                "ano": request.edital_summary["ano"],
                "topico": request.topic,
                "dificuldade": request.edital_summary.get("dificuldade", "intermediaria"),
                "estilo": request.edital_summary.get("estilo", "conceitual"),
                "plausibilidade_score": quality_result["plausibility"],
                "consistency_score": consistency_result["score"],
                "plagiarism_score": plagiarism_result["score"]
            },
            generation_time=0.0,  # TODO: Calcular tempo real
            timestamp=datetime.now()
        )
        
        return question_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/batch", response_model=BatchGenerationResponse)
async def generate_batch(
    background_tasks: BackgroundTasks,
    request: BatchGenerationRequest
):
    """Gerar questões em lote"""
    try:
        # Processar lote
        batch_result = await batch_service.process_batch(request)
        
        return BatchGenerationResponse(
            batch_id=batch_result["batch_id"],
            status=batch_result["status"],
            total_requests=len(request.requests),
            successful=batch_result["successful"],
            failed=batch_result["failed"],
            questions=batch_result["questions"],
            failed_requests=batch_result["failed_requests"],
            processing_time=batch_result["processing_time"],
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate/question", response_model=ValidationResponse)
async def validate_question(request: ValidationRequest):
    """Validar questão"""
    try:
        # Validar questão
        validation_result = await validation_service.validate_question({
            "question": request.question,
            "alternatives": request.alternatives,
            "correct_answer": request.correct_answer,
            "justification": request.justification,
            "source_chunks": request.source_chunks
        })
        
        return ValidationResponse(
            validation_id=f"val_{int(time.time())}",
            is_valid=validation_result["is_valid"],
            scores=validation_result["scores"],
            checks=validation_result["checks"],
            recommendations=validation_result.get("recommendations", []),
            validation_time=validation_result["validation_time"],
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/questions/{question_id}")
async def get_question(question_id: str):
    """Obter questão por ID"""
    try:
        # TODO: Implementar busca de questão
        return {"message": f"Question {question_id} not found"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/batches/{batch_id}")
async def get_batch(batch_id: str):
    """Obter lote por ID"""
    try:
        # TODO: Implementar busca de lote
        return {"message": f"Batch {batch_id} not found"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/questions")
async def list_questions(
    skip: int = 0,
    limit: int = 100,
    filters: Optional[dict] = None
):
    """Listar questões"""
    try:
        # TODO: Implementar listagem de questões
        return {"questions": [], "total": 0}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/batches")
async def list_batches(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
):
    """Listar lotes"""
    try:
        # TODO: Implementar listagem de lotes
        return {"batches": [], "total": 0}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/questions/{question_id}")
async def delete_question(question_id: str):
    """Deletar questão"""
    try:
        # TODO: Implementar deleção de questão
        return {"message": f"Question {question_id} deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/batches/{batch_id}")
async def delete_batch(batch_id: str):
    """Deletar lote"""
    try:
        # TODO: Implementar deleção de lote
        return {"message": f"Batch {batch_id} deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
