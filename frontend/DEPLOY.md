# Deploy na Vercel - Concurso AI Frontend

Este guia explica como fazer o deploy da aplicação frontend na Vercel.

## 🚀 Deploy Automático via Git

### 1. Conectar Repositório
1. Acesse [vercel.com](https://vercel.com)
2. Faça login com sua conta GitHub
3. Clique em "New Project"
4. Selecione o repositório `concurso-ai-orchestrated`
5. Configure o projeto:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend/web-001`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 2. Configurar Variáveis de Ambiente
No painel da Vercel, vá em Settings > Environment Variables e adicione:

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

### 3. Deploy
1. Clique em "Deploy"
2. Aguarde o build completar
3. Acesse sua aplicação na URL fornecida

## 🛠️ Deploy Manual via CLI

### 1. Instalar Vercel CLI
```bash
npm i -g vercel
```

### 2. Login na Vercel
```bash
vercel login
```

### 3. Navegar para o Frontend
```bash
cd frontend/web-001
```

### 4. Deploy
```bash
# Deploy de produção
vercel --prod

# Deploy de preview
vercel
```

## ⚙️ Configurações Avançadas

### Domínio Customizado
1. No painel da Vercel, vá em Settings > Domains
2. Adicione seu domínio customizado
3. Configure os registros DNS conforme instruído

### Configurações de Build
O arquivo `vercel.json` já está configurado com:
- Build otimizado para Next.js
- Headers de segurança
- Compressão habilitada
- Runtime Node.js 18.x

### Monitoramento
- **Analytics**: Habilitado automaticamente na Vercel
- **Logs**: Disponíveis no painel da Vercel
- **Performance**: Métricas automáticas

## 🔧 Troubleshooting

### Build Falha
```bash
# Verificar logs
vercel logs

# Build local para testar
npm run build
```

### Variáveis de Ambiente
- Certifique-se que todas as variáveis `NEXT_PUBLIC_*` estão configuradas
- Variáveis sem `NEXT_PUBLIC_` não são expostas ao cliente

### Performance
- Use `npm run build` localmente para verificar otimizações
- Verifique o bundle analyzer: `npm run analyze`

## 📊 Monitoramento Pós-Deploy

### Métricas Importantes
- **Core Web Vitals**: LCP, FID, CLS
- **Performance Score**: Lighthouse
- **Uptime**: Disponibilidade da aplicação

### Alertas
Configure alertas para:
- Falhas de build
- Tempo de resposta alto
- Erros 5xx

## 🔄 CI/CD

### GitHub Actions (Opcional)
Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Vercel
on:
  push:
    branches: [main]
    paths: ['frontend/web-001/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: cd frontend/web-001 && npm ci
      - run: cd frontend/web-001 && npm run build
      - uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          working-directory: ./frontend/web-001
```

## 📝 Checklist de Deploy

- [ ] Repositório conectado à Vercel
- [ ] Root directory configurado como `frontend/web-001`
- [ ] Variáveis de ambiente configuradas
- [ ] Build local funcionando
- [ ] Domínio customizado (se necessário)
- [ ] Monitoramento configurado
- [ ] Testes de produção realizados

## 🆘 Suporte

- **Documentação Vercel**: [vercel.com/docs](https://vercel.com/docs)
- **Next.js na Vercel**: [nextjs.org/docs/deployment](https://nextjs.org/docs/deployment)
- **Logs de Deploy**: Painel da Vercel > Functions > View Function Logs
