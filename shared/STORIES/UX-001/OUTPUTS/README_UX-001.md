# README_UX-001: Sistema de Feedback do Usuário (Reportar Erro na Questão)

## 1. Objetivo/Contexto

### **Objetivo**
Implementar um sistema completo de coleta de feedback dos usuários sobre questões de simulados, permitindo reportar problemas, erros e sugestões para melhoria contínua da qualidade do banco de questões.

### **Contexto do Projeto**
- **Projeto**: Concurso-AI Orchestrated
- **Sprint**: 4 - Frontend & Go-to-Market (MVP)
- **História**: UX-001 - Feedback do usuário (reportar erro na questão)
- **Usuário**: Estudante
- **Valor**: Melhoria contínua do banco/geração

### **Problema Resolvido**
Permitir que estudantes reportem problemas encontrados nas questões de simulados, incluindo erros factuais, questões ambíguas, alternativas incorretas e outros problemas, facilitando a melhoria contínua da qualidade do banco de questões.

### **Arquitetura do Sistema**
```
Usuário identifica problema → Clique em "Reportar Problema" → Modal de Feedback → Seleção de Categoria → Comentário do Usuário → Validação do Formulário → Salvamento Local → Envio para API → Confirmação de Recebimento → Fechamento do Modal
```

### **Funcionalidades Principais**
- **Botão de feedback** por questão com ícone e texto adequados
- **Modal de feedback** com formulário completo e responsivo
- **Seleção de categoria** com prioridades visuais (alta, média, baixa)
- **Campo de comentário** com validação em tempo real
- **Auto-save de rascunho** a cada 30 segundos
- **Validação de formulário** com feedback visual
- **Envio para API** com confirmação de recebimento
- **Gerenciamento de rascunhos** com TTL de 7 dias
- **Interface responsiva** para todos os dispositivos
- **Acessibilidade** com ARIA labels e navegação por teclado
- **Error handling** robusto com retry mechanism
- **Loading states** adequados para melhor UX

## 2. Como Rodar (Conceitual)

### **Pré-requisitos**
- Node.js 18+
- npm ou yarn
- Git
- Backend UX-001 rodando na porta 8004

### **Instalação**
```bash
# 1. Clonar o repositório
git clone <repository-url>
cd ux-001

# 2. Instalar dependências
npm install
# ou
yarn install

# 3. Configurar variáveis de ambiente
cp .env.example .env.local
# Editar .env.local com suas configurações

# 4. Executar em modo desenvolvimento
npm run dev
# ou
yarn dev
```

### **Execução**
```bash
# Desenvolvimento
npm run dev
# Acesse http://localhost:3000

# Build para produção
npm run build

# Executar build de produção
npm run start

# Linting
npm run lint

# Testes
npm run test
npm run test:watch
npm run test:coverage
```

### **Verificação**
```bash
# Verificar se a aplicação está rodando
curl http://localhost:3000

# Verificar página de feedback
curl http://localhost:3000/feedback/q_123456

# Verificar se o backend está rodando
curl http://localhost:8004/api/v1/health
```

### **Estrutura de Desenvolvimento**
```bash
# Estrutura de pastas
src/
├── components/
│   ├── feedback/        # Componentes de feedback
│   ├── ui/              # Componentes UI reutilizáveis
│   └── layout/          # Componentes de layout
├── hooks/               # Hooks customizados
├── services/            # Serviços de API
├── types/               # Definições TypeScript
├── pages/               # Páginas Next.js
└── contexts/            # Contextos React

# Comandos úteis
npm run dev              # Desenvolvimento
npm run build           # Build de produção
npm run start           # Executar produção
npm run lint            # Verificar código
npm run test            # Executar testes
```

## 3. APIs/Contratos (se houver)

### **APIs de Feedback**

#### Enviar Feedback
```typescript
// POST /api/v1/feedback
interface FeedbackRequest {
  questionId: string;
  userId: string;
  category: FeedbackCategory;
  comment: string;
  metadata: FeedbackMetadata;
  timestamp: string;
  userAgent: string;
  sessionId: string;
}

interface FeedbackCategory {
  id: string;
  name: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  icon: string;
}

interface FeedbackMetadata {
  questionText: string;
  questionOptions: string[];
  selectedAnswer?: string;
  correctAnswer?: string;
  timeSpent: number;
  difficulty: 'easy' | 'medium' | 'hard';
  topic: string;
  banca: string;
  edital: string;
  simuladoId: string;
  browserInfo: BrowserInfo;
  deviceInfo: DeviceInfo;
}
```

#### Obter Feedback
```typescript
// GET /api/v1/feedback/{id}
interface FeedbackResponse {
  success: boolean;
  feedbackId: string;
  message: string;
  timestamp: string;
  status: 'pending' | 'reviewed' | 'resolved' | 'rejected';
}
```

#### Listar Feedbacks
```typescript
// GET /api/v1/feedback
interface FeedbacksResponse {
  data: FeedbackResponse[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}
```

#### Atualizar Status
```typescript
// PUT /api/v1/feedback/{id}/status
interface UpdateStatusRequest {
  status: 'pending' | 'reviewed' | 'resolved' | 'rejected';
  adminComment?: string;
}
```

#### Obter Categorias
```typescript
// GET /api/v1/feedback/categories
interface CategoriesResponse {
  categories: FeedbackCategory[];
}
```

#### Gerenciar Rascunhos
```typescript
// POST /api/v1/feedback/draft
interface DraftRequest {
  questionId: string;
  category?: FeedbackCategory;
  comment: string;
  lastSaved: string;
  isDirty: boolean;
}

// GET /api/v1/feedback/draft/{questionId}
interface DraftResponse {
  draft: DraftRequest | null;
}

// DELETE /api/v1/feedback/draft/{questionId}
interface DeleteDraftResponse {
  success: boolean;
  message: string;
}
```

#### Analytics de Feedback
```typescript
// GET /api/v1/feedback/analytics
interface AnalyticsResponse {
  totalFeedback: number;
  feedbackByCategory: CategoryStats[];
  feedbackByPriority: PriorityStats[];
  feedbackByStatus: StatusStats[];
  feedbackByTopic: TopicStats[];
  feedbackByBanca: BancaStats[];
  responseTimeAvg: number;
  resolutionRate: number;
}
```

### **Exemplos de Uso das APIs**

#### Enviar Feedback
```javascript
// Exemplo de envio de feedback
const submitFeedback = async (feedbackData) => {
  const response = await fetch('/api/v1/feedback', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      questionId: 'q_123456',
      userId: 'user_789012',
      category: {
        id: 'error_in_question',
        name: 'Erro na Questão',
        description: 'A questão contém um erro factual ou técnico',
        priority: 'high',
        icon: 'alert-triangle'
      },
      comment: 'A alternativa B está incorreta. A resposta correta deveria ser A.',
      metadata: {
        questionText: 'Qual é o prazo para recurso em processo administrativo?',
        questionOptions: ['A) 30 dias', 'B) 60 dias', 'C) 90 dias', 'D) 120 dias', 'E) 180 dias'],
        selectedAnswer: 'A',
        correctAnswer: 'B',
        timeSpent: 45,
        difficulty: 'medium',
        topic: 'direito administrativo',
        banca: 'CESPE',
        edital: 'MPU_2024',
        simuladoId: 'sim_345678',
        browserInfo: {
          name: 'Chrome',
          version: '120.0.0.0',
          os: 'Windows 10',
          language: 'pt-BR',
          timezone: 'America/Sao_Paulo'
        },
        deviceInfo: {
          type: 'desktop',
          screen: { width: 1920, height: 1080 },
          userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
      },
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      sessionId: 'sess_abc123def456'
    }),
  });
  
  if (!response.ok) {
    throw new Error('Falha ao enviar feedback');
  }
  
  return response.json();
};
```

#### Obter Categorias
```javascript
// Exemplo de obtenção de categorias
const getCategories = async () => {
  const response = await fetch('/api/v1/feedback/categories', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  if (!response.ok) {
    throw new Error('Falha ao carregar categorias');
  }
  
  return response.json();
};
```

#### Salvar Rascunho
```javascript
// Exemplo de salvamento de rascunho
const saveDraft = async (questionId, draftData) => {
  const response = await fetch('/api/v1/feedback/draft', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      questionId,
      category: draftData.category,
      comment: draftData.comment,
      lastSaved: new Date().toISOString(),
      isDirty: draftData.isDirty
    }),
  });
  
  if (!response.ok) {
    throw new Error('Falha ao salvar rascunho');
  }
  
  return response.json();
};
```

#### Obter Analytics
```javascript
// Exemplo de obtenção de analytics
const getAnalytics = async (period = '30d') => {
  const response = await fetch(`/api/v1/feedback/analytics?period=${period}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  if (!response.ok) {
    throw new Error('Falha ao carregar analytics');
  }
  
  return response.json();
};
```

## 4. Variáveis de Ambiente

### **Configuração Base**
```bash
# .env.local
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8004
NEXT_PUBLIC_APP_NAME=Concurso AI Feedback

# Feedback Configuration
NEXT_PUBLIC_MAX_COMMENT_LENGTH=1000
NEXT_PUBLIC_MIN_COMMENT_LENGTH=10
NEXT_PUBLIC_DRAFT_AUTO_SAVE_INTERVAL=30000
NEXT_PUBLIC_DRAFT_TTL=604800000

# Performance Configuration
NEXT_PUBLIC_MODAL_OPEN_TIMEOUT=1000
NEXT_PUBLIC_FORM_VALIDATION_DEBOUNCE=500
NEXT_PUBLIC_AUTO_SAVE_DEBOUNCE=30000

# Development
NODE_ENV=development
```

### **Variáveis de Desenvolvimento**
```bash
# .env.development
NEXT_PUBLIC_API_URL=http://localhost:8004
NEXT_PUBLIC_APP_NAME=Concurso AI Feedback (Dev)
NODE_ENV=development
NEXT_PUBLIC_MAX_COMMENT_LENGTH=1000
NEXT_PUBLIC_MIN_COMMENT_LENGTH=10
NEXT_PUBLIC_DRAFT_AUTO_SAVE_INTERVAL=30000
NEXT_PUBLIC_DRAFT_TTL=604800000
NEXT_PUBLIC_MODAL_OPEN_TIMEOUT=1000
NEXT_PUBLIC_FORM_VALIDATION_DEBOUNCE=500
NEXT_PUBLIC_AUTO_SAVE_DEBOUNCE=30000
```

### **Variáveis de Produção**
```bash
# .env.production
NEXT_PUBLIC_API_URL=https://api.concurso-ai.com
NEXT_PUBLIC_APP_NAME=Concurso AI Feedback
NODE_ENV=production
NEXT_PUBLIC_MAX_COMMENT_LENGTH=1000
NEXT_PUBLIC_MIN_COMMENT_LENGTH=10
NEXT_PUBLIC_DRAFT_AUTO_SAVE_INTERVAL=30000
NEXT_PUBLIC_DRAFT_TTL=604800000
NEXT_PUBLIC_MODAL_OPEN_TIMEOUT=1000
NEXT_PUBLIC_FORM_VALIDATION_DEBOUNCE=500
NEXT_PUBLIC_AUTO_SAVE_DEBOUNCE=30000
```

### **Variáveis de Teste**
```bash
# .env.test
NEXT_PUBLIC_API_URL=http://localhost:8004
NEXT_PUBLIC_APP_NAME=Concurso AI Feedback (Test)
NODE_ENV=test
NEXT_PUBLIC_MAX_COMMENT_LENGTH=1000
NEXT_PUBLIC_MIN_COMMENT_LENGTH=10
NEXT_PUBLIC_DRAFT_AUTO_SAVE_INTERVAL=30000
NEXT_PUBLIC_DRAFT_TTL=604800000
NEXT_PUBLIC_MODAL_OPEN_TIMEOUT=1000
NEXT_PUBLIC_FORM_VALIDATION_DEBOUNCE=500
NEXT_PUBLIC_AUTO_SAVE_DEBOUNCE=30000
```

### **Configuração de Build**
```bash
# next.config.js
module.exports = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME,
    NEXT_PUBLIC_MAX_COMMENT_LENGTH: process.env.NEXT_PUBLIC_MAX_COMMENT_LENGTH,
    NEXT_PUBLIC_MIN_COMMENT_LENGTH: process.env.NEXT_PUBLIC_MIN_COMMENT_LENGTH,
    NEXT_PUBLIC_DRAFT_AUTO_SAVE_INTERVAL: process.env.NEXT_PUBLIC_DRAFT_AUTO_SAVE_INTERVAL,
    NEXT_PUBLIC_DRAFT_TTL: process.env.NEXT_PUBLIC_DRAFT_TTL,
    NEXT_PUBLIC_MODAL_OPEN_TIMEOUT: process.env.NEXT_PUBLIC_MODAL_OPEN_TIMEOUT,
    NEXT_PUBLIC_FORM_VALIDATION_DEBOUNCE: process.env.NEXT_PUBLIC_FORM_VALIDATION_DEBOUNCE,
    NEXT_PUBLIC_AUTO_SAVE_DEBOUNCE: process.env.NEXT_PUBLIC_AUTO_SAVE_DEBOUNCE,
  },
  // ... outras configurações
}
```

## 5. Limitações e Próximos Passos

### **Limitações Conhecidas**

#### **Funcionalidades**
- **APIs Mock**: Algumas APIs são simuladas com dados estáticos
- **Categorias fixas**: Categorias são pré-definidas e não dinâmicas
- **Rascunhos locais**: Rascunhos são armazenados apenas localmente
- **Analytics básicos**: Analytics são limitados e não em tempo real

#### **Técnicas**
- **Performance**: Sem otimizações avançadas de performance
- **Cache**: Cache básico implementado
- **Offline**: Sem suporte offline
- **PWA**: Funcionalidades PWA não implementadas

#### **UX/UI**
- **Design system**: Sistema básico sem consistência
- **Responsividade**: Layout responsivo básico
- **Animações**: Sem transições suaves
- **Acessibilidade**: Implementação básica de acessibilidade

#### **Segurança**
- **Validação**: Validação básica implementada
- **Sanitização**: Sanitização básica de inputs
- **Rate limiting**: Limitação básica de requisições
- **CORS**: Configuração básica de CORS

### **Próximos Passos**

#### **Curto Prazo (Sprint 4)**
1. **Implementar funcionalidades restantes**:
   - APIs reais de feedback
   - Categorias dinâmicas
   - Analytics em tempo real
   - Notificações de status

2. **Melhorar UX**:
   - Implementar loading states avançados
   - Adicionar animações suaves
   - Melhorar responsividade
   - Adicionar tooltips e help

3. **Integração completa**:
   - Conectar com APIs reais
   - Implementar cache avançado
   - Adicionar validações de dados
   - Implementar error handling robusto

#### **Médio Prazo (Sprint 5-6)**
1. **Integração Backend**:
   - Conectar com APIs reais
   - Implementar gerenciamento de estado
   - Adicionar cache de dados
   - Implementar sincronização

2. **Performance**:
   - Implementar lazy loading
   - Adicionar code splitting
   - Otimizar bundle size
   - Implementar service workers

3. **Funcionalidades Avançadas**:
   - Implementar PWA
   - Adicionar notificações
   - Implementar modo offline
   - Adicionar analytics

#### **Longo Prazo (Sprint 7+)**
1. **Escalabilidade**:
   - Implementar micro-frontends
   - Adicionar CDN
   - Implementar edge caching
   - Adicionar load balancing

2. **Funcionalidades Avançadas**:
   - Implementar real-time updates
   - Adicionar colaboração
   - Implementar gamificação
   - Adicionar IA integrada

3. **Otimizações**:
   - Implementar SSR/SSG
   - Adicionar image optimization
   - Implementar font optimization
   - Adicionar performance monitoring

### **Dependências Externas**
- **Backend APIs**: Requer implementação das APIs reais
- **Banco de Dados**: Requer configuração de banco
- **Serviços de Notificação**: Requer integração com provedor
- **CDN**: Requer configuração de CDN para assets

### **Compatibilidade**
- **Navegadores**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Dispositivos**: Desktop, tablet, mobile
- **Sistemas Operacionais**: Windows, macOS, Linux
- **Resoluções**: 320px+ (mobile first)

### **Roadmap de Desenvolvimento**
1. **Sprint 4**: Sistema de feedback funcional com mock data
2. **Sprint 5**: Integração com backend real
3. **Sprint 6**: Otimizações de performance
4. **Sprint 7**: Funcionalidades avançadas
5. **Sprint 8**: Deploy e monitoramento

### **Métricas de Sucesso**
- **Funcionalidade**: 100% dos componentes de feedback funcionais
- **Testes**: 90% de cobertura de código
- **Performance**: < 500ms Modal Opening
- **Acessibilidade**: WCAG 2.1 AA compliance
- **Responsividade**: Funcional em todos os dispositivos
- **Usabilidade**: Interface intuitiva e eficiente

### **Considerações de Segurança**
- **Validação de dados**: Sanitização e validação rigorosa
- **Proteção contra ataques**: XSS, CSRF, injection
- **Rate limiting**: Limitação de requisições
- **Gerenciamento de sessões**: Timeout adequado
- **Logs de segurança**: Auditoria de tentativas de acesso

### **Categorias de Feedback**
- **Erro na Questão** (Alta prioridade) - Erro factual ou técnico
- **Questão Ambígua** (Média prioridade) - Múltiplas interpretações
- **Alternativa Incorreta** (Alta prioridade) - Alternativa com erro
- **Qualidade da Questão** (Média prioridade) - Problemas de redação
- **Problema Técnico** (Baixa prioridade) - Problema de exibição
- **Outro** (Baixa prioridade) - Outros problemas

### **Fluxo de Feedback**
1. Usuário identifica problema na questão
2. Clica em "Reportar Problema"
3. Modal de feedback é aberto
4. Seleciona categoria do problema
5. Escreve comentário detalhado
6. Rascunho é salvo automaticamente
7. Usuário envia feedback
8. Confirmação de recebimento
9. Modal é fechado
10. Feedback é processado pelo sistema

---

**Este documento fornece documentação completa para o sistema de feedback UX-001, incluindo instalação, uso, APIs, configuração e roadmap de desenvolvimento.**
