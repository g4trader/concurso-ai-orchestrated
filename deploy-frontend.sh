#!/bin/bash

# Script para deploy do frontend no Vercel

set -e

echo "🚀 Fazendo deploy do frontend no Vercel..."

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

# Navegar para o diretório do frontend
cd frontend

# Verificar se Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    log "Instalando Vercel CLI..."
    npm install -g vercel
fi

# Verificar se está logado no Vercel
if ! vercel whoami &> /dev/null; then
    log "Fazendo login no Vercel..."
    vercel login
fi

# Verificar build local
log "Testando build local..."
npm run build

if [ $? -eq 0 ]; then
    log "✅ Build local bem-sucedido!"
else
    error "❌ Build local falhou. Corrija os erros antes do deploy."
fi

# Fazer deploy
log "Fazendo deploy no Vercel..."
vercel --prod

# Obter URL do deploy
FRONTEND_URL=$(vercel ls | grep -o 'https://[^[:space:]]*' | head -1)
log "Frontend deployado em: $FRONTEND_URL"

# Testar deploy
log "Testando deploy..."
sleep 10

if curl -f "$FRONTEND_URL" > /dev/null 2>&1; then
    log "✅ Deploy do frontend realizado com sucesso!"
    log "URL: $FRONTEND_URL"
else
    warn "Deploy realizado, mas teste de acesso falhou."
fi

# Voltar para o diretório raiz
cd ..

log "🎉 Deploy do frontend concluído!"
echo ""
echo "📋 Próximos passos:"
echo "1. Atualize a variável FRONTEND_URL no Railway com: $FRONTEND_URL"
echo "2. Teste a integração frontend + backend"
echo "3. Verifique se as APIs estão funcionando corretamente"