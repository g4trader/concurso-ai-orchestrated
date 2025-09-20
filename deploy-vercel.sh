#!/bin/bash

# Script para deploy do frontend no Vercel

echo "🚀 Iniciando deploy do frontend no Vercel..."

# Verificar se Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI não encontrado. Instalando..."
    npm install -g vercel
fi

# Navegar para o diretório do frontend
cd frontend

# Fazer login no Vercel (se necessário)
echo "🔐 Verificando login no Vercel..."
vercel whoami || vercel login

# Configurar variáveis de ambiente
echo "⚙️  Configurando variáveis de ambiente..."
vercel env add NEXT_PUBLIC_API_URL production
# Digite: https://concurso-ai-backend.railway.app

# Deploy
echo "🚀 Fazendo deploy..."
vercel --prod

echo "✅ Deploy concluído!"
echo "🌐 URL do frontend: https://concurso-ai-frontend.vercel.app"
echo "📊 Dashboard: https://vercel.com/dashboard"
