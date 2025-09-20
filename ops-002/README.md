# OPS-002 Backend: Observabilidade Básica

## Visão Geral
Sistema de observabilidade com logs, métricas, health checks e alertas para monitoramento de aplicações.

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
- `POST /api/v1/logs` - Criar entrada de log
- `GET /api/v1/logs` - Consultar logs
- `POST /api/v1/logs/bulk` - Criar múltiplas entradas de log
- `POST /api/v1/metrics` - Criar métrica
- `GET /api/v1/metrics` - Consultar métricas
- `POST /api/v1/metrics/bulk` - Criar múltiplas métricas
- `GET /api/v1/services/{service_name}/health` - Health check de serviço
- `POST /api/v1/alerts` - Criar alerta
- `GET /api/v1/alerts` - Listar alertas
- `POST /api/v1/services` - Registrar serviço
- `GET /api/v1/services` - Listar serviços registrados
- `GET /api/v1/dashboard` - Obter dados do dashboard
- `GET /api/v1/health` - Health check
- `GET /api/v1/metrics` - Métricas do sistema

## Funcionalidades
- Sistema completo de logging estruturado
- Coleta e agregação de métricas
- Health checks para serviços
- Sistema de alertas e notificações
- Service discovery e registro
- Dashboard de observabilidade
- Processamento em lote
- Integração com Elasticsearch e Prometheus
- Correlação de traces e logs

## Configuração
- Porta: 8000
- Logs: JSON estruturado
- Métricas: Prometheus
- Cache: Redis
- Database: PostgreSQL/SQLite
- Queue: Celery + Redis
- Search: Elasticsearch

## Deploy
O serviço está configurado para deploy no Google Cloud Run.

## Uso
```bash
# Local
uvicorn src.main:app --reload

# Docker
docker build -t ops-002-observability .
docker run -p 8000:8000 ops-002-observability
```
