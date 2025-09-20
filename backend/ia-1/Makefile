# IA-1 Pipeline de Ingestão Makefile

.PHONY: help build test run clean install dev

help: ## Mostrar ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependências
	pip install -r requirements.txt

dev: ## Instalar dependências de desenvolvimento
	pip install -r requirements.txt
	pip install -e .

build: ## Construir aplicação
	python -m build

test: ## Executar testes
	pytest tests/ -v --cov=src --cov-report=html

run: ## Executar aplicação
	uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload

run-prod: ## Executar em produção
	gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001

lint: ## Executar linting
	black src/ tests/
	isort src/ tests/
	flake8 src/ tests/

clean: ## Limpar arquivos temporários
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/
	rm -rf data/ uploads/ backups/

docker-build: ## Construir imagem Docker
	docker build -t ia-1-pipeline .

docker-run: ## Executar container Docker
	docker run -p 8001:8001 ia-1-pipeline

docker-compose-up: ## Executar com docker-compose
	docker-compose up -d

docker-compose-down: ## Parar docker-compose
	docker-compose down

logs: ## Ver logs da aplicação
	docker-compose logs -f

health: ## Verificar saúde da aplicação
	curl http://localhost:8001/api/v1/health

index-status: ## Verificar status do índice
	curl http://localhost:8001/api/v1/index/status

metrics: ## Ver métricas da aplicação
	curl http://localhost:8001/api/v1/metrics

setup-dirs: ## Criar diretórios necessários
	mkdir -p data/faiss_index
	mkdir -p data/metadata
	mkdir -p uploads/
	mkdir -p backups/

download-models: ## Baixar modelos ML
	python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-m3')"
	python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-reranker-large')"

init: setup-dirs download-models ## Inicializar projeto completo
