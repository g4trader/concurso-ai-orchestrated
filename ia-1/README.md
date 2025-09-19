# IA-1 Pipeline de Ingestão

Pipeline completo para ingestão de documentos: parse→chunk→embed→index→rerank

## 🎯 Objetivo

Implementar um pipeline completo de ingestão de documentos para RAG (Retrieval-Augmented Generation), incluindo parsing, chunking, embedding, indexação e reranking.

## 🚀 Como rodar

### Pré-requisitos
- Python 3.11+
- Tesseract OCR instalado
- Modelos ML baixados (BGE-M3, BGE-Reranker-Large)

### Instalação
```bash
# Instalar dependências
make install

# Configurar diretórios
make setup-dirs

# Baixar modelos ML
make download-models

# Inicializar projeto completo
make init
```

### Execução
```bash
# Desenvolvimento
make run

# Produção
make run-prod

# Docker
make docker-build
make docker-run
```

## 📚 APIs Disponíveis

### Health Check
```bash
GET /api/v1/health
```

### Upload de Documento
```bash
POST /api/v1/documents/upload
{
  "file_path": "/path/to/document.pdf",
  "metadata": {
    "banca": "CESPE",
    "ano": 2024,
    "topico": "Direito Constitucional"
  }
}
```

### Busca de Documentos
```bash
POST /api/v1/query
{
  "query": "princípios fundamentais da constituição",
  "filters": {
    "banca": "CESPE",
    "topico": "Direito Constitucional"
  },
  "top_k": 10,
  "rerank": true
}
```

### Status do Índice
```bash
GET /api/v1/index/status
```

## 🔧 Variáveis de Ambiente

- `CHUNK_SIZE`: Tamanho do chunk (padrão: 512)
- `CHUNK_OVERLAP`: Overlap entre chunks (padrão: 50)
- `EMBEDDING_MODEL`: Modelo de embedding (padrão: BAAI/bge-m3)
- `RERANKER_MODEL`: Modelo de reranker (padrão: BAAI/bge-reranker-large)
- `FAISS_INDEX_PATH`: Caminho do índice FAISS
- `API_PORT`: Porta da API (padrão: 8001)

## 🧪 Testes

```bash
# Executar todos os testes
make test

# Executar com cobertura
pytest tests/ --cov=src --cov-report=html
```

## 📊 Observabilidade

- Logs estruturados em JSON
- Métricas de performance
- Health checks detalhados
- Monitoramento do índice

## 🚀 Deploy

### Google Cloud Run
```bash
gcloud run deploy ia-1-pipeline \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Vercel
```bash
vercel --prod
```

## ⚠️ Limitações Conhecidas

- Requer Tesseract OCR instalado
- Modelos ML consomem memória significativa
- Processamento de PDFs grandes pode ser lento
- Índice FAISS não é distribuído
