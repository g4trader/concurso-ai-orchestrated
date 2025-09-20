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
- `GET /api/v1/health` - Health check
- `GET /api/v1/metrics` - Métricas do sistema

## Funcionalidades
- Geração de simulados personalizados
- Seleção de banca e edital
- Configuração de dificuldade e tópicos
- Submissão e correção automática
- Relatórios de resultados
- Health checks e métricas

## Configuração
- Porta: 8000
- Logs: JSON estruturado
- Métricas: Prometheus
- Cache: Redis
- Database: PostgreSQL/SQLite
- Queue: Celery + Redis

## Deploy
O serviço está configurado para deploy no Google Cloud Run.

## Uso
```bash
# Local
uvicorn src.main:app --reload

# Docker
docker build -t web-003-simulado .
docker run -p 8000:8000 web-003-simulado
```
