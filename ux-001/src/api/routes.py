"""
Rotas da API UX-001
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional, List
import time
import uuid
from datetime import datetime, timedelta
from src.models.request import (
    FeedbackRequest, FeedbackStatusUpdate, FeedbackDraftRequest,
    BulkFeedbackRequest, FeedbackAnalyticsRequest, HealthCheckRequest, MetricsRequest
)
from src.models.response import (
    FeedbackResponse, FeedbackListResponse, FeedbackStatusResponse,
    FeedbackDraftResponse, BulkFeedbackResponse, FeedbackAnalyticsResponse,
    FeedbackSubmissionResponse, HealthResponse, MetricsResponse, ErrorResponse,
    FeedbackCategoryResponse
)
from src.services.health_check import HealthCheckService

router = APIRouter(prefix="/api/v1", tags=["ux-001"])

# Dependências
health_service = HealthCheckService()

@router.get("/", response_model=dict)
async def root():
    """Endpoint raiz"""
    return {
        "service": "UX-001 Sistema de Feedback do Usuário",
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

@router.post("/feedback", response_model=FeedbackSubmissionResponse)
async def submit_feedback(request: FeedbackRequest):
    """Enviar feedback"""
    try:
        # Mock feedback submission - em produção seria persistência real
        feedback_id = str(uuid.uuid4())
        
        submission_response = FeedbackSubmissionResponse(
            id=feedback_id,
            message="Feedback enviado com sucesso! Obrigado pela sua contribuição.",
            status="pending",
            estimated_response_time="2-5 dias úteis"
        )
        
        return submission_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(feedback_id: str):
    """Obter feedback específico"""
    try:
        # Mock feedback - em produção seria busca real
        mock_category = FeedbackCategoryResponse(
            id="error_in_question",
            name="Erro na Questão",
            description="A questão contém um erro factual ou técnico",
            priority="high",
            icon="alert-triangle"
        )
        
        mock_feedback = FeedbackResponse(
            id=feedback_id,
            question_id="q_123456",
            user_id="user_789012",
            category=mock_category,
            comment="A alternativa B está incorreta. A resposta correta deveria ser A.",
            status="pending",
            priority="high",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            admin_comment=None,
            metadata={
                "question_text": "Qual é o prazo para recurso em processo administrativo?",
                "question_options": ["A) 30 dias", "B) 60 dias", "C) 90 dias"],
                "correct_answer": "A",
                "user_answer": "B",
                "topic": "Direito Administrativo",
                "difficulty": "medium",
                "banca": "CESPE"
            }
        )
        
        return mock_feedback
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback", response_model=FeedbackListResponse)
async def list_feedbacks(
    page: int = 1,
    page_size: int = 10,
    status: Optional[str] = None,
    category: Optional[str] = None
):
    """Listar feedbacks (admin)"""
    try:
        # Mock feedback list - em produção seria busca real
        mock_feedbacks = []
        for i in range(min(page_size, 5)):  # Mock com 5 itens máximo
            mock_category = FeedbackCategoryResponse(
                id="error_in_question",
                name="Erro na Questão",
                description="A questão contém um erro factual ou técnico",
                priority="high",
                icon="alert-triangle"
            )
            
            mock_feedback = FeedbackResponse(
                id=f"feedback_{i}",
                question_id=f"q_{i}",
                user_id=f"user_{i}",
                category=mock_category,
                comment=f"Comentário de exemplo {i}",
                status="pending",
                priority="high",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                admin_comment=None,
                metadata={"topic": "Direito Administrativo"}
            )
            mock_feedbacks.append(mock_feedback)
        
        feedback_list = FeedbackListResponse(
            feedbacks=mock_feedbacks,
            total=50,
            page=page,
            page_size=page_size,
            has_next=page * page_size < 50
        )
        
        return feedback_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/feedback/{feedback_id}/status", response_model=FeedbackStatusResponse)
async def update_feedback_status(feedback_id: str, request: FeedbackStatusUpdate):
    """Atualizar status do feedback"""
    try:
        # Mock status update - em produção seria atualização real
        status_response = FeedbackStatusResponse(
            id=feedback_id,
            status=request.status,
            priority=request.priority or "medium",
            admin_comment=request.admin_comment,
            updated_at=datetime.now()
        )
        
        return status_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback/categories", response_model=List[FeedbackCategoryResponse])
async def get_feedback_categories():
    """Obter categorias de feedback"""
    try:
        # Mock categories - em produção seria busca real
        categories = [
            FeedbackCategoryResponse(
                id="error_in_question",
                name="Erro na Questão",
                description="A questão contém um erro factual ou técnico",
                priority="high",
                icon="alert-triangle"
            ),
            FeedbackCategoryResponse(
                id="typo_in_question",
                name="Erro de Digitação",
                description="A questão contém erro de ortografia ou digitação",
                priority="medium",
                icon="type"
            ),
            FeedbackCategoryResponse(
                id="unclear_question",
                name="Questão Confusa",
                description="A questão não está clara ou é ambígua",
                priority="medium",
                icon="help-circle"
            ),
            FeedbackCategoryResponse(
                id="wrong_answer",
                name="Resposta Incorreta",
                description="A resposta marcada como correta está incorreta",
                priority="high",
                icon="x-circle"
            ),
            FeedbackCategoryResponse(
                id="suggestion",
                name="Sugestão",
                description="Sugestão para melhoria da questão",
                priority="low",
                icon="lightbulb"
            ),
            FeedbackCategoryResponse(
                id="compliment",
                name="Elogio",
                description="Elogio sobre a qualidade da questão",
                priority="low",
                icon="thumbs-up"
            ),
            FeedbackCategoryResponse(
                id="other",
                name="Outros",
                description="Outros tipos de feedback",
                priority="low",
                icon="more-horizontal"
            )
        ]
        
        return categories
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback/draft", response_model=FeedbackDraftResponse)
async def save_feedback_draft(request: FeedbackDraftRequest):
    """Salvar rascunho de feedback"""
    try:
        # Mock draft save - em produção seria salvamento real
        draft_id = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(hours=24)
        
        draft_response = FeedbackDraftResponse(
            id=draft_id,
            question_id=request.question_id,
            user_id=request.user_id,
            category=request.category,
            comment=request.comment,
            metadata=request.metadata.dict() if request.metadata else None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            expires_at=expires_at
        )
        
        return draft_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback/draft/{question_id}", response_model=FeedbackDraftResponse)
async def get_feedback_draft(question_id: str, user_id: str):
    """Obter rascunho de feedback"""
    try:
        # Mock draft retrieval - em produção seria busca real
        draft_response = FeedbackDraftResponse(
            id="draft_123",
            question_id=question_id,
            user_id=user_id,
            category=FeedbackCategoryResponse(
                id="error_in_question",
                name="Erro na Questão",
                description="A questão contém um erro factual ou técnico",
                priority="high",
                icon="alert-triangle"
            ),
            comment="Rascunho de comentário...",
            metadata={"topic": "Direito Administrativo"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=20)
        )
        
        return draft_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/feedback/draft/{question_id}")
async def delete_feedback_draft(question_id: str, user_id: str):
    """Limpar rascunho de feedback"""
    try:
        # Mock draft deletion - em produção seria remoção real
        return {"message": "Rascunho removido com sucesso"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback/analytics", response_model=FeedbackAnalyticsResponse)
async def get_feedback_analytics(request: FeedbackAnalyticsRequest):
    """Analytics de feedback"""
    try:
        # Mock analytics - em produção seria análise real
        analytics_response = FeedbackAnalyticsResponse(
            total_feedbacks=150,
            feedbacks_by_category={
                "error_in_question": 45,
                "typo_in_question": 30,
                "unclear_question": 25,
                "wrong_answer": 20,
                "suggestion": 15,
                "compliment": 10,
                "other": 5
            },
            feedbacks_by_status={
                "pending": 80,
                "reviewing": 40,
                "resolved": 25,
                "rejected": 5
            },
            feedbacks_by_priority={
                "high": 65,
                "medium": 50,
                "low": 35
            },
            feedbacks_by_date={
                "2024-01-15": 15,
                "2024-01-16": 20,
                "2024-01-17": 18
            },
            top_question_issues=[
                {"question_id": "q_123", "issue_count": 5},
                {"question_id": "q_456", "issue_count": 3}
            ],
            average_response_time=2.5,
            user_satisfaction_score=4.2
        )
        
        return analytics_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback/bulk", response_model=BulkFeedbackResponse)
async def submit_bulk_feedback(request: BulkFeedbackRequest):
    """Envio em lote de feedback"""
    try:
        # Mock bulk submission - em produção seria processamento real
        feedback_ids = [str(uuid.uuid4()) for _ in range(len(request.feedbacks))]
        
        bulk_response = BulkFeedbackResponse(
            processed=len(request.feedbacks),
            failed=0,
            feedback_ids=feedback_ids,
            errors=[],
            processing_time=1.5
        )
        
        return bulk_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
