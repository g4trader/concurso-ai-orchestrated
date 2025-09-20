#!/bin/bash

# Script para deploy do backend no Google Cloud Run

echo "🚀 Iniciando deploy do backend no Google Cloud Run..."

# Verificar se gcloud CLI está instalado
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI não encontrado. Instalando..."
    echo "Por favor, instale o Google Cloud CLI: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Configurar variáveis
PROJECT_ID="automatizar-452311"
SERVICE_NAME="concurso-ai-backend"
REGION="us-central1"

echo "📦 Configurando projeto: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Navegar para o diretório do backend
cd backend

# Build e push da imagem Docker
echo "🐳 Fazendo build da imagem Docker..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy no Cloud Run
echo "🚀 Fazendo deploy no Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars ENVIRONMENT=production,SECRET_KEY=$(openssl rand -hex 32),FRONTEND_URL=https://concurso-ai-frontend.vercel.app

echo "✅ Deploy concluído!"
echo "🌐 URL do backend: https://$SERVICE_NAME-$PROJECT_ID-$REGION.a.run.app"
echo "📊 Console: https://console.cloud.google.com/run"
