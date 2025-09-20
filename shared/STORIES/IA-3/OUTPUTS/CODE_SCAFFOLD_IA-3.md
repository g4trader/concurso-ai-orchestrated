# CODE_SCAFFOLD_IA-3: Backend Scaffolding para Avaliação Offline

## /backend/ia-3/ - Estrutura do Projeto

### README.md
```markdown
# IA-3 Backend: Avaliação Offline — Topic-Hit Rate, Style Match, Answerability

## Visão Geral
Sistema de avaliação offline para medir qualidade de simulados gerados usando métricas objetivas.

## Arquitetura
- **FastAPI** para API REST
- **Pydantic** para validação de dados
- **Async/await** para operações assíncronas
- **Structured logging** para observabilidade

## Endpoints Principais
- `POST /api/v1/evaluate/simulados` - Avaliar simulados gerados
- `POST /api/v1/benchmark/evaluation` - Benchmark de avaliação
- `POST /api/v1/report/generate` - Gerar relatório de avaliação
- `GET /api/v1/health` - Health check
- `GET /api/v1/metrics` - Métricas do sistema

## Serviços
- **Topic Hit Rate Service** - Calcular hit rate de tópicos
- **Style Match Service** - Analisar consistência de estilo
- **Answerability Service** - Verificar capacidade de resposta
- **Metrics Aggregator Service** - Agregar métricas
- **Gap Analysis Service** - Analisar gaps de qualidade
- **Report Generator Service** - Gerar relatórios
- **Benchmark Service** - Executar benchmarks

## Configuração
- Porta: 8003
- Logs: JSON estruturado
- Métricas: Prometheus
- Cache: Redis (opcional)
```

### DTOs em Markdown

#### EvaluationRequest
```markdown
# EvaluationRequest

## Campos
- `evaluation_id: str` - ID único da avaliação
- `generated_simulados: List[Simulado]` - Simulados gerados para avaliação
- `held_out_dataset: HeldOutDataset` - Dataset de validação
- `evaluation_config: EvaluationConfig` - Configurações de avaliação

## Exemplo
```json
{
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
}
```

#### EvaluationResponse
```markdown
# EvaluationResponse

## Campos
- `evaluation_id: str` - ID da avaliação
- `status: str` - Status da avaliação (completed/failed)
- `metrics: Dict[str, MetricResult]` - Resultados das métricas
- `gap_analysis: GapAnalysis` - Análise de gaps
- `recommendations: List[str]` - Recomendações
- `processing_time: float` - Tempo de processamento
- `timestamp: str` - Timestamp da avaliação

## Exemplo
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
        "topic_miss": 15
      }
    }
  },
  "gap_analysis": {
    "critical_gaps": [...],
    "moderate_gaps": [...]
  },
  "recommendations": [...],
  "processing_time": 45.2,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### BenchmarkRequest
```markdown
# BenchmarkRequest

## Campos
- `benchmark_id: str` - ID único do benchmark
- `evaluation_requests: List[EvaluationRequest]` - Requisições de avaliação
- `benchmark_config: BenchmarkConfig` - Configurações do benchmark

## Exemplo
```json
{
  "benchmark_id": "bench_789012",
  "evaluation_requests": [...],
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

#### ReportRequest
```markdown
# ReportRequest

## Campos
- `report_id: str` - ID único do relatório
- `evaluation_results: List[EvaluationResponse]` - Resultados de avaliação
- `benchmark_results: List[BenchmarkResponse]` - Resultados de benchmark
- `report_config: ReportConfig` - Configurações do relatório

## Exemplo
```json
{
  "report_id": "report_345678",
  "evaluation_results": [...],
  "benchmark_results": [...],
  "report_config": {
    "format": "markdown",
    "include_charts": true,
    "include_recommendations": true,
    "include_gap_analysis": true
  }
}
```

### Exemplos de Payloads

#### Avaliação de Simulados
```json
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

#### Benchmark de Avaliação
```json
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

#### Geração de Relatório
```json
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

## Requirements/PyProject

### requirements.txt
```txt
# Core Framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
pydantic-settings>=2.1.0

# HTTP Client
httpx>=0.25.0
aiohttp>=3.9.0

# Data Processing
pandas>=2.1.0
numpy>=1.24.0
scikit-learn>=1.3.0

# ML Libraries
sentence-transformers>=2.2.0
transformers>=4.35.0
torch>=2.1.0

# Text Processing
nltk>=3.8.0
spacy>=3.7.0
textstat>=0.7.0

# Database
sqlalchemy>=2.0.0
alembic>=1.13.0
asyncpg>=0.29.0

# Cache
redis>=5.0.0
aioredis>=2.0.0

# Monitoring
prometheus-client>=0.19.0
structlog>=23.2.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
httpx>=0.25.0

# Development
black>=23.11.0
isort>=5.12.0
flake8>=6.1.0
mypy>=1.7.0

# Documentation
mkdocs>=1.5.0
mkdocs-material>=9.4.0
```

### pyproject.toml
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ia-3-evaluation"
version = "0.1.0"
description = "Sistema de avaliação offline para simulados gerados"
authors = [
    {name = "Concurso-AI Team", email = "team@concurso-ai.com"}
]
readme = "README.md"
requires-python = ">=3.11"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "httpx>=0.25.0",
    "pandas>=2.1.0",
    "numpy>=1.24.0",
    "scikit-learn>=1.3.0",
    "sentence-transformers>=2.2.0",
    "transformers>=4.35.0",
    "torch>=2.1.0",
    "nltk>=3.8.0",
    "spacy>=3.7.0",
    "textstat>=0.7.0",
    "sqlalchemy>=2.0.0",
    "redis>=5.0.0",
    "prometheus-client>=0.19.0",
    "structlog>=23.2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "black>=23.11.0",
    "isort>=5.12.0",
    "flake8>=6.1.0",
    "mypy>=1.7.0",
]

[project.urls]
Homepage = "https://github.com/concurso-ai/ia-3-evaluation"
Repository = "https://github.com/concurso-ai/ia-3-evaluation.git"
Documentation = "https://docs.concurso-ai.com/ia-3"

[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["src"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
```

## Makefile

### Makefile
```makefile
# IA-3 Evaluation System Makefile

.PHONY: help build test run clean install dev-install lint format type-check

# Default target
help:
	@echo "IA-3 Evaluation System - Available targets:"
	@echo "  build       - Build the application"
	@echo "  test        - Run tests"
	@echo "  run         - Run the application"
	@echo "  clean       - Clean build artifacts"
	@echo "  install     - Install dependencies"
	@echo "  dev-install - Install development dependencies"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"
	@echo "  type-check  - Run type checking"

# Build targets
build:
	@echo "Building IA-3 Evaluation System..."
	python -m build
	@echo "Build completed!"

# Test targets
test:
	@echo "Running tests..."
	pytest tests/ -v --cov=src --cov-report=term-missing
	@echo "Tests completed!"

test-unit:
	@echo "Running unit tests..."
	pytest tests/ -v -m "unit" --cov=src --cov-report=term-missing
	@echo "Unit tests completed!"

test-integration:
	@echo "Running integration tests..."
	pytest tests/ -v -m "integration" --cov=src --cov-report=term-missing
	@echo "Integration tests completed!"

# Run targets
run:
	@echo "Starting IA-3 Evaluation System..."
	uvicorn src.main:app --host 0.0.0.0 --port 8003 --reload

run-prod:
	@echo "Starting IA-3 Evaluation System in production mode..."
	gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8003

# Clean targets
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Clean completed!"

# Install targets
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Installation completed!"

dev-install:
	@echo "Installing development dependencies..."
	pip install -r requirements.txt
	pip install -e ".[dev]"
	@echo "Development installation completed!"

# Code quality targets
lint:
	@echo "Running linting..."
	flake8 src/ tests/
	@echo "Linting completed!"

format:
	@echo "Formatting code..."
	black src/ tests/
	isort src/ tests/
	@echo "Formatting completed!"

type-check:
	@echo "Running type checking..."
	mypy src/
	@echo "Type checking completed!"

# Docker targets
docker-build:
	@echo "Building Docker image..."
	docker build -t ia-3-evaluation .
	@echo "Docker build completed!"

docker-run:
	@echo "Running Docker container..."
	docker run -p 8003:8003 ia-3-evaluation

# Data targets
download-models:
	@echo "Downloading ML models..."
	python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-m3')"
	python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-reranker-large')"
	@echo "Models downloaded!"

# Development targets
dev-setup: dev-install download-models
	@echo "Development setup completed!"

# Health check
health:
	@echo "Checking system health..."
	curl -f http://localhost:8003/api/v1/health || echo "Health check failed!"

# Metrics
metrics:
	@echo "Checking system metrics..."
	curl -f http://localhost:8003/api/v1/metrics || echo "Metrics check failed!"

# All quality checks
quality: lint format type-check test
	@echo "All quality checks completed!"
```

## NOTES de Logs/Observabilidade

### Logs Estruturados
```python
# Exemplo de log estruturado
import structlog

logger = structlog.get_logger()

# Log de avaliação
logger.info(
    "evaluation_started",
    evaluation_id="eval_123456",
    banca="CESPE",
    ano=2023,
    total_questions=100,
    metrics=["topic_hit_rate", "style_match", "answerability"]
)

# Log de métricas
logger.info(
    "metrics_calculated",
    evaluation_id="eval_123456",
    topic_hit_rate=0.85,
    style_match=0.75,
    answerability=0.92,
    processing_time=45.2
)

# Log de erro
logger.error(
    "evaluation_failed",
    evaluation_id="eval_123456",
    error="Validation failed: low plausibility score",
    details={"score": 0.3, "threshold": 0.8}
)
```

### Métricas Prometheus
```python
# Exemplo de métricas
from prometheus_client import Counter, Histogram, Gauge

# Contadores
evaluations_total = Counter('evaluations_total', 'Total evaluations', ['status'])
benchmarks_total = Counter('benchmarks_total', 'Total benchmarks', ['status'])

# Histogramas
evaluation_duration = Histogram('evaluation_duration_seconds', 'Evaluation duration')
benchmark_duration = Histogram('benchmark_duration_seconds', 'Benchmark duration')

# Gauges
active_evaluations = Gauge('active_evaluations', 'Active evaluations')
system_health = Gauge('system_health', 'System health status')
```

### Health Checks
```python
# Exemplo de health check
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "topic_hit_rate": {"status": "healthy", "response_time": 2.1},
            "style_match": {"status": "healthy", "response_time": 1.8},
            "answerability": {"status": "healthy", "response_time": 1.5},
            "metrics_aggregator": {"status": "healthy", "response_time": 0.5},
            "gap_analysis": {"status": "healthy", "response_time": 3.2},
            "report_generator": {"status": "healthy", "response_time": 15.3}
        },
        "uptime": 3600.5,
        "timestamp": "2024-01-15T10:30:00Z"
    }
```

---

**Este documento define o scaffolding completo do backend IA-3, incluindo estrutura, DTOs, requirements, Makefile e observabilidade.**
