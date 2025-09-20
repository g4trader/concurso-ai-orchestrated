# README_WEB-003: Tela de Geração de Simulado

## 1. Objetivo/Contexto

### **Objetivo**
Implementar uma tela completa de geração de simulados para concursos públicos, permitindo que usuários selecionem banca, edital e configurem questões para gerar simulados personalizados.

### **Contexto do Projeto**
- **Projeto**: Concurso-AI Orchestrated
- **Sprint**: 4 - Frontend & Go-to-Market (MVP)
- **História**: WEB-003 - Tela de geração de simulado
- **Usuário**: Estudante
- **Valor**: Acesso ao core do produto

### **Problema Resolvido**
Permitir que estudantes configurem e gerem simulados personalizados baseados em bancas e editais específicos, proporcionando uma experiência de estudo direcionada e eficaz.

### **Arquitetura do Sistema**
```
Usuário → Formulário de Seleção → Validação de Campos → Preview do Conjunto → Confirmação → Geração de Simulado → Estado de Carregamento → API de Geração → Processamento Backend → Resposta com Questões → Exibição das Questões → Interface de Resposta → Placeholder de Correção
```

### **Funcionalidades Principais**
- **Seleção de banca** com filtro dinâmico
- **Seleção de edital** baseada na banca escolhida
- **Configuração de questões** (quantidade, tempo, dificuldade)
- **Preview do simulado** antes da geração
- **Geração assíncrona** com progress tracking
- **Estados de loading** para melhor UX
- **Validação de formulários** em tempo real
- **Tratamento de erros** robusto
- **Interface responsiva** para todos os dispositivos
- **Navegação intuitiva** entre etapas

## 2. Como Rodar (Conceitual)

### **Pré-requisitos**
- Node.js 18+
- npm ou yarn
- Git
- Backend WEB-003 rodando na porta 8002

### **Instalação**
```bash
# 1. Clonar o repositório
git clone <repository-url>
cd web-003

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

# Verificar página de geração de simulado
curl http://localhost:3000/simulado/generate

# Verificar se o backend está rodando
curl http://localhost:8002/api/v1/health
```

### **Estrutura de Desenvolvimento**
```bash
# Estrutura de pastas
src/
├── components/
│   ├── simulado/        # Componentes de simulado
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

### **APIs de Simulado**

#### Gerar Simulado
```typescript
// POST /api/v1/simulados/generate
interface SimuladoGenerationRequest {
  bancaId: string;
  editalId: string;
  totalQuestions: number;
  timeLimit: number;
  difficulty: 'easy' | 'medium' | 'hard';
  topics?: string[];
  customInstructions?: string;
}

interface SimuladoGenerationResponse {
  simulado: {
    id: string;
    title: string;
    description: string;
    banca: {
      id: string;
      name: string;
      code: string;
    };
    edital: {
      id: string;
      title: string;
      year: number;
    };
    totalQuestions: number;
    timeLimit: number;
    difficulty: 'easy' | 'medium' | 'hard';
    topics: string[];
    status: 'ready';
    createdAt: string;
  };
  questions: Array<{
    id: string;
    question: string;
    alternatives: {
      A: string;
      B: string;
      C: string;
      D: string;
      E: string;
    };
    correctAnswer: 'A' | 'B' | 'C' | 'D' | 'E';
    difficulty: 'easy' | 'medium' | 'hard';
    topic: string;
    order: number;
  }>;
  estimatedTime: number;
  generationId: string;
}
```

#### Listar Bancas
```typescript
// GET /api/v1/bancas
interface BancaListResponse {
  bancas: Array<{
    id: string;
    name: string;
    code: string;
    description: string;
    logo?: string;
    website?: string;
    isActive: boolean;
    characteristics: {
      questionStyle: 'multiple_choice' | 'true_false' | 'mixed';
      answerFormat: 'A-E' | 'A-D' | 'A-C' | 'V-F';
      timePerQuestion: number;
      difficultyDistribution: {
        easy: number;
        medium: number;
        hard: number;
      };
      commonTopics: string[];
    };
    createdAt: string;
  }>;
  total: number;
  page: number;
  limit: number;
}
```

#### Listar Editais
```typescript
// GET /api/v1/editais
interface EditalListResponse {
  editais: Array<{
    id: string;
    title: string;
    description: string;
    bancaId: string;
    year: number;
    month?: number;
    examType: 'concurso' | 'vestibular' | 'enem' | 'outro';
    subjects: string[];
    totalQuestions: number;
    timeLimit: number;
    isActive: boolean;
    publishedAt: string;
    examDate?: string;
    createdAt: string;
  }>;
  total: number;
  page: number;
  limit: number;
}
```

#### Status da Geração
```typescript
// GET /api/v1/generation/{id}/status
interface GenerationStatus {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number; // 0-100
  currentStep: string;
  estimatedTimeRemaining: number; // em segundos
  error?: string;
  createdAt: string;
  updatedAt: string;
}
```

### **Exemplos de Uso das APIs**

#### Gerar Simulado
```javascript
// Exemplo de geração de simulado
const generateSimulado = async (config) => {
  const response = await fetch('/api/v1/simulados/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      bancaId: 'banca_123',
      editalId: 'edital_456',
      totalQuestions: 50,
      timeLimit: 120,
      difficulty: 'medium',
      topics: ['matemática', 'português', 'conhecimentos gerais'],
      customInstructions: 'Foco em questões de raciocínio lógico'
    }),
  });
  
  if (!response.ok) {
    throw new Error('Falha na geração do simulado');
  }
  
  return response.json();
};
```

#### Listar Bancas
```javascript
// Exemplo de listagem de bancas
const getBancas = async () => {
  const response = await fetch('/api/v1/bancas?page=1&limit=10&isActive=true', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  if (!response.ok) {
    throw new Error('Falha ao carregar bancas');
  }
  
  return response.json();
};
```

#### Listar Editais
```javascript
// Exemplo de listagem de editais
const getEditais = async (bancaId) => {
  const response = await fetch(`/api/v1/editais?bancaId=${bancaId}&year=2024&isActive=true`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  if (!response.ok) {
    throw new Error('Falha ao carregar editais');
  }
  
  return response.json();
};
```

#### Status da Geração
```javascript
// Exemplo de verificação de status
const getGenerationStatus = async (generationId) => {
  const response = await fetch(`/api/v1/generation/${generationId}/status`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  if (!response.ok) {
    throw new Error('Falha ao obter status da geração');
  }
  
  return response.json();
};
```

## 4. Variáveis de Ambiente

### **Configuração Base**
```bash
# .env.local
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8002
NEXT_PUBLIC_APP_NAME=Concurso AI

# Simulado Configuration
NEXT_PUBLIC_MAX_QUESTIONS=100
NEXT_PUBLIC_MIN_QUESTIONS=1
NEXT_PUBLIC_MAX_TIME_LIMIT=300
NEXT_PUBLIC_MIN_TIME_LIMIT=30

# Generation Configuration
NEXT_PUBLIC_GENERATION_TIMEOUT=30000
NEXT_PUBLIC_PROGRESS_POLLING_INTERVAL=2000
NEXT_PUBLIC_MAX_GENERATION_RETRIES=3

# Development
NODE_ENV=development
```

### **Variáveis de Desenvolvimento**
```bash
# .env.development
NEXT_PUBLIC_API_URL=http://localhost:8002
NEXT_PUBLIC_APP_NAME=Concurso AI (Dev)
NODE_ENV=development
NEXT_PUBLIC_MAX_QUESTIONS=100
NEXT_PUBLIC_MIN_QUESTIONS=1
NEXT_PUBLIC_MAX_TIME_LIMIT=300
NEXT_PUBLIC_MIN_TIME_LIMIT=30
NEXT_PUBLIC_GENERATION_TIMEOUT=30000
NEXT_PUBLIC_PROGRESS_POLLING_INTERVAL=2000
```

### **Variáveis de Produção**
```bash
# .env.production
NEXT_PUBLIC_API_URL=https://api.concurso-ai.com
NEXT_PUBLIC_APP_NAME=Concurso AI
NODE_ENV=production
NEXT_PUBLIC_MAX_QUESTIONS=100
NEXT_PUBLIC_MIN_QUESTIONS=1
NEXT_PUBLIC_MAX_TIME_LIMIT=300
NEXT_PUBLIC_MIN_TIME_LIMIT=30
NEXT_PUBLIC_GENERATION_TIMEOUT=30000
NEXT_PUBLIC_PROGRESS_POLLING_INTERVAL=2000
```

### **Variáveis de Teste**
```bash
# .env.test
NEXT_PUBLIC_API_URL=http://localhost:8002
NEXT_PUBLIC_APP_NAME=Concurso AI (Test)
NODE_ENV=test
NEXT_PUBLIC_MAX_QUESTIONS=100
NEXT_PUBLIC_MIN_QUESTIONS=1
NEXT_PUBLIC_MAX_TIME_LIMIT=300
NEXT_PUBLIC_MIN_TIME_LIMIT=30
NEXT_PUBLIC_GENERATION_TIMEOUT=30000
NEXT_PUBLIC_PROGRESS_POLLING_INTERVAL=2000
```

### **Configuração de Build**
```bash
# next.config.js
module.exports = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME,
    NEXT_PUBLIC_MAX_QUESTIONS: process.env.NEXT_PUBLIC_MAX_QUESTIONS,
    NEXT_PUBLIC_MIN_QUESTIONS: process.env.NEXT_PUBLIC_MIN_QUESTIONS,
    NEXT_PUBLIC_MAX_TIME_LIMIT: process.env.NEXT_PUBLIC_MAX_TIME_LIMIT,
    NEXT_PUBLIC_MIN_TIME_LIMIT: process.env.NEXT_PUBLIC_MIN_TIME_LIMIT,
    NEXT_PUBLIC_GENERATION_TIMEOUT: process.env.NEXT_PUBLIC_GENERATION_TIMEOUT,
    NEXT_PUBLIC_PROGRESS_POLLING_INTERVAL: process.env.NEXT_PUBLIC_PROGRESS_POLLING_INTERVAL,
  },
  // ... outras configurações
}
```

## 5. Limitações e Próximos Passos

### **Limitações Conhecidas**

#### **Funcionalidades**
- **APIs Mock**: Algumas APIs são simuladas com dados estáticos
- **Geração real**: Geração de simulados é simulada
- **Questões reais**: Questões são placeholders
- **Correção automática**: Correção não implementada
- **Salvamento de progresso**: Progresso não é salvo

#### **Técnicas**
- **Performance**: Sem otimizações avançadas de performance
- **Cache**: Cache básico implementado
- **Offline**: Sem suporte offline
- **PWA**: Funcionalidades PWA não implementadas

#### **UX/UI**
- **Design System**: Sistema de design básico
- **Responsividade**: Layout responsivo básico
- **Animações**: Sem animações avançadas
- **Acessibilidade**: Implementação básica de acessibilidade

#### **Segurança**
- **Validação**: Validação básica implementada
- **Sanitização**: Sanitização básica de inputs
- **Rate Limiting**: Limitação básica de requisições
- **CORS**: Configuração básica de CORS

### **Próximos Passos**

#### **Curto Prazo (Sprint 4)**
1. **Implementar funcionalidades restantes**:
   - Geração real de simulados
   - Questões reais
   - Correção automática
   - Salvamento de progresso

2. **Melhorar UX**:
   - Implementar loading states avançados
   - Adicionar progress tracking
   - Melhorar responsividade
   - Adicionar animações básicas

3. **Integração completa**:
   - Conectar com APIs reais
   - Implementar cache avançado
   - Adicionar validações de formulário
   - Implementar error handling robusto

#### **Médio Prazo (Sprint 5-6)**
1. **Integração Backend**:
   - Conectar com APIs reais
   - Implementar geração real de simulados
   - Adicionar gerenciamento de estado
   - Implementar cache de dados

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
- **Serviços de Geração**: Requer integração com provedor
- **CDN**: Requer configuração de CDN para assets

### **Compatibilidade**
- **Navegadores**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Dispositivos**: Desktop, tablet, mobile
- **Sistemas Operacionais**: Windows, macOS, Linux
- **Resoluções**: 320px+ (mobile first)

### **Roadmap de Desenvolvimento**
1. **Sprint 4**: Tela de geração funcional com mock data
2. **Sprint 5**: Integração com backend real
3. **Sprint 6**: Otimizações de performance
4. **Sprint 7**: Funcionalidades avançadas
5. **Sprint 8**: Deploy e monitoramento

### **Métricas de Sucesso**
- **Funcionalidade**: 100% dos componentes de geração funcionais
- **Testes**: 90% de cobertura de código
- **Performance**: < 2s First Contentful Paint
- **Acessibilidade**: WCAG 2.1 AA compliance
- **Responsividade**: Funcional em todos os dispositivos
- **Usabilidade**: Fluxo intuitivo e eficiente

### **Considerações de Segurança**
- **Validação de inputs**: Sanitização e validação rigorosa
- **Proteção contra ataques**: XSS, CSRF, injection
- **Rate limiting**: Limitação de requisições
- **Gerenciamento de sessões**: Timeout adequado
- **Logs de segurança**: Auditoria de tentativas de geração

---

**Este documento fornece documentação completa para a tela de geração de simulado WEB-003, incluindo instalação, uso, APIs, configuração e roadmap de desenvolvimento.**
