# 🚀 **GUIA COMPLETO DE DEPLOY NO GOOGLE CLOUD**

## 📋 **PRÉ-REQUISITOS**

### **1. Contas Necessárias:**
- ✅ **Google Cloud Platform** (para backend): https://cloud.google.com
- ✅ **Vercel** (para frontend): https://vercel.com
- ✅ **GitHub** (repositório): https://github.com

### **2. Ferramentas Necessárias:**
- ✅ **Google Cloud CLI**: https://cloud.google.com/sdk/docs/install
- ✅ **Vercel CLI**: `npm install -g vercel`
- ✅ **Docker** (para build local): https://docker.com
- ✅ **Git** (já instalado)

## 🎯 **ESTRATÉGIA DE DEPLOY CORRETA**

### **Backend → Google Cloud Run**
- **URL**: `https://concurso-ai-backend-<PROJECT_ID>-uc.a.run.app`
- **Banco**: Cloud SQL PostgreSQL
- **Configuração**: Docker + Cloud Run

### **Frontend → Vercel**
- **URL**: `https://concurso-ai-frontend.vercel.app`
- **Configuração**: Variáveis de ambiente
- **Integração**: Conectado com Cloud Run

## 🚀 **PASSO A PASSO - DEPLOY DO BACKEND**

### **1. Configurar Google Cloud**

```bash
# Instalar Google Cloud CLI
# https://cloud.google.com/sdk/docs/install

# Fazer login
gcloud auth login

# Criar projeto (ou usar existente)
gcloud projects create concurso-ai-project --name="Concurso AI"

# Configurar projeto
gcloud config set project concurso-ai-project

# Habilitar APIs necessárias
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable sqladmin.googleapis.com
```

### **2. Configurar Cloud SQL (PostgreSQL)**

```bash
# Criar instância Cloud SQL
gcloud sql instances create concurso-ai-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=concurso123

# Criar banco de dados
gcloud sql databases create concurso_ai \
  --instance=concurso-ai-db

# Criar usuário
gcloud sql users create concurso_user \
  --instance=concurso-ai-db \
  --password=concurso123
```

### **3. Deploy no Cloud Run**

```bash
# Opção 1: Usar script automatizado
./deploy-cloud-run.sh

# Opção 2: Deploy manual
cd backend

# Build e push da imagem
gcloud builds submit --tag gcr.io/concurso-ai-project/concurso-ai-backend

# Deploy no Cloud Run
gcloud run deploy concurso-ai-backend \
  --image gcr.io/concurso-ai-project/concurso-ai-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars ENVIRONMENT=production,SECRET_KEY=$(openssl rand -hex 32),FRONTEND_URL=https://concurso-ai-frontend.vercel.app
```

### **4. Configurar Conexão com Cloud SQL**

```bash
# Conectar Cloud Run com Cloud SQL
gcloud run services update concurso-ai-backend \
  --add-cloudsql-instances=concurso-ai-project:us-central1:concurso-ai-db \
  --region=us-central1

# Configurar variável de ambiente do banco
gcloud run services update concurso-ai-backend \
  --set-env-vars CLOUD_SQL_DATABASE_URL=postgresql://concurso_user:concurso123@/concurso_ai?host=/cloudsql/concurso-ai-project:us-central1:concurso-ai-db \
  --region=us-central1
```

### **5. Inicializar Banco de Dados**

```bash
# Executar init_db.py no Cloud Run
gcloud run services proxy concurso-ai-backend --port=8080 &
sleep 5
curl -X POST http://localhost:8080/init-db
kill %1
```

## 🌐 **PASSO A PASSO - DEPLOY DO FRONTEND**

### **1. Preparar Frontend para Produção**

```bash
# Navegar para o diretório do frontend
cd frontend

# Verificar se todas as dependências estão no package.json
npm install
```

### **2. Deploy no Vercel**

```bash
# Opção 1: Usar script automatizado
./deploy-vercel.sh

# Opção 2: Deploy manual
vercel login
vercel --prod
```

### **3. Configurar Variáveis de Ambiente**

```bash
# Configurar URL do backend (Cloud Run)
vercel env add NEXT_PUBLIC_API_URL production
# Digite: https://concurso-ai-backend-<PROJECT_ID>-uc.a.run.app
```

## 🔧 **CONFIGURAÇÕES DE PRODUÇÃO**

### **Backend (Google Cloud Run)**

**Variáveis de Ambiente:**
```env
ENVIRONMENT=production
SECRET_KEY=<gerado automaticamente>
FRONTEND_URL=https://concurso-ai-frontend.vercel.app
CLOUD_SQL_DATABASE_URL=postgresql://concurso_user:concurso123@/concurso_ai?host=/cloudsql/concurso-ai-project:us-central1:concurso-ai-db
```

**Arquivos de Configuração:**
- ✅ `Dockerfile` - Imagem Docker
- ✅ `.dockerignore` - Arquivos ignorados
- ✅ `requirements.txt` - Dependências Python

### **Frontend (Vercel)**

**Variáveis de Ambiente:**
```env
NEXT_PUBLIC_API_URL=https://concurso-ai-backend-<PROJECT_ID>-uc.a.run.app
NODE_ENV=production
```

**Arquivos de Configuração:**
- ✅ `vercel.json` - Configuração do Vercel
- ✅ `package.json` - Dependências Node.js

## 🧪 **TESTES PÓS-DEPLOY**

### **1. Testar Backend (Cloud Run)**

```bash
# Health check
curl https://concurso-ai-backend-<PROJECT_ID>-uc.a.run.app/health

# Testar login
curl -X POST "https://concurso-ai-backend-<PROJECT_ID>-uc.a.run.app/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=teste@concursoai.com&password=teste123"
```

### **2. Testar Frontend (Vercel)**

```bash
# Acessar frontend
open https://concurso-ai-frontend.vercel.app

# Testar login
# Email: teste@concursoai.com
# Senha: teste123
```

### **3. Testar Integração Completa**

1. **Login** no frontend
2. **Dashboard** carregando dados
3. **Criar simulado**
4. **Executar simulado**
5. **Ver resultados**

## 📊 **MONITORAMENTO**

### **Google Cloud Console**
- **URL**: https://console.cloud.google.com
- **Cloud Run**: https://console.cloud.google.com/run
- **Cloud SQL**: https://console.cloud.google.com/sql
- **Métricas**: CPU, RAM, Requests, Latency
- **Logs**: Cloud Logging

### **Vercel Dashboard**
- **URL**: https://vercel.com/dashboard
- **Métricas**: Performance, Analytics
- **Logs**: Function logs
- **Deployments**: Histórico

## 🔄 **ATUALIZAÇÕES**

### **Backend (Cloud Run)**
```bash
# Fazer mudanças no código
git add .
git commit -m "feat: nova funcionalidade"
git push

# Deploy automático via Cloud Build
gcloud builds submit --tag gcr.io/concurso-ai-project/concurso-ai-backend
gcloud run deploy concurso-ai-backend --image gcr.io/concurso-ai-project/concurso-ai-backend
```

### **Frontend (Vercel)**
```bash
# Fazer mudanças no código
git add .
git commit -m "feat: nova funcionalidade"
git push

# Deploy automático via Vercel
```

## 🚨 **TROUBLESHOOTING**

### **Problemas Comuns:**

**1. Backend não inicia:**
```bash
# Verificar logs
gcloud run services logs read concurso-ai-backend --region=us-central1

# Verificar variáveis
gcloud run services describe concurso-ai-backend --region=us-central1
```

**2. Frontend não conecta:**
```bash
# Verificar variáveis de ambiente
vercel env ls

# Verificar CORS no backend
```

**3. Banco não conecta:**
```bash
# Verificar Cloud SQL
gcloud sql instances describe concurso-ai-db

# Testar conexão
gcloud sql connect concurso-ai-db --user=concurso_user --database=concurso_ai
```

## 🎯 **URLS FINAIS**

### **Produção:**
- **Frontend**: https://concurso-ai-frontend.vercel.app
- **Backend**: https://concurso-ai-backend-<PROJECT_ID>-uc.a.run.app
- **API Docs**: https://concurso-ai-backend-<PROJECT_ID>-uc.a.run.app/docs

### **Desenvolvimento:**
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ✅ **CHECKLIST DE DEPLOY**

### **Google Cloud:**
- [ ] Google Cloud CLI instalado
- [ ] Projeto criado no GCP
- [ ] APIs habilitadas
- [ ] Cloud SQL configurado
- [ ] Cloud Run deployado
- [ ] Variáveis configuradas
- [ ] Conexão Cloud SQL configurada
- [ ] Health check funcionando

### **Frontend:**
- [ ] Vercel CLI instalado
- [ ] Projeto criado no Vercel
- [ ] Variáveis configuradas
- [ ] Deploy realizado
- [ ] Frontend acessível
- [ ] Login funcionando

### **Integração:**
- [ ] Frontend conectando com Cloud Run
- [ ] CORS configurado
- [ ] Autenticação funcionando
- [ ] Dashboard carregando
- [ ] Simulados funcionando
- [ ] Resultados funcionando

## 🎉 **SISTEMA 100% EM PRODUÇÃO NO GOOGLE CLOUD!**

Após seguir este guia, você terá:
- ✅ **Backend** rodando no Google Cloud Run
- ✅ **Frontend** rodando no Vercel
- ✅ **Banco Cloud SQL PostgreSQL** configurado
- ✅ **Sistema completo** funcionando
- ✅ **URLs de produção** ativas
- ✅ **Monitoramento** configurado

**O sistema estará 100% completo e em produção no Google Cloud!**
