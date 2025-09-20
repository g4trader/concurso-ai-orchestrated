"""
Modelos de Response para UX-001
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class FeedbackCategoryResponse(BaseModel):
    """Categoria do feedback"""
    id: str = Field(..., description="ID da categoria")
    name: str = Field(..., description="Nome da categoria")
    description: str = Field(..., description="Descrição da categoria")
    priority: str = Field(..., description="Prioridade da categoria")
    icon: str = Field(..., description="Ícone da categoria")

class FeedbackResponse(BaseModel):
    """Response do feedback"""
    id: str = Field(..., description="ID único do feedback")
    question_id: str = Field(..., description="ID da questão")
    user_id: str = Field(..., description="ID do usuário")
    category: FeedbackCategoryResponse = Field(..., description="Categoria do feedback")
    comment: str = Field(..., description="Comentário do usuário")
    status: str = Field(..., description="Status do feedback")
    priority: str = Field(..., description="Prioridade do feedback")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data de atualização")
    admin_comment: Optional[str] = Field(None, description="Comentário do administrador")
    metadata: Dict[str, Any] = Field(..., description="Metadados da questão")

class FeedbackListResponse(BaseModel):
    """Response para lista de feedbacks"""
    feedbacks: List[FeedbackResponse] = Field(..., description="Lista de feedbacks")
    total: int = Field(..., description="Total de feedbacks")
    page: int = Field(..., description="Página atual")
    page_size: int = Field(..., description="Tamanho da página")
    has_next: bool = Field(..., description="Tem próxima página")

class FeedbackStatusResponse(BaseModel):
    """Response para atualização de status"""
    id: str = Field(..., description="ID do feedback")
    status: str = Field(..., description="Novo status")
    priority: str = Field(..., description="Prioridade")
    admin_comment: Optional[str] = Field(None, description="Comentário do administrador")
    updated_at: datetime = Field(..., description="Data de atualização")

class FeedbackDraftResponse(BaseModel):
    """Response para rascunho de feedback"""
    id: str = Field(..., description="ID do rascunho")
    question_id: str = Field(..., description="ID da questão")
    user_id: str = Field(..., description="ID do usuário")
    category: Optional[FeedbackCategoryResponse] = Field(None, description="Categoria do feedback")
    comment: Optional[str] = Field(None, description="Comentário do usuário")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadados da questão")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data de atualização")
    expires_at: datetime = Field(..., description="Data de expiração")

class BulkFeedbackResponse(BaseModel):
    """Response para envio em lote"""
    processed: int = Field(..., description="Número de feedbacks processados")
    failed: int = Field(..., description="Número de feedbacks falharam")
    feedback_ids: List[str] = Field(..., description="IDs dos feedbacks criados")
    errors: List[Dict[str, Any]] = Field(..., description="Erros encontrados")
    processing_time: float = Field(..., description="Tempo de processamento")

class FeedbackAnalyticsResponse(BaseModel):
    """Response para analytics de feedback"""
    total_feedbacks: int = Field(..., description="Total de feedbacks")
    feedbacks_by_category: Dict[str, int] = Field(..., description="Feedbacks por categoria")
    feedbacks_by_status: Dict[str, int] = Field(..., description="Feedbacks por status")
    feedbacks_by_priority: Dict[str, int] = Field(..., description="Feedbacks por prioridade")
    feedbacks_by_date: Dict[str, int] = Field(..., description="Feedbacks por data")
    top_question_issues: List[Dict[str, Any]] = Field(..., description="Principais problemas por questão")
    average_response_time: float = Field(..., description="Tempo médio de resposta")
    user_satisfaction_score: float = Field(..., description="Score de satisfação do usuário")

class FeedbackSubmissionResponse(BaseModel):
    """Response para submissão de feedback"""
    id: str = Field(..., description="ID do feedback criado")
    message: str = Field(..., description="Mensagem de confirmação")
    status: str = Field(..., description="Status inicial do feedback")
    estimated_response_time: str = Field(..., description="Tempo estimado de resposta")

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
