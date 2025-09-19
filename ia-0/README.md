# IA-0 Ollama Service

Serviço de inferência com Ollama para geração de questões de concursos públicos.

## 🎯 Objetivo

Fornecer uma API REST para geração de questões de concursos usando modelos LLM locais via Ollama.

## 🚀 Como rodar

### Pré-requisitos
- Python 3.11+
- Ollama instalado e rodando
- Modelos LLM configurados (qwen2:7b, llama3.1:8b)

### Instalação
```bash
# Instalar dependências
make install

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env conforme necessário
```

### Execução
```bash
# Desenvolvimento
make run

# Produção
make run-prod

# Docker
make docker-build
make docker-run
```

## 📚 APIs Disponíveis

### Health Check
```bash
GET /api/v1/health
```

### Listar Modelos
```bash
GET /api/v1/models
```

### Gerar Questão
```bash
POST /api/v1/generate
{
  "prompt": "Gere uma questão sobre matemática",
  "model": "qwen2:7b",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

### Gerar em Lote
```bash
POST /api/v1/generate/batch
{
  "requests": [
    {"prompt": "Questão 1"},
    {"prompt": "Questão 2"}
  ]
}
```

## 🔧 Variáveis de Ambiente

- `OLLAMA_HOST`: URL do Ollama (padrão: http://localhost:11434)
- `OLLAMA_TIMEOUT`: Timeout para requisições (padrão: 30)
- `DEFAULT_MODEL`: Modelo padrão (padrão: qwen2:7b)
- `API_HOST`: Host da API (padrão: 0.0.0.0)
- `API_PORT`: Porta da API (padrão: 8000)
- `LOG_LEVEL`: Nível de log (padrão: INFO)

## 🧪 Testes

```bash
# Executar todos os testes
make test

# Executar com cobertura
pytest tests/ --cov=src --cov-report=html
```

## 📊 Observabilidade

- Logs estruturados em JSON
- Métricas de performance
- Health checks
- Monitoramento de modelos

## 🚀 Deploy

### Google Cloud Run
```bash
# Construir e fazer deploy
gcloud run deploy ia-0-ollama-service \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Vercel
```bash
# Deploy automático via vercel.json
vercel --prod
```

## ⚠️ Limitações Conhecidas

- Requer Ollama rodando localmente
- Modelos devem estar pré-carregados
- Timeout de 30s para requisições
- Máximo de 1000 tokens por geração
