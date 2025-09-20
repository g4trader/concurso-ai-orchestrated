# README_IA-1: Pipeline de Ingestão — Parse→Chunk→Embed→Index (+Rerank)

## 1. Objetivo/Contexto

### **Objetivo**
Implementar um pipeline completo de ingestão de documentos para RAG (Retrieval-Augmented Generation), transformando documentos brutos (PDFs, imagens, textos) em representações vetoriais indexadas e pesquisáveis.

### **Contexto do Projeto**
- **Projeto**: Concurso-AI Orchestrated
- **Sprint**: 2 - Camada IA — Infra e Ingestão
- **História**: IA-1 - Pipeline de ingestão
- **Usuário**: Motor de geração de questões
- **Valor**: Recuperação precisa de contexto por banca/tópico

### **Problema Resolvido**
Estruturar conteúdo para RAG (editais/provas) com embeddings e reranker local, permitindo busca semântica eficiente em documentos de concursos públicos.

### **Arquitetura do Pipeline**
```
PDF/Imagem → Parser → Chunking → Embedding → Indexing → Vector Store
                                                           ↓
Query → Search → Reranking → Ranked Results → Response
```

## 2. Como Rodar (Conceitual)

### **Pré-requisitos**
- Python 3.11+
- Tesseract OCR instalado
- Modelos ML baixados (BGE-M3, BGE-Reranker-Large)
- Espaço em disco para índices FAISS

### **Instalação**
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar diretórios
mkdir -p data/faiss_index data/metadata uploads/ backups/

# 3. Baixar modelos ML
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-m3')"
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-reranker-large')"

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações
```

### **Execução**
```bash
# Desenvolvimento
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload

# Produção
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001

# Docker
docker build -t ia-1-pipeline .
docker run -p 8001:8001 ia-1-pipeline
```

### **Verificação**
```bash
# Health check
curl http://localhost:8001/api/v1/health

# Status do índice
curl http://localhost:8001/api/v1/index/status

# Métricas
curl http://localhost:8001/api/v1/metrics
```

## 3. APIs/Contratos com Exemplos

### **Upload de Documento**
```bash
POST /api/v1/documents/upload
Content-Type: application/json

{
  "file_path": "/path/to/document.pdf",
  "metadata": {
    "banca": "CESPE",
    "ano": 2024,
    "topico": "Direito Constitucional",
    "tipo": "edital",
    "orgao": "STF"
  },
  "chunk_size": 512,
  "chunk_overlap": 50
}
```

**Response:**
```json
{
  "document_id": "doc_123456",
  "status": "processed",
  "chunks_created": 45,
  "processing_time": 12.5,
  "metadata": {
    "banca": "CESPE",
    "ano": 2024,
    "topico": "Direito Constitucional",
    "tipo": "edital",
    "orgao": "STF"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Upload de Arquivo via Multipart**
```bash
POST /api/v1/documents/upload/file
Content-Type: multipart/form-data

file: [arquivo.pdf]
metadata: {"banca": "CESPE", "ano": 2024, "topico": "Direito Constitucional"}
```

### **Busca de Documentos**
```bash
POST /api/v1/query
Content-Type: application/json

{
  "query": "princípios fundamentais da constituição",
  "filters": {
    "banca": "CESPE",
    "topico": "Direito Constitucional",
    "ano": 2024
  },
  "top_k": 10,
  "rerank": true,
  "similarity_threshold": 0.7
}
```

**Response:**
```json
{
  "query_id": "qry_789012",
  "results": [
    {
      "chunk_id": "chunk_001",
      "document_id": "doc_123456",
      "text": "Os princípios fundamentais da Constituição Federal...",
      "score": 0.95,
      "rerank_score": 0.98,
      "metadata": {
        "banca": "CESPE",
        "ano": 2024,
        "topico": "Direito Constitucional",
        "tipo": "edital",
        "orgao": "STF",
        "page": 15,
        "section": "Título I"
      }
    }
  ],
  "total_results": 10,
  "processing_time": 0.8,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Upload em Lote**
```bash
POST /api/v1/documents/upload/batch
Content-Type: application/json

{
  "documents": [
    {
      "file_path": "/path/to/doc1.pdf",
      "metadata": {"banca": "CESPE", "ano": 2024}
    },
    {
      "file_path": "/path/to/doc2.pdf",
      "metadata": {"banca": "FGV", "ano": 2024}
    }
  ],
  "batch_size": 10
}
```

### **Status do Índice**
```bash
GET /api/v1/index/status
```

**Response:**
```json
{
  "total_documents": 150,
  "total_chunks": 6750,
  "index_size": "2.3 GB",
  "last_updated": "2024-01-15T10:30:00Z",
  "health": "healthy"
}
```

### **Health Check**
```bash
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "parser": {"status": "healthy", "response_time": 0.1},
    "embedding": {"status": "healthy", "response_time": 0.5},
    "indexing": {"status": "healthy", "response_time": 0.2},
    "reranker": {"status": "healthy", "response_time": 0.3}
  },
  "uptime": 3600.5,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Métricas**
```bash
GET /api/v1/metrics
```

**Response:**
```json
{
  "uptime": 3600.5,
  "total_queries": 1250,
  "total_documents": 150,
  "total_chunks": 6750,
  "avg_query_time": 0.8,
  "avg_processing_time": 12.5,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 4. Variáveis de Ambiente e Logs

### **Variáveis de Ambiente**
```bash
# Pipeline Configuration
CHUNK_SIZE=512                    # Tamanho do chunk
CHUNK_OVERLAP=50                  # Overlap entre chunks
MAX_FILE_SIZE=10485760           # Tamanho máximo do arquivo (10MB)
SUPPORTED_FORMATS=pdf,txt,docx,png,jpg,jpeg

# Embedding Configuration
EMBEDDING_MODEL=BAAI/bge-m3      # Modelo de embedding
EMBEDDING_DIMENSION=1024         # Dimensão do embedding
EMBEDDING_BATCH_SIZE=32          # Tamanho do batch

# Reranker Configuration
RERANKER_MODEL=BAAI/bge-reranker-large  # Modelo de reranker
RERANKER_TOP_K=10                # Top K para reranking
SIMILARITY_THRESHOLD=0.7         # Threshold de similaridade

# FAISS Configuration
FAISS_INDEX_TYPE=IndexFlatIP     # Tipo do índice FAISS
FAISS_INDEX_PATH=./data/faiss_index  # Caminho do índice
FAISS_METADATA_PATH=./data/metadata  # Caminho dos metadados

# Parser Configuration
PYMUPDF_TIMEOUT=30               # Timeout PyMuPDF
TESSERACT_TIMEOUT=60             # Timeout Tesseract
OCR_LANGUAGE=por                 # Idioma do OCR

# API Configuration
API_HOST=0.0.0.0                 # Host da API
API_PORT=8001                    # Porta da API
API_RELOAD=true                  # Reload em desenvolvimento

# Logging
LOG_LEVEL=INFO                   # Nível de log

# Storage
DATA_DIR=./data                  # Diretório de dados
UPLOAD_DIR=./uploads             # Diretório de uploads
BACKUP_DIR=./backups             # Diretório de backups
```

### **Logs Estruturados**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "parser",
  "operation": "parse_document",
  "document_id": "doc_123456",
  "file_path": "/path/to/document.pdf",
  "processing_time": 12.5,
  "chunks_created": 45,
  "status": "success"
}
```

### **Métricas de Log**
- **Performance**: Tempo de processamento por operação
- **Volume**: Número de documentos/chunks processados
- **Erros**: Taxa de erro por serviço
- **Recursos**: Uso de CPU/memória/disco

## 5. Limitações e Próximos Passos

### **Limitações Conhecidas**

#### **Técnicas**
- **Tesseract OCR**: Requer instalação local, pode ser lento para imagens grandes
- **Modelos ML**: Consomem memória significativa (BGE-M3: ~2GB, BGE-Reranker: ~1GB)
- **FAISS**: Índice não é distribuído, limitado a uma máquina
- **Processamento**: PDFs muito grandes podem causar timeout
- **Formato**: DOCX parsing não implementado completamente

#### **Performance**
- **Upload**: Processamento sequencial, não paralelo
- **Busca**: Sem cache de queries frequentes
- **Índice**: Rebuild completo necessário para atualizações
- **Memória**: Modelos carregados em memória

#### **Segurança**
- **Upload**: Sem validação de conteúdo malicioso
- **Autenticação**: Sem sistema de autenticação implementado
- **Rate Limiting**: Sem limitação de requisições
- **CORS**: Configuração básica

### **Próximos Passos**

#### **Curto Prazo (Sprint 3)**
1. **Implementar serviços restantes**:
   - Chunking Service completo
   - Embedding Service completo
   - Indexing Service completo
   - Reranker Service completo
   - Query Service completo

2. **Melhorar robustez**:
   - Implementar retry logic
   - Adicionar circuit breakers
   - Melhorar tratamento de erros
   - Implementar fallbacks

3. **Otimizar performance**:
   - Implementar cache de embeddings
   - Adicionar processamento paralelo
   - Otimizar queries FAISS
   - Implementar lazy loading

#### **Médio Prazo (Sprint 4-5)**
1. **Escalabilidade**:
   - Implementar índices distribuídos
   - Adicionar load balancing
   - Implementar sharding
   - Adicionar replicação

2. **Segurança**:
   - Implementar autenticação JWT
   - Adicionar rate limiting
   - Implementar validação de uploads
   - Adicionar auditoria

3. **Monitoramento**:
   - Implementar métricas Prometheus
   - Adicionar alertas
   - Implementar dashboard
   - Adicionar tracing distribuído

#### **Longo Prazo (Sprint 6+)**
1. **Funcionalidades avançadas**:
   - Implementar busca híbrida (semântica + lexical)
   - Adicionar suporte a mais formatos
   - Implementar versionamento de documentos
   - Adicionar busca temporal

2. **Integração**:
   - Conectar com IA-0 (Ollama)
   - Integrar com frontend
   - Adicionar webhooks
   - Implementar API GraphQL

3. **Otimizações**:
   - Implementar quantização de modelos
   - Adicionar cache distribuído
   - Implementar compressão de índices
   - Otimizar para edge computing

### **Dependências Externas**
- **Tesseract OCR**: Requer instalação local
- **Modelos ML**: Download automático na primeira execução
- **Python 3.11+**: Versão mínima necessária
- **Espaço em disco**: ~5GB para modelos + índices

### **Compatibilidade**
- **Sistemas operacionais**: Linux, macOS, Windows
- **Python**: 3.11, 3.12
- **Docker**: Suporte completo
- **Cloud**: Google Cloud Run, AWS Lambda, Azure Functions

---

**Este documento fornece documentação completa para o pipeline IA-1, incluindo instalação, uso, APIs, configuração e roadmap de desenvolvimento.**
