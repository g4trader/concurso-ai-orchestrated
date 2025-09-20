# 🚀 **GUIA COMPLETO DE DEPLOY EM PRODUÇÃO**

## 📋 **PRÉ-REQUISITOS**

### **1. Contas Necessárias:**
- ✅ **Railway** (para backend): https://railway.app
- ✅ **Vercel** (para frontend): https://vercel.com
- ✅ **GitHub** (repositório): https://github.com

### **2. Ferramentas Necessárias:**
- ✅ **Railway CLI**: `npm install -g @railway/cli`
- ✅ **Vercel CLI**: `npm install -g vercel`
- ✅ **Git** (já instalado)

## 🎯 **ESTRATÉGIA DE DEPLOY**

### **Backend → Railway**
- **URL**: `https://concurso-ai-backend.railway.app`
- **Banco**: PostgreSQL (Railway)
- **Configuração**: Automática via Railway

### **Frontend → Vercel**
- **URL**: `https://concurso-ai-frontend.vercel.app`
- **Configuração**: Variáveis de ambiente
- **Integração**: Conectado com backend Railway

## 🚀 **PASSO A PASSO - DEPLOY DO BACKEND**

### **1. Preparar Backend para Produção**

```bash
# Navegar para o diretório do backend
cd backend

# Verificar se todas as dependências estão no requirements.txt
pip freeze > requirements.txt
```

### **2. Deploy no Railway**

```bash
# Opção 1: Usar script automatizado
./deploy-railway.sh

# Opção 2: Deploy manual
railway login
railway init
railway up
```

### **3. Configurar Banco PostgreSQL**

```bash
# Adicionar serviço PostgreSQL no Railway
railway add postgresql

# Configurar variáveis de ambiente
railway variables set ENVIRONMENT=production
railway variables set SECRET_KEY=$(openssl rand -hex 32)
railway variables set FRONTEND_URL=https://concurso-ai-frontend.vercel.app
```

### **4. Inicializar Banco de Dados**

```bash
# Conectar ao banco e executar init_db.py
railway run python init_db.py
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
# Configurar URL do backend
vercel env add NEXT_PUBLIC_API_URL production
# Digite: https://concurso-ai-backend.railway.app
```

## 🔧 **CONFIGURAÇÕES DE PRODUÇÃO**

### **Backend (Railway)**

**Variáveis de Ambiente:**
```env
ENVIRONMENT=production
SECRET_KEY=<gerado automaticamente>
FRONTEND_URL=https://concurso-ai-frontend.vercel.app
DATABASE_URL=<URL do PostgreSQL Railway>
```

**Arquivos de Configuração:**
- ✅ `railway.json` - Configuração do Railway
- ✅ `nixpacks.toml` - Configuração do build
- ✅ `requirements.txt` - Dependências Python

### **Frontend (Vercel)**

**Variáveis de Ambiente:**
```env
NEXT_PUBLIC_API_URL=https://concurso-ai-backend.railway.app
NODE_ENV=production
```

**Arquivos de Configuração:**
- ✅ `vercel.json` - Configuração do Vercel
- ✅ `package.json` - Dependências Node.js

## 🧪 **TESTES PÓS-DEPLOY**

### **1. Testar Backend**

```bash
# Health check
curl https://concurso-ai-backend.railway.app/health

# Testar login
curl -X POST "https://concurso-ai-backend.railway.app/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=teste@concursoai.com&password=teste123"
```

### **2. Testar Frontend**

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

### **Railway Dashboard**
- **URL**: https://railway.app/dashboard
- **Métricas**: CPU, RAM, Requests
- **Logs**: Em tempo real
- **Banco**: PostgreSQL metrics

### **Vercel Dashboard**
- **URL**: https://vercel.com/dashboard
- **Métricas**: Performance, Analytics
- **Logs**: Function logs
- **Deployments**: Histórico

## 🔄 **ATUALIZAÇÕES**

### **Backend (Railway)**
```bash
# Fazer mudanças no código
git add .
git commit -m "feat: nova funcionalidade"
git push

# Deploy automático via Railway
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
railway logs

# Verificar variáveis
railway variables
```

**2. Frontend não conecta:**
```bash
# Verificar variáveis de ambiente
vercel env ls

# Verificar CORS no backend
```

**3. Banco não conecta:**
```bash
# Verificar DATABASE_URL
railway variables

# Testar conexão
railway run python -c "from app.database import engine; print(engine.url)"
```

## 🎯 **URLs FINAIS**

### **Produção:**
- **Frontend**: https://concurso-ai-frontend.vercel.app
- **Backend**: https://concurso-ai-backend.railway.app
- **API Docs**: https://concurso-ai-backend.railway.app/docs

### **Desenvolvimento:**
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ✅ **CHECKLIST DE DEPLOY**

### **Backend:**
- [ ] Railway CLI instalado
- [ ] Projeto criado no Railway
- [ ] PostgreSQL adicionado
- [ ] Variáveis configuradas
- [ ] Deploy realizado
- [ ] Banco inicializado
- [ ] Health check funcionando

### **Frontend:**
- [ ] Vercel CLI instalado
- [ ] Projeto criado no Vercel
- [ ] Variáveis configuradas
- [ ] Deploy realizado
- [ ] Frontend acessível
- [ ] Login funcionando

### **Integração:**
- [ ] Frontend conectando com backend
- [ ] CORS configurado
- [ ] Autenticação funcionando
- [ ] Dashboard carregando
- [ ] Simulados funcionando
- [ ] Resultados funcionando

## 🎉 **SISTEMA 100% EM PRODUÇÃO!**

Após seguir este guia, você terá:
- ✅ **Backend** rodando em Railway
- ✅ **Frontend** rodando em Vercel
- ✅ **Banco PostgreSQL** configurado
- ✅ **Sistema completo** funcionando
- ✅ **URLs de produção** ativas
- ✅ **Monitoramento** configurado

**O sistema estará 100% completo e em produção!**
