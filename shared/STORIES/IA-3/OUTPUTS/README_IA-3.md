# README_IA-3: Avaliação Offline — Topic-Hit Rate, Style Match, Answerability

## 1. Objetivo/Contexto

### **Objetivo**
Implementar um sistema completo de avaliação offline para medir qualidade de simulados gerados usando métricas objetivas de topic-hit rate, style match e answerability.

### **Contexto do Projeto**
- **Projeto**: Concurso-AI Orchestrated
- **Sprint**: 3 - Camada IA — Geração e Avaliação
- **História**: IA-3 - Avaliação offline de simulados gerados
- **Usuário**: Time de produto/engenharia
- **Valor**: Métricas objetivas para orientar iteração e PMF

### **Problema Resolvido**
Medir qualidade em dados de validação (provas antigas não vistas) para fornecer métricas objetivas que orientem a iteração do sistema e o Product-Market Fit.

### **Arquitetura do Sistema**
```
Simulados Gerados → Dataset Held-Out → Topic Hit Rate → Style Match → Answerability → Metrics Aggregator → Gap Analysis → Report Generator → REPORT.md
```

### **Métricas Principais**
- **Topic Hit Rate**: Percentual de questões que correspondem aos tópicos do dataset held-out
- **Style Match**: Consistência de estilo entre simulados gerados e provas reais
- **Answerability**: Capacidade das questões de serem respondidas corretamente

## 2. Como Rodar (Conceitual)

### **Pré-requisitos**
- Python 3.11+
- Dataset held-out (provas antigas)
- Simulados gerados para avaliação
- Modelos ML para classificação e análise

### **Instalação**
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar diretórios
mkdir -p data/held_out/ data/generated/ data/benchmarks/ reports/

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
uvicorn src.main:app --host 0.0.0.0 --port 8003 --reload

# Produção
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8003

# Docker
docker build -t ia-3-evaluation .
docker run -p 8003:8003 ia-3-evaluation
```

### **Verificação**
```bash
# Health check
curl http://localhost:8003/api/v1/health

# Métricas
curl http://localhost:8003/api/v1/metrics

# Avaliar simulados de exemplo
curl -X POST http://localhost:8003/api/v1/evaluate/simulados \
  -H "Content-Type: application/json" \
  -d '{
    "evaluation_id": "eval_123456",
    "generated_simulados": [
      {
        "simulado_id": "sim_001",
        "banca": "CESPE",
        "ano": 2023,
        "topico": "Direito Constitucional",
        "questoes": [...]
      }
    ],
    "held_out_dataset": {
      "banca": "CESPE",
      "ano": 2023,
      "topico": "Direito Constitucional",
      "questoes_reais": [...]
    },
    "evaluation_config": {
      "metrics": ["topic_hit_rate", "style_match", "answerability"],
      "thresholds": {
        "topic_hit_rate": 0.8,
        "style_match": 0.7,
        "answerability": 0.9
      }
    }
  }'
```

## 3. APIs/Contratos com Exemplos

### **Avaliação de Simulados**
```bash
POST /api/v1/evaluate/simulados
Content-Type: application/json

{
  "evaluation_id": "eval_123456",
  "generated_simulados": [
    {
      "simulado_id": "sim_001",
      "banca": "CESPE",
      "ano": 2023,
      "topico": "Direito Constitucional",
      "questoes": [
        {
          "questao_id": "q_001",
          "pergunta": "Qual é o princípio fundamental da Constituição Federal?",
          "alternativas": {
            "A": "Princípio da legalidade",
            "B": "Princípio da separação dos poderes",
            "C": "Princípio da igualdade",
            "D": "Princípio da dignidade da pessoa humana",
            "E": "Princípio da publicidade"
          },
          "resposta_correta": "B",
          "justificativa": "O princípio da separação dos poderes está expressamente previsto no art. 2º da CF/88..."
        }
      ]
    }
  ],
  "held_out_dataset": {
    "banca": "CESPE",
    "ano": 2023,
    "topico": "Direito Constitucional",
    "questoes_reais": [
      {
        "questao_id": "real_001",
        "pergunta": "Sobre os princípios fundamentais da Constituição Federal...",
        "alternativas": {
          "A": "Apenas I e II",
          "B": "Apenas II e III",
          "C": "Apenas I e III",
          "D": "I, II e III",
          "E": "Nenhuma das alternativas"
        },
        "resposta_correta": "D"
      }
    ]
  },
  "evaluation_config": {
    "metrics": ["topic_hit_rate", "style_match", "answerability"],
    "thresholds": {
      "topic_hit_rate": 0.8,
      "style_match": 0.7,
      "answerability": 0.9
    }
  }
}
```

**Response:**
```json
{
  "evaluation_id": "eval_123456",
  "status": "completed",
  "metrics": {
    "topic_hit_rate": {
      "score": 0.85,
      "details": {
        "total_questions": 100,
        "topic_matches": 85,
        "topic_miss": 15,
        "breakdown": {
          "Direito Constitucional": 0.90,
          "Direito Administrativo": 0.80,
          "Direito Penal": 0.85
        }
      }
    },
    "style_match": {
      "score": 0.75,
      "details": {
        "total_questions": 100,
        "style_matches": 75,
        "style_miss": 25,
        "breakdown": {
          "linguagem_formal": 0.80,
          "estrutura_questao": 0.70,
          "nivel_dificuldade": 0.75
        }
      }
    },
    "answerability": {
      "score": 0.92,
      "details": {
        "total_questions": 100,
        "answerable": 92,
        "unanswerable": 8,
        "breakdown": {
          "clareza_pergunta": 0.95,
          "alternativas_validas": 0.90,
          "justificativa_coerente": 0.90
        }
      }
    }
  },
  "gap_analysis": {
    "critical_gaps": [
      {
        "gap_type": "topic_coverage",
        "description": "Baixa cobertura em Direito Tributário",
        "impact": "high",
        "recommendation": "Aumentar contextos de Direito Tributário"
      }
    ],
    "moderate_gaps": [
      {
        "gap_type": "style_consistency",
        "description": "Inconsistência no nível de formalidade",
        "impact": "medium",
        "recommendation": "Refinar prompts de estilo"
      }
    ]
  },
  "recommendations": [
    "Aumentar diversidade de tópicos no dataset de treinamento",
    "Melhorar consistência de estilo entre questões",
    "Implementar validação de answerability mais rigorosa"
  ],
  "processing_time": 45.2,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Benchmark de Avaliação**
```bash
POST /api/v1/benchmark/evaluation
Content-Type: application/json

{
  "benchmark_id": "bench_789012",
  "evaluation_requests": [
    {
      "evaluation_id": "eval_001",
      "generated_simulados": [...],
      "held_out_dataset": {...}
    },
    {
      "evaluation_id": "eval_002",
      "generated_simulados": [...],
      "held_out_dataset": {...}
    }
  ],
  "benchmark_config": {
    "metrics": ["topic_hit_rate", "style_match", "answerability"],
    "aggregation_method": "weighted_average",
    "weights": {
      "topic_hit_rate": 0.4,
      "style_match": 0.3,
      "answerability": 0.3
    }
  }
}
```

**Response:**
```json
{
  "benchmark_id": "bench_789012",
  "status": "completed",
  "overall_score": 0.84,
  "evaluations": [
    {
      "evaluation_id": "eval_001",
      "metrics": {...},
      "score": 0.85
    },
    {
      "evaluation_id": "eval_002",
      "metrics": {...},
      "score": 0.83
    }
  ],
  "aggregated_metrics": {
    "topic_hit_rate": 0.85,
    "style_match": 0.75,
    "answerability": 0.92
  },
  "performance_trends": {
    "improvement_rate": 0.05,
    "consistency_score": 0.88,
    "reliability_score": 0.90
  },
  "processing_time": 120.5,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Geração de Relatório**
```bash
POST /api/v1/report/generate
Content-Type: application/json

{
  "report_id": "report_345678",
  "evaluation_results": [
    {
      "evaluation_id": "eval_001",
      "status": "completed",
      "metrics": {...},
      "gap_analysis": {...},
      "recommendations": [...]
    }
  ],
  "benchmark_results": [
    {
      "benchmark_id": "bench_001",
      "status": "completed",
      "overall_score": 0.84,
      "aggregated_metrics": {...}
    }
  ],
  "report_config": {
    "format": "markdown",
    "include_charts": true,
    "include_recommendations": true,
    "include_gap_analysis": true
  }
}
```

**Response:**
```json
{
  "report_id": "report_345678",
  "status": "generated",
  "report_path": "/reports/evaluation_report_2024-01-15.md",
  "sections": [
    "executive_summary",
    "metrics_analysis",
    "gap_analysis",
    "recommendations",
    "appendix"
  ],
  "generation_time": 15.3,
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
    "topic_hit_rate": {
      "status": "healthy",
      "response_time": 2.1,
      "evaluations_performed": 150
    },
    "style_match": {
      "status": "healthy",
      "response_time": 1.8,
      "evaluations_performed": 150
    },
    "answerability": {
      "status": "healthy",
      "response_time": 1.5,
      "evaluations_performed": 150
    },
    "metrics_aggregator": {
      "status": "healthy",
      "response_time": 0.5,
      "aggregations_performed": 50
    },
    "gap_analysis": {
      "status": "healthy",
      "response_time": 3.2,
      "analyses_performed": 50
    },
    "report_generator": {
      "status": "healthy",
      "response_time": 15.3,
      "reports_generated": 10
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
  "total_evaluations": 150,
  "total_benchmarks": 25,
  "avg_evaluation_time": 45.2,
  "avg_benchmark_time": 120.5,
  "success_rate": 0.95,
  "metrics_scores": {
    "topic_hit_rate": 0.85,
    "style_match": 0.75,
    "answerability": 0.92
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 4. Variáveis de Ambiente e Logs

### **Variáveis de Ambiente**
```bash
# Evaluation Configuration
EVALUATION_METRICS=topic_hit_rate,style_match,answerability  # Métricas de avaliação
EVALUATION_THRESHOLDS={"topic_hit_rate": 0.8, "style_match": 0.7, "answerability": 0.9}  # Thresholds

# Topic Hit Rate Configuration
TOPIC_CLASSIFICATION_MODEL=BAAI/bge-m3  # Modelo para classificação de tópicos
TOPIC_CLASSIFICATION_TIMEOUT=10  # Timeout de classificação
TOPIC_HIT_RATE_THRESHOLD=0.8  # Threshold de hit rate

# Style Match Configuration
STYLE_ANALYSIS_MODEL=BAAI/bge-reranker-large  # Modelo para análise de estilo
STYLE_ANALYSIS_TIMEOUT=15  # Timeout de análise
STYLE_MATCH_THRESHOLD=0.7  # Threshold de style match

# Answerability Configuration
ANSWERABILITY_CRITERIA=clareza_pergunta,alternativas_validas,justificativa_coerente  # Critérios
ANSWERABILITY_TIMEOUT=10  # Timeout de verificação
ANSWERABILITY_THRESHOLD=0.9  # Threshold de answerability

# Metrics Aggregator Configuration
AGGREGATION_METHOD=weighted_average  # Método de agregação
AGGREGATION_WEIGHTS={"topic_hit_rate": 0.4, "style_match": 0.3, "answerability": 0.3}  # Pesos

# Gap Analysis Configuration
GAP_ANALYSIS_TIMEOUT=20  # Timeout de análise
CRITICAL_GAP_THRESHOLD=0.7  # Threshold para gaps críticos
MODERATE_GAP_THRESHOLD=0.8  # Threshold para gaps moderados

# Report Generator Configuration
REPORT_FORMAT=markdown  # Formato do relatório
REPORT_INCLUDE_CHARTS=true  # Incluir gráficos
REPORT_INCLUDE_RECOMMENDATIONS=true  # Incluir recomendações
REPORT_GENERATION_TIMEOUT=30  # Timeout de geração

# Benchmark Configuration
BENCHMARK_TIMEOUT=60  # Timeout de benchmark
BENCHMARK_AGGREGATION_METHOD=weighted_average  # Método de agregação
BENCHMARK_WEIGHTS={"topic_hit_rate": 0.4, "style_match": 0.3, "answerability": 0.3}  # Pesos

# API Configuration
API_HOST=0.0.0.0  # Host da API
API_PORT=8003  # Porta da API
API_RELOAD=true  # Reload em desenvolvimento

# Logging
LOG_LEVEL=INFO  # Nível de log

# Storage
DATA_DIR=./data  # Diretório de dados
REPORTS_DIR=./reports  # Diretório de relatórios
CACHE_DIR=./cache  # Diretório de cache

# ML Models Configuration
ML_MODELS_DIR=./models  # Diretório de modelos ML
MODEL_DOWNLOAD_TIMEOUT=300  # Timeout de download de modelos
MODEL_LOAD_TIMEOUT=60  # Timeout de carregamento de modelos
```

### **Logs Estruturados**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "topic_hit_rate",
  "operation": "calculate_hit_rate",
  "evaluation_id": "eval_123456",
  "banca": "CESPE",
  "ano": 2023,
  "total_questions": 100,
  "topic_matches": 85,
  "hit_rate": 0.85,
  "processing_time": 2.1,
  "status": "success"
}
```

### **Métricas de Log**
- **Performance**: Tempo de avaliação e benchmark por operação
- **Volume**: Número de avaliações e benchmarks executados
- **Qualidade**: Scores médios de topic hit rate, style match e answerability
- **Erros**: Taxa de erro por serviço e tipo de erro

## 5. Limitações e Próximos Passos

### **Limitações Conhecidas**

#### **Técnicas**
- **Dataset held-out**: Requer provas antigas não vistas pelo sistema
- **Modelos ML**: Consomem memória significativa (BGE-M3: ~2GB, BGE-Reranker: ~1GB)
- **Avaliação**: Pode ser lenta para grandes volumes de simulados
- **Classificação**: Classificação automática pode ter imprecisões

#### **Performance**
- **Avaliação**: Processamento sequencial por simulado
- **Análise**: Múltiplas análises podem ser lentas
- **Cache**: Cache de resultados pode não ser eficiente
- **Memória**: Modelos carregados em memória

#### **Segurança**
- **Input validation**: Sem validação rigorosa de simulados
- **Autenticação**: Sem sistema de autenticação implementado
- **Rate limiting**: Sem limitação de requisições
- **CORS**: Configuração básica

### **Próximos Passos**

#### **Curto Prazo (Sprint 4)**
1. **Implementar serviços restantes**:
   - Topic Hit Rate Service completo
   - Style Match Service completo
   - Answerability Service completo
   - Metrics Aggregator Service completo
   - Gap Analysis Service completo
   - Report Generator Service completo
   - Benchmark Service completo

2. **Melhorar robustez**:
   - Implementar retry logic
   - Adicionar circuit breakers
   - Melhorar tratamento de erros
   - Implementar fallbacks

3. **Otimizar performance**:
   - Implementar cache de resultados
   - Adicionar processamento paralelo
   - Otimizar análises
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
   - Implementar avaliação de questões por dificuldade
   - Adicionar suporte a mais bancas
   - Implementar versionamento de avaliações
   - Adicionar avaliação de questões por estilo

2. **Integração**:
   - Conectar com IA-1 (Pipeline de Ingestão)
   - Conectar com IA-2 (Geração Condicionada)
   - Integrar com frontend
   - Adicionar webhooks

3. **Otimizações**:
   - Implementar quantização de modelos
   - Adicionar cache distribuído
   - Implementar compressão de dados
   - Otimizar para edge computing

### **Dependências Externas**
- **Dataset held-out**: Provas antigas não vistas pelo sistema
- **Modelos ML**: Download automático na primeira execução
- **Python 3.11+**: Versão mínima necessária
- **Redis**: Opcional para cache

### **Compatibilidade**
- **Sistemas operacionais**: Linux, macOS, Windows
- **Python**: 3.11, 3.12
- **Docker**: Suporte completo
- **Cloud**: Google Cloud Run, AWS Lambda, Azure Functions

---

**Este documento fornece documentação completa para o sistema de avaliação offline IA-3, incluindo instalação, uso, APIs, configuração e roadmap de desenvolvimento.**
