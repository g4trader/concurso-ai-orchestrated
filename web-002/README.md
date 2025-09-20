# WEB-002 Backend: Autenticação Simples

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
- `GET /api/v1/health` - Health check
- `GET /api/v1/metrics` - Métricas do sistema

## Funcionalidades
- Autenticação com email/senha
- Geração e validação de tokens JWT
- Refresh tokens para renovação automática
- Registro de novos usuários
- Recuperação de senha
- Health checks e métricas

## Configuração
- Porta: 8000
- Logs: JSON estruturado
- Métricas: Prometheus
- Cache: Redis (opcional)
- Database: PostgreSQL/SQLite

## Deploy
O serviço está configurado para deploy no Google Cloud Run.

## Uso
```bash
# Local
uvicorn src.main:app --reload

# Docker
docker build -t web-002-auth .
docker run -p 8000:8000 web-002-auth
```
