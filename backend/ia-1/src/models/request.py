"""
Modelos de request para IA-1
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class DocumentType(str, Enum):
    """Tipos de documento suportados"""
    PDF = "pdf"
    TXT = "txt"
    DOCX = "docx"
    IMAGE = "image"

class DocumentUploadRequest(BaseModel):
    """Request para upload de documento"""
    file_path: str = Field(..., description="Caminho do arquivo")
    metadata: Dict[str, Any] = Field(..., description="Metadados do documento")
    chunk_size: Optional[int] = Field(512, description="Tamanho do chunk")
    chunk_overlap: Optional[int] = Field(50, description="Overlap entre chunks")

class DocumentMetadata(BaseModel):
    """Metadados do documento"""
    banca: str = Field(..., description="Banca organizadora")
    ano: int = Field(..., description="Ano do documento")
    topico: str = Field(..., description="Tópico/área")
    tipo: str = Field(..., description="Tipo do documento")
    orgao: Optional[str] = Field(None, description="Órgão responsável")
    edital: Optional[str] = Field(None, description="Número do edital")
    cargo: Optional[str] = Field(None, description="Cargo/área")

class QueryRequest(BaseModel):
    """Request para busca de documentos"""
    query: str = Field(..., description="Consulta de busca")
    filters: Optional[Dict[str, Any]] = Field(None, description="Filtros de busca")
    top_k: Optional[int] = Field(10, description="Número de resultados")
    rerank: Optional[bool] = Field(True, description="Aplicar reranking")
    similarity_threshold: Optional[float] = Field(0.7, description="Threshold de similaridade")

class QueryFilters(BaseModel):
    """Filtros para busca"""
    banca: Optional[str] = Field(None, description="Filtrar por banca")
    topico: Optional[str] = Field(None, description="Filtrar por tópico")
    ano: Optional[int] = Field(None, description="Filtrar por ano")
    tipo: Optional[str] = Field(None, description="Filtrar por tipo")
    orgao: Optional[str] = Field(None, description="Filtrar por órgão")

class BatchUploadRequest(BaseModel):
    """Request para upload em lote"""
    documents: List[DocumentUploadRequest] = Field(..., description="Lista de documentos")
    batch_size: Optional[int] = Field(10, description="Tamanho do lote")

class IndexRebuildRequest(BaseModel):
    """Request para rebuild do índice"""
    force_rebuild: Optional[bool] = Field(False, description="Forçar rebuild completo")
    backup_existing: Optional[bool] = Field(True, description="Fazer backup do índice existente")

class HealthCheckRequest(BaseModel):
    """Request para health check"""
    check_services: Optional[List[str]] = Field(None, description="Serviços para verificar")
    deep_check: Optional[bool] = Field(False, description="Verificação profunda")
