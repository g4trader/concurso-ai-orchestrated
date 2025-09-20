#!/bin/bash

# Script para configurar o ambiente de desenvolvimento

set -e

echo "🚀 Configurando ambiente de desenvolvimento do Concurso AI..."

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    error "Docker não está instalado. Por favor, instale o Docker primeiro."
fi

if ! command -v docker-compose &> /dev/null; then
    error "Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
fi

# Verificar se Python está instalado (para desenvolvimento local)
if ! command -v python3 &> /dev/null; then
    warn "Python 3 não está instalado. Será necessário para desenvolvimento local."
fi

log "Configurando backend..."

# Criar arquivo .env se não existir
if [ ! -f backend/.env ]; then
    log "Criando arquivo .env para o backend..."
    cp backend/env.example backend/.env
    warn "Arquivo .env criado. Por favor, configure as variáveis de ambiente."
fi

# Instalar dependências do backend (se Python estiver disponível)
if command -v python3 &> /dev/null; then
    log "Instalando dependências do backend..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    log "Dependências do backend instaladas."
else
    warn "Python não encontrado. Dependências do backend serão instaladas via Docker."
fi

log "Configurando frontend..."

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    warn "Node.js não está instalado. Será necessário para desenvolvimento local do frontend."
else
    log "Instalando dependências do frontend..."
    cd frontend
    npm install
    cd ..
    log "Dependências do frontend instaladas."
fi

log "Iniciando serviços com Docker Compose..."

# Iniciar serviços
docker-compose up -d db

log "Aguardando banco de dados ficar pronto..."
sleep 10

# Inicializar banco de dados
if command -v python3 &> /dev/null; then
    log "Inicializando banco de dados..."
    cd backend
    source venv/bin/activate
    python init_db.py
    cd ..
    log "Banco de dados inicializado."
else
    warn "Python não encontrado. Execute 'python init_db.py' no diretório backend para inicializar o banco."
fi

log "✅ Ambiente configurado com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure as variáveis de ambiente em backend/.env"
echo "2. Execute 'docker-compose up' para iniciar todos os serviços"
echo "3. Acesse:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "🔧 Para desenvolvimento local:"
echo "1. Backend: cd backend && source venv/bin/activate && python run.py"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo "🎉 Pronto para desenvolver!"
