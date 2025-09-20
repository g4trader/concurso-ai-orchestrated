#!/bin/bash

# Script de Deploy do Frontend para Vercel
# Concurso AI Orchestrated

set -e

echo "🚀 Iniciando deploy do frontend para Vercel..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verificar se estamos na raiz do projeto
if [ ! -d "frontend/web-001" ]; then
    error "Execute este script na raiz do projeto (onde está a pasta frontend/)"
fi

# Navegar para o frontend
cd frontend/web-001

log "Verificando dependências..."
if [ ! -d "node_modules" ]; then
    log "Instalando dependências..."
    npm install
fi

log "Executando linting..."
npm run lint

log "Executando testes..."
npm test

log "Verificando tipos TypeScript..."
npm run type-check

log "Fazendo build de produção..."
npm run build

log "Verificando se Vercel CLI está instalado..."
if ! command -v vercel &> /dev/null; then
    warning "Vercel CLI não encontrado. Instalando..."
    npm install -g vercel
fi

log "Fazendo login na Vercel (se necessário)..."
vercel whoami || vercel login

log "Fazendo deploy para Vercel..."
if [ "$1" = "--prod" ]; then
    log "Deploy de PRODUÇÃO"
    vercel --prod
else
    log "Deploy de PREVIEW"
    vercel
fi

success "Deploy concluído com sucesso! 🎉"

# Voltar para a raiz
cd ../..

log "Para verificar o status do deploy:"
echo "  - Acesse: https://vercel.com/dashboard"
echo "  - Ou execute: vercel ls"
