"""
Modelos de response para IA-1
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class DocumentUploadResponse(BaseModel):
    """Response para upload de documento"""
    document_id: str = Field(..., description="ID do documento")
    status: str = Field(..., description="Status do processamento")
    chunks_created: int = Field(..., description="Número de chunks criados")
    processing_time: float = Field(..., description="Tempo de processamento")
    metadata: Dict[str, Any] = Field(..., description="Metadados do documento")
    timestamp: datetime = Field(..., description="Timestamp do processamento")

class QueryResult(BaseModel):
    """Resultado de uma busca"""
    chunk_id: str = Field(..., description="ID do chunk")
    document_id: str = Field(..., description="ID do documento")
    text: str = Field(..., description="Texto do chunk")
    score: float = Field(..., description="Score de similaridade")
    rerank_score: Optional[float] = Field(None, description="Score após reranking")
    metadata: Dict[str, Any] = Field(..., description="Metadados do chunk")

class QueryResponse(BaseModel):
    """Response para busca de documentos"""
    query_id: str = Field(..., description="ID da consulta")
    results: List[QueryResult] = Field(..., description="Resultados da busca")
    total_results: int = Field(..., description="Total de resultados")
    processing_time: float = Field(..., description="Tempo de processamento")
    timestamp: datetime = Field(..., description="Timestamp da consulta")

class HealthResponse(BaseModel):
    """Response para health check"""
    status: str = Field(..., description="Status geral")
    services: Dict[str, Dict[str, Any]] = Field(..., description="Status dos serviços")
    uptime: float = Field(..., description="Tempo de atividade")
    timestamp: datetime = Field(..., description="Timestamp do check")

class ServiceStatus(BaseModel):
    """Status de um serviço"""
    name: str = Field(..., description="Nome do serviço")
    status: str = Field(..., description="Status do serviço")
    response_time: Optional[float] = Field(None, description="Tempo de resposta")
    error: Optional[str] = Field(None, description="Erro se houver")
    last_check: datetime = Field(..., description="Última verificação")

class IndexStatus(BaseModel):
    """Status do índice"""
    total_documents: int = Field(..., description="Total de documentos")
    total_chunks: int = Field(..., description="Total de chunks")
    index_size: str = Field(..., description="Tamanho do índice")
    last_updated: datetime = Field(..., description="Última atualização")
    health: str = Field(..., description="Saúde do índice")

class MetricsResponse(BaseModel):
    """Response para métricas"""
    uptime: float = Field(..., description="Tempo de atividade")
    total_queries: int = Field(..., description="Total de consultas")
    total_documents: int = Field(..., description="Total de documentos")
    total_chunks: int = Field(..., description="Total de chunks")
    avg_query_time: float = Field(..., description="Tempo médio de consulta")
    avg_processing_time: float = Field(..., description="Tempo médio de processamento")
    timestamp: datetime = Field(..., description="Timestamp das métricas")

class BatchUploadResponse(BaseModel):
    """Response para upload em lote"""
    batch_id: str = Field(..., description="ID do lote")
    total_documents: int = Field(..., description="Total de documentos")
    successful: int = Field(..., description="Documentos processados com sucesso")
    failed: int = Field(..., description="Documentos que falharam")
    processing_time: float = Field(..., description="Tempo total de processamento")
    results: List[DocumentUploadResponse] = Field(..., description="Resultados individuais")
    timestamp: datetime = Field(..., description="Timestamp do processamento")

class IndexRebuildResponse(BaseModel):
    """Response para rebuild do índice"""
    rebuild_id: str = Field(..., description="ID do rebuild")
    status: str = Field(..., description="Status do rebuild")
    documents_processed: int = Field(..., description="Documentos processados")
    chunks_created: int = Field(..., description="Chunks criados")
    processing_time: float = Field(..., description="Tempo de processamento")
    backup_created: bool = Field(..., description="Backup criado")
    timestamp: datetime = Field(..., description="Timestamp do rebuild")

class ErrorResponse(BaseModel):
    """Response de erro"""
    error: str = Field(..., description="Mensagem de erro")
    code: str = Field(..., description="Código do erro")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalhes do erro")
    timestamp: datetime = Field(..., description="Timestamp do erro")

class ChunkInfo(BaseModel):
    """Informações de um chunk"""
    chunk_id: str = Field(..., description="ID do chunk")
    document_id: str = Field(..., description="ID do documento")
    text: str = Field(..., description="Texto do chunk")
    metadata: Dict[str, Any] = Field(..., description="Metadados do chunk")
    created_at: datetime = Field(..., description="Data de criação")

class DocumentInfo(BaseModel):
    """Informações de um documento"""
    document_id: str = Field(..., description="ID do documento")
    file_path: str = Field(..., description="Caminho do arquivo")
    metadata: Dict[str, Any] = Field(..., description="Metadados do documento")
    chunks_count: int = Field(..., description="Número de chunks")
    status: str = Field(..., description="Status do documento")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data de atualização")
