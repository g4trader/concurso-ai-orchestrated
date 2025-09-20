"""
Modelos de Request para UX-001
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class FeedbackCategory(BaseModel):
    """Categoria do feedback"""
    id: str = Field(..., description="ID da categoria")
    name: str = Field(..., description="Nome da categoria")
    description: str = Field(..., description="Descrição da categoria")
    priority: str = Field(..., description="Prioridade da categoria")
    icon: str = Field(..., description="Ícone da categoria")

class FeedbackMetadata(BaseModel):
    """Metadados da questão"""
    question_text: str = Field(..., description="Texto da questão")
    question_options: List[str] = Field(..., description="Opções da questão")
    correct_answer: str = Field(..., description="Resposta correta")
    user_answer: str = Field(..., description="Resposta do usuário")
    topic: str = Field(..., description="Tópico da questão")
    difficulty: str = Field(..., description="Dificuldade da questão")
    banca: str = Field(..., description="Banca da questão")

class FeedbackRequest(BaseModel):
    """Request para enviar feedback"""
    question_id: str = Field(..., description="ID da questão")
    user_id: str = Field(..., description="ID do usuário")
    category: FeedbackCategory = Field(..., description="Categoria do feedback")
    comment: str = Field(..., min_length=10, max_length=1000, description="Comentário do usuário")
    metadata: FeedbackMetadata = Field(..., description="Metadados da questão")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp do feedback")
    user_agent: str = Field(..., description="User agent do navegador")
    session_id: str = Field(..., description="ID da sessão")

class FeedbackStatusUpdate(BaseModel):
    """Request para atualizar status do feedback"""
    status: str = Field(..., pattern="^(pending|reviewing|resolved|rejected)$", description="Novo status do feedback")
    admin_comment: Optional[str] = Field(None, description="Comentário do administrador")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$", description="Prioridade do feedback")

class FeedbackDraftRequest(BaseModel):
    """Request para salvar rascunho de feedback"""
    question_id: str = Field(..., description="ID da questão")
    user_id: str = Field(..., description="ID do usuário")
    category: Optional[FeedbackCategory] = Field(None, description="Categoria do feedback")
    comment: Optional[str] = Field(None, max_length=1000, description="Comentário do usuário")
    metadata: Optional[FeedbackMetadata] = Field(None, description="Metadados da questão")

class BulkFeedbackRequest(BaseModel):
    """Request para envio em lote de feedback"""
    feedbacks: List[FeedbackRequest] = Field(..., max_items=50, description="Lista de feedbacks")
    session_id: str = Field(..., description="ID da sessão")

class FeedbackAnalyticsRequest(BaseModel):
    """Request para analytics de feedback"""
    date_from: Optional[datetime] = Field(None, description="Data inicial")
    date_to: Optional[datetime] = Field(None, description="Data final")
    category: Optional[str] = Field(None, description="Filtrar por categoria")
    status: Optional[str] = Field(None, description="Filtrar por status")
    user_id: Optional[str] = Field(None, description="Filtrar por usuário")

class HealthCheckRequest(BaseModel):
    """Request para health check"""
    check_components: Optional[bool] = Field(False, description="Verificar componentes")

class MetricsRequest(BaseModel):
    """Request para métricas"""
    time_range: Optional[str] = Field("1h", description="Período das métricas")
