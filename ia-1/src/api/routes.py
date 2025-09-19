"""
Rotas da API IA-1
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from typing import List, Optional
import json
import time
from datetime import datetime
from src.models.request import (
    DocumentUploadRequest, QueryRequest, BatchUploadRequest,
    IndexRebuildRequest, HealthCheckRequest
)
from src.models.response import (
    DocumentUploadResponse, QueryResponse, HealthResponse,
    BatchUploadResponse, IndexRebuildResponse, MetricsResponse,
    IndexStatus, ErrorResponse
)
from src.services.parser_service import ParserService
from src.services.chunking_service import ChunkingService
from src.services.embedding_service import EmbeddingService
from src.services.indexing_service import IndexingService
from src.services.reranker_service import RerankerService
from src.services.query_service import QueryService
from src.services.health_check import HealthCheckService
import aiofiles
import os

router = APIRouter(prefix="/api/v1", tags=["ia-1"])

async def save_uploaded_file(file: UploadFile) -> str:
    """Salva arquivo enviado e retorna o caminho"""
    # Criar diretório temporário se não existir
    temp_dir = "/tmp/uploads"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Gerar nome único para o arquivo
    file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
    temp_filename = f"upload_{int(time.time())}{file_extension}"
    file_path = os.path.join(temp_dir, temp_filename)
    
    # Salvar arquivo
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return file_path

# Dependências
parser_service = ParserService()
chunking_service = ChunkingService()
embedding_service = EmbeddingService()
indexing_service = IndexingService()
reranker_service = RerankerService()
query_service = QueryService()
health_service = HealthCheckService()

@router.get("/", response_model=dict)
async def root():
    """Endpoint raiz"""
    return {
        "service": "IA-1 Pipeline de Ingestão",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@router.get("/health", response_model=HealthResponse)
async def health_check(request: HealthCheckRequest = None):
    """Health check da aplicação"""
    return await health_service.check_health(request)

@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Métricas da aplicação"""
    return await health_service.get_metrics()

@router.get("/index/status", response_model=IndexStatus)
async def get_index_status():
    """Status do índice"""
    return await indexing_service.get_index_status()

@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    request: DocumentUploadRequest
):
    """Upload e processamento de documento"""
    try:
        # 1. Parse do documento
        parsed_content = await parser_service.parse_document(request.file_path)
        
        # 2. Chunking
        chunks = await chunking_service.create_chunks(
            parsed_content, 
            request.chunk_size, 
            request.chunk_overlap
        )
        
        # 3. Embedding
        embeddings = await embedding_service.generate_embeddings(chunks)
        
        # 4. Indexing
        document_id = await indexing_service.index_document(
            chunks, embeddings, request.metadata
        )
        
        return DocumentUploadResponse(
            document_id=document_id,
            status="processed",
            chunks_created=len(chunks),
            processing_time=0.0,  # TODO: Calcular tempo real
            metadata=request.metadata,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/upload/file", response_model=DocumentUploadResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    metadata: str = None
):
    """Upload de arquivo via multipart"""
    try:
        # Salvar arquivo temporariamente
        file_path = await save_uploaded_file(file)
        
        # Processar documento
        request = DocumentUploadRequest(
            file_path=file_path,
            metadata=json.loads(metadata) if metadata else {},
            chunk_size=512,
            chunk_overlap=50
        )
        
        return await upload_document(background_tasks, request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/upload/batch", response_model=BatchUploadResponse)
async def upload_batch(
    background_tasks: BackgroundTasks,
    request: BatchUploadRequest
):
    """Upload em lote de documentos"""
    try:
        results = []
        successful = 0
        failed = 0
        
        for doc_request in request.documents:
            try:
                result = await upload_document(background_tasks, doc_request)
                results.append(result)
                successful += 1
            except Exception as e:
                failed += 1
                # TODO: Adicionar resultado de erro
        
        return BatchUploadResponse(
            batch_id=f"batch_{int(time.time())}",
            total_documents=len(request.documents),
            successful=successful,
            failed=failed,
            processing_time=0.0,  # TODO: Calcular tempo real
            results=results,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Busca de documentos"""
    try:
        # 1. Busca por similaridade
        results = await query_service.search_similarity(
            request.query,
            request.filters,
            request.top_k
        )
        
        # 2. Reranking se solicitado
        if request.rerank and len(results) > 0:
            results = await reranker_service.rerank_results(
                request.query, results
            )
        
        # 3. Filtrar por threshold
        filtered_results = [
            r for r in results 
            if r.score >= request.similarity_threshold
        ]
        
        return QueryResponse(
            query_id=f"qry_{int(time.time())}",
            results=filtered_results,
            total_results=len(filtered_results),
            processing_time=0.0,  # TODO: Calcular tempo real
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/index/rebuild", response_model=IndexRebuildResponse)
async def rebuild_index(
    background_tasks: BackgroundTasks,
    request: IndexRebuildRequest
):
    """Rebuild do índice"""
    try:
        # TODO: Implementar rebuild do índice
        return IndexRebuildResponse(
            rebuild_id=f"rebuild_{int(time.time())}",
            status="completed",
            documents_processed=0,
            chunks_created=0,
            processing_time=0.0,
            backup_created=request.backup_existing,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Deletar documento do índice"""
    try:
        await indexing_service.delete_document(document_id)
        return {"message": f"Document {document_id} deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{document_id}")
async def get_document(document_id: str):
    """Obter informações de um documento"""
    try:
        document_info = await indexing_service.get_document_info(document_id)
        return document_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    filters: Optional[dict] = None
):
    """Listar documentos"""
    try:
        documents = await indexing_service.list_documents(skip, limit, filters)
        return documents
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
