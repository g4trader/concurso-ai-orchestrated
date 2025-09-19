# CODE_SCAFFOLD_WEB-002: Backend Scaffolding - Autenticação Simples

## /backend/web-002/ - Estrutura do Projeto

### README.md
```markdown
# WEB-002 Backend: Autenticação Simples (E-mail/Senha)

## Visão Geral
Sistema de autenticação simples para identificação de usuários e persistência de histórico de simulados.

## Arquitetura
- **FastAPI** para API REST
- **Pydantic** para validação de dados
- **JWT** para tokens de autenticação
- **SQLAlchemy** para ORM
- **Alembic** para migrações
- **Redis** para cache de tokens

## Endpoints Principais
- `POST /api/v1/auth/login` - Login do usuário
- `POST /api/v1/auth/logout` - Logout do usuário
- `POST /api/v1/auth/refresh` - Refresh do token
- `GET /api/v1/auth/me` - Informações do usuário
- `POST /api/v1/auth/register` - Registro de usuário
- `POST /api/v1/auth/forgot-password` - Recuperação de senha
- `POST /api/v1/auth/reset-password` - Reset de senha

## Serviços
- **AuthService** - Lógica de autenticação
- **TokenService** - Geração e validação de tokens
- **UserService** - Gerenciamento de usuários
- **EmailService** - Envio de emails
- **PasswordService** - Hash e validação de senhas

## Configuração
- Porta: 8001
- Logs: JSON estruturado
- Métricas: Prometheus
- Cache: Redis
- Database: PostgreSQL
```

### DTOs em Markdown

#### LoginRequest
```markdown
# LoginRequest

## Campos
- `email: str` - Email do usuário (obrigatório)
- `password: str` - Senha do usuário (obrigatório)
- `remember_me: bool` - Lembrar usuário (opcional, default: false)

## Validações
- Email deve ser válido
- Senha deve ter pelo menos 8 caracteres
- Campos obrigatórios não podem ser vazios

## Exemplo
```json
{
  "email": "usuario@exemplo.com",
  "password": "senha123456",
  "remember_me": true
}
```

#### LoginResponse
```markdown
# LoginResponse

## Campos
- `user: User` - Dados do usuário
- `token: str` - Token JWT de acesso
- `refresh_token: str` - Token para refresh
- `expires_in: int` - Tempo de expiração em segundos
- `token_type: str` - Tipo do token (Bearer)

## Exemplo
```json
{
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "usuario@exemplo.com",
    "name": "João Silva",
    "avatar": "https://example.com/avatar.jpg",
    "created_at": "2024-01-15T10:30:00Z",
    "last_login": "2024-01-15T10:30:00Z",
    "is_active": true
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

#### LogoutRequest
```markdown
# LogoutRequest

## Campos
- `token: str` - Token JWT atual (obrigatório)

## Exemplo
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### LogoutResponse
```markdown
# LogoutResponse

## Campos
- `message: str` - Mensagem de confirmação
- `success: bool` - Status da operação

## Exemplo
```json
{
  "message": "Logout realizado com sucesso",
  "success": true
}
```

#### RefreshTokenRequest
```markdown
# RefreshTokenRequest

## Campos
- `refresh_token: str` - Token de refresh (obrigatório)

## Exemplo
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### RefreshTokenResponse
```markdown
# RefreshTokenResponse

## Campos
- `token: str` - Novo token JWT
- `refresh_token: str` - Novo token de refresh
- `expires_in: int` - Tempo de expiração em segundos

## Exemplo
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

#### User
```markdown
# User

## Campos
- `id: str` - ID único do usuário
- `email: str` - Email do usuário
- `name: str` - Nome do usuário
- `avatar: str` - URL do avatar (opcional)
- `created_at: str` - Data de criação
- `last_login: str` - Último login (opcional)
- `is_active: bool` - Status ativo

## Exemplo
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "usuario@exemplo.com",
  "name": "João Silva",
  "avatar": "https://example.com/avatar.jpg",
  "created_at": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-15T10:30:00Z",
  "is_active": true
}
```

#### RegisterRequest
```markdown
# RegisterRequest

## Campos
- `email: str` - Email do usuário (obrigatório)
- `password: str` - Senha do usuário (obrigatório)
- `name: str` - Nome do usuário (obrigatório)
- `confirm_password: str` - Confirmação de senha (obrigatório)

## Validações
- Email deve ser único
- Senha deve ter pelo menos 8 caracteres
- Senha e confirmação devem ser iguais
- Nome deve ter pelo menos 2 caracteres

## Exemplo
```json
{
  "email": "novo@exemplo.com",
  "password": "senha123456",
  "name": "Maria Santos",
  "confirm_password": "senha123456"
}
```

#### ForgotPasswordRequest
```markdown
# ForgotPasswordRequest

## Campos
- `email: str` - Email do usuário (obrigatório)

## Exemplo
```json
{
  "email": "usuario@exemplo.com"
}
```

#### ResetPasswordRequest
```markdown
# ResetPasswordRequest

## Campos
- `token: str` - Token de reset (obrigatório)
- `new_password: str` - Nova senha (obrigatório)
- `confirm_password: str` - Confirmação de senha (obrigatório)

## Exemplo
```json
{
  "token": "reset_token_123",
  "new_password": "nova_senha123",
  "confirm_password": "nova_senha123"
}
```

### Exemplos de Payloads

#### Login
```json
{
  "email": "usuario@exemplo.com",
  "password": "senha123456",
  "remember_me": true
}
```

#### Registro
```json
{
  "email": "novo@exemplo.com",
  "password": "senha123456",
  "name": "Maria Santos",
  "confirm_password": "senha123456"
}
```

#### Refresh Token
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Logout
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Forgot Password
```json
{
  "email": "usuario@exemplo.com"
}
```

#### Reset Password
```json
{
  "token": "reset_token_123",
  "new_password": "nova_senha123",
  "confirm_password": "nova_senha123"
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

# Authentication
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6

# Cache
redis>=5.0.0
aioredis>=2.0.0

# Email
fastapi-mail>=1.4.0
jinja2>=3.1.0

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
name = "web-002-auth"
version = "0.1.0"
description = "Sistema de autenticação simples para Concurso AI"
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
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.6",
    "redis>=5.0.0",
    "fastapi-mail>=1.4.0",
    "httpx>=0.25.0",
    "email-validator>=2.1.0",
    "cryptography>=41.0.0",
    "bcrypt>=4.1.0",
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
Homepage = "https://github.com/concurso-ai/web-002-auth"
Repository = "https://github.com/concurso-ai/web-002-auth.git"
Documentation = "https://docs.concurso-ai.com/web-002-auth"

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
# WEB-002 Auth System Makefile

.PHONY: help build test run clean install dev-install lint format type-check

# Default target
help:
	@echo "WEB-002 Auth System - Available targets:"
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
	@echo "Building WEB-002 Auth System..."
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
	@echo "Starting WEB-002 Auth System..."
	uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload

run-prod:
	@echo "Starting WEB-002 Auth System in production mode..."
	gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001

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
	docker build -t web-002-auth .
	@echo "Docker build completed!"

docker-run:
	@echo "Running Docker container..."
	docker run -p 8001:8001 web-002-auth

# Development targets
dev-setup: dev-install db-migrate
	@echo "Development setup completed!"

# Health check
health:
	@echo "Checking system health..."
	curl -f http://localhost:8001/api/v1/health || echo "Health check failed!"

# All quality checks
quality: lint format type-check test
	@echo "All quality checks completed!"
```

## Exemplos de Chamadas cURL

### Login
```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@exemplo.com",
    "password": "senha123456",
    "remember_me": true
  }'
```

### Registro
```bash
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "novo@exemplo.com",
    "password": "senha123456",
    "name": "Maria Santos",
    "confirm_password": "senha123456"
  }'
```

### Refresh Token
```bash
curl -X POST http://localhost:8001/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

### Logout
```bash
curl -X POST http://localhost:8001/api/v1/auth/logout \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

### Informações do Usuário
```bash
curl -X GET http://localhost:8001/api/v1/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Forgot Password
```bash
curl -X POST http://localhost:8001/api/v1/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@exemplo.com"
  }'
```

### Reset Password
```bash
curl -X POST http://localhost:8001/api/v1/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "token": "reset_token_123",
    "new_password": "nova_senha123",
    "confirm_password": "nova_senha123"
  }'
```

### Health Check
```bash
curl -X GET http://localhost:8001/api/v1/health
```

---

**Este documento define o scaffolding completo do backend WEB-002, incluindo estrutura, DTOs, requirements, Makefile e exemplos de uso.**
