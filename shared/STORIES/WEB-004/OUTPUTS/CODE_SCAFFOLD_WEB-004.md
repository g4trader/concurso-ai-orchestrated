# CODE_SCAFFOLD_WEB-004: Backend Scaffolding - Relatório Pós-Simulado

## /backend/web-004/ - Estrutura do Projeto

### README.md
```markdown
# WEB-004 Backend: Relatório Pós-Simulado

## Visão Geral
Sistema de análise e geração de relatórios pós-simulado com métricas de performance, análise de tempo e identificação de pontos fracos.

## Arquitetura
- **FastAPI** para API REST
- **Pydantic** para validação de dados
- **SQLAlchemy** para ORM
- **Alembic** para migrações
- **Redis** para cache e filas
- **Celery** para processamento assíncrono
- **PostgreSQL** para banco de dados
- **Pandas** para análise de dados
- **NumPy** para cálculos estatísticos

## Endpoints Principais
- `GET /api/v1/results/{id}` - Obter resultados do simulado
- `POST /api/v1/results/{id}/analyze` - Analisar resultados
- `GET /api/v1/results/{id}/performance` - Obter análise de performance
- `GET /api/v1/results/{id}/weak-points` - Identificar pontos fracos
- `GET /api/v1/results/{id}/recommendations` - Obter recomendações
- `POST /api/v1/results/{id}/export` - Exportar relatório
- `GET /api/v1/results/{id}/charts` - Obter dados para gráficos
- `POST /api/v1/results/{id}/save` - Salvar rascunho
- `GET /api/v1/results/{id}/share` - Compartilhar resultados

## Serviços
- **ResultsService** - Gerenciamento de resultados
- **AnalyticsService** - Análise de performance
- **ExportService** - Exportação de relatórios
- **StorageService** - Armazenamento de rascunhos
- **ShareService** - Compartilhamento de resultados
- **CacheService** - Gerenciamento de cache

## Configuração
- Porta: 8003
- Logs: JSON estruturado
- Métricas: Prometheus
- Cache: Redis
- Database: PostgreSQL
- Queue: Celery + Redis
```

### DTOs em Markdown

#### SimuladoResults
```markdown
# SimuladoResults

## Campos
- `id: str` - ID único do resultado
- `simulado_id: str` - ID do simulado (obrigatório)
- `user_id: str` - ID do usuário (obrigatório)
- `total_questions: int` - Total de questões (obrigatório)
- `correct_answers: int` - Respostas corretas (obrigatório)
- `wrong_answers: int` - Respostas incorretas (obrigatório)
- `unanswered_questions: int` - Questões não respondidas (obrigatório)
- `score: float` - Pontuação 0-100 (obrigatório)
- `time_spent: int` - Tempo gasto em segundos (obrigatório)
- `average_time_per_question: float` - Tempo médio por questão (obrigatório)
- `submitted_at: str` - Data de submissão (obrigatório)
- `completed_at: str` - Data de conclusão (obrigatório)
- `results: List[QuestionResult]` - Resultados por questão (obrigatório)
- `performance: PerformanceAnalysis` - Análise de performance (obrigatório)
- `weak_points: List[WeakPoint]` - Pontos fracos identificados (obrigatório)
- `recommendations: List[Recommendation]` - Recomendações (obrigatório)

## Validações
- simulado_id deve existir e estar ativo
- user_id deve existir e estar ativo
- total_questions deve ser > 0
- correct_answers + wrong_answers + unanswered_questions = total_questions
- score deve estar entre 0 e 100
- time_spent deve ser > 0
- submitted_at deve ser anterior a completed_at

## Exemplo
```json
{
  "id": "result_123456",
  "simulado_id": "sim_789012",
  "user_id": "user_345678",
  "total_questions": 50,
  "correct_answers": 35,
  "wrong_answers": 12,
  "unanswered_questions": 3,
  "score": 70.0,
  "time_spent": 7200,
  "average_time_per_question": 144.0,
  "submitted_at": "2024-01-15T12:30:00Z",
  "completed_at": "2024-01-15T12:35:00Z",
  "results": [
    {
      "question_id": "q1",
      "question": "Qual é a capital do Brasil?",
      "selected_answer": "C",
      "correct_answer": "C",
      "is_correct": true,
      "time_spent": 30,
      "topic": "conhecimentos gerais",
      "difficulty": "easy",
      "order": 1,
      "explanation": "Brasília é a capital do Brasil desde 1960"
    }
  ],
  "performance": {
    "overall_score": 70.0,
    "score_by_topic": [
      {
        "topic": "matemática",
        "total_questions": 15,
        "correct_answers": 12,
        "score": 80.0,
        "average_time": 120.0,
        "accuracy": 0.8
      }
    ],
    "score_by_difficulty": [
      {
        "difficulty": "easy",
        "total_questions": 20,
        "correct_answers": 18,
        "score": 90.0,
        "average_time": 60.0,
        "accuracy": 0.9
      }
    ],
    "time_analysis": {
      "total_time": 7200,
      "average_time_per_question": 144.0,
      "fastest_question": 15,
      "slowest_question": 300,
      "time_distribution": [
        {
          "range": "0-30s",
          "count": 5,
          "percentage": 10.0
        }
      ],
      "time_efficiency": 75.0
    },
    "accuracy_rate": 0.7,
    "completion_rate": 0.94,
    "improvement_areas": ["matemática", "física"],
    "strengths": ["português", "história"]
  },
  "weak_points": [
    {
      "topic": "matemática",
      "difficulty": "hard",
      "accuracy": 0.4,
      "average_time": 200.0,
      "questions": [],
      "recommendations": ["Estudar álgebra", "Praticar geometria"]
    }
  ],
  "recommendations": [
    {
      "type": "study",
      "priority": "high",
      "title": "Focar em matemática",
      "description": "Sua performance em matemática está abaixo da média",
      "action_items": ["Revisar álgebra", "Praticar exercícios"],
      "resources": ["Livro de matemática", "Vídeo aulas"]
    }
  ]
}
```

#### PerformanceAnalysis
```markdown
# PerformanceAnalysis

## Campos
- `overall_score: float` - Pontuação geral (obrigatório)
- `score_by_topic: List[TopicScore]` - Pontuação por tópico (obrigatório)
- `score_by_difficulty: List[DifficultyScore]` - Pontuação por dificuldade (obrigatório)
- `time_analysis: TimeAnalysis` - Análise de tempo (obrigatório)
- `accuracy_rate: float` - Taxa de acerto (obrigatório)
- `completion_rate: float` - Taxa de conclusão (obrigatório)
- `improvement_areas: List[str]` - Áreas de melhoria (obrigatório)
- `strengths: List[str]` - Pontos fortes (obrigatório)

## Exemplo
```json
{
  "overall_score": 70.0,
  "score_by_topic": [
    {
      "topic": "matemática",
      "total_questions": 15,
      "correct_answers": 12,
      "score": 80.0,
      "average_time": 120.0,
      "accuracy": 0.8
    },
    {
      "topic": "português",
      "total_questions": 20,
      "correct_answers": 18,
      "score": 90.0,
      "average_time": 90.0,
      "accuracy": 0.9
    }
  ],
  "score_by_difficulty": [
    {
      "difficulty": "easy",
      "total_questions": 20,
      "correct_answers": 18,
      "score": 90.0,
      "average_time": 60.0,
      "accuracy": 0.9
    },
    {
      "difficulty": "medium",
      "total_questions": 20,
      "correct_answers": 14,
      "score": 70.0,
      "average_time": 120.0,
      "accuracy": 0.7
    },
    {
      "difficulty": "hard",
      "total_questions": 10,
      "correct_answers": 3,
      "score": 30.0,
      "average_time": 180.0,
      "accuracy": 0.3
    }
  ],
  "time_analysis": {
    "total_time": 7200,
    "average_time_per_question": 144.0,
    "fastest_question": 15,
    "slowest_question": 300,
    "time_distribution": [
      {
        "range": "0-30s",
        "count": 5,
        "percentage": 10.0
      },
      {
        "range": "30-60s",
        "count": 15,
        "percentage": 30.0
      },
      {
        "range": "60-120s",
        "count": 20,
        "percentage": 40.0
      },
      {
        "range": "120s+",
        "count": 10,
        "percentage": 20.0
      }
    ],
    "time_efficiency": 75.0
  },
  "accuracy_rate": 0.7,
  "completion_rate": 0.94,
  "improvement_areas": ["matemática", "física"],
  "strengths": ["português", "história"]
}
```

#### WeakPoint
```markdown
# WeakPoint

## Campos
- `topic: str` - Tópico (obrigatório)
- `difficulty: str` - Dificuldade (obrigatório)
- `accuracy: float` - Precisão (obrigatório)
- `average_time: float` - Tempo médio (obrigatório)
- `questions: List[QuestionResult]` - Questões relacionadas (obrigatório)
- `recommendations: List[str]` - Recomendações (obrigatório)

## Exemplo
```json
{
  "topic": "matemática",
  "difficulty": "hard",
  "accuracy": 0.4,
  "average_time": 200.0,
  "questions": [
    {
      "question_id": "q15",
      "question": "Resolva a equação x² + 5x + 6 = 0",
      "selected_answer": "B",
      "correct_answer": "A",
      "is_correct": false,
      "time_spent": 180,
      "topic": "matemática",
      "difficulty": "hard",
      "order": 15
    }
  ],
  "recommendations": [
    "Estudar álgebra básica",
    "Praticar resolução de equações",
    "Revisar fórmulas matemáticas"
  ]
}
```

#### Recommendation
```markdown
# Recommendation

## Campos
- `type: str` - Tipo de recomendação (obrigatório)
- `priority: str` - Prioridade (obrigatório)
- `title: str` - Título (obrigatório)
- `description: str` - Descrição (obrigatório)
- `action_items: List[str]` - Itens de ação (obrigatório)
- `resources: List[str]` - Recursos (opcional)

## Exemplo
```json
{
  "type": "study",
  "priority": "high",
  "title": "Focar em matemática",
  "description": "Sua performance em matemática está abaixo da média. Recomendamos estudar os tópicos básicos.",
  "action_items": [
    "Revisar álgebra básica",
    "Praticar exercícios de equações",
    "Estudar geometria plana"
  ],
  "resources": [
    "Livro: Matemática Básica",
    "Vídeo: Resolução de Equações",
    "Site: Khan Academy"
  ]
}
```

#### ExportRequest
```markdown
# ExportRequest

## Campos
- `format: str` - Formato de exportação (obrigatório)
- `include_charts: bool` - Incluir gráficos (obrigatório)
- `include_details: bool` - Incluir detalhes (obrigatório)
- `include_recommendations: bool` - Incluir recomendações (obrigatório)
- `include_weak_points: bool` - Incluir pontos fracos (obrigatório)
- `theme: str` - Tema (obrigatório)

## Validações
- format deve ser um dos valores: markdown, pdf, json, csv
- theme deve ser um dos valores: light, dark

## Exemplo
```json
{
  "format": "markdown",
  "include_charts": true,
  "include_details": true,
  "include_recommendations": true,
  "include_weak_points": true,
  "theme": "light"
}
```

#### ExportResponse
```markdown
# ExportResponse

## Campos
- `success: bool` - Sucesso da operação (obrigatório)
- `data: str` - Dados exportados (opcional)
- `filename: str` - Nome do arquivo (opcional)
- `error: str` - Mensagem de erro (opcional)
- `size: int` - Tamanho do arquivo (opcional)

## Exemplo
```json
{
  "success": true,
  "data": "# Relatório de Resultados\n\n## Resumo\n\n- **Pontuação**: 70/100\n- **Acertos**: 35/50\n- **Tempo**: 2h 00min\n\n## Análise por Tópico\n\n| Tópico | Acertos | Total | % |\n|--------|---------|-------|---|\n| Matemática | 12 | 15 | 80% |\n| Português | 18 | 20 | 90% |\n\n## Recomendações\n\n1. Focar em matemática\n2. Praticar exercícios\n\n## Pontos Fracos\n\n- Álgebra básica\n- Geometria plana",
  "filename": "relatorio_simulado_20240115.md",
  "size": 1024
}
```

#### ChartData
```markdown
# ChartData

## Campos
- `labels: List[str]` - Rótulos (obrigatório)
- `datasets: List[ChartDataset]` - Conjuntos de dados (obrigatório)

## Exemplo
```json
{
  "labels": ["Matemática", "Português", "História", "Geografia"],
  "datasets": [
    {
      "label": "Acertos",
      "data": [12, 18, 8, 7],
      "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"],
      "borderColor": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"],
      "borderWidth": 1
    }
  ]
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

# Database
sqlalchemy>=2.0.0
alembic>=1.13.0
asyncpg>=0.29.0
psycopg2-binary>=2.9.0

# Cache and Queue
redis>=5.0.0
aioredis>=2.0.0
celery>=5.3.0
kombu>=5.3.0

# Data Analysis
pandas>=2.1.0
numpy>=1.24.0
scipy>=1.11.0

# HTTP Client
httpx>=0.25.0
aiohttp>=3.9.0

# Validation
email-validator>=2.1.0
phonenumbers>=8.13.0

# Security
cryptography>=41.0.0
bcrypt>=4.1.0

# Monitoring
prometheus-client>=0.19.0
structlog>=23.2.0

# Export
reportlab>=4.0.0
weasyprint>=60.0.0
jinja2>=3.1.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
httpx>=0.25.0
factory-boy>=3.3.0

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
name = "web-004-results"
version = "0.1.0"
description = "Sistema de relatórios pós-simulado para Concurso AI"
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
    "sqlalchemy>=2.0.0",
    "alembic>=1.13.0",
    "asyncpg>=0.29.0",
    "redis>=5.0.0",
    "celery>=5.3.0",
    "pandas>=2.1.0",
    "numpy>=1.24.0",
    "httpx>=0.25.0",
    "cryptography>=41.0.0",
    "prometheus-client>=0.19.0",
    "structlog>=23.2.0",
    "reportlab>=4.0.0",
    "weasyprint>=60.0.0",
    "jinja2>=3.1.0",
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
Homepage = "https://github.com/concurso-ai/web-004-results"
Repository = "https://github.com/concurso-ai/web-004-results.git"
Documentation = "https://docs.concurso-ai.com/web-004-results"

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
# WEB-004 Results System Makefile

.PHONY: help build test run clean install dev-install lint format type-check

# Default target
help:
	@echo "WEB-004 Results System - Available targets:"
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
	@echo "Building WEB-004 Results System..."
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
	@echo "Starting WEB-004 Results System..."
	uvicorn src.main:app --host 0.0.0.0 --port 8003 --reload

run-prod:
	@echo "Starting WEB-004 Results System in production mode..."
	gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8003

run-celery:
	@echo "Starting Celery worker..."
	celery -A src.celery worker --loglevel=info

run-celery-beat:
	@echo "Starting Celery beat..."
	celery -A src.celery beat --loglevel=info

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

# Database targets
db-migrate:
	@echo "Running database migrations..."
	alembic upgrade head
	@echo "Migrations completed!"

db-revision:
	@echo "Creating new migration..."
	alembic revision --autogenerate -m "$(message)"
	@echo "Migration created!"

db-reset:
	@echo "Resetting database..."
	alembic downgrade base
	alembic upgrade head
	@echo "Database reset completed!"

# Docker targets
docker-build:
	@echo "Building Docker image..."
	docker build -t web-004-results .
	@echo "Docker build completed!"

docker-run:
	@echo "Running Docker container..."
	docker run -p 8003:8003 web-004-results

# Development targets
dev-setup: dev-install db-migrate
	@echo "Development setup completed!"

# Health check
health:
	@echo "Checking system health..."
	curl -f http://localhost:8003/api/v1/health || echo "Health check failed!"

# All quality checks
quality: lint format type-check test
	@echo "All quality checks completed!"
```

## Exemplos de Chamadas cURL

### Obter Resultados
```bash
curl -X GET "http://localhost:8003/api/v1/results/result_123456" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

### Analisar Resultados
```bash
curl -X POST "http://localhost:8003/api/v1/results/result_123456/analyze" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

### Obter Análise de Performance
```bash
curl -X GET "http://localhost:8003/api/v1/results/result_123456/performance" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

### Identificar Pontos Fracos
```bash
curl -X GET "http://localhost:8003/api/v1/results/result_123456/weak-points" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

### Obter Recomendações
```bash
curl -X GET "http://localhost:8003/api/v1/results/result_123456/recommendations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

### Exportar Relatório
```bash
curl -X POST "http://localhost:8003/api/v1/results/result_123456/export" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "format": "markdown",
    "include_charts": true,
    "include_details": true,
    "include_recommendations": true,
    "include_weak_points": true,
    "theme": "light"
  }'
```

### Obter Dados para Gráficos
```bash
curl -X GET "http://localhost:8003/api/v1/results/result_123456/charts" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

### Salvar Rascunho
```bash
curl -X POST "http://localhost:8003/api/v1/results/result_123456/save" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "draft_data": {
      "notes": "Preciso estudar mais matemática",
      "bookmarks": ["q15", "q23", "q41"]
    }
  }'
```

### Compartilhar Resultados
```bash
curl -X GET "http://localhost:8003/api/v1/results/result_123456/share" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

### Health Check
```bash
curl -X GET "http://localhost:8003/api/v1/health"
```

---

**Este documento define o scaffolding completo do backend WEB-004, incluindo estrutura, DTOs, requirements, Makefile e exemplos de uso.**
