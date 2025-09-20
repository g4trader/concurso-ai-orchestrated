# Concurso AI Orchestrated - Makefile
# Comandos para facilitar o desenvolvimento e deploy

.PHONY: help install build start stop clean test lint format deploy deploy-preview deploy-prod

# Variáveis
FRONTEND_DIR = frontend/web-001
BACKEND_DIRS = backend/ia-0 backend/ia-1 backend/ia-2 backend/ia-3 backend/ops-002 backend/ux-001 backend/web-002 backend/web-003 backend/web-004

# Ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  install     - Instala dependências de todos os serviços"
	@echo "  build       - Builda todos os serviços"
	@echo "  start       - Inicia todos os serviços com docker-compose"
	@echo "  stop        - Para todos os serviços"
	@echo "  clean       - Limpa containers e volumes"
	@echo "  test        - Executa testes de todos os serviços"
	@echo "  lint        - Executa linting em todos os serviços"
	@echo "  format      - Formata código de todos os serviços"
	@echo "  deploy      - Deploy do frontend para Vercel (preview)"
	@echo "  deploy-prod - Deploy do frontend para Vercel (produção)"
	@echo ""
	@echo "Comandos específicos:"
	@echo "  install-frontend - Instala dependências do frontend"
	@echo "  install-backend  - Instala dependências do backend"
	@echo "  start-frontend   - Inicia apenas o frontend"
	@echo "  start-backend    - Inicia apenas os serviços backend"

# Instalação
install: install-frontend install-backend

install-frontend:
	@echo "Instalando dependências do frontend..."
	cd $(FRONTEND_DIR) && npm install

install-backend:
	@echo "Instalando dependências do backend..."
	@for dir in $(BACKEND_DIRS); do \
		echo "Instalando dependências em $$dir..."; \
		cd $$dir && pip install -r requirements.txt && cd -; \
	done

# Build
build:
	@echo "Buildando todos os serviços..."
	docker-compose build

# Inicialização
start:
	@echo "Iniciando todos os serviços..."
	docker-compose up -d

start-frontend:
	@echo "Iniciando frontend..."
	cd $(FRONTEND_DIR) && npm run dev

start-backend:
	@echo "Iniciando serviços backend..."
	@for dir in $(BACKEND_DIRS); do \
		echo "Iniciando $$dir..."; \
		cd $$dir && python src/main.py &; \
	done

# Parada
stop:
	@echo "Parando todos os serviços..."
	docker-compose down

# Limpeza
clean:
	@echo "Limpando containers e volumes..."
	docker-compose down -v --remove-orphans
	docker system prune -f

# Testes
test: test-frontend test-backend

test-frontend:
	@echo "Executando testes do frontend..."
	cd $(FRONTEND_DIR) && npm test

test-backend:
	@echo "Executando testes do backend..."
	@for dir in $(BACKEND_DIRS); do \
		echo "Executando testes em $$dir..."; \
		cd $$dir && python -m pytest && cd -; \
	done

# Linting
lint: lint-frontend lint-backend

lint-frontend:
	@echo "Executando linting do frontend..."
	cd $(FRONTEND_DIR) && npm run lint

lint-backend:
	@echo "Executando linting do backend..."
	@for dir in $(BACKEND_DIRS); do \
		echo "Executando linting em $$dir..."; \
		cd $$dir && flake8 src/ && cd -; \
	done

# Formatação
format: format-frontend format-backend

format-frontend:
	@echo "Formatando código do frontend..."
	cd $(FRONTEND_DIR) && npm run format

format-backend:
	@echo "Formatando código do backend..."
	@for dir in $(BACKEND_DIRS); do \
		echo "Formatando código em $$dir..."; \
		cd $$dir && black src/ && isort src/ && cd -; \
	done

# Desenvolvimento
dev: install
	@echo "Iniciando ambiente de desenvolvimento..."
	@echo "Frontend: http://localhost:3000"
	@echo "Backend services:"
	@echo "  - IA-0: http://localhost:8000"
	@echo "  - IA-1: http://localhost:8001"
	@echo "  - IA-2: http://localhost:8002"
	@echo "  - IA-3: http://localhost:8003"
	@echo "  - OPS-002: http://localhost:8004"
	@echo "  - UX-001: http://localhost:8005"
	@echo "  - WEB-002: http://localhost:8006"
	@echo "  - WEB-003: http://localhost:8007"
	@echo "  - WEB-004: http://localhost:8008"
	make start

# Deploy
deploy:
	@echo "Fazendo deploy do frontend para Vercel (preview)..."
	./deploy-frontend.sh

deploy-prod:
	@echo "Fazendo deploy do frontend para Vercel (produção)..."
	./deploy-frontend.sh --prod

deploy-preview:
	@echo "Fazendo deploy de preview do frontend..."
	cd $(FRONTEND_DIR) && vercel

# Verificação pré-deploy
pre-deploy:
	@echo "Verificando se está tudo pronto para deploy..."
	cd $(FRONTEND_DIR) && npm run lint
	cd $(FRONTEND_DIR) && npm run type-check
	cd $(FRONTEND_DIR) && npm run build
	@echo "✅ Tudo pronto para deploy!"
