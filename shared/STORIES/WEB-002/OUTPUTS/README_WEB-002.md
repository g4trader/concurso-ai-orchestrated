# README_WEB-002: Autenticação Simples (E-mail/Senha)

## 1. Objetivo/Contexto

### **Objetivo**
Implementar um sistema completo de autenticação simples usando e-mail e senha para identificação de usuários e persistência de histórico de simulados.

### **Contexto do Projeto**
- **Projeto**: Concurso-AI Orchestrated
- **Sprint**: 4 - Frontend & Go-to-Market (MVP)
- **História**: WEB-002 - Autenticação simples (e-mail/senha)
- **Usuário**: Estudante
- **Valor**: Persistência de histórico de simulados

### **Problema Resolvido**
Identificar usuários de forma segura para salvar progresso e histórico de simulados, permitindo que estudantes acompanhem sua evolução ao longo do tempo.

### **Arquitetura do Sistema**
```
Usuário → Login Form → Validação Frontend → API Auth Service → Backend Auth → Token Generation → Response → Token Storage → Auth Context Update → Redirect Dashboard
```

### **Funcionalidades Principais**
- **Login seguro** com e-mail e senha
- **Logout** com limpeza de tokens
- **Proteção de rotas** com AuthGuard
- **Gerenciamento de tokens** JWT
- **Refresh automático** de tokens
- **Validação de formulários** em tempo real
- **Estados de loading/error** para melhor UX
- **Armazenamento seguro** de tokens em cookies
- **Interceptação de requisições** para adicionar tokens
- **Tratamento de erros** robusto

## 2. Como Rodar (Conceitual)

### **Pré-requisitos**
- Node.js 18+
- npm ou yarn
- Git
- Backend WEB-002 rodando na porta 8001

### **Instalação**
```bash
# 1. Clonar o repositório
git clone <repository-url>
cd web-002

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

# Verificar páginas de autenticação
curl http://localhost:3000/login
curl http://localhost:3000/dashboard

# Verificar se o backend está rodando
curl http://localhost:8001/api/v1/health
```

### **Estrutura de Desenvolvimento**
```bash
# Estrutura de pastas
src/
├── components/
│   ├── auth/           # Componentes de autenticação
│   ├── ui/             # Componentes UI reutilizáveis
│   └── layout/         # Componentes de layout
├── hooks/              # Hooks customizados
├── services/           # Serviços de API
├── types/              # Definições TypeScript
├── pages/              # Páginas Next.js
└── contexts/           # Contextos React

# Comandos úteis
npm run dev              # Desenvolvimento
npm run build           # Build de produção
npm run start           # Executar produção
npm run lint            # Verificar código
npm run test            # Executar testes
```

## 3. APIs/Contratos (se houver)

### **APIs de Autenticação**

#### Login
```typescript
// POST /api/v1/auth/login
interface LoginRequest {
  email: string;
  password: string;
  rememberMe?: boolean;
}

interface LoginResponse {
  user: {
    id: string;
    email: string;
    name: string;
    avatar?: string;
    createdAt: string;
    lastLogin?: string;
    isActive: boolean;
  };
  token: string;
  refreshToken: string;
  expiresIn: number;
  tokenType: 'Bearer';
}
```

#### Logout
```typescript
// POST /api/v1/auth/logout
interface LogoutRequest {
  token: string;
}

interface LogoutResponse {
  message: string;
  success: boolean;
}
```

#### Refresh Token
```typescript
// POST /api/v1/auth/refresh
interface RefreshTokenRequest {
  refreshToken: string;
}

interface RefreshTokenResponse {
  token: string;
  refreshToken: string;
  expiresIn: number;
}
```

#### User Info
```typescript
// GET /api/v1/auth/me
interface UserResponse {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  createdAt: string;
  lastLogin?: string;
  isActive: boolean;
}
```

### **Exemplos de Uso das APIs**

#### Login
```javascript
// Exemplo de login
const loginUser = async (email, password, rememberMe = false) => {
  const response = await fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password, rememberMe }),
  });
  
  if (!response.ok) {
    throw new Error('Login failed');
  }
  
  return response.json();
};
```

#### Logout
```javascript
// Exemplo de logout
const logoutUser = async (token) => {
  const response = await fetch('/api/v1/auth/logout', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ token }),
  });
  
  if (!response.ok) {
    throw new Error('Logout failed');
  }
  
  return response.json();
};
```

#### Refresh Token
```javascript
// Exemplo de refresh token
const refreshToken = async (refreshToken) => {
  const response = await fetch('/api/v1/auth/refresh', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refreshToken }),
  });
  
  if (!response.ok) {
    throw new Error('Token refresh failed');
  }
  
  return response.json();
};
```

#### Get User Info
```javascript
// Exemplo de busca de informações do usuário
const getUserInfo = async (token) => {
  const response = await fetch('/api/v1/auth/me', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  if (!response.ok) {
    throw new Error('Failed to get user info');
  }
  
  return response.json();
};
```

## 4. Variáveis de Ambiente

### **Configuração Base**
```bash
# .env.local
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_APP_NAME=Concurso AI

# Authentication
NEXTAUTH_SECRET=your-secret-key-here
NEXTAUTH_URL=http://localhost:3000

# Security
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret
NEXT_PUBLIC_REFRESH_TOKEN_SECRET=your-refresh-token-secret

# Development
NODE_ENV=development
```

### **Variáveis de Desenvolvimento**
```bash
# .env.development
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_APP_NAME=Concurso AI (Dev)
NODE_ENV=development
NEXT_PUBLIC_JWT_SECRET=dev-jwt-secret
NEXT_PUBLIC_REFRESH_TOKEN_SECRET=dev-refresh-secret
```

### **Variáveis de Produção**
```bash
# .env.production
NEXT_PUBLIC_API_URL=https://api.concurso-ai.com
NEXT_PUBLIC_APP_NAME=Concurso AI
NODE_ENV=production
NEXTAUTH_URL=https://concurso-ai.com
NEXT_PUBLIC_JWT_SECRET=production-jwt-secret
NEXT_PUBLIC_REFRESH_TOKEN_SECRET=production-refresh-secret
```

### **Variáveis de Teste**
```bash
# .env.test
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_APP_NAME=Concurso AI (Test)
NODE_ENV=test
NEXT_PUBLIC_JWT_SECRET=test-jwt-secret
NEXT_PUBLIC_REFRESH_TOKEN_SECRET=test-refresh-secret
```

### **Configuração de Build**
```bash
# next.config.js
module.exports = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME,
    NEXT_PUBLIC_JWT_SECRET: process.env.NEXT_PUBLIC_JWT_SECRET,
    NEXT_PUBLIC_REFRESH_TOKEN_SECRET: process.env.NEXT_PUBLIC_REFRESH_TOKEN_SECRET,
  },
  // ... outras configurações
}
```

## 5. Limitações e Próximos Passos

### **Limitações Conhecidas**

#### **Funcionalidades**
- **APIs Mock**: Algumas APIs são simuladas com dados estáticos
- **Registro de usuário**: Funcionalidade não implementada
- **Recuperação de senha**: Funcionalidade não implementada
- **Reset de senha**: Funcionalidade não implementada
- **Validação de email**: Validação básica implementada

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

#### **Segurança**
- **HTTPS**: Configuração básica de HTTPS
- **CSP**: Sem Content Security Policy
- **Rate Limiting**: Limitação básica de requisições
- **Input Sanitization**: Sanitização básica de inputs

### **Próximos Passos**

#### **Curto Prazo (Sprint 4)**
1. **Implementar funcionalidades restantes**:
   - Registro de usuário
   - Recuperação de senha
   - Reset de senha
   - Validação de email

2. **Melhorar UX**:
   - Implementar loading states
   - Adicionar error boundaries
   - Melhorar responsividade
   - Adicionar animações básicas

3. **Integração completa**:
   - Conectar com APIs reais
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
1. **Sprint 4**: Sistema de autenticação funcional com mock data
2. **Sprint 5**: Integração com backend real
3. **Sprint 6**: Otimizações de performance
4. **Sprint 7**: Funcionalidades avançadas
5. **Sprint 8**: Deploy e monitoramento

### **Métricas de Sucesso**
- **Funcionalidade**: 100% dos componentes de autenticação funcionais
- **Testes**: 90% de cobertura de código
- **Performance**: < 2s First Contentful Paint
- **Acessibilidade**: WCAG 2.1 AA compliance
- **Responsividade**: Funcional em todos os dispositivos
- **Segurança**: Tokens seguros, validação rigorosa

### **Considerações de Segurança**
- **Armazenamento de tokens**: Cookies seguros com HttpOnly
- **Validação de inputs**: Sanitização e validação rigorosa
- **Proteção contra ataques**: XSS, CSRF, brute force
- **Gerenciamento de sessões**: Timeout adequado, refresh automático
- **Logs de segurança**: Auditoria de tentativas de login

---

**Este documento fornece documentação completa para o sistema de autenticação WEB-002, incluindo instalação, uso, APIs, configuração e roadmap de desenvolvimento.**
