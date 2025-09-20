#!/bin/bash

# Script para deploy do backend no Railway

echo "🚀 Iniciando deploy do backend no Railway..."

# Verificar se Railway CLI está instalado
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI não encontrado. Instalando..."
    npm install -g @railway/cli
fi

# Navegar para o diretório do backend
cd backend

# Fazer login no Railway (se necessário)
echo "🔐 Verificando login no Railway..."
railway whoami || railway login

# Criar novo projeto ou usar existente
echo "📦 Configurando projeto no Railway..."
railway link || railway init

# Configurar variáveis de ambiente
echo "⚙️  Configurando variáveis de ambiente..."
railway variables set ENVIRONMENT=production
railway variables set SECRET_KEY=$(openssl rand -hex 32)
railway variables set FRONTEND_URL=https://concurso-ai-frontend.vercel.app

# Deploy
echo "🚀 Fazendo deploy..."
railway up

echo "✅ Deploy concluído!"
echo "🌐 URL do backend: https://concurso-ai-backend.railway.app"
echo "📊 Dashboard: https://railway.app/dashboard"
