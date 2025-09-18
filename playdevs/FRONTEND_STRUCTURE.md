# 🎨 Estrutura Frontend - Concurso-AI

## Visão Geral
Estrutura completa para desenvolvimento frontend do projeto Concurso-AI Orchestrated.

## Tecnologias Principais

### **Core Stack**
- **Next.js 14** - Framework React com App Router
- **React 18** - Biblioteca de UI
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Framework CSS utilitário

### **UI/UX**
- **Headless UI** - Componentes acessíveis
- **Heroicons** - Biblioteca de ícones
- **Framer Motion** - Animações
- **React Hook Form** - Gerenciamento de formulários

### **Estado e Dados**
- **Zustand** - Gerenciamento de estado global
- **React Query** - Cache e sincronização de dados
- **Axios** - Cliente HTTP

## Estrutura de Pastas

```
src/
├── app/                    # App Router (Next.js 14)
│   ├── (auth)/            # Grupo de rotas de autenticação
│   │   ├── login/         # Página de login
│   │   └── register/      # Página de registro
│   ├── (dashboard)/       # Grupo de rotas do dashboard
│   │   ├── dashboard/     # Dashboard principal
│   │   ├── simulados/     # Geração de simulados
│   │   └── resultados/    # Resultados e relatórios
│   ├── globals.css        # Estilos globais
│   ├── layout.tsx         # Layout raiz
│   └── page.tsx           # Página inicial
├── components/            # Componentes reutilizáveis
│   ├── ui/               # Componentes base
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Modal.tsx
│   │   └── index.ts
│   ├── forms/            # Componentes de formulário
│   │   ├── LoginForm.tsx
│   │   ├── SimuladoForm.tsx
│   │   └── index.ts
│   ├── layout/           # Componentes de layout
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   ├── Footer.tsx
│   │   └── index.ts
│   ├── features/         # Componentes específicos
│   │   ├── auth/         # Autenticação
│   │   ├── simulados/    # Simulados
│   │   ├── dashboard/    # Dashboard
│   │   └── index.ts
│   └── index.ts
├── hooks/                # Custom hooks
│   ├── useAuth.ts
│   ├── useSimulados.ts
│   ├── useLocalStorage.ts
│   └── index.ts
├── lib/                  # Configurações e utilitários
│   ├── auth.ts          # Configuração de autenticação
│   ├── api.ts           # Cliente API
│   ├── utils.ts         # Funções utilitárias
│   ├── validations.ts   # Validações de formulário
│   └── constants.ts     # Constantes da aplicação
├── types/               # Definições TypeScript
│   ├── auth.ts
│   ├── simulados.ts
│   ├── api.ts
│   └── index.ts
├── stores/              # Stores Zustand
│   ├── authStore.ts
│   ├── simuladosStore.ts
│   └── index.ts
└── styles/              # Estilos adicionais
    ├── components.css
    └── utilities.css
```

## Componentes por História

### **WEB-001: Protótipo Web**
```
components/
├── layout/
│   ├── Header.tsx           # Cabeçalho com navegação
│   ├── Sidebar.tsx          # Menu lateral
│   ├── Footer.tsx           # Rodapé
│   └── Layout.tsx           # Layout principal
├── ui/
│   ├── Button.tsx           # Botão base
│   ├── Input.tsx            # Input base
│   ├── Card.tsx             # Card base
│   └── Loading.tsx          # Componente de loading
└── features/
    ├── auth/
    │   ├── LoginForm.tsx    # Formulário de login
    │   └── RegisterForm.tsx # Formulário de registro
    └── dashboard/
        ├── StatsCard.tsx    # Card de estatísticas
        └── RecentActivity.tsx # Atividade recente
```

### **WEB-002: Autenticação**
```
components/
├── auth/
│   ├── LoginForm.tsx        # Formulário de login
│   ├── RegisterForm.tsx     # Formulário de registro
│   ├── ForgotPassword.tsx   # Recuperação de senha
│   ├── AuthGuard.tsx        # Proteção de rotas
│   └── AuthProvider.tsx     # Provider de autenticação
├── hooks/
│   └── useAuth.ts           # Hook de autenticação
└── lib/
    └── auth.ts              # Configuração de auth
```

### **WEB-003: Geração de Simulados**
```
components/
├── simulados/
│   ├── SimuladoForm.tsx     # Formulário de configuração
│   ├── SimuladoCard.tsx     # Card do simulado
│   ├── QuestionCard.tsx     # Card da questão
│   ├── AnswerOptions.tsx    # Opções de resposta
│   └── SimuladoProgress.tsx # Barra de progresso
├── hooks/
│   └── useSimulados.ts      # Hook de simulados
└── types/
    └── simulados.ts         # Tipos de simulado
```

### **WEB-004: Relatórios**
```
components/
├── relatorios/
│   ├── RelatorioCard.tsx    # Card do relatório
│   ├── GraficoPerformance.tsx # Gráfico de performance
│   ├── TabelaResultados.tsx # Tabela de resultados
│   ├── Estatisticas.tsx     # Estatísticas gerais
│   └── ExportButton.tsx     # Botão de exportação
├── hooks/
│   └── useRelatorios.ts     # Hook de relatórios
└── lib/
    └── export.ts            # Funções de exportação
```

## Padrões de Design

### **Design System**
```typescript
// Cores
const colors = {
  primary: {
    50: '#eff6ff',
    500: '#3b82f6',
    900: '#1e3a8a',
  },
  secondary: {
    50: '#f8fafc',
    500: '#64748b',
    900: '#0f172a',
  },
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
};

// Tipografia
const typography = {
  fontFamily: {
    sans: ['Inter', 'system-ui', 'sans-serif'],
    mono: ['JetBrains Mono', 'monospace'],
  },
  fontSize: {
    xs: '0.75rem',
    sm: '0.875rem',
    base: '1rem',
    lg: '1.125rem',
    xl: '1.25rem',
    '2xl': '1.5rem',
    '3xl': '1.875rem',
  },
};

// Espaçamentos
const spacing = {
  xs: '0.25rem',
  sm: '0.5rem',
  md: '1rem',
  lg: '1.5rem',
  xl: '2rem',
  '2xl': '3rem',
};
```

### **Componentes Base**
```typescript
// Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  children,
  onClick,
}) => {
  const baseClasses = 'font-medium rounded-lg transition-colors focus:outline-none focus:ring-2';
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500',
    outline: 'border border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-blue-500',
  };
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
      onClick={onClick}
      disabled={loading}
    >
      {loading ? 'Carregando...' : children}
    </button>
  );
};
```

## Integração com Backend

### **API Client**
```typescript
// lib/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para autenticação
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const apiClient = {
  // Auth
  login: (credentials: LoginCredentials) => api.post('/auth/login', credentials),
  register: (userData: RegisterData) => api.post('/auth/register', userData),
  logout: () => api.post('/auth/logout'),
  
  // Simulados
  createSimulado: (config: SimuladoConfig) => api.post('/simulados', config),
  getSimulados: () => api.get('/simulados'),
  getSimulado: (id: string) => api.get(`/simulados/${id}`),
  submitSimulado: (id: string, answers: Answer[]) => api.post(`/simulados/${id}/submit`, answers),
  
  // Relatórios
  getRelatorios: () => api.get('/relatorios'),
  getRelatorio: (id: string) => api.get(`/relatorios/${id}`),
};
```

### **Estado Global**
```typescript
// stores/authStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  updateUser: (user: User) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      
      login: async (credentials) => {
        try {
          const response = await apiClient.login(credentials);
          set({
            user: response.data.user,
            token: response.data.token,
            isAuthenticated: true,
          });
        } catch (error) {
          throw error;
        }
      },
      
      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
        localStorage.removeItem('auth_token');
      },
      
      updateUser: (user) => {
        set({ user });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
```

## Testes

### **Configuração Jest**
```javascript
// jest.config.js
const nextJest = require('next/jest');

const createJestConfig = nextJest({
  dir: './',
});

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  testEnvironment: 'jest-environment-jsdom',
};

module.exports = createJestConfig(customJestConfig);
```

### **Teste de Componente**
```typescript
// __tests__/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '@/components/ui/Button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('shows loading state', () => {
    render(<Button loading>Click me</Button>);
    expect(screen.getByText('Carregando...')).toBeInTheDocument();
  });
});
```

## Deploy e Build

### **Scripts Package.json**
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "analyze": "cross-env ANALYZE=true next build"
  }
}
```

### **Variáveis de Ambiente**
```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_APP_NAME=Concurso-AI
NEXT_PUBLIC_VERSION=1.0.0
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=GA_MEASUREMENT_ID
```

---

**Esta estrutura fornece uma base sólida para o desenvolvimento frontend do projeto Concurso-AI, seguindo as melhores práticas de Next.js, React e TypeScript.**
