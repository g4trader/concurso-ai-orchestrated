# README_IA-2: Geração Condicionada por Banca+Edital com Validação Automática

## 1. Objetivo/Contexto

### **Objetivo**
Implementar um sistema completo de geração de questões de múltipla escolha condicionado por banca organizadora e edital, com validação automática de qualidade, consistência e plágio.

### **Contexto do Projeto**
- **Projeto**: Concurso-AI Orchestrated
- **Sprint**: 3 - Camada IA — Geração e Avaliação
- **História**: IA-2 - Geração condicionada por banca+edital
- **Usuário**: Estudante (via simulados)
- **Valor**: Questões coerentes, gabarito único, justificativa e fontes (chunks)

### **Problema Resolvido**
Gerar questões plausíveis no estilo da banca e do edital atual, com validação automática para garantir qualidade, consistência e originalidade.

### **Arquitetura do Sistema**
```
Contextos + Edital + Tópico → Prompt Engineering → LLM Generation → Validation → Self-Consistency → Anti-Plagiarism → Quality Assessment → Question JSON
```

## 2. Como Rodar (Conceitual)

### **Pré-requisitos**
- Python 3.11+
- Ollama instalado e rodando
- Modelos ML baixados (BGE-M3, BGE-Reranker-Large)
- Redis para cache (opcional)

### **Instalação**
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar diretórios
mkdir -p data/ cache/ prompts/system_prompts/ prompts/task_prompts/ prompts/templates/

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
uvicorn src.main:app --host 0.0.0.0 --port 8002 --reload

# Produção
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8002

# Docker
docker build -t ia-2-generation .
docker run -p 8002:8002 ia-2-generation
```

### **Verificação**
```bash
# Health check
curl http://localhost:8002/api/v1/health

# Métricas
curl http://localhost:8002/api/v1/metrics

# Gerar questão de exemplo
curl -X POST http://localhost:8002/api/v1/generate/question \
  -H "Content-Type: application/json" \
  -d '{
    "contexts": [{"chunk_id": "chunk_001", "text": "Os princípios fundamentais da Constituição Federal...", "metadata": {"banca": "CESPE", "ano": 2024}}],
    "edital_summary": {"banca": "CESPE", "ano": 2024, "cargo": "Analista Judiciário", "topico": "Direito Constitucional"},
    "topic": "Direito Constitucional"
  }'
```

## 3. APIs/Contratos com Exemplos

### **Geração de Questão Única**
```bash
POST /api/v1/generate/question
Content-Type: application/json

{
  "contexts": [
    {
      "chunk_id": "chunk_001",
      "text": "Os princípios fundamentais da Constituição Federal...",
      "metadata": {
        "banca": "CESPE",
        "ano": 2024,
        "topico": "Direito Constitucional",
        "page": 15
      }
    }
  ],
  "edital_summary": {
    "banca": "CESPE",
    "ano": 2024,
    "cargo": "Analista Judiciário",
    "orgao": "STF",
    "topico": "Direito Constitucional",
    "dificuldade": "intermediaria",
    "estilo": "conceitual"
  },
  "topic": "Direito Constitucional",
  "generation_config": {
    "num_questions": 1,
    "difficulty": "intermediaria",
    "style": "conceitual",
    "validation_level": "strict"
  }
}
```

**Response:**
```json
{
  "question_id": "q_123456",
  "question": "Qual é o princípio fundamental da Constituição Federal que estabelece a separação dos poderes?",
  "alternatives": {
    "A": "Princípio da legalidade",
    "B": "Princípio da separação dos poderes",
    "C": "Princípio da igualdade",
    "D": "Princípio da dignidade da pessoa humana",
    "E": "Princípio da publicidade"
  },
  "correct_answer": "B",
  "justification": "O princípio da separação dos poderes está expressamente previsto no art. 2º da CF/88, estabelecendo a independência e harmonia entre os Poderes Executivo, Legislativo e Judiciário.",
  "source_chunks": ["chunk_001", "chunk_002"],
  "metadata": {
    "banca": "CESPE",
    "ano": 2024,
    "topico": "Direito Constitucional",
    "dificuldade": "intermediaria",
    "estilo": "conceitual",
    "plausibilidade_score": 0.95,
    "consistency_score": 0.92,
    "plagiarism_score": 0.05
  },
  "generation_time": 2.5,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Geração em Lote**
```bash
POST /api/v1/generate/batch
Content-Type: application/json

{
  "batch_id": "batch_789012",
  "requests": [
    {
      "contexts": [...],
      "edital_summary": {...},
      "topic": "Direito Constitucional"
    },
    {
      "contexts": [...],
      "edital_summary": {...},
      "topic": "Direito Administrativo"
    }
  ],
  "batch_config": {
    "max_parallel": 5,
    "timeout_per_question": 30,
    "quality_threshold": 0.9,
    "validation_level": "strict"
  }
}
```

**Response:**
```json
{
  "batch_id": "batch_789012",
  "status": "completed",
  "total_requests": 10,
  "successful": 8,
  "failed": 2,
  "questions": [
    {
      "question_id": "q_123456",
      "question": "...",
      "alternatives": {...},
      "correct_answer": "B",
      "justification": "...",
      "source_chunks": [...],
      "metadata": {...}
    }
  ],
  "failed_requests": [
    {
      "index": 2,
      "error": "Validation failed: low plausibility score",
      "details": {...}
    }
  ],
  "processing_time": 45.2,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Validação de Questão**
```bash
POST /api/v1/validate/question
Content-Type: application/json

{
  "question": "Qual é o princípio fundamental da Constituição Federal?",
  "alternatives": {
    "A": "Princípio da legalidade",
    "B": "Princípio da separação dos poderes",
    "C": "Princípio da igualdade",
    "D": "Princípio da dignidade da pessoa humana",
    "E": "Princípio da publicidade"
  },
  "correct_answer": "B",
  "justification": "O princípio da separação dos poderes está expressamente previsto no art. 2º da CF/88...",
  "source_chunks": ["chunk_001"],
  "validation_config": {
    "check_consistency": true,
    "check_plagiarism": true,
    "check_quality": true,
    "consistency_threshold": 0.8,
    "plagiarism_threshold": 0.3,
    "quality_threshold": 0.9
  }
}
```

**Response:**
```json
{
  "validation_id": "val_345678",
  "is_valid": true,
  "scores": {
    "plausibility": 0.95,
    "consistency": 0.92,
    "plagiarism": 0.05,
    "quality": 0.94
  },
  "checks": {
    "uniqueness": {
      "passed": true,
      "score": 1.0,
      "details": "Gabarito único identificado"
    },
    "consistency": {
      "passed": true,
      "score": 0.92,
      "details": "Justificativa coerente com resposta"
    },
    "plagiarism": {
      "passed": true,
      "score": 0.05,
      "details": "Baixo risco de plágio"
    },
    "quality": {
      "passed": true,
      "score": 0.94,
      "details": "Questão bem formulada"
    }
  },
  "recommendations": [
    "Considerar adicionar mais contexto na justificativa"
  ],
  "validation_time": 1.2,
  "timestamp": "2024-01-15T10:30:00Z"
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
    "prompt_engineering": {
      "status": "healthy",
      "response_time": 0.1,
      "prompts_loaded": 4
    },
    "llm_generation": {
      "status": "healthy",
      "response_time": 2.5,
      "model_loaded": "llama-3.1-8b"
    },
    "validation": {
      "status": "healthy",
      "response_time": 1.2,
      "validators_active": 3
    },
    "self_consistency": {
      "status": "healthy",
      "response_time": 0.8,
      "checks_performed": 150
    },
    "anti_plagiarism": {
      "status": "healthy",
      "response_time": 0.5,
      "checks_performed": 150
    },
    "quality_assessment": {
      "status": "healthy",
      "response_time": 0.3,
      "assessments_performed": 150
    }
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
  "total_questions_generated": 1250,
  "total_validations": 1500,
  "avg_generation_time": 2.5,
  "avg_validation_time": 1.2,
  "success_rate": 0.95,
  "quality_scores": {
    "plausibility": 0.92,
    "consistency": 0.89,
    "plagiarism": 0.08,
    "quality": 0.91
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 4. Variáveis de Ambiente e Logs

### **Variáveis de Ambiente**
```bash
# LLM Configuration
LLM_MODEL=llama-3.1-8b                    # Modelo LLM
LLM_TEMPERATURE=0.7                       # Temperatura do modelo
LLM_MAX_TOKENS=2048                       # Máximo de tokens
LLM_TIMEOUT=30                            # Timeout de geração

# Generation Configuration
MAX_QUESTIONS_PER_BATCH=10                # Máximo de questões por lote
MAX_PARALLEL_GENERATIONS=5                # Máximo de gerações paralelas
GENERATION_TIMEOUT=30                     # Timeout por questão

# Validation Configuration
VALIDATION_LEVEL=strict                   # Nível de validação (strict/medium/loose)
CONSISTENCY_THRESHOLD=0.8                 # Threshold de consistência
PLAGIARISM_THRESHOLD=0.3                  # Threshold de plágio
QUALITY_THRESHOLD=0.9                     # Threshold de qualidade

# Self-Consistency Configuration
CONSISTENCY_CHECKS=2                      # Número de verificações de consistência
CONSISTENCY_TIMEOUT=10                    # Timeout de consistência

# Anti-Plagiarism Configuration
PLAGIARISM_CHECK_ENABLED=true             # Habilitar verificação de plágio
PLAGIARISM_TIMEOUT=5                      # Timeout de verificação de plágio

# Quality Assessment Configuration
QUALITY_METRICS=plausibility,consistency,clarity,difficulty  # Métricas de qualidade
QUALITY_WEIGHTS={"plausibility": 0.4, "consistency": 0.3, "clarity": 0.2, "difficulty": 0.1}

# Prompt Configuration
PROMPT_CACHE_ENABLED=true                 # Habilitar cache de prompts
PROMPT_CACHE_TTL=3600                     # TTL do cache de prompts

# API Configuration
API_HOST=0.0.0.0                         # Host da API
API_PORT=8002                            # Porta da API
API_RELOAD=true                          # Reload em desenvolvimento

# Logging
LOG_LEVEL=INFO                           # Nível de log

# Storage
DATA_DIR=./data                          # Diretório de dados
PROMPTS_DIR=./prompts                    # Diretório de prompts
CACHE_DIR=./cache                        # Diretório de cache

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434       # Host do Ollama
OLLAMA_TIMEOUT=60                        # Timeout do Ollama
```

### **Logs Estruturados**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "llm_generation",
  "operation": "generate_question",
  "question_id": "q_123456",
  "banca": "CESPE",
  "topic": "Direito Constitucional",
  "generation_time": 2.5,
  "validation_scores": {
    "plausibility": 0.95,
    "consistency": 0.92,
    "plagiarism": 0.05
  },
  "status": "success"
}
```

### **Métricas de Log**
- **Performance**: Tempo de geração e validação por operação
- **Volume**: Número de questões geradas e validadas
- **Qualidade**: Scores médios de qualidade, consistência e plágio
- **Erros**: Taxa de erro por serviço e tipo de erro

## 5. Limitações e Próximos Passos

### **Limitações Conhecidas**

#### **Técnicas**
- **Ollama**: Requer instalação local e modelo carregado
- **Modelos ML**: Consomem memória significativa (BGE-M3: ~2GB, BGE-Reranker: ~1GB)
- **Geração**: Pode ser lenta para questões complexas
- **Validação**: Validação rigorosa pode rejeitar questões válidas

#### **Performance**
- **Geração**: Processamento sequencial por questão
- **Validação**: Múltiplas verificações podem ser lentas
- **Cache**: Cache de prompts pode não ser eficiente
- **Memória**: Modelos carregados em memória

#### **Segurança**
- **Input validation**: Sem validação rigorosa de contextos
- **Autenticação**: Sem sistema de autenticação implementado
- **Rate limiting**: Sem limitação de requisições
- **CORS**: Configuração básica

### **Próximos Passos**

#### **Curto Prazo (Sprint 4)**
1. **Implementar serviços restantes**:
   - Prompt Engineering Service completo
   - LLM Generation Service completo
   - Validation Service completo
   - Self-Consistency Service completo
   - Anti-Plagiarism Service completo
   - Quality Assessment Service completo
   - Batch Processor Service completo

2. **Melhorar robustez**:
   - Implementar retry logic
   - Adicionar circuit breakers
   - Melhorar tratamento de erros
   - Implementar fallbacks

3. **Otimizar performance**:
   - Implementar cache de prompts
   - Adicionar processamento paralelo
   - Otimizar validações
   - Implementar lazy loading

#### **Médio Prazo (Sprint 5-6)**
1. **Escalabilidade**:
   - Implementar load balancing
   - Adicionar sharding
   - Implementar replicação
   - Adicionar auto-scaling

2. **Segurança**:
   - Implementar autenticação JWT
   - Adicionar rate limiting
   - Implementar validação de input
   - Adicionar auditoria

3. **Monitoramento**:
   - Implementar métricas Prometheus
   - Adicionar alertas
   - Implementar dashboard
   - Adicionar tracing distribuído

#### **Longo Prazo (Sprint 7+)**
1. **Funcionalidades avançadas**:
   - Implementar geração de questões por dificuldade
   - Adicionar suporte a mais bancas
   - Implementar versionamento de questões
   - Adicionar geração de questões por estilo

2. **Integração**:
   - Conectar com IA-1 (Pipeline de Ingestão)
   - Integrar com frontend
   - Adicionar webhooks
   - Implementar API GraphQL

3. **Otimizações**:
   - Implementar quantização de modelos
   - Adicionar cache distribuído
   - Implementar compressão de dados
   - Otimizar para edge computing

### **Dependências Externas**
- **Ollama**: Requer instalação local e modelo carregado
- **Modelos ML**: Download automático na primeira execução
- **Python 3.11+**: Versão mínima necessária
- **Redis**: Opcional para cache

### **Compatibilidade**
- **Sistemas operacionais**: Linux, macOS, Windows
- **Python**: 3.11, 3.12
- **Docker**: Suporte completo
- **Cloud**: Google Cloud Run, AWS Lambda, Azure Functions

---

**Este documento fornece documentação completa para o sistema de geração condicionada IA-2, incluindo instalação, uso, APIs, configuração e roadmap de desenvolvimento.**
