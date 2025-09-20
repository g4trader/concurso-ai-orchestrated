# Cebraspe Crawler Makefile

.PHONY: help install test build clean run dev

help: ## Mostra esta ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências
	pip install -r requirements.txt

test: ## Executa testes
	pytest tests/ -v --cov=src

build: ## Build do projeto (placeholder)
	@echo "Build placeholder - implementar lógica de build"

clean: ## Limpa arquivos temporários
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/

run: ## Executa o crawler
	python src/main.py

dev: ## Modo desenvolvimento
	python src/main.py --debug

lint: ## Executa linters
	black src/ tests/
	flake8 src/ tests/
	mypy src/


