'use client'

import { createContext, useContext, useReducer } from 'react'
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
      // Credenciais padrão para demonstração
      const DEFAULT_CREDENTIALS = {
        email: 'admin@concursoai.com',
        password: 'admin123'
      }

      // Verificar credenciais localmente (fallback)
      if (credentials.email === DEFAULT_CREDENTIALS.email && credentials.password === DEFAULT_CREDENTIALS.password) {
        const user = {
          id: '1',
          name: 'Administrador',
          email: 'admin@concursoai.com',
          createdAt: new Date().toISOString(),
          lastLogin: new Date().toISOString()
        }

        const data: LoginResponse = {
          user,
          token: 'demo-token-12345',
          expiresIn: 3600
        }

        dispatch({ type: 'LOGIN_SUCCESS', payload: data })
        return
      }

      // Tentar chamada da API
      try {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(credentials),
        })
        
        if (response.ok) {
          const data: LoginResponse = await response.json()
          dispatch({ type: 'LOGIN_SUCCESS', payload: data })
          return
        }
      } catch {
        console.log('API não disponível, usando autenticação local')
      }

      // Se chegou até aqui, credenciais inválidas
      throw new Error('Credenciais inválidas')
    } catch (error) {
      dispatch({ type: 'LOGIN_ERROR', payload: error instanceof Error ? error.message : 'Erro desconhecido' })
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
