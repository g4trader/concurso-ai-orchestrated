#!/bin/bash

# Script simples para deploy usando Vercel

set -e

echo "🚀 Fazendo deploy completo no Vercel..."

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

# 1. Deploy do Backend
log "🚀 Deploy do Backend..."
cd backend

# Gerar secret key
SECRET_KEY=$(openssl rand -hex 32)
log "Secret key gerado: $SECRET_KEY"

# Deploy backend
vercel --prod --env SECRET_KEY="$SECRET_KEY" --env ALGORITHM="HS256" --env ACCESS_TOKEN_EXPIRE_MINUTES="30" --env ENVIRONMENT="production"

BACKEND_URL=$(vercel ls | grep -o 'https://[^[:space:]]*' | head -1)
log "Backend deployado em: $BACKEND_URL"

cd ..

# 2. Deploy do Frontend
log "🚀 Deploy do Frontend..."
cd frontend

# Atualizar URL do backend
echo "NEXT_PUBLIC_API_URL=$BACKEND_URL" > .env.local

# Deploy frontend
vercel --prod

FRONTEND_URL=$(vercel ls | grep -o 'https://[^[:space:]]*' | head -1)
log "Frontend deployado em: $FRONTEND_URL"

cd ..

log "🎉 Deploy completo realizado com sucesso!"
echo ""
echo "📋 URLs do Deploy:"
echo "   Backend: $BACKEND_URL"
echo "   Frontend: $FRONTEND_URL"
echo "   API Docs: $BACKEND_URL/docs"
echo ""
echo "🔧 Próximos passos:"
echo "1. Teste o frontend: $FRONTEND_URL"
echo "2. Teste a API: $BACKEND_URL/health"
echo "3. Verifique a documentação: $BACKEND_URL/docs"
echo "4. Configure o banco de dados se necessário"
