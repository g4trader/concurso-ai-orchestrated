# IA-2 Geração Condicionada

Sistema de geração de questões com validação automática por banca+edital

## 🎯 Objetivo

Implementar um sistema completo de geração de questões de múltipla escolha condicionado por banca organizadora e edital, com validação automática de qualidade, consistência e plágio.

## 🚀 Como rodar

### Pré-requisitos
- Python 3.11+
- Ollama instalado e rodando
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

### Geração de Questão
```bash
POST /api/v1/generate/question
{
  "contexts": [
    {
      "chunk_id": "chunk_001",
      "text": "Os princípios fundamentais da Constituição Federal...",
      "metadata": {
        "banca": "CESPE",
        "ano": 2024,
        "topico": "Direito Constitucional"
      }
    }
  ],
  "edital_summary": {
    "banca": "CESPE",
    "ano": 2024,
    "cargo": "Analista Judiciário",
    "topico": "Direito Constitucional",
    "dificuldade": "intermediaria",
    "estilo": "conceitual"
  },
  "topic": "Direito Constitucional"
}
```

### Geração em Lote
```bash
POST /api/v1/generate/batch
{
  "requests": [
    {
      "contexts": [...],
      "edital_summary": {...},
      "topic": "Direito Constitucional"
    }
  ],
  "batch_config": {
    "max_parallel": 5,
    "timeout_per_question": 30,
    "quality_threshold": 0.9
  }
}
```

### Validação de Questão
```bash
POST /api/v1/validate/question
{
  "question": "Qual é o princípio fundamental da Constituição Federal?",
  "alternatives": {
    "A": "Princípio da legalidade",
    "B": "Princípio da separação dos poderes",
    "C": "Princípio da igualdade"
  },
  "correct_answer": "B",
  "justification": "O princípio da separação dos poderes...",
  "source_chunks": ["chunk_001"]
}
```

### Métricas
```bash
GET /api/v1/metrics
```

## 🔧 Variáveis de Ambiente

- `LLM_MODEL`: Modelo LLM (padrão: llama-3.1-8b)
- `LLM_TEMPERATURE`: Temperatura do modelo (padrão: 0.7)
- `LLM_MAX_TOKENS`: Máximo de tokens (padrão: 2048)
- `VALIDATION_LEVEL`: Nível de validação (strict/medium/loose)
- `CONSISTENCY_THRESHOLD`: Threshold de consistência (padrão: 0.8)
- `PLAGIARISM_THRESHOLD`: Threshold de plágio (padrão: 0.3)
- `QUALITY_THRESHOLD`: Threshold de qualidade (padrão: 0.9)
- `API_PORT`: Porta da API (padrão: 8002)

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
- Monitoramento de qualidade

## 🚀 Deploy

### Google Cloud Run
```bash
gcloud run deploy ia-2-generation \
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

- Requer Ollama instalado e rodando
- Modelos ML consomem memória significativa
- Geração de questões pode ser lenta
- Validação rigorosa pode rejeitar questões válidas
