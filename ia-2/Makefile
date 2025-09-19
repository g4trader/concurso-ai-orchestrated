# IA-2 Geração Condicionada Makefile

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
	uvicorn src.main:app --host 0.0.0.0 --port 8002 --reload

run-prod: ## Executar em produção
	gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8002

lint: ## Executar linting
	black src/ tests/
	isort src/ tests/
	flake8 src/ tests/

clean: ## Limpar arquivos temporários
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/
	rm -rf data/ cache/ prompts/

docker-build: ## Construir imagem Docker
	docker build -t ia-2-generation .

docker-run: ## Executar container Docker
	docker run -p 8002:8002 ia-2-generation

docker-compose-up: ## Executar com docker-compose
	docker-compose up -d

docker-compose-down: ## Parar docker-compose
	docker-compose down

logs: ## Ver logs da aplicação
	docker-compose logs -f

health: ## Verificar saúde da aplicação
	curl http://localhost:8002/api/v1/health

metrics: ## Ver métricas da aplicação
	curl http://localhost:8002/api/v1/metrics

generate-question: ## Gerar questão de exemplo
	curl -X POST http://localhost:8002/api/v1/generate/question \
		-H "Content-Type: application/json" \
		-d '{
			"contexts": [{"chunk_id": "chunk_001", "text": "Os princípios fundamentais da Constituição Federal...", "metadata": {"banca": "CESPE", "ano": 2024}}],
			"edital_summary": {"banca": "CESPE", "ano": 2024, "cargo": "Analista Judiciário", "topico": "Direito Constitucional"},
			"topic": "Direito Constitucional"
		}'

validate-question: ## Validar questão de exemplo
	curl -X POST http://localhost:8002/api/v1/validate/question \
		-H "Content-Type: application/json" \
		-d '{
			"question": "Qual é o princípio fundamental da Constituição Federal?",
			"alternatives": {"A": "Princípio da legalidade", "B": "Princípio da separação dos poderes", "C": "Princípio da igualdade"},
			"correct_answer": "B",
			"justification": "O princípio da separação dos poderes está expressamente previsto no art. 2º da CF/88...",
			"source_chunks": ["chunk_001"]
		}'

setup-dirs: ## Criar diretórios necessários
	mkdir -p data/
	mkdir -p cache/
	mkdir -p prompts/system_prompts/
	mkdir -p prompts/task_prompts/
	mkdir -p prompts/templates/

download-models: ## Baixar modelos ML
	python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-m3')"
	python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-reranker-large')"

init: setup-dirs download-models ## Inicializar projeto completo
