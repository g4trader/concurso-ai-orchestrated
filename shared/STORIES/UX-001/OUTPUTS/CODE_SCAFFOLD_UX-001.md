# CODE_SCAFFOLD_UX-001: Backend Scaffolding - Sistema de Feedback do Usuário

## /backend/ux-001/ - Estrutura do Projeto

### README.md
```markdown
# UX-001 Backend: Sistema de Feedback do Usuário

## Visão Geral
Sistema de coleta de feedback dos usuários sobre questões de simulados, permitindo reportar problemas, erros e sugestões para melhoria contínua da qualidade.

## Arquitetura
- **FastAPI** para API REST
- **Pydantic** para validação de dados
- **SQLAlchemy** para ORM
- **Alembic** para migrações
- **Redis** para cache e filas
- **Celery** para processamento assíncrono
- **PostgreSQL** para banco de dados
- **Elasticsearch** para busca e análise
- **Prometheus** para métricas

## Endpoints Principais
- `POST /api/v1/feedback` - Enviar feedback
- `GET /api/v1/feedback/{id}` - Obter feedback específico
- `GET /api/v1/feedback` - Listar feedbacks (admin)
- `PUT /api/v1/feedback/{id}/status` - Atualizar status do feedback
- `GET /api/v1/feedback/categories` - Obter categorias de feedback
- `POST /api/v1/feedback/draft` - Salvar rascunho de feedback
- `GET /api/v1/feedback/draft/{question_id}` - Obter rascunho
- `DELETE /api/v1/feedback/draft/{question_id}` - Limpar rascunho
- `GET /api/v1/feedback/analytics` - Analytics de feedback
- `POST /api/v1/feedback/bulk` - Envio em lote

## Serviços
- **FeedbackService** - Gerenciamento de feedback
- **DraftService** - Gerenciamento de rascunhos
- **AnalyticsService** - Análise de feedback
- **NotificationService** - Notificações
- **CacheService** - Gerenciamento de cache
- **QueueService** - Processamento assíncrono

## Configuração
- Porta: 8004
- Logs: JSON estruturado
- Métricas: Prometheus
- Cache: Redis
- Database: PostgreSQL
- Queue: Celery + Redis
- Search: Elasticsearch
```

### DTOs em Markdown

#### FeedbackRequest
```markdown
# FeedbackRequest

## Campos
- `question_id: str` - ID da questão (obrigatório)
- `user_id: str` - ID do usuário (obrigatório)
- `category: FeedbackCategory` - Categoria do feedback (obrigatório)
- `comment: str` - Comentário do usuário (obrigatório)
- `metadata: FeedbackMetadata` - Metadados da questão (obrigatório)
- `timestamp: str` - Timestamp do feedback (obrigatório)
- `user_agent: str` - User agent do navegador (obrigatório)
- `session_id: str` - ID da sessão (obrigatório)

## Validações
- question_id deve existir e estar ativo
- user_id deve existir e estar ativo
- category deve ser uma categoria válida
- comment deve ter entre 10 e 1000 caracteres
- metadata deve conter informações válidas da questão
- timestamp deve ser uma data válida
- user_agent deve ser uma string válida
- session_id deve ser um UUID válido

## Exemplo
```json
{
  "question_id": "q_123456",
  "user_id": "user_789012",
  "category": {
    "id": "error_in_question",
    "name": "Erro na Questão",
    "description": "A questão contém um erro factual ou técnico",
    "priority": "high",
    "icon": "alert-triangle"
  },
  "comment": "A alternativa B está incorreta. A resposta correta deveria ser A, pois segundo a lei 8.112/90, o prazo é de 30 dias, não 60.",
  "metadata": {
    "question_text": "Qual é o prazo para recurso em processo administrativo?",
    "question_options": [
      "A) 30 dias",
      "B) 60 dias",
      "C) 90 dias",
      "D) 120 dias",
      "E) 180 dias"
    ],
    "selected_answer": "A",
    "correct_answer": "B",
    "time_spent": 45,
    "difficulty": "medium",
    "topic": "direito administrativo",
    "banca": "CESPE",
    "edital": "MPU_2024",
    "simulado_id": "sim_345678",
    "browser_info": {
      "name": "Chrome",
      "version": "120.0.0.0",
      "os": "Windows 10",
      "language": "pt-BR",
      "timezone": "America/Sao_Paulo"
    },
    "device_info": {
      "type": "desktop",
      "screen": {
        "width": 1920,
        "height": 1080
      },
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
  },
  "timestamp": "2024-01-15T14:30:00Z",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "session_id": "sess_abc123def456"
}
```

#### FeedbackCategory
```markdown
# FeedbackCategory

## Campos
- `id: str` - ID da categoria (obrigatório)
- `name: str` - Nome da categoria (obrigatório)
- `description: str` - Descrição da categoria (obrigatório)
- `priority: str` - Prioridade da categoria (obrigatório)
- `icon: str` - Ícone da categoria (obrigatório)

## Validações
- id deve ser único e válido
- name deve ter entre 3 e 50 caracteres
- description deve ter entre 10 e 200 caracteres
- priority deve ser um dos valores: low, medium, high
- icon deve ser um nome de ícone válido

## Exemplo
```json
{
  "id": "error_in_question",
  "name": "Erro na Questão",
  "description": "A questão contém um erro factual ou técnico",
  "priority": "high",
  "icon": "alert-triangle"
}
```

#### FeedbackMetadata
```markdown
# FeedbackMetadata

## Campos
- `question_text: str` - Texto da questão (obrigatório)
- `question_options: List[str]` - Opções da questão (obrigatório)
- `selected_answer: str` - Resposta selecionada (opcional)
- `correct_answer: str` - Resposta correta (opcional)
- `time_spent: int` - Tempo gasto na questão (obrigatório)
- `difficulty: str` - Dificuldade da questão (obrigatório)
- `topic: str` - Tópico da questão (obrigatório)
- `banca: str` - Banca organizadora (obrigatório)
- `edital: str` - Edital (obrigatório)
- `simulado_id: str` - ID do simulado (obrigatório)
- `browser_info: BrowserInfo` - Informações do navegador (obrigatório)
- `device_info: DeviceInfo` - Informações do dispositivo (obrigatório)

## Exemplo
```json
{
  "question_text": "Qual é o prazo para recurso em processo administrativo?",
  "question_options": [
    "A) 30 dias",
    "B) 60 dias",
    "C) 90 dias",
    "D) 120 dias",
    "E) 180 dias"
  ],
  "selected_answer": "A",
  "correct_answer": "B",
  "time_spent": 45,
  "difficulty": "medium",
  "topic": "direito administrativo",
  "banca": "CESPE",
  "edital": "MPU_2024",
  "simulado_id": "sim_345678",
  "browser_info": {
    "name": "Chrome",
    "version": "120.0.0.0",
    "os": "Windows 10",
    "language": "pt-BR",
    "timezone": "America/Sao_Paulo"
  },
  "device_info": {
    "type": "desktop",
    "screen": {
      "width": 1920,
      "height": 1080
    },
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  }
}
```

#### FeedbackResponse
```markdown
# FeedbackResponse

## Campos
- `success: bool` - Sucesso da operação (obrigatório)
- `feedback_id: str` - ID do feedback criado (opcional)
- `message: str` - Mensagem de resposta (obrigatório)
- `timestamp: str` - Timestamp da resposta (obrigatório)
- `status: str` - Status do feedback (obrigatório)

## Validações
- success deve ser boolean
- feedback_id deve ser um UUID válido se success for true
- message deve ter entre 5 e 200 caracteres
- timestamp deve ser uma data válida
- status deve ser um dos valores: pending, reviewed, resolved, rejected

## Exemplo
```json
{
  "success": true,
  "feedback_id": "fb_abc123def456",
  "message": "Feedback enviado com sucesso. Obrigado pela sua contribuição!",
  "timestamp": "2024-01-15T14:30:05Z",
  "status": "pending"
}
```

#### FeedbackDraft
```markdown
# FeedbackDraft

## Campos
- `question_id: str` - ID da questão (obrigatório)
- `category: FeedbackCategory` - Categoria do feedback (opcional)
- `comment: str` - Comentário do usuário (obrigatório)
- `last_saved: str` - Última vez salvo (obrigatório)
- `is_dirty: bool` - Se há mudanças não salvas (obrigatório)

## Validações
- question_id deve existir e estar ativo
- category deve ser uma categoria válida se fornecida
- comment deve ter entre 0 e 1000 caracteres
- last_saved deve ser uma data válida
- is_dirty deve ser boolean

## Exemplo
```json
{
  "question_id": "q_123456",
  "category": {
    "id": "error_in_question",
    "name": "Erro na Questão",
    "description": "A questão contém um erro factual ou técnico",
    "priority": "high",
    "icon": "alert-triangle"
  },
  "comment": "A alternativa B está incorreta. A resposta correta deveria ser A...",
  "last_saved": "2024-01-15T14:25:00Z",
  "is_dirty": false
}
```

#### FeedbackAnalytics
```markdown
# FeedbackAnalytics

## Campos
- `total_feedback: int` - Total de feedbacks (obrigatório)
- `feedback_by_category: List[CategoryStats]` - Estatísticas por categoria (obrigatório)
- `feedback_by_priority: List[PriorityStats]` - Estatísticas por prioridade (obrigatório)
- `feedback_by_status: List[StatusStats]` - Estatísticas por status (obrigatório)
- `feedback_by_topic: List[TopicStats]` - Estatísticas por tópico (obrigatório)
- `feedback_by_banca: List[BancaStats]` - Estatísticas por banca (obrigatório)
- `response_time_avg: float` - Tempo médio de resposta (obrigatório)
- `resolution_rate: float` - Taxa de resolução (obrigatório)

## Exemplo
```json
{
  "total_feedback": 1250,
  "feedback_by_category": [
    {
      "category": "error_in_question",
      "count": 450,
      "percentage": 36.0
    },
    {
      "category": "ambiguous_question",
      "count": 320,
      "percentage": 25.6
    }
  ],
  "feedback_by_priority": [
    {
      "priority": "high",
      "count": 500,
      "percentage": 40.0
    },
    {
      "priority": "medium",
      "count": 450,
      "percentage": 36.0
    },
    {
      "priority": "low",
      "count": 300,
      "percentage": 24.0
    }
  ],
  "feedback_by_status": [
    {
      "status": "pending",
      "count": 600,
      "percentage": 48.0
    },
    {
      "status": "reviewed",
      "count": 400,
      "percentage": 32.0
    },
    {
      "status": "resolved",
      "count": 200,
      "percentage": 16.0
    },
    {
      "status": "rejected",
      "count": 50,
      "percentage": 4.0
    }
  ],
  "feedback_by_topic": [
    {
      "topic": "direito administrativo",
      "count": 300,
      "percentage": 24.0
    },
    {
      "topic": "matemática",
      "count": 250,
      "percentage": 20.0
    }
  ],
  "feedback_by_banca": [
    {
      "banca": "CESPE",
      "count": 500,
      "percentage": 40.0
    },
    {
      "banca": "FGV",
      "count": 300,
      "percentage": 24.0
    }
  ],
  "response_time_avg": 2.5,
  "resolution_rate": 0.16
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

# Search
elasticsearch>=8.11.0
elasticsearch-dsl>=8.11.0

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

# Analytics
pandas>=2.1.0
numpy>=1.24.0

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
name = "ux-001-feedback"
version = "0.1.0"
description = "Sistema de feedback do usuário para Concurso AI"
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
    "elasticsearch>=8.11.0",
    "httpx>=0.25.0",
    "cryptography>=41.0.0",
    "prometheus-client>=0.19.0",
    "structlog>=23.2.0",
    "pandas>=2.1.0",
    "numpy>=1.24.0",
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
Homepage = "https://github.com/concurso-ai/ux-001-feedback"
Repository = "https://github.com/concurso-ai/ux-001-feedback.git"
Documentation = "https://docs.concurso-ai.com/ux-001-feedback"

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
# UX-001 Feedback System Makefile

.PHONY: help build test run clean install dev-install lint format type-check

# Default target
help:
	@echo "UX-001 Feedback System - Available targets:"
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
	@echo "Building UX-001 Feedback System..."
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
	@echo "Starting UX-001 Feedback System..."
	uvicorn src.main:app --host 0.0.0.0 --port 8004 --reload

run-prod:
	@echo "Starting UX-001 Feedback System in production mode..."
	gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8004

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
	docker build -t ux-001-feedback .
	@echo "Docker build completed!"

docker-run:
	@echo "Running Docker container..."
	docker run -p 8004:8004 ux-001-feedback

# Development targets
dev-setup: dev-install db-migrate
	@echo "Development setup completed!"

# Health check
health:
	@echo "Checking system health..."
	curl -f http://localhost:8004/api/v1/health || echo "Health check failed!"

# All quality checks
quality: lint format type-check test
	@echo "All quality checks completed!"
```

## Exemplos de Chamadas cURL

### Enviar Feedback
```bash
curl -X POST "http://localhost:8004/api/v1/feedback" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "question_id": "q_123456",
    "user_id": "user_789012",
    "category": {
      "id": "error_in_question",
      "name": "Erro na Questão",
      "description": "A questão contém um erro factual ou técnico",
      "priority": "high",
      "icon": "alert-triangle"
    },
    "comment": "A alternativa B está incorreta. A resposta correta deveria ser A.",
    "metadata": {
      "question_text": "Qual é o prazo para recurso em processo administrativo?",
      "question_options": ["A) 30 dias", "B) 60 dias", "C) 90 dias", "D) 120 dias", "E) 180 dias"],
      "selected_answer": "A",
      "correct_answer": "B",
      "time_spent": 45,
      "difficulty": "medium",
      "topic": "direito administrativo",
      "banca": "CESPE",
      "edital": "MPU_2024",
      "simulado_id": "sim_345678",
      "browser_info": {
        "name": "Chrome",
        "version": "120.0.0.0",
        "os": "Windows 10",
        "language": "pt-BR",
        "timezone": "America/Sao_Paulo"
      },
      "device_info": {
        "type": "desktop",
        "screen": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      }
    },
    "timestamp": "2024-01-15T14:30:00Z",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "session_id": "sess_abc123def456"
  }'
```

### Obter Feedback
```bash
curl -X GET "http://localhost:8004/api/v1/feedback/fb_abc123def456" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

### Listar Feedbacks
```bash
curl -X GET "http://localhost:8004/api/v1/feedback?page=1&limit=10&status=pending" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

### Atualizar Status do Feedback
```bash
curl -X PUT "http://localhost:8004/api/v1/feedback/fb_abc123def456/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "status": "reviewed",
    "admin_comment": "Feedback analisado e aceito"
  }'
```

### Obter Categorias
```bash
curl -X GET "http://localhost:8004/api/v1/feedback/categories" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

### Salvar Rascunho
```bash
curl -X POST "http://localhost:8004/api/v1/feedback/draft" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "question_id": "q_123456",
    "category": {
      "id": "error_in_question",
      "name": "Erro na Questão",
      "description": "A questão contém um erro factual ou técnico",
      "priority": "high",
      "icon": "alert-triangle"
    },
    "comment": "A alternativa B está incorreta...",
    "last_saved": "2024-01-15T14:25:00Z",
    "is_dirty": false
  }'
```

### Obter Rascunho
```bash
curl -X GET "http://localhost:8004/api/v1/feedback/draft/q_123456" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

### Limpar Rascunho
```bash
curl -X DELETE "http://localhost:8004/api/v1/feedback/draft/q_123456" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

### Obter Analytics
```bash
curl -X GET "http://localhost:8004/api/v1/feedback/analytics?period=30d" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>"
```

### Envio em Lote
```bash
curl -X POST "http://localhost:8004/api/v1/feedback/bulk" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "feedbacks": [
      {
        "question_id": "q_123456",
        "user_id": "user_789012",
        "category": {"id": "error_in_question", "name": "Erro na Questão", "description": "A questão contém um erro factual ou técnico", "priority": "high", "icon": "alert-triangle"},
        "comment": "Primeiro feedback",
        "metadata": {"question_text": "Questão 1", "question_options": ["A", "B", "C", "D", "E"], "time_spent": 30, "difficulty": "easy", "topic": "matemática", "banca": "CESPE", "edital": "MPU_2024", "simulado_id": "sim_345678", "browser_info": {"name": "Chrome", "version": "120.0.0.0", "os": "Windows 10", "language": "pt-BR", "timezone": "America/Sao_Paulo"}, "device_info": {"type": "desktop", "screen": {"width": 1920, "height": 1080}, "user_agent": "Mozilla/5.0"}},
        "timestamp": "2024-01-15T14:30:00Z",
        "user_agent": "Mozilla/5.0",
        "session_id": "sess_abc123def456"
      }
    ]
  }'
```

### Health Check
```bash
curl -X GET "http://localhost:8004/api/v1/health"
```

---

**Este documento define o scaffolding completo do backend UX-001, incluindo estrutura, DTOs, requirements, Makefile e exemplos de uso.**
