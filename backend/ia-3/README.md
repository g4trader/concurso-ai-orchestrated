# IA-3 Backend: Avaliação Offline

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
- `GET /api/v1/health` - Health check
- `GET /api/v1/metrics` - Métricas do sistema

## Métricas de Avaliação
- **Topic Hit Rate** - Taxa de acerto de tópicos
- **Style Match** - Consistência de estilo
- **Answerability** - Capacidade de resposta

## Configuração
- Porta: 8000
- Logs: JSON estruturado
- Métricas: Prometheus
- Cache: Opcional

## Deploy
O serviço está configurado para deploy no Google Cloud Run.

## Uso
```bash
# Local
uvicorn src.main:app --reload

# Docker
docker build -t ia-3-evaluation .
docker run -p 8000:8000 ia-3-evaluation
```
