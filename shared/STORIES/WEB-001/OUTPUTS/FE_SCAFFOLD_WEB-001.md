# FE_SCAFFOLD_WEB-001: Frontend Scaffolding - Protótipo Web Next.js

## Estrutura de Arquivos Criados

### 1. Configuração Base

#### package.json
```json
{
  "name": "concurso-ai-web",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "dependencies": {
    "next": "14.0.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@types/node": "20.0.0",
    "@types/react": "18.2.0",
    "@types/react-dom": "18.2.0",
    "typescript": "5.0.0",
    "tailwindcss": "3.3.0",
    "autoprefixer": "10.4.0",
    "postcss": "8.4.0",
    "lucide-react": "0.292.0",
    "clsx": "2.0.0",
    "tailwind-merge": "2.0.0"
  },
  "devDependencies": {
    "eslint": "8.0.0",
    "eslint-config-next": "14.0.0",
    "@testing-library/react": "13.4.0",
    "@testing-library/jest-dom": "6.0.0",
    "jest": "29.0.0",
    "jest-environment-jsdom": "29.0.0"
  }
}
```

#### next.config.js
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['localhost'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME || 'Concurso AI',
  },
}

module.exports = nextConfig
```

#### tailwind.config.js
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        secondary: {
          50: '#f8fafc',
          500: '#64748b',
          600: '#475569',
        }
      },
    },
  },
  plugins: [],
}
```

#### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/types/*": ["./src/types/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### 2. Layout Principal

#### src/app/layout.tsx
```typescript
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Header } from '@/components/layout/header'
import { Footer } from '@/components/layout/footer'
import { AuthProvider } from '@/hooks/use-auth'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Concurso AI - Simulados Inteligentes',
  description: 'Plataforma de simulados para concursos públicos com IA',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        <AuthProvider>
          <div className="min-h-screen flex flex-col">
            <Header />
            <main className="flex-1">
              {children}
            </main>
            <Footer />
          </div>
        </AuthProvider>
      </body>
    </html>
  )
}
```

#### src/app/page.tsx
```typescript
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Concurso AI
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Simulados inteligentes para concursos públicos
        </p>
        <div className="space-x-4">
          <Link href="/login">
            <Button size="lg">
              Entrar
            </Button>
          </Link>
          <Link href="/dashboard">
            <Button variant="outline" size="lg">
              Dashboard
            </Button>
          </Link>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-2">
            Simulados Personalizados
          </h3>
          <p className="text-gray-600">
            Questões geradas por IA baseadas no seu perfil de estudo
          </p>
        </Card>
        
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-2">
            Análise de Performance
          </h3>
          <p className="text-gray-600">
            Relatórios detalhados do seu progresso e pontos de melhoria
          </p>
        </Card>
        
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-2">
            Múltiplas Bancas
          </h3>
          <p className="text-gray-600">
            CESPE, FGV, VUNESP e outras bancas organizadoras
          </p>
        </Card>
      </div>
    </div>
  )
}
```

#### src/app/loading.tsx
```typescript
import { Spinner } from '@/components/ui/spinner'

export default function Loading() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <Spinner size="lg" />
    </div>
  )
}
```

#### src/app/error.tsx
```typescript
'use client'

import { useEffect } from 'react'
import { Alert } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div className="container mx-auto px-4 py-8">
      <Alert variant="destructive">
        <h2 className="text-lg font-semibold mb-2">
          Algo deu errado!
        </h2>
        <p className="mb-4">
          Ocorreu um erro inesperado. Tente novamente.
        </p>
        <Button onClick={reset}>
          Tentar novamente
        </Button>
      </Alert>
    </div>
  )
}
```

#### src/app/not-found.tsx
```typescript
import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function NotFound() {
  return (
    <div className="container mx-auto px-4 py-8 text-center">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        404 - Página não encontrada
      </h1>
      <p className="text-xl text-gray-600 mb-8">
        A página que você está procurando não existe.
      </p>
      <Link href="/">
        <Button>
          Voltar ao início
        </Button>
      </Link>
    </div>
  )
}
```

### 3. Páginas Principais

#### src/app/login/page.tsx
```typescript
import { LoginForm } from '@/components/auth/login-form'
import { Card } from '@/components/ui/card'

export default function LoginPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-md mx-auto">
        <Card className="p-6">
          <h1 className="text-2xl font-bold text-center mb-6">
            Entrar
          </h1>
          <LoginForm />
        </Card>
      </div>
    </div>
  )
}
```

#### src/app/login/loading.tsx
```typescript
import { Spinner } from '@/components/ui/spinner'

export default function LoginLoading() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-md mx-auto">
        <div className="flex items-center justify-center p-6">
          <Spinner size="lg" />
        </div>
      </div>
    </div>
  )
}
```

#### src/app/dashboard/page.tsx
```typescript
import { AuthGuard } from '@/components/auth/auth-guard'
import { StatsCard } from '@/components/dashboard/stats-card'
import { RecentSimulados } from '@/components/dashboard/recent-simulados'
import { ProgressChart } from '@/components/dashboard/progress-chart'

export default function DashboardPage() {
  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Dashboard
        </h1>
        
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <StatsCard
            title="Simulados Realizados"
            value="12"
            change="+2 esta semana"
          />
          <StatsCard
            title="Taxa de Acerto"
            value="78%"
            change="+5% este mês"
          />
          <StatsCard
            title="Tempo Médio"
            value="45min"
            change="-3min por simulado"
          />
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          <RecentSimulados />
          <ProgressChart />
        </div>
      </div>
    </AuthGuard>
  )
}
```

#### src/app/gerador-simulado/page.tsx
```typescript
import { AuthGuard } from '@/components/auth/auth-guard'
import { SimuladoForm } from '@/components/simulado/simulado-form'
import { Card } from '@/components/ui/card'

export default function GeradorSimuladoPage() {
  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Gerar Simulado
        </h1>
        
        <Card className="p-6">
          <SimuladoForm />
        </Card>
      </div>
    </AuthGuard>
  )
}
```

#### src/app/resultados/page.tsx
```typescript
import { AuthGuard } from '@/components/auth/auth-guard'
import { ScoreDisplay } from '@/components/resultados/score-display'
import { QuestionReview } from '@/components/resultados/question-review'
import { PerformanceChart } from '@/components/resultados/performance-chart'

export default function ResultadosPage() {
  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Resultados
        </h1>
        
        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-1">
            <ScoreDisplay />
          </div>
          <div className="lg:col-span-2">
            <PerformanceChart />
          </div>
        </div>

        <QuestionReview />
      </div>
    </AuthGuard>
  )
}
```

### 4. Componentes UI Base

#### src/components/ui/button.tsx
```typescript
import { ButtonHTMLAttributes, forwardRef } from 'react'
import { clsx } from 'clsx'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost' | 'destructive'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'md', loading, children, ...props }, ref) => {
    return (
      <button
        className={clsx(
          'inline-flex items-center justify-center rounded-md font-medium transition-colors',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
          'disabled:pointer-events-none disabled:opacity-50',
          {
            'bg-primary-600 text-white hover:bg-primary-700': variant === 'default',
            'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50': variant === 'outline',
            'text-gray-700 hover:bg-gray-100': variant === 'ghost',
            'bg-red-600 text-white hover:bg-red-700': variant === 'destructive',
          },
          {
            'h-8 px-3 text-sm': size === 'sm',
            'h-10 px-4': size === 'md',
            'h-12 px-6 text-lg': size === 'lg',
          },
          className
        )}
        ref={ref}
        disabled={loading}
        {...props}
      >
        {loading && <Spinner size="sm" className="mr-2" />}
        {children}
      </button>
    )
  }
)
```

#### src/components/ui/card.tsx
```typescript
import { HTMLAttributes, forwardRef } from 'react'
import { clsx } from 'clsx'

interface CardProps extends HTMLAttributes<HTMLDivElement> {}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={clsx(
          'rounded-lg border border-gray-200 bg-white shadow-sm',
          className
        )}
        {...props}
      />
    )
  }
)
```

#### src/components/ui/spinner.tsx
```typescript
import { HTMLAttributes } from 'react'
import { clsx } from 'clsx'

interface SpinnerProps extends HTMLAttributes<HTMLDivElement> {
  size?: 'sm' | 'md' | 'lg'
}

export function Spinner({ className, size = 'md', ...props }: SpinnerProps) {
  return (
    <div
      className={clsx(
        'animate-spin rounded-full border-2 border-gray-300 border-t-primary-600',
        {
          'h-4 w-4': size === 'sm',
          'h-6 w-6': size === 'md',
          'h-8 w-8': size === 'lg',
        },
        className
      )}
      {...props}
    />
  )
}
```

### 5. Componentes de Layout

#### src/components/layout/header.tsx
```typescript
'use client'

import Link from 'next/link'
import { useAuth } from '@/hooks/use-auth'
import { LogoutButton } from '@/components/auth/logout-button'

export function Header() {
  const { user, isAuthenticated } = useAuth()

  return (
    <header className="bg-white border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="text-xl font-bold text-primary-600">
            Concurso AI
          </Link>
          
          <nav className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Link href="/dashboard" className="text-gray-700 hover:text-primary-600">
                  Dashboard
                </Link>
                <Link href="/gerador-simulado" className="text-gray-700 hover:text-primary-600">
                  Simulados
                </Link>
                <span className="text-gray-600">
                  Olá, {user?.name}
                </span>
                <LogoutButton />
              </>
            ) : (
              <Link href="/login" className="text-gray-700 hover:text-primary-600">
                Entrar
              </Link>
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}
```

#### src/components/layout/footer.tsx
```typescript
export function Footer() {
  return (
    <footer className="bg-gray-50 border-t border-gray-200">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-gray-600">
          <p>&copy; 2024 Concurso AI. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  )
}
```

### 6. Hooks e Context

#### src/hooks/use-auth.tsx
```typescript
'use client'

import { createContext, useContext, useReducer, useEffect } from 'react'
import { User, LoginRequest, LoginResponse } from '@/types/auth'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: LoginResponse }
  | { type: 'LOGIN_ERROR'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'LOAD_USER'; payload: User }

const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
}

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, isLoading: true, error: null }
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        isLoading: false,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        error: null,
      }
    case 'LOGIN_ERROR':
      return {
        ...state,
        isLoading: false,
        error: action.payload,
      }
    case 'LOGOUT':
      return initialState
    case 'LOAD_USER':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
      }
    default:
      return state
  }
}

const AuthContext = createContext<{
  state: AuthState
  login: (credentials: LoginRequest) => Promise<void>
  logout: () => void
} | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, initialState)

  const login = async (credentials: LoginRequest) => {
    dispatch({ type: 'LOGIN_START' })
    
    try {
      // TODO: Implementar chamada real da API
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      })
      
      if (!response.ok) {
        throw new Error('Credenciais inválidas')
      }
      
      const data: LoginResponse = await response.json()
      dispatch({ type: 'LOGIN_SUCCESS', payload: data })
    } catch (error) {
      dispatch({ type: 'LOGIN_ERROR', payload: error.message })
    }
  }

  const logout = () => {
    dispatch({ type: 'LOGOUT' })
  }

  return (
    <AuthContext.Provider value={{ state, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de AuthProvider')
  }
  return context
}
```

### 7. Tipos TypeScript

#### src/types/auth.ts
```typescript
export interface User {
  id: string
  email: string
  name: string
  avatar?: string
  createdAt: string
  lastLogin?: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  user: User
  token: string
  expiresIn: number
}
```

#### src/types/simulado.ts
```typescript
export interface Simulado {
  id: string
  title: string
  description: string
  banca: 'CESPE' | 'FGV' | 'VUNESP' | 'FCC'
  ano: number
  topico: string
  totalQuestions: number
  timeLimit: number
  createdAt: string
  status: 'draft' | 'active' | 'completed' | 'expired'
}

export interface Question {
  id: string
  simuladoId: string
  question: string
  alternatives: {
    A: string
    B: string
    C: string
    D: string
    E: string
  }
  correctAnswer: 'A' | 'B' | 'C' | 'D' | 'E'
  explanation?: string
  difficulty: 'easy' | 'medium' | 'hard'
  topic: string
}
```

### 8. Variáveis de Ambiente

#### .env.example
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Concurso AI

# Authentication
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3000

# Database (futuro)
DATABASE_URL=postgresql://user:password@localhost:5432/concurso_ai

# External Services (futuro)
OPENAI_API_KEY=your-openai-key
```

### 9. README de Rotas

#### ROUTES.md
```markdown
# Rotas da Aplicação

## Páginas Públicas
- `/` - Página inicial com apresentação da plataforma
- `/login` - Página de login/autenticação

## Páginas Protegidas (requer autenticação)
- `/dashboard` - Dashboard principal com estatísticas
- `/gerador-simulado` - Formulário para gerar novos simulados
- `/resultados` - Visualização de resultados de simulados

## Estados de Loading
- Todas as páginas possuem `loading.tsx` para estados de carregamento
- Componente `Spinner` reutilizável para indicadores de loading

## Tratamento de Erros
- `error.tsx` global para captura de erros
- `not-found.tsx` para páginas não encontradas
- Componente `Alert` para exibição de mensagens de erro

## Variáveis de Ambiente
- `NEXT_PUBLIC_API_URL` - URL base da API backend
- `NEXT_PUBLIC_APP_NAME` - Nome da aplicação
- `NEXTAUTH_SECRET` - Chave secreta para autenticação
- `NEXTAUTH_URL` - URL base da aplicação

## Componentes Reutilizáveis
- `Button` - Botão com variantes e estados
- `Card` - Container com bordas e sombra
- `Spinner` - Indicador de carregamento
- `Alert` - Mensagens de feedback
- `Input` - Campo de entrada de texto
- `Modal` - Janela modal

## Hooks Customizados
- `useAuth` - Gerenciamento de autenticação
- `useSimulado` - Gerenciamento de simulados
- `useLocalStorage` - Persistência local
```

---

**Este documento define o scaffolding completo do frontend WEB-001, incluindo estrutura Next.js, componentes, rotas, tipos e configurações.**
