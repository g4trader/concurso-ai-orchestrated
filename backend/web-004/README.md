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
- `GET /api/v1/health` - Health check
- `GET /api/v1/metrics` - Métricas do sistema

## Funcionalidades
- Análise detalhada de performance
- Identificação automática de pontos fracos
- Geração de recomendações personalizadas
- Exportação de relatórios em múltiplos formatos
- Dados para visualização em gráficos
- Sistema de rascunhos e compartilhamento
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
docker build -t web-004-results .
docker run -p 8000:8000 web-004-results
```
