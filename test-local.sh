#!/bin/bash

# Script para testar a aplicação localmente
# Use enquanto espera o reset do limite da Vercel

set -e

echo "🧪 Testando aplicação localmente..."
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

# Verificar se estamos na pasta frontend
if [ ! -f "package.json" ]; then
    echo "Navegando para a pasta frontend..."
    cd frontend
fi

log "Verificando dependências..."
if [ ! -d "node_modules" ]; then
    log "Instalando dependências..."
    npm install
fi

log "Executando linting..."
npm run lint

log "Verificando tipos TypeScript..."
npm run type-check

log "Fazendo build de produção..."
npm run build

success "Build concluído com sucesso!"

log "Iniciando servidor de produção..."
echo ""
echo "🚀 Aplicação rodando em: http://localhost:3000"
echo "📱 Teste todas as funcionalidades:"
echo "   - Página inicial"
echo "   - Login"
echo "   - Dashboard"
echo "   - Gerador de simulado"
echo "   - Resultados"
echo ""
echo "⏰ Em 2 horas você poderá fazer o deploy na Vercel!"
echo ""

# Iniciar servidor
npm run start
