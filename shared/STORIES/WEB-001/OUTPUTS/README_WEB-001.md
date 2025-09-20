# README_WEB-001: Protótipo Web — Shell do App (Next.js)

## 1. Objetivo/Contexto

### **Objetivo**
Implementar um protótipo web completo usando Next.js 14+ com App Router, criando a base estrutural para uma plataforma de simulados inteligentes para concursos públicos.

### **Contexto do Projeto**
- **Projeto**: Concurso-AI Orchestrated
- **Sprint**: 4 - Frontend & Go-to-Market (MVP)
- **História**: WEB-001 - Protótipo Web shell do app
- **Usuário**: Estudante (B2C)
- **Valor**: Base para navegação e evolução da plataforma

### **Problema Resolvido**
Criar uma casca de aplicação (layout básico, rotas) para hospedar as features futuras, fornecendo uma base sólida para navegação e evolução do sistema.

### **Arquitetura do Sistema**
```
Usuário → Next.js App Router → Layout Principal → Páginas → Componentes → Mock Data → UI Components → Estados Loading/Error → Theme System
```

### **Funcionalidades Principais**
- **Layout responsivo** com header, main content e footer
- **Sistema de roteamento** com páginas principais
- **Autenticação** com login/logout
- **Dashboard** com estatísticas e simulados recentes
- **Gerador de simulados** com formulário de configuração
- **Página de resultados** com análise de performance
- **Estados de loading/error** para melhor UX
- **Sistema de temas** básico

## 2. Como Rodar (Conceitual)

### **Pré-requisitos**
- Node.js 18+ 
- npm ou yarn
- Git

### **Instalação**
```bash
# 1. Clonar o repositório
git clone <repository-url>
cd web-001

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

# Verificar páginas principais
curl http://localhost:3000/login
curl http://localhost:3000/dashboard
curl http://localhost:3000/gerador-simulado
curl http://localhost:3000/resultados
```

### **Estrutura de Desenvolvimento**
```bash
# Estrutura de pastas
src/
├── app/                 # Páginas Next.js (App Router)
├── components/          # Componentes React reutilizáveis
├── hooks/              # Hooks customizados
├── lib/                # Utilitários e configurações
├── types/              # Definições TypeScript
└── styles/             # Estilos CSS/Tailwind

# Comandos úteis
npm run dev              # Desenvolvimento
npm run build           # Build de produção
npm run start           # Executar produção
npm run lint            # Verificar código
npm run test            # Executar testes
```

## 3. APIs/Contratos (se houver)

### **Mock APIs Implementadas**

#### Auth API
```typescript
// POST /api/auth/login
interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  user: {
    id: string;
    email: string;
    name: string;
    avatar?: string;
  };
  token: string;
  expiresIn: number;
}

// GET /api/auth/me
interface UserResponse {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  createdAt: string;
  lastLogin?: string;
}
```

#### Simulados API
```typescript
// GET /api/simulados
interface SimuladosResponse {
  data: Simulado[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// POST /api/simulados
interface CreateSimuladoRequest {
  title: string;
  description: string;
  banca: 'CESPE' | 'FGV' | 'VUNESP' | 'FCC';
  ano: number;
  topico: string;
  totalQuestions: number;
  timeLimit: number;
}

// GET /api/simulados/[id]/questions
interface QuestionsResponse {
  data: Question[];
}
```

#### Results API
```typescript
// GET /api/simulados/[id]/results
interface ResultsResponse {
  simuladoId: string;
  score: number;
  totalQuestions: number;
  correctAnswers: number;
  timeSpent: number;
  responses: SimuladoResponse[];
  completedAt: string;
}

// POST /api/simulados/[id]/submit
interface SubmitRequest {
  responses: SimuladoResponse[];
  timeSpent: number;
}
```

### **Exemplos de Uso das APIs**

#### Login
```javascript
// Exemplo de login
const loginUser = async (email, password) => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });
  
  if (!response.ok) {
    throw new Error('Login failed');
  }
  
  return response.json();
};
```

#### Buscar Simulados
```javascript
// Exemplo de busca de simulados
const getSimulados = async (page = 1, limit = 10) => {
  const response = await fetch(`/api/simulados?page=${page}&limit=${limit}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch simulados');
  }
  
  return response.json();
};
```

#### Criar Simulado
```javascript
// Exemplo de criação de simulado
const createSimulado = async (simuladoData) => {
  const response = await fetch('/api/simulados', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(simuladoData),
  });
  
  if (!response.ok) {
    throw new Error('Failed to create simulado');
  }
  
  return response.json();
};
```

## 4. Variáveis de Ambiente

### **Configuração Base**
```bash
# .env.local
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Concurso AI

# Authentication
NEXTAUTH_SECRET=your-secret-key-here
NEXTAUTH_URL=http://localhost:3000

# Database (futuro)
DATABASE_URL=postgresql://user:password@localhost:5432/concurso_ai

# External Services (futuro)
OPENAI_API_KEY=your-openai-key
ANALYTICS_ID=your-analytics-id
```

### **Variáveis de Desenvolvimento**
```bash
# .env.development
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Concurso AI (Dev)
NODE_ENV=development
```

### **Variáveis de Produção**
```bash
# .env.production
NEXT_PUBLIC_API_URL=https://api.concurso-ai.com
NEXT_PUBLIC_APP_NAME=Concurso AI
NODE_ENV=production
NEXTAUTH_URL=https://concurso-ai.com
```

### **Variáveis de Teste**
```bash
# .env.test
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_APP_NAME=Concurso AI (Test)
NODE_ENV=test
```

### **Configuração de Build**
```bash
# next.config.js
module.exports = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME,
  },
  // ... outras configurações
}
```

## 5. Limitações e Próximos Passos

### **Limitações Conhecidas**

#### **Funcionalidades**
- **APIs Mock**: Todas as APIs são simuladas com dados estáticos
- **Autenticação**: Sistema básico sem integração real
- **Persistência**: Dados não persistem entre sessões
- **Integração Backend**: Sem conexão com serviços reais

#### **Técnicas**
- **Performance**: Sem otimizações avançadas de performance
- **SEO**: Configuração básica de SEO
- **Acessibilidade**: Implementação básica de acessibilidade
- **Testes**: Cobertura de testes limitada

#### **UX/UI**
- **Design System**: Sistema de design básico
- **Responsividade**: Layout responsivo básico
- **Animações**: Sem animações avançadas
- **Temas**: Sistema de temas simples

### **Próximos Passos**

#### **Curto Prazo (Sprint 4)**
1. **Implementar componentes restantes**:
   - LoginForm completo
   - SimuladoForm funcional
   - Dashboard com dados reais
   - Resultados com visualizações

2. **Melhorar UX**:
   - Implementar loading states
   - Adicionar error boundaries
   - Melhorar responsividade
   - Adicionar animações básicas

3. **Integração básica**:
   - Conectar com APIs mock
   - Implementar persistência local
   - Adicionar validações de formulário
   - Implementar navegação protegida

#### **Médio Prazo (Sprint 5-6)**
1. **Integração Backend**:
   - Conectar com APIs reais
   - Implementar autenticação JWT
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
- **Serviços de Auth**: Requer integração com provedor
- **CDN**: Requer configuração de CDN para assets

### **Compatibilidade**
- **Navegadores**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Dispositivos**: Desktop, tablet, mobile
- **Sistemas Operacionais**: Windows, macOS, Linux
- **Resoluções**: 320px+ (mobile first)

### **Roadmap de Desenvolvimento**
1. **Sprint 4**: Protótipo funcional com mock data
2. **Sprint 5**: Integração com backend real
3. **Sprint 6**: Otimizações de performance
4. **Sprint 7**: Funcionalidades avançadas
5. **Sprint 8**: Deploy e monitoramento

---

**Este documento fornece documentação completa para o protótipo web WEB-001, incluindo instalação, uso, APIs, configuração e roadmap de desenvolvimento.**
