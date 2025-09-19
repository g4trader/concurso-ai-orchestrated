# README_OPS-001: Deploy Mínimo (Vercel/Cloud Run) - Guia de Deploy

## 1. Objetivo/Contexto

### **Objetivo**
Disponibilizar o MVP do Concurso-AI Orchestrated para testadores internos através de um sistema de deploy mínimo e confiável, utilizando Vercel para frontend e Google Cloud Run para backend.

### **Contexto do Projeto**
- **Projeto**: Concurso-AI Orchestrated
- **Sprint**: 4 - Frontend & Go-to-Market (MVP)
- **História**: OPS-001 - Deploy mínimo (Vercel/Cloud Run)
- **Usuário**: Equipe e beta testers
- **Valor**: Feedback real de uso

### **Problema Resolvido**
Permitir que a equipe e beta testers acessem o MVP de forma confiável e escalável, com deploy automatizado, monitoramento básico e capacidade de rollback rápido.

### **Arquitetura do Sistema**
```
Desenvolvimento → Git Push → CI/CD Pipeline → Deploy Automático → Produção
     ↓              ↓              ↓              ↓              ↓
   Local Dev    GitHub Repo    Cloud Build    Vercel/Cloud Run   Monitoring
```

### **Funcionalidades Principais**
- **Deploy automático** via Git push
- **Frontend na Vercel** com CDN global
- **Backend no Cloud Run** com auto-scaling
- **Domínios customizados** com SSL automático
- **Monitoramento básico** com logs e métricas
- **Rollback automático** em caso de falha
- **Health checks** para verificação de saúde
- **Preview deployments** para feature branches

## 2. Como Rodar (Conceitual)

### **Pré-requisitos**
- Conta Vercel (gratuita)
- Conta Google Cloud Platform
- Repositório Git (GitHub/GitLab)
- Domínio customizado (opcional)
- Node.js 18+ (para desenvolvimento local)

### **Instalação**

#### **2.1 Configuração Vercel (Frontend)**
```bash
# 1. Instalar Vercel CLI
npm install -g vercel

# 2. Fazer login na Vercel
vercel login

# 3. Conectar projeto ao repositório
vercel link

# 4. Configurar variáveis de ambiente
vercel env add NEXT_PUBLIC_API_URL
vercel env add NEXT_PUBLIC_APP_NAME
vercel env add NEXT_PUBLIC_ENVIRONMENT

# 5. Deploy inicial
vercel --prod
```

#### **2.2 Configuração Google Cloud Run (Backend)**
```bash
# 1. Instalar Google Cloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# 2. Fazer login no GCP
gcloud auth login

# 3. Configurar projeto
gcloud config set project CONCURSO_AI_PROJECT_ID

# 4. Habilitar APIs necessárias
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com

# 5. Configurar secrets
gcloud secrets create database-url --data-file=database-url.txt
gcloud secrets create jwt-secret --data-file=jwt-secret.txt

# 6. Deploy inicial
gcloud run deploy concurso-ai-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### **2.3 Configuração de Domínio (Opcional)**
```bash
# 1. Configurar DNS
# Adicionar registros CNAME no seu provedor DNS:
# www -> cname.vercel-dns.com
# api -> ghs.googlehosted.com

# 2. Configurar domínio na Vercel
vercel domains add concurso-ai.com

# 3. Configurar domínio no Cloud Run
gcloud run domain-mappings create \
  --service concurso-ai-backend \
  --domain api.concurso-ai.com \
  --region us-central1
```

### **Execução**

#### **2.4 Deploy Automático**
```bash
# Deploy automático via Git push
git add .
git commit -m "feat: nova funcionalidade"
git push origin main

# O deploy será executado automaticamente:
# 1. Vercel detecta push
# 2. Build do frontend
# 3. Deploy para produção
# 4. Cloud Build detecta push
# 5. Build da imagem Docker
# 6. Deploy para Cloud Run
```

#### **2.5 Deploy Manual**
```bash
# Deploy manual do frontend
vercel --prod

# Deploy manual do backend
gcloud run deploy concurso-ai-backend \
  --source . \
  --platform managed \
  --region us-central1

# Deploy para staging
vercel --target staging
gcloud run deploy concurso-ai-backend-staging \
  --source . \
  --platform managed \
  --region us-central1
```

#### **2.6 Verificação de Deploy**
```bash
# Verificar status do frontend
vercel ls
vercel inspect [deployment-url]

# Verificar status do backend
gcloud run services list
gcloud run services describe concurso-ai-backend \
  --region us-central1

# Testar endpoints
curl https://concurso-ai.com
curl https://api.concurso-ai.com/health
```

### **Verificação**
```bash
# Verificar se o frontend está funcionando
curl -I https://concurso-ai.com
# Deve retornar: HTTP/2 200

# Verificar se o backend está funcionando
curl https://api.concurso-ai.com/health
# Deve retornar: {"status": "healthy", "timestamp": "..."}

# Verificar SSL
openssl s_client -connect concurso-ai.com:443 -servername concurso-ai.com
# Deve mostrar certificado válido

# Verificar performance
curl -w "@curl-format.txt" -o /dev/null -s https://concurso-ai.com
# Deve mostrar tempo de resposta < 2 segundos
```

### **Estrutura de Desenvolvimento**
```bash
# Estrutura de pastas
concurso-ai-orchestrated/
├── .github/workflows/     # CI/CD workflows
├── .vercel/              # Configuração Vercel
├── .gcloud/              # Configuração GCP
├── docs/deployment/      # Documentação de deploy
├── scripts/deploy/       # Scripts de deploy
├── config/environments/  # Variáveis de ambiente
├── monitoring/           # Configuração de monitoramento
└── tests/deployment/     # Testes de deploy

# Comandos úteis
npm run deploy:frontend   # Deploy frontend
npm run deploy:backend    # Deploy backend
npm run deploy:all        # Deploy completo
npm run health:check      # Verificar saúde
npm run rollback          # Rollback
```

## 3. APIs/Contratos (se houver)

### **APIs de Deploy**

#### **Vercel API**
```typescript
// Deploy via Vercel API
interface VercelDeployRequest {
  name: string;
  gitSource?: {
    type: 'github' | 'gitlab' | 'bitbucket';
    repo: string;
    ref: string;
  };
  target?: 'production' | 'preview' | 'development';
  env?: Record<string, string>;
  buildCommand?: string;
  outputDirectory?: string;
  installCommand?: string;
  framework?: string;
}

interface VercelDeployResponse {
  id: string;
  name: string;
  url: string;
  status: 'queued' | 'building' | 'ready' | 'error';
  createdAt: string;
  updatedAt: string;
  creator: {
    uid: string;
    email: string;
  };
  target: string;
  alias: string[];
  aliasAssigned: boolean;
  aliasError?: {
    code: string;
    message: string;
  };
}
```

#### **Google Cloud Run API**
```typescript
// Deploy via Cloud Run API
interface CloudRunDeployRequest {
  apiVersion: 'serving.knative.dev/v1';
  kind: 'Service';
  metadata: {
    name: string;
    namespace: string;
    labels?: Record<string, string>;
    annotations?: Record<string, string>;
  };
  spec: {
    template: {
      metadata: {
        annotations?: Record<string, string>;
      };
      spec: {
        containerConcurrency?: number;
        timeoutSeconds?: number;
        containers: Array<{
          image: string;
          ports?: Array<{
            containerPort: number;
            name?: string;
          }>;
          env?: Array<{
            name: string;
            value?: string;
            valueFrom?: {
              secretKeyRef?: {
                name: string;
                key: string;
              };
            };
          }>;
          resources?: {
            limits?: {
              cpu: string;
              memory: string;
            };
            requests?: {
              cpu: string;
              memory: string;
            };
          };
          livenessProbe?: {
            httpGet: {
              path: string;
              port: number;
            };
            initialDelaySeconds?: number;
            periodSeconds?: number;
          };
          readinessProbe?: {
            httpGet: {
              path: string;
              port: number;
            };
            initialDelaySeconds?: number;
            periodSeconds?: number;
          };
        }>;
      };
    };
  };
}

interface CloudRunDeployResponse {
  apiVersion: 'serving.knative.dev/v1';
  kind: 'Service';
  metadata: {
    name: string;
    namespace: string;
    selfLink: string;
    uid: string;
    resourceVersion: string;
    generation: number;
    creationTimestamp: string;
    labels?: Record<string, string>;
    annotations?: Record<string, string>;
  };
  spec: {
    template: {
      metadata: {
        name: string;
        annotations?: Record<string, string>;
      };
      spec: {
        containerConcurrency: number;
        timeoutSeconds: number;
        containers: Array<{
          image: string;
          ports: Array<{
            containerPort: number;
            name: string;
          }>;
          env: Array<{
            name: string;
            value: string;
          }>;
          resources: {
            limits: {
              cpu: string;
              memory: string;
            };
            requests: {
              cpu: string;
              memory: string;
            };
          };
        }>;
      };
    };
  };
  status: {
    observedGeneration: number;
    conditions: Array<{
      type: string;
      status: string;
      lastTransitionTime: string;
      reason?: string;
      message?: string;
    }>;
    url: string;
    traffic: Array<{
      revisionName: string;
      percent: number;
      latestRevision: boolean;
    }>;
  };
}
```

#### **Health Check API**
```typescript
// Health check endpoints
interface HealthCheckResponse {
  status: 'healthy' | 'unhealthy';
  timestamp: string;
  version: string;
  environment: string;
  services: {
    database: {
      status: 'healthy' | 'unhealthy';
      responseTime: number;
    };
    cache: {
      status: 'healthy' | 'unhealthy';
      responseTime: number;
    };
    external: {
      status: 'healthy' | 'unhealthy';
      responseTime: number;
    };
  };
  metrics: {
    uptime: number;
    memory: {
      used: number;
      total: number;
    };
    cpu: {
      usage: number;
    };
  };
}
```

#### **Deploy Status API**
```typescript
// Deploy status endpoints
interface DeployStatusResponse {
  id: string;
  status: 'pending' | 'building' | 'deploying' | 'ready' | 'error' | 'cancelled';
  progress: number;
  message: string;
  logs: Array<{
    timestamp: string;
    level: 'info' | 'warn' | 'error';
    message: string;
  }>;
  metrics: {
    buildTime: number;
    deployTime: number;
    totalTime: number;
  };
  rollback?: {
    available: boolean;
    previousVersion: string;
  };
}
```

### **Exemplos de Uso das APIs**

#### **Deploy Frontend via Vercel API**
```javascript
// Exemplo de deploy via Vercel API
const deployFrontend = async (deployData) => {
  const response = await fetch('https://api.vercel.com/v13/deployments', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${VERCEL_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: 'concurso-ai-frontend',
      gitSource: {
        type: 'github',
        repo: 'g4trader/concurso-ai-orchestrated',
        ref: 'main'
      },
      target: 'production',
      env: {
        NEXT_PUBLIC_API_URL: 'https://api.concurso-ai.com',
        NEXT_PUBLIC_APP_NAME: 'Concurso AI',
        NEXT_PUBLIC_ENVIRONMENT: 'production'
      },
      buildCommand: 'npm run build',
      outputDirectory: '.next',
      installCommand: 'npm install',
      framework: 'nextjs'
    }),
  });
  
  if (!response.ok) {
    throw new Error('Falha no deploy do frontend');
  }
  
  return response.json();
};
```

#### **Deploy Backend via Cloud Run API**
```javascript
// Exemplo de deploy via Cloud Run API
const deployBackend = async (deployData) => {
  const response = await fetch('https://run.googleapis.com/v1/projects/CONCURSO_AI_PROJECT_ID/locations/us-central1/services', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${GCP_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      apiVersion: 'serving.knative.dev/v1',
      kind: 'Service',
      metadata: {
        name: 'concurso-ai-backend',
        namespace: 'default',
        labels: {
          app: 'concurso-ai',
          component: 'backend'
        }
      },
      spec: {
        template: {
          metadata: {
            annotations: {
              'autoscaling.knative.dev/maxScale': '10',
              'autoscaling.knative.dev/minScale': '1',
              'run.googleapis.com/cpu-throttling': 'false'
            }
          },
          spec: {
            containerConcurrency: 100,
            timeoutSeconds: 300,
            containers: [{
              image: 'gcr.io/concurso-ai/backend:latest',
              ports: [{
                containerPort: 8000,
                name: 'http1'
              }],
              env: [
                {
                  name: 'ENVIRONMENT',
                  value: 'production'
                },
                {
                  name: 'DATABASE_URL',
                  valueFrom: {
                    secretKeyRef: {
                      name: 'database-secret',
                      key: 'url'
                    }
                  }
                }
              ],
              resources: {
                limits: {
                  cpu: '2',
                  memory: '2Gi'
                },
                requests: {
                  cpu: '1',
                  memory: '1Gi'
                }
              },
              livenessProbe: {
                httpGet: {
                  path: '/health',
                  port: 8000
                },
                initialDelaySeconds: 30,
                periodSeconds: 10
              },
              readinessProbe: {
                httpGet: {
                  path: '/ready',
                  port: 8000
                },
                initialDelaySeconds: 5,
                periodSeconds: 5
              }
            }]
          }
        }
      }
    }),
  });
  
  if (!response.ok) {
    throw new Error('Falha no deploy do backend');
  }
  
  return response.json();
};
```

#### **Verificar Status de Deploy**
```javascript
// Exemplo de verificação de status
const checkDeployStatus = async (deployId) => {
  const response = await fetch(`https://api.vercel.com/v13/deployments/${deployId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${VERCEL_TOKEN}`,
    },
  });
  
  if (!response.ok) {
    throw new Error('Falha ao verificar status do deploy');
  }
  
  return response.json();
};
```

#### **Health Check**
```javascript
// Exemplo de health check
const healthCheck = async () => {
  const response = await fetch('https://api.concurso-ai.com/health', {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('Health check falhou');
  }
  
  return response.json();
};
```

## 4. Variáveis de Ambiente

### **Configuração Frontend (Vercel)**
```bash
# .env.production
NEXT_PUBLIC_API_URL=https://api.concurso-ai.com
NEXT_PUBLIC_APP_NAME=Concurso AI
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_VERCEL_URL=https://concurso-ai.com
NEXT_PUBLIC_ANALYTICS_ID=GA_MEASUREMENT_ID
NEXT_PUBLIC_SENTRY_DSN=SENTRY_DSN
```

### **Configuração Backend (Cloud Run)**
```bash
# .env.production
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host:port/db
JWT_SECRET=jwt-secret-key
CORS_ORIGINS=https://concurso-ai.com,https://www.concurso-ai.com
LOG_LEVEL=info
SENTRY_DSN=SENTRY_DSN
GOOGLE_CLOUD_PROJECT=concurso-ai-project
GOOGLE_CLOUD_REGION=us-central1
```

### **Configuração de Desenvolvimento**
```bash
# .env.development
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Concurso AI (Dev)
NEXT_PUBLIC_ENVIRONMENT=development
ENVIRONMENT=development
DATABASE_URL=postgresql://localhost:5432/concurso_ai_dev
JWT_SECRET=dev-jwt-secret
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=debug
```

### **Configuração de Staging**
```bash
# .env.staging
NEXT_PUBLIC_API_URL=https://api-staging.concurso-ai.com
NEXT_PUBLIC_APP_NAME=Concurso AI (Staging)
NEXT_PUBLIC_ENVIRONMENT=staging
ENVIRONMENT=staging
DATABASE_URL=postgresql://staging-user:pass@staging-host:port/staging-db
JWT_SECRET=staging-jwt-secret
CORS_ORIGINS=https://staging.concurso-ai.com
LOG_LEVEL=info
```

### **Configuração de Beta**
```bash
# .env.beta
NEXT_PUBLIC_API_URL=https://api-beta.concurso-ai.com
NEXT_PUBLIC_APP_NAME=Concurso AI (Beta)
NEXT_PUBLIC_ENVIRONMENT=beta
ENVIRONMENT=beta
DATABASE_URL=postgresql://beta-user:pass@beta-host:port/beta-db
JWT_SECRET=beta-jwt-secret
CORS_ORIGINS=https://beta.concurso-ai.com
LOG_LEVEL=info
```

### **Secrets do Google Cloud**
```bash
# Configurar secrets no Google Cloud Secret Manager
gcloud secrets create database-url --data-file=database-url.txt
gcloud secrets create jwt-secret --data-file=jwt-secret.txt
gcloud secrets create sentry-dsn --data-file=sentry-dsn.txt
gcloud secrets create analytics-id --data-file=analytics-id.txt

# Atualizar secrets
gcloud secrets versions add database-url --data-file=database-url.txt
gcloud secrets versions add jwt-secret --data-file=jwt-secret.txt
gcloud secrets versions add sentry-dsn --data-file=sentry-dsn.txt
gcloud secrets versions add analytics-id --data-file=analytics-id.txt
```

### **Configuração de Build**
```bash
# next.config.js
module.exports = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME,
    NEXT_PUBLIC_ENVIRONMENT: process.env.NEXT_PUBLIC_ENVIRONMENT,
    NEXT_PUBLIC_VERCEL_URL: process.env.NEXT_PUBLIC_VERCEL_URL,
    NEXT_PUBLIC_ANALYTICS_ID: process.env.NEXT_PUBLIC_ANALYTICS_ID,
    NEXT_PUBLIC_SENTRY_DSN: process.env.NEXT_PUBLIC_SENTRY_DSN,
  },
  // ... outras configurações
}
```

## 5. Limitações e Próximos Passos

### **Limitações Conhecidas**

#### **Funcionalidades**
- **Deploy manual**: Deploy automático via Git, mas sem CI/CD avançado
- **Monitoramento básico**: Logs e métricas básicas, sem alertas avançados
- **Rollback manual**: Rollback automático básico, sem rollback inteligente
- **Secrets básicos**: Gerenciamento de secrets básico, sem rotação automática

#### **Técnicas**
- **Performance**: Sem otimizações avançadas de performance
- **Escalabilidade**: Auto-scaling básico, sem previsão de carga
- **Segurança**: Segurança básica, sem WAF ou DDoS protection
- **Backup**: Backup básico, sem backup automático

#### **Operacionais**
- **CI/CD**: Pipeline básico, sem testes automatizados
- **Monitoring**: Monitoramento básico, sem observabilidade completa
- **Alerting**: Alertas básicos, sem alertas inteligentes
- **Documentation**: Documentação básica, sem runbooks automatizados

### **Próximos Passos**

#### **Curto Prazo (Sprint 4)**
1. **Implementar funcionalidades restantes**:
   - CI/CD pipeline completo
   - Testes automatizados
   - Monitoramento avançado
   - Alertas inteligentes

2. **Melhorar segurança**:
   - WAF (Web Application Firewall)
   - DDoS protection
   - Secrets rotation
   - Security scanning

3. **Otimizar performance**:
   - CDN avançado
   - Caching inteligente
   - Database optimization
   - Image optimization

#### **Médio Prazo (Sprint 5-6)**
1. **Implementar observabilidade**:
   - Distributed tracing
   - APM (Application Performance Monitoring)
   - Log aggregation
   - Metrics dashboard

2. **Automação avançada**:
   - Auto-scaling inteligente
   - Auto-healing
   - Predictive scaling
   - Cost optimization

3. **Funcionalidades avançadas**:
   - Blue-green deployment
   - Canary deployment
   - Feature flags
   - A/B testing

#### **Longo Prazo (Sprint 7+)**
1. **Escalabilidade**:
   - Multi-region deployment
   - Edge computing
   - Global load balancing
   - Disaster recovery

2. **Funcionalidades avançadas**:
   - GitOps
   - Infrastructure as Code
   - Policy as Code
   - Compliance automation

3. **Otimizações**:
   - Cost optimization
   - Performance optimization
   - Security optimization
   - Operational optimization

### **Dependências Externas**
- **Vercel**: Plataforma de deploy do frontend
- **Google Cloud Platform**: Plataforma de deploy do backend
- **GitHub**: Repositório de código
- **Domínio**: Domínio customizado para produção

### **Compatibilidade**
- **Navegadores**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Dispositivos**: Desktop, tablet, mobile
- **Sistemas Operacionais**: Windows, macOS, Linux
- **Resoluções**: 320px+ (mobile first)

### **Roadmap de Desenvolvimento**
1. **Sprint 4**: Deploy mínimo funcional
2. **Sprint 5**: CI/CD pipeline completo
3. **Sprint 6**: Monitoramento avançado
4. **Sprint 7**: Observabilidade completa
5. **Sprint 8**: Automação avançada

### **Métricas de Sucesso**
- **Deploy Success Rate**: > 99%
- **Deploy Duration**: < 10 minutos
- **Rollback Time**: < 5 minutos
- **Uptime**: > 99.9%
- **Error Rate**: < 0.1%

### **Considerações de Segurança**
- **Secrets Management**: Google Secret Manager
- **HTTPS/TLS**: Let's Encrypt via Vercel
- **CORS**: Configuração restritiva
- **Rate Limiting**: Limitação básica
- **Audit Logs**: Logs de auditoria

### **Checklist de Deploy**
1. **Pré-Deploy**:
   - [ ] Código revisado e aprovado
   - [ ] Tests passando
   - [ ] Environment variables configuradas
   - [ ] Secrets atualizados

2. **Deploy**:
   - [ ] Deploy para staging
   - [ ] Health checks passando
   - [ ] Deploy para produção
   - [ ] Verificação de funcionamento

3. **Pós-Deploy**:
   - [ ] Monitoramento ativo
   - [ ] Logs sendo coletados
   - [ ] Métricas sendo coletadas
   - [ ] Documentação atualizada

### **Troubleshooting**
1. **Deploy Failure**:
   - Verificar logs do build
   - Verificar environment variables
   - Verificar secrets
   - Verificar dependências

2. **Health Check Failure**:
   - Verificar aplicação
   - Verificar dependências
   - Verificar configuração
   - Verificar logs

3. **Performance Issues**:
   - Verificar métricas
   - Verificar logs
   - Verificar configuração
   - Verificar dependências

---

**Este documento fornece um guia completo para deploy mínimo do MVP, incluindo configuração, execução, APIs, variáveis de ambiente e roadmap de desenvolvimento.**
