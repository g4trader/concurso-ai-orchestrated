# CODE_SCAFFOLD_WEB-003: Backend Scaffolding - Tela de Geração de Simulado

## /backend/web-003/ - Estrutura do Projeto

### README.md
```markdown
# WEB-003 Backend: Tela de Geração de Simulado

## Visão Geral
Sistema de geração de simulados para concursos públicos com seleção de banca, edital e configuração de questões.

## Arquitetura
- **FastAPI** para API REST
- **Pydantic** para validação de dados
- **SQLAlchemy** para ORM
- **Alembic** para migrações
- **Redis** para cache e filas
- **Celery** para processamento assíncrono
- **PostgreSQL** para banco de dados

## Endpoints Principais
- `GET /api/v1/bancas` - Listar bancas disponíveis
- `GET /api/v1/bancas/{id}` - Obter banca específica
- `GET /api/v1/editais` - Listar editais
- `GET /api/v1/editais/{id}` - Obter edital específico
- `POST /api/v1/simulados/generate` - Gerar simulado
- `GET /api/v1/simulados/{id}` - Obter simulado
- `GET /api/v1/simulados/{id}/questions` - Obter questões do simulado
- `GET /api/v1/generation/{id}/status` - Status da geração
- `POST /api/v1/simulados/{id}/submit` - Submeter respostas
- `GET /api/v1/simulados/{id}/results` - Obter resultados

## Serviços
- **SimuladoService** - Gerenciamento de simulados
- **BancaService** - Gerenciamento de bancas
- **EditalService** - Gerenciamento de editais
- **QuestionService** - Gerenciamento de questões
- **GenerationService** - Geração de simulados
- **CacheService** - Gerenciamento de cache

## Configuração
- Porta: 8002
- Logs: JSON estruturado
- Métricas: Prometheus
- Cache: Redis
- Database: PostgreSQL
- Queue: Celery + Redis
```

### DTOs em Markdown

#### SimuladoGenerationRequest
```markdown
# SimuladoGenerationRequest

## Campos
- `banca_id: str` - ID da banca (obrigatório)
- `edital_id: str` - ID do edital (obrigatório)
- `total_questions: int` - Número total de questões (obrigatório, 1-100)
- `time_limit: int` - Tempo limite em minutos (obrigatório, 30-300)
- `difficulty: str` - Dificuldade (obrigatório, easy/medium/hard)
- `topics: List[str]` - Tópicos específicos (opcional)
- `custom_instructions: str` - Instruções customizadas (opcional)

## Validações
- banca_id deve existir e estar ativa
- edital_id deve existir e estar ativo
- total_questions deve estar entre 1 e 100
- time_limit deve estar entre 30 e 300 minutos
- difficulty deve ser uma das opções válidas
- topics deve ser uma lista de strings válidas

## Exemplo
```json
{
  "banca_id": "123e4567-e89b-12d3-a456-426614174000",
  "edital_id": "456e7890-e89b-12d3-a456-426614174001",
  "total_questions": 50,
  "time_limit": 120,
  "difficulty": "medium",
  "topics": ["matemática", "português", "conhecimentos gerais"],
  "custom_instructions": "Foco em questões de raciocínio lógico"
}
```

#### SimuladoGenerationResponse
```markdown
# SimuladoGenerationResponse

## Campos
- `simulado: Simulado` - Dados do simulado criado
- `questions: List[Question]` - Lista de questões geradas
- `estimated_time: int` - Tempo estimado em minutos
- `generation_id: str` - ID da geração para tracking

## Exemplo
```json
{
  "simulado": {
    "id": "789e0123-e89b-12d3-a456-426614174002",
    "title": "Simulado CESPE 2024 - Concurso X",
    "description": "Simulado baseado no edital CESPE 2024",
    "banca": {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "CESPE",
      "code": "CESPE"
    },
    "edital": {
      "id": "456e7890-e89b-12d3-a456-426614174001",
      "title": "Concurso X 2024",
      "year": 2024
    },
    "total_questions": 50,
    "time_limit": 120,
    "difficulty": "medium",
    "topics": ["matemática", "português", "conhecimentos gerais"],
    "status": "ready",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "questions": [
    {
      "id": "q1",
      "question": "Qual é a capital do Brasil?",
      "alternatives": {
        "A": "São Paulo",
        "B": "Rio de Janeiro",
        "C": "Brasília",
        "D": "Belo Horizonte",
        "E": "Salvador"
      },
      "correct_answer": "C",
      "difficulty": "easy",
      "topic": "conhecimentos gerais",
      "order": 1
    }
  ],
  "estimated_time": 120,
  "generation_id": "gen_123456"
}
```

#### BancaListResponse
```markdown
# BancaListResponse

## Campos
- `bancas: List[Banca]` - Lista de bancas
- `total: int` - Total de bancas
- `page: int` - Página atual
- `limit: int` - Limite por página

## Exemplo
```json
{
  "bancas": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "CESPE",
      "code": "CESPE",
      "description": "Centro de Seleção e de Promoção de Eventos",
      "logo": "https://example.com/cespe-logo.png",
      "website": "https://www.cespe.unb.br",
      "is_active": true,
      "characteristics": {
        "question_style": "multiple_choice",
        "answer_format": "A-E",
        "time_per_question": 2,
        "difficulty_distribution": {
          "easy": 20,
          "medium": 60,
          "hard": 20
        },
        "common_topics": ["português", "matemática", "conhecimentos gerais"]
      },
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10
}
```

#### EditalListResponse
```markdown
# EditalListResponse

## Campos
- `editais: List[Edital]` - Lista de editais
- `total: int` - Total de editais
- `page: int` - Página atual
- `limit: int` - Limite por página

## Exemplo
```json
{
  "editais": [
    {
      "id": "456e7890-e89b-12d3-a456-426614174001",
      "title": "Concurso X 2024",
      "description": "Concurso público para cargo X",
      "banca_id": "123e4567-e89b-12d3-a456-426614174000",
      "year": 2024,
      "month": 6,
      "exam_type": "concurso",
      "subjects": ["português", "matemática", "conhecimentos gerais"],
      "total_questions": 100,
      "time_limit": 240,
      "is_active": true,
      "published_at": "2024-01-15T10:30:00Z",
      "exam_date": "2024-06-15T09:00:00Z",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10
}
```

#### GenerationStatus
```markdown
# GenerationStatus

## Campos
- `id: str` - ID da geração
- `status: str` - Status atual (pending/processing/completed/failed)
- `progress: int` - Progresso de 0 a 100
- `current_step: str` - Etapa atual
- `estimated_time_remaining: int` - Tempo estimado restante em segundos
- `error: str` - Mensagem de erro (se houver)
- `created_at: str` - Data de criação
- `updated_at: str` - Data de atualização

## Exemplo
```json
{
  "id": "gen_123456",
  "status": "processing",
  "progress": 65,
  "current_step": "Gerando questões de matemática",
  "estimated_time_remaining": 45,
  "error": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:32:00Z"
}
```

#### SimuladoSubmitRequest
```markdown
# SimuladoSubmitRequest

## Campos
- `responses: List[QuestionResponse]` - Lista de respostas
- `time_spent: int` - Tempo total gasto em segundos
- `submitted_at: str` - Data/hora de submissão

## Exemplo
```json
{
  "responses": [
    {
      "question_id": "q1",
      "selected_answer": "C",
      "time_spent": 30,
      "answered_at": "2024-01-15T10:30:00Z"
    }
  ],
  "time_spent": 7200,
  "submitted_at": "2024-01-15T12:30:00Z"
}
```

#### SimuladoResults
```markdown
# SimuladoResults

## Campos
- `simulado_id: str` - ID do simulado
- `total_questions: int` - Total de questões
- `correct_answers: int` - Respostas corretas
- `wrong_answers: int` - Respostas incorretas
- `score: float` - Pontuação (0-100)
- `time_spent: int` - Tempo gasto em segundos
- `submitted_at: str` - Data de submissão
- `results: List[QuestionResult]` - Resultados por questão

## Exemplo
```json
{
  "simulado_id": "789e0123-e89b-12d3-a456-426614174002",
  "total_questions": 50,
  "correct_answers": 35,
  "wrong_answers": 15,
  "score": 70.0,
  "time_spent": 7200,
  "submitted_at": "2024-01-15T12:30:00Z",
  "results": [
    {
      "question_id": "q1",
      "selected_answer": "C",
      "correct_answer": "C",
      "is_correct": true,
      "time_spent": 30
    }
  ]
}
```

### Exemplos de Payloads

#### Gerar Simulado
```json
{
  "banca_id": "123e4567-e89b-12d3-a456-426614174000",
  "edital_id": "456e7890-e89b-12d3-a456-426614174001",
  "total_questions": 50,
  "time_limit": 120,
  "difficulty": "medium",
  "topics": ["matemática", "português", "conhecimentos gerais"],
  "custom_instructions": "Foco em questões de raciocínio lógico"
}
```

#### Listar Bancas
```json
{
  "page": 1,
  "limit": 10,
  "search": "CESPE",
  "is_active": true
}
```

#### Listar Editais
```json
{
  "banca_id": "123e4567-e89b-12d3-a456-426614174000",
  "year": 2024,
  "exam_type": "concurso",
  "page": 1,
  "limit": 10
}
```

#### Submeter Respostas
```json
{
  "responses": [
    {
      "question_id": "q1",
      "selected_answer": "C",
      "time_spent": 30,
      "answered_at": "2024-01-15T10:30:00Z"
    },
    {
      "question_id": "q2",
      "selected_answer": "A",
      "time_spent": 45,
      "answered_at": "2024-01-15T10:31:00Z"
    }
  ],
  "time_spent": 7200,
  "submitted_at": "2024-01-15T12:30:00Z"
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
name = "web-003-simulado"
version = "0.1.0"
description = "Sistema de geração de simulados para Concurso AI"
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
    "httpx>=0.25.0",
    "cryptography>=41.0.0",
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
Homepage = "https://github.com/concurso-ai/web-003-simulado"
Repository = "https://github.com/concurso-ai/web-003-simulado.git"
Documentation = "https://docs.concurso-ai.com/web-003-simulado"

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
# WEB-003 Simulado System Makefile

.PHONY: help build test run clean install dev-install lint format type-check

# Default target
help:
	@echo "WEB-003 Simulado System - Available targets:"
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
	@echo "Building WEB-003 Simulado System..."
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
	@echo "Starting WEB-003 Simulado System..."
	uvicorn src.main:app --host 0.0.0.0 --port 8002 --reload

run-prod:
	@echo "Starting WEB-003 Simulado System in production mode..."
	gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8002

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
	docker build -t web-003-simulado .
	@echo "Docker build completed!"

docker-run:
	@echo "Running Docker container..."
	docker run -p 8002:8002 web-003-simulado

# Development targets
dev-setup: dev-install db-migrate
	@echo "Development setup completed!"

# Health check
health:
	@echo "Checking system health..."
	curl -f http://localhost:8002/api/v1/health || echo "Health check failed!"

# All quality checks
quality: lint format type-check test
	@echo "All quality checks completed!"
```

## Exemplos de Chamadas cURL

### Listar Bancas
```bash
curl -X GET "http://localhost:8002/api/v1/bancas?page=1&limit=10&search=CESPE" \
  -H "Content-Type: application/json"
```

### Obter Banca
```bash
curl -X GET "http://localhost:8002/api/v1/bancas/123e4567-e89b-12d3-a456-426614174000" \
  -H "Content-Type: application/json"
```

### Listar Editais
```bash
curl -X GET "http://localhost:8002/api/v1/editais?banca_id=123e4567-e89b-12d3-a456-426614174000&year=2024" \
  -H "Content-Type: application/json"
```

### Obter Edital
```bash
curl -X GET "http://localhost:8002/api/v1/editais/456e7890-e89b-12d3-a456-426614174001" \
  -H "Content-Type: application/json"
```

### Gerar Simulado
```bash
curl -X POST "http://localhost:8002/api/v1/simulados/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "banca_id": "123e4567-e89b-12d3-a456-426614174000",
    "edital_id": "456e7890-e89b-12d3-a456-426614174001",
    "total_questions": 50,
    "time_limit": 120,
    "difficulty": "medium",
    "topics": ["matemática", "português", "conhecimentos gerais"],
    "custom_instructions": "Foco em questões de raciocínio lógico"
  }'
```

### Status da Geração
```bash
curl -X GET "http://localhost:8002/api/v1/generation/gen_123456/status" \
  -H "Content-Type: application/json"
```

### Obter Simulado
```bash
curl -X GET "http://localhost:8002/api/v1/simulados/789e0123-e89b-12d3-a456-426614174002" \
  -H "Content-Type: application/json"
```

### Obter Questões do Simulado
```bash
curl -X GET "http://localhost:8002/api/v1/simulados/789e0123-e89b-12d3-a456-426614174002/questions" \
  -H "Content-Type: application/json"
```

### Submeter Respostas
```bash
curl -X POST "http://localhost:8002/api/v1/simulados/789e0123-e89b-12d3-a456-426614174002/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      {
        "question_id": "q1",
        "selected_answer": "C",
        "time_spent": 30,
        "answered_at": "2024-01-15T10:30:00Z"
      }
    ],
    "time_spent": 7200,
    "submitted_at": "2024-01-15T12:30:00Z"
  }'
```

### Obter Resultados
```bash
curl -X GET "http://localhost:8002/api/v1/simulados/789e0123-e89b-12d3-a456-426614174002/results" \
  -H "Content-Type: application/json"
```

### Health Check
```bash
curl -X GET "http://localhost:8002/api/v1/health"
```

---

**Este documento define o scaffolding completo do backend WEB-003, incluindo estrutura, DTOs, requirements, Makefile e exemplos de uso.**
