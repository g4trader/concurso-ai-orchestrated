#!/bin/bash

# Script para deploy do backend no Railway

set -e

echo "🚀 Fazendo deploy do backend no Railway..."

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

# Verificar se Railway CLI está instalado
if ! command -v railway &> /dev/null; then
    log "Instalando Railway CLI..."
    npm install -g @railway/cli
fi

# Navegar para o diretório do backend
cd backend

# Fazer login no Railway (se necessário)
log "Verificando login no Railway..."
if ! railway whoami &> /dev/null; then
    log "Fazendo login no Railway..."
    railway login
fi

# Inicializar projeto Railway (se necessário)
if [ ! -f "railway.toml" ]; then
    log "Inicializando projeto Railway..."
    railway init
fi

# Configurar variáveis de ambiente
log "Configurando variáveis de ambiente..."

# Gerar secret key seguro
SECRET_KEY=$(openssl rand -hex 32)
railway variables SECRET_KEY="$SECRET_KEY"

# Configurar outras variáveis
railway variables ALGORITHM="HS256"
railway variables ACCESS_TOKEN_EXPIRE_MINUTES="30"
railway variables ENVIRONMENT="production"
railway variables HOST="0.0.0.0"
railway variables PORT="8000"

# Configurar CORS para o frontend
railway variables FRONTEND_URL="https://concurso-ai-orchestrated.vercel.app"

log "Variáveis de ambiente configuradas:"
railway variables

# Fazer deploy
log "Fazendo deploy..."
railway up

# Obter URL do deploy
BACKEND_URL=$(railway domain)
log "Backend deployado em: $BACKEND_URL"

# Testar deploy
log "Testando deploy..."
sleep 10

if curl -f "$BACKEND_URL/health" > /dev/null 2>&1; then
    log "✅ Deploy do backend realizado com sucesso!"
    log "URL: $BACKEND_URL"
    log "Health check: $BACKEND_URL/health"
    log "API Docs: $BACKEND_URL/docs"
else
    warn "Deploy realizado, mas health check falhou. Verifique os logs:"
    railway logs
fi

# Voltar para o diretório raiz
cd ..

log "🎉 Deploy do backend concluído!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure o banco de dados PostgreSQL no Railway"
echo "2. Execute 'railway run python init_db.py' para inicializar o banco"
echo "3. Atualize a variável FRONTEND_URL no Railway"
echo "4. Faça o deploy do frontend com a nova URL do backend"
