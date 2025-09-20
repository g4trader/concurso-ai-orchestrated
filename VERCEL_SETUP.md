# 🚀 Configuração para Deploy na Vercel

Este documento contém todas as informações necessárias para configurar o deploy do frontend na Vercel.

## 📋 Checklist de Configuração

### ✅ Arquivos Criados/Configurados

- [x] `frontend/web-001/vercel.json` - Configuração específica do frontend
- [x] `frontend/web-001/next.config.js` - Configurações otimizadas para produção
- [x] `frontend/web-001/package.json` - Scripts de deploy adicionados
- [x] `frontend/web-001/DEPLOY.md` - Instruções detalhadas de deploy
- [x] `frontend/web-001/vercel-env.example` - Exemplo de variáveis de ambiente
- [x] `deploy-frontend.sh` - Script automatizado de deploy
- [x] `vercel-frontend.json` - Configuração alternativa para Vercel
- [x] `Makefile` - Comandos de deploy adicionados

## 🎯 Passos para Deploy

### 1. Via Interface Web da Vercel (Recomendado)

1. **Acesse [vercel.com](https://vercel.com)**
2. **Faça login com GitHub**
3. **Clique em "New Project"**
4. **Configure o projeto:**
   - **Repository**: `concurso-ai-orchestrated`
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `frontend/web-001`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 2. Via CLI da Vercel

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login na Vercel
vercel login

# Deploy (na raiz do projeto)
make deploy          # Preview
make deploy-prod     # Produção
```

### 3. Via Script Automatizado

```bash
# Deploy de preview
./deploy-frontend.sh

# Deploy de produção
./deploy-frontend.sh --prod
```

## ⚙️ Configurações Importantes

### Variáveis de Ambiente na Vercel

Configure estas variáveis no painel da Vercel:

```bash
# Produção
NEXT_PUBLIC_API_URL=https://your-backend-api.com
NEXT_PUBLIC_APP_NAME=Concurso AI
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_DEBUG=false

# Desenvolvimento
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Concurso AI (Dev)
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_DEBUG=true
```

### Configurações de Build

O projeto está configurado com:
- **Output**: `standalone` (otimizado para Vercel)
- **Compressão**: Habilitada
- **Headers de Segurança**: Configurados
- **Otimizações de Imagem**: WebP e AVIF
- **Runtime**: Node.js 18.x

## 🔧 Comandos Disponíveis

```bash
# Desenvolvimento
make dev                    # Inicia ambiente de desenvolvimento
make pre-deploy            # Verifica se está pronto para deploy

# Deploy
make deploy                # Deploy de preview
make deploy-prod           # Deploy de produção
make deploy-preview        # Deploy rápido via CLI

# Frontend específico
cd frontend/web-001
npm run deploy             # Deploy de produção
npm run deploy:preview     # Deploy de preview
npm run analyze            # Análise do bundle
```

## 📊 Monitoramento

Após o deploy, você terá acesso a:

- **Analytics**: Métricas automáticas da Vercel
- **Performance**: Core Web Vitals
- **Logs**: Logs de função e build
- **Domínios**: Gerenciamento de domínios customizados

## 🆘 Troubleshooting

### Build Falha
```bash
# Verificar localmente
cd frontend/web-001
npm run build

# Ver logs na Vercel
vercel logs
```

### Variáveis de Ambiente
- Certifique-se que todas as variáveis `NEXT_PUBLIC_*` estão configuradas
- Variáveis sem `NEXT_PUBLIC_` não são expostas ao cliente

### Performance
- Use `npm run analyze` para verificar o tamanho do bundle
- Verifique as métricas no painel da Vercel

## 🔗 Links Úteis

- **Dashboard Vercel**: https://vercel.com/dashboard
- **Documentação Vercel**: https://vercel.com/docs
- **Next.js na Vercel**: https://nextjs.org/docs/deployment#vercel

## 📝 Próximos Passos

1. **Configure as variáveis de ambiente** no painel da Vercel
2. **Faça o primeiro deploy** usando `make deploy`
3. **Configure domínio customizado** (se necessário)
4. **Configure monitoramento** e alertas
5. **Teste a aplicação** em produção

---

**🎉 Seu frontend está pronto para deploy na Vercel!**
