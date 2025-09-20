"""
Modelos de Response para WEB-004
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class QuestionResult(BaseModel):
    """Resultado de uma questão"""
    question_id: str = Field(..., description="ID da questão")
    user_answer: str = Field(..., description="Resposta do usuário")
    correct_answer: str = Field(..., description="Resposta correta")
    is_correct: bool = Field(..., description="Se a resposta está correta")
    time_spent: int = Field(..., description="Tempo gasto em segundos")
    topic: str = Field(..., description="Tópico da questão")
    difficulty: str = Field(..., description="Dificuldade da questão")

class PerformanceAnalysis(BaseModel):
    """Análise de performance"""
    overall_score: float = Field(..., description="Pontuação geral")
    time_efficiency: float = Field(..., description="Eficiência de tempo")
    accuracy_rate: float = Field(..., description="Taxa de precisão")
    completion_rate: float = Field(..., description="Taxa de conclusão")
    topic_performance: Dict[str, float] = Field(..., description="Performance por tópico")
    difficulty_performance: Dict[str, float] = Field(..., description="Performance por dificuldade")
    time_analysis: Dict[str, Any] = Field(..., description="Análise de tempo")
    improvement_areas: List[str] = Field(..., description="Áreas de melhoria")

class WeakPoint(BaseModel):
    """Ponto fraco identificado"""
    topic: str = Field(..., description="Tópico")
    difficulty: str = Field(..., description="Dificuldade")
    accuracy: float = Field(..., description="Precisão no tópico")
    time_spent: int = Field(..., description="Tempo gasto")
    questions_count: int = Field(..., description="Número de questões")
    severity: str = Field(..., description="Severidade do ponto fraco")

class Recommendation(BaseModel):
    """Recomendação de estudo"""
    type: str = Field(..., description="Tipo de recomendação")
    priority: str = Field(..., description="Prioridade")
    title: str = Field(..., description="Título da recomendação")
    description: str = Field(..., description="Descrição")
    action_items: List[str] = Field(..., description="Itens de ação")
    estimated_time: Optional[int] = Field(None, description="Tempo estimado em horas")
    resources: Optional[List[str]] = Field(None, description="Recursos recomendados")

class SimuladoResults(BaseModel):
    """Resultados do simulado"""
    id: str = Field(..., description="ID único do resultado")
    simulado_id: str = Field(..., description="ID do simulado")
    user_id: str = Field(..., description="ID do usuário")
    total_questions: int = Field(..., description="Total de questões")
    correct_answers: int = Field(..., description="Respostas corretas")
    wrong_answers: int = Field(..., description="Respostas incorretas")
    unanswered_questions: int = Field(..., description="Questões não respondidas")
    score: float = Field(..., description="Pontuação 0-100")
    time_spent: int = Field(..., description="Tempo gasto em segundos")
    average_time_per_question: float = Field(..., description="Tempo médio por questão")
    submitted_at: datetime = Field(..., description="Data de submissão")
    completed_at: datetime = Field(..., description="Data de conclusão")
    results: List[QuestionResult] = Field(..., description="Resultados por questão")
    performance: PerformanceAnalysis = Field(..., description="Análise de performance")
    weak_points: List[WeakPoint] = Field(..., description="Pontos fracos identificados")
    recommendations: List[Recommendation] = Field(..., description="Recomendações")

class AnalyzeResultsResponse(BaseModel):
    """Response para análise de resultados"""
    results_id: str = Field(..., description="ID dos resultados")
    analysis_completed: bool = Field(..., description="Se a análise foi concluída")
    performance_analysis: Optional[PerformanceAnalysis] = Field(None, description="Análise de performance")
    weak_points: Optional[List[WeakPoint]] = Field(None, description="Pontos fracos")
    recommendations: Optional[List[Recommendation]] = Field(None, description="Recomendações")
    processing_time: float = Field(..., description="Tempo de processamento")
    timestamp: datetime = Field(..., description="Timestamp da análise")

class ExportResultsResponse(BaseModel):
    """Response para exportação de resultados"""
    export_id: str = Field(..., description="ID da exportação")
    format: str = Field(..., description="Formato do arquivo")
    download_url: Optional[str] = Field(None, description="URL de download")
    expires_at: datetime = Field(..., description="Data de expiração")
    file_size: Optional[int] = Field(None, description="Tamanho do arquivo em bytes")
    processing_time: float = Field(..., description="Tempo de processamento")

class SaveDraftResponse(BaseModel):
    """Response para salvar rascunho"""
    draft_id: str = Field(..., description="ID do rascunho")
    saved_at: datetime = Field(..., description="Data de salvamento")
    message: str = Field(..., description="Mensagem de confirmação")

class ShareResultsResponse(BaseModel):
    """Response para compartilhar resultados"""
    share_id: str = Field(..., description="ID do compartilhamento")
    share_url: str = Field(..., description="URL de compartilhamento")
    share_token: str = Field(..., description="Token de compartilhamento")
    expires_at: datetime = Field(..., description="Data de expiração")
    access_type: str = Field(..., description="Tipo de acesso")

class ChartsResponse(BaseModel):
    """Response para dados de gráficos"""
    chart_data: Dict[str, Any] = Field(..., description="Dados dos gráficos")
    chart_types: List[str] = Field(..., description="Tipos de gráficos gerados")
    time_range: str = Field(..., description="Período de tempo")
    generated_at: datetime = Field(..., description="Data de geração")

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
