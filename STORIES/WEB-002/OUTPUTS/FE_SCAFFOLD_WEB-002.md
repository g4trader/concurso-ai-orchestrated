# FE_SCAFFOLD_WEB-002: Frontend Scaffolding - Autenticação Simples

## Estrutura de Arquivos Criados

### 1. Configuração Base

#### package.json
```json
{
  "name": "concurso-ai-auth",
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
    "tailwind-merge": "2.0.0",
    "react-hook-form": "7.47.0",
    "@hookform/resolvers": "3.3.0",
    "zod": "3.22.0",
    "axios": "1.6.0",
    "js-cookie": "3.0.5",
    "@types/js-cookie": "3.0.6"
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
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001',
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME || 'Concurso AI',
  },
}

module.exports = nextConfig
```

### 2. Componentes de Autenticação

#### src/components/auth/login-form.tsx
```typescript
'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuth } from '@/hooks/use-auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Alert } from '@/components/ui/alert'
import { Spinner } from '@/components/ui/spinner'

const loginSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(8, 'Senha deve ter pelo menos 8 caracteres'),
  rememberMe: z.boolean().optional(),
})

type LoginFormData = z.infer<typeof loginSchema>

export function LoginForm() {
  const [isLoading, setIsLoading] = useState(false)
  const { login, error, clearError } = useAuth()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true)
    clearError()
    
    try {
      await login(data)
    } catch (err) {
      console.error('Login error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {error && (
        <Alert variant="destructive">
          {error}
        </Alert>
      )}
      
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700">
          Email
        </label>
        <Input
          id="email"
          type="email"
          {...register('email')}
          className="mt-1"
          placeholder="seu@email.com"
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700">
          Senha
        </label>
        <Input
          id="password"
          type="password"
          {...register('password')}
          className="mt-1"
          placeholder="Sua senha"
        />
        {errors.password && (
          <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
        )}
      </div>

      <div className="flex items-center">
        <input
          id="rememberMe"
          type="checkbox"
          {...register('rememberMe')}
          className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
        />
        <label htmlFor="rememberMe" className="ml-2 block text-sm text-gray-700">
          Lembrar de mim
        </label>
      </div>

      <Button
        type="submit"
        className="w-full"
        disabled={isLoading}
      >
        {isLoading ? (
          <>
            <Spinner size="sm" className="mr-2" />
            Entrando...
          </>
        ) : (
          'Entrar'
        )}
      </Button>
    </form>
  )
}
```

#### src/components/auth/logout-button.tsx
```typescript
'use client'

import { useState } from 'react'
import { useAuth } from '@/hooks/use-auth'
import { Button } from '@/components/ui/button'
import { Spinner } from '@/components/ui/spinner'

interface LogoutButtonProps {
  variant?: 'default' | 'outline' | 'ghost' | 'destructive'
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function LogoutButton({ 
  variant = 'outline', 
  size = 'md',
  className 
}: LogoutButtonProps) {
  const [isLoading, setIsLoading] = useState(false)
  const { logout } = useAuth()

  const handleLogout = async () => {
    setIsLoading(true)
    
    try {
      await logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Button
      variant={variant}
      size={size}
      onClick={handleLogout}
      disabled={isLoading}
      className={className}
    >
      {isLoading ? (
        <>
          <Spinner size="sm" className="mr-2" />
          Saindo...
        </>
      ) : (
        'Sair'
      )}
    </Button>
  )
}
```

#### src/components/auth/auth-guard.tsx
```typescript
'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/use-auth'
import { Spinner } from '@/components/ui/spinner'

interface AuthGuardProps {
  children: React.ReactNode
  fallback?: React.ReactNode
}

export function AuthGuard({ children, fallback }: AuthGuardProps) {
  const { isAuthenticated, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, isLoading, router])

  if (isLoading) {
    return fallback || (
      <div className="flex items-center justify-center min-h-screen">
        <Spinner size="lg" />
      </div>
    )
  }

  if (!isAuthenticated) {
    return null
  }

  return <>{children}</>
}
```

#### src/components/auth/protected-route.tsx
```typescript
'use client'

import { useAuth } from '@/hooks/use-auth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

interface ProtectedRouteProps {
  children: React.ReactNode
  redirectTo?: string
}

export function ProtectedRoute({ 
  children, 
  redirectTo = '/login' 
}: ProtectedRouteProps) {
  const { isAuthenticated, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push(redirectTo)
    }
  }, [isAuthenticated, isLoading, router, redirectTo])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Spinner size="lg" />
      </div>
    )
  }

  if (!isAuthenticated) {
    return null
  }

  return <>{children}</>
}
```

#### src/components/auth/password-input.tsx
```typescript
'use client'

import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Eye, EyeOff } from 'lucide-react'

interface PasswordInputProps {
  id?: string
  name?: string
  placeholder?: string
  value?: string
  onChange?: (value: string) => void
  error?: string
  className?: string
}

export function PasswordInput({
  id,
  name,
  placeholder = 'Sua senha',
  value,
  onChange,
  error,
  className,
}: PasswordInputProps) {
  const [showPassword, setShowPassword] = useState(false)

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword)
  }

  return (
    <div className="relative">
      <Input
        id={id}
        name={name}
        type={showPassword ? 'text' : 'password'}
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        className={`pr-10 ${className}`}
      />
      <Button
        type="button"
        variant="ghost"
        size="sm"
        className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
        onClick={togglePasswordVisibility}
      >
        {showPassword ? (
          <EyeOff className="h-4 w-4" />
        ) : (
          <Eye className="h-4 w-4" />
        )}
      </Button>
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  )
}
```

### 3. Hooks de Autenticação

#### src/hooks/use-auth.ts
```typescript
'use client'

import { createContext, useContext, useReducer, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { User, LoginRequest, AuthState } from '@/types/auth'
import { authService } from '@/services/auth-service'
import { tokenService } from '@/services/token-service'

type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: { user: User; token: string; refreshToken: string } }
  | { type: 'LOGIN_ERROR'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'CLEAR_ERROR' }
  | { type: 'UPDATE_USER'; payload: Partial<User> }

const initialState: AuthState = {
  user: null,
  token: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
  lastActivity: Date.now(),
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
        refreshToken: action.payload.refreshToken,
        isAuthenticated: true,
        error: null,
        lastActivity: Date.now(),
      }
    case 'LOGIN_ERROR':
      return {
        ...state,
        isLoading: false,
        error: action.payload,
      }
    case 'LOGOUT':
      return {
        ...initialState,
        lastActivity: Date.now(),
      }
    case 'CLEAR_ERROR':
      return { ...state, error: null }
    case 'UPDATE_USER':
      return {
        ...state,
        user: state.user ? { ...state.user, ...action.payload } : null,
      }
    default:
      return state
  }
}

const AuthContext = createContext<{
  state: AuthState
  login: (credentials: LoginRequest) => Promise<void>
  logout: () => Promise<void>
  refreshToken: () => Promise<void>
  clearError: () => void
  updateUser: (user: Partial<User>) => void
} | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, initialState)
  const router = useRouter()

  const login = async (credentials: LoginRequest) => {
    dispatch({ type: 'LOGIN_START' })
    
    try {
      const response = await authService.login(credentials)
      
      // Store tokens
      tokenService.setToken(response.token)
      tokenService.setRefreshToken(response.refreshToken)
      
      dispatch({ 
        type: 'LOGIN_SUCCESS', 
        payload: { 
          user: response.user, 
          token: response.token,
          refreshToken: response.refreshToken
        } 
      })
      
      // Redirect to dashboard
      router.push('/dashboard')
    } catch (error: any) {
      dispatch({ type: 'LOGIN_ERROR', payload: error.message })
    }
  }

  const logout = async () => {
    try {
      if (state.token) {
        await authService.logout({ token: state.token })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear tokens
      tokenService.clearTokens()
      
      dispatch({ type: 'LOGOUT' })
      
      // Redirect to login
      router.push('/login')
    }
  }

  const refreshToken = async () => {
    try {
      const refreshToken = tokenService.getRefreshToken()
      if (!refreshToken) {
        throw new Error('No refresh token available')
      }

      const response = await authService.refreshToken({ refreshToken })
      
      // Update tokens
      tokenService.setToken(response.token)
      tokenService.setRefreshToken(response.refreshToken)
      
      dispatch({ 
        type: 'LOGIN_SUCCESS', 
        payload: { 
          user: state.user!, 
          token: response.token,
          refreshToken: response.refreshToken
        } 
      })
    } catch (error) {
      console.error('Token refresh error:', error)
      logout()
    }
  }

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' })
  }

  const updateUser = (user: Partial<User>) => {
    dispatch({ type: 'UPDATE_USER', payload: user })
  }

  // Check for existing token on mount
  useEffect(() => {
    const token = tokenService.getToken()
    if (token) {
      // Validate token and get user info
      authService.getMe()
        .then((user) => {
          dispatch({ 
            type: 'LOGIN_SUCCESS', 
            payload: { 
              user, 
              token,
              refreshToken: tokenService.getRefreshToken() || ''
            } 
          })
        })
        .catch(() => {
          tokenService.clearTokens()
        })
    }
  }, [])

  return (
    <AuthContext.Provider value={{ 
      state, 
      login, 
      logout, 
      refreshToken, 
      clearError, 
      updateUser 
    }}>
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

#### src/hooks/use-login.ts
```typescript
'use client'

import { useState } from 'react'
import { useAuth } from './use-auth'
import { LoginRequest } from '@/types/auth'

export function useLogin() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { login } = useAuth()

  const handleLogin = async (credentials: LoginRequest) => {
    setIsLoading(true)
    setError(null)
    
    try {
      await login(credentials)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return {
    login: handleLogin,
    isLoading,
    error,
    clearError: () => setError(null),
  }
}
```

#### src/hooks/use-logout.ts
```typescript
'use client'

import { useState } from 'react'
import { useAuth } from './use-auth'

export function useLogout() {
  const [isLoading, setIsLoading] = useState(false)
  const { logout } = useAuth()

  const handleLogout = async () => {
    setIsLoading(true)
    
    try {
      await logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return {
    logout: handleLogout,
    isLoading,
  }
}
```

#### src/hooks/use-token.ts
```typescript
'use client'

import { useState, useEffect } from 'react'
import { tokenService } from '@/services/token-service'

export function useToken() {
  const [token, setToken] = useState<string | null>(null)
  const [refreshToken, setRefreshToken] = useState<string | null>(null)

  useEffect(() => {
    setToken(tokenService.getToken())
    setRefreshToken(tokenService.getRefreshToken())
  }, [])

  const updateToken = (newToken: string) => {
    tokenService.setToken(newToken)
    setToken(newToken)
  }

  const updateRefreshToken = (newRefreshToken: string) => {
    tokenService.setRefreshToken(newRefreshToken)
    setRefreshToken(newRefreshToken)
  }

  const clearTokens = () => {
    tokenService.clearTokens()
    setToken(null)
    setRefreshToken(null)
  }

  return {
    token,
    refreshToken,
    updateToken,
    updateRefreshToken,
    clearTokens,
  }
}
```

### 4. Serviços

#### src/services/auth-service.ts
```typescript
import { apiClient } from './api-client'
import { 
  LoginRequest, 
  LoginResponse, 
  LogoutRequest, 
  LogoutResponse,
  RefreshTokenRequest,
  RefreshTokenResponse,
  User 
} from '@/types/auth'

export const authService = {
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await apiClient.post('/auth/login', credentials)
    return response.data
  },

  async logout(request: LogoutRequest): Promise<LogoutResponse> {
    const response = await apiClient.post('/auth/logout', request)
    return response.data
  },

  async refreshToken(request: RefreshTokenRequest): Promise<RefreshTokenResponse> {
    const response = await apiClient.post('/auth/refresh', request)
    return response.data
  },

  async getMe(): Promise<User> {
    const response = await apiClient.get('/auth/me')
    return response.data
  },

  async register(userData: any): Promise<LoginResponse> {
    const response = await apiClient.post('/auth/register', userData)
    return response.data
  },

  async forgotPassword(email: string): Promise<{ message: string }> {
    const response = await apiClient.post('/auth/forgot-password', { email })
    return response.data
  },

  async resetPassword(token: string, newPassword: string): Promise<{ message: string }> {
    const response = await apiClient.post('/auth/reset-password', { 
      token, 
      new_password: newPassword 
    })
    return response.data
  },
}
```

#### src/services/token-service.ts
```typescript
import Cookies from 'js-cookie'

const TOKEN_KEY = 'auth_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

export const tokenService = {
  getToken(): string | null {
    if (typeof window === 'undefined') return null
    return Cookies.get(TOKEN_KEY) || null
  },

  setToken(token: string): void {
    if (typeof window === 'undefined') return
    Cookies.set(TOKEN_KEY, token, { 
      expires: 7, // 7 days
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict'
    })
  },

  getRefreshToken(): string | null {
    if (typeof window === 'undefined') return null
    return Cookies.get(REFRESH_TOKEN_KEY) || null
  },

  setRefreshToken(refreshToken: string): void {
    if (typeof window === 'undefined') return
    Cookies.set(REFRESH_TOKEN_KEY, refreshToken, { 
      expires: 30, // 30 days
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict'
    })
  },

  clearTokens(): void {
    if (typeof window === 'undefined') return
    Cookies.remove(TOKEN_KEY)
    Cookies.remove(REFRESH_TOKEN_KEY)
  },

  isTokenExpired(token: string): boolean {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return payload.exp * 1000 < Date.now()
    } catch {
      return true
    }
  },
}
```

#### src/services/api-client.ts
```typescript
import axios from 'axios'
import { tokenService } from './token-service'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = tokenService.getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = tokenService.getRefreshToken()
        if (refreshToken) {
          const response = await apiClient.post('/auth/refresh', { refreshToken })
          const { token, refresh_token } = response.data

          tokenService.setToken(token)
          tokenService.setRefreshToken(refresh_token)

          originalRequest.headers.Authorization = `Bearer ${token}`
          return apiClient(originalRequest)
        }
      } catch (refreshError) {
        tokenService.clearTokens()
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)
```

### 5. Tipos TypeScript

#### src/types/auth.ts
```typescript
export interface User {
  id: string
  email: string
  name: string
  avatar?: string
  createdAt: string
  lastLogin?: string
  isActive: boolean
}

export interface LoginRequest {
  email: string
  password: string
  rememberMe?: boolean
}

export interface LoginResponse {
  user: User
  token: string
  refreshToken: string
  expiresIn: number
  tokenType: 'Bearer'
}

export interface LogoutRequest {
  token: string
}

export interface LogoutResponse {
  message: string
  success: boolean
}

export interface RefreshTokenRequest {
  refreshToken: string
}

export interface RefreshTokenResponse {
  token: string
  refreshToken: string
  expiresIn: number
}

export interface AuthState {
  user: User | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  lastActivity: number
}
```

### 6. Páginas

#### src/pages/login/index.tsx
```typescript
import { LoginForm } from '@/components/auth/login-form'
import { Card } from '@/components/ui/card'
import Link from 'next/link'

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Entre na sua conta
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Ou{' '}
            <Link href="/register" className="font-medium text-primary-600 hover:text-primary-500">
              crie uma nova conta
            </Link>
          </p>
        </div>
        
        <Card className="p-6">
          <LoginForm />
        </Card>
      </div>
    </div>
  )
}
```

#### src/pages/dashboard/index.tsx
```typescript
import { AuthGuard } from '@/components/auth/auth-guard'
import { LogoutButton } from '@/components/auth/logout-button'
import { useAuth } from '@/hooks/use-auth'

export default function DashboardPage() {
  const { state } = useAuth()

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        <div className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Dashboard
                </h1>
                <p className="text-gray-600">
                  Bem-vindo, {state.user?.name}!
                </p>
              </div>
              <LogoutButton />
            </div>
          </div>
        </div>
        
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 flex items-center justify-center">
              <p className="text-gray-500">
                Conteúdo do dashboard será implementado aqui
              </p>
            </div>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}
```

### 7. Variáveis de Ambiente

#### .env.example
```bash
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

### 8. README de Rotas

#### ROUTES.md
```markdown
# Rotas da Aplicação - Autenticação

## Páginas Públicas
- `/login` - Página de login
- `/register` - Página de registro (futuro)
- `/forgot-password` - Recuperação de senha (futuro)
- `/reset-password` - Reset de senha (futuro)

## Páginas Protegidas (requer autenticação)
- `/dashboard` - Dashboard principal
- `/profile` - Perfil do usuário (futuro)
- `/settings` - Configurações (futuro)

## Componentes de Autenticação
- `LoginForm` - Formulário de login
- `LogoutButton` - Botão de logout
- `AuthGuard` - Proteção de rotas
- `ProtectedRoute` - Rota protegida
- `PasswordInput` - Input de senha com toggle

## Hooks de Autenticação
- `useAuth` - Hook principal de autenticação
- `useLogin` - Hook para login
- `useLogout` - Hook para logout
- `useToken` - Hook para gerenciamento de tokens

## Serviços
- `authService` - Serviço de autenticação
- `tokenService` - Gerenciamento de tokens
- `apiClient` - Cliente HTTP com interceptors

## Variáveis de Ambiente
- `NEXT_PUBLIC_API_URL` - URL base da API
- `NEXT_PUBLIC_APP_NAME` - Nome da aplicação
- `NEXTAUTH_SECRET` - Chave secreta para autenticação
- `NEXTAUTH_URL` - URL base da aplicação
- `NEXT_PUBLIC_JWT_SECRET` - Chave secreta do JWT
- `NEXT_PUBLIC_REFRESH_TOKEN_SECRET` - Chave secreta do refresh token

## Fluxo de Autenticação
1. Usuário acessa página protegida
2. AuthGuard verifica se está autenticado
3. Se não estiver, redireciona para /login
4. Usuário faz login
5. Token é armazenado em cookies
6. Usuário é redirecionado para /dashboard
7. API client adiciona token automaticamente
8. Token é renovado automaticamente quando expira
```

---

**Este documento define o scaffolding completo do frontend WEB-002, incluindo componentes de autenticação, hooks, serviços, tipos e páginas.**
