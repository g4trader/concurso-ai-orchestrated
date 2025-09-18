# Cebraspe Parser Makefile

.PHONY: help install test build clean run dev setup-ocr

help: ## Mostra esta ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências
	pip install -r requirements.txt

setup-ocr: ## Configura Tesseract OCR
	@echo "Configurando Tesseract OCR..."
	@echo "Verifique se Tesseract está instalado: tesseract --version"
	@echo "Para Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-por"
	@echo "Para macOS: brew install tesseract tesseract-lang"

test: ## Executa testes
	pytest tests/ -v --cov=src

build: ## Build do projeto (placeholder)
	@echo "Build placeholder - implementar lógica de build"

clean: ## Limpa arquivos temporários
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf temp_images/
	rm -rf temp_pdfs/

run: ## Executa o parser
	python src/main.py

dev: ## Modo desenvolvimento
	python src/main.py --debug --verbose

lint: ## Executa linters
	black src/ tests/
	flake8 src/ tests/
	mypy src/

process-sample: ## Processa arquivos de exemplo
	python src/main.py --input ./data/input --output ./data/output

benchmark: ## Executa benchmark de performance
	pytest tests/test_performance.py -v


