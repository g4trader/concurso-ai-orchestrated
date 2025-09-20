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
- `GET /api/v1/health` - Health check
- `GET /api/v1/metrics` - Métricas do sistema

## Funcionalidades
- Sistema completo de feedback de questões
- Categorização automática de feedback
- Sistema de rascunhos para usuários
- Analytics e relatórios de feedback
- Processamento em lote
- Sistema de prioridades e status
- Integração com Elasticsearch para busca
- Notificações e alertas

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
docker build -t ux-001-feedback .
docker run -p 8000:8000 ux-001-feedback
```
