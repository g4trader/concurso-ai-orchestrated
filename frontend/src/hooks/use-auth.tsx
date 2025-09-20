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

  // Carregar usuário do localStorage na inicialização
  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    const userData = localStorage.getItem('user_data')
    
    if (token && userData) {
      try {
        const user = JSON.parse(userData)
        dispatch({ type: 'LOAD_USER', payload: user })
      } catch {
        // Limpar dados inválidos
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user_data')
      }
    }
  }, [])

  const login = async (credentials: LoginRequest) => {
    dispatch({ type: 'LOGIN_START' })
    
    try {
      // Chamar API real do backend
      const formData = new FormData()
      formData.append('username', credentials.email)
      formData.append('password', credentials.password)

            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 
              (typeof window !== 'undefined' && window.location.hostname === 'localhost' 
                ? 'http://localhost:8000' 
                : 'https://concurso-ai-backend-609095880025.us-central1.run.app')

      const response = await fetch(`${apiUrl}/auth/login`, {
        method: 'POST',
        body: formData,
      })
      
      if (response.ok) {
        const tokenData = await response.json()
        
        // Buscar dados do usuário
        const userResponse = await fetch(`${apiUrl}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${tokenData.access_token}`
          }
        })
        
        if (userResponse.ok) {
          const userData = await userResponse.json()
          
          const data: LoginResponse = {
            user: {
              id: userData.id.toString(),
              name: userData.name || userData.email,
              email: userData.email,
              createdAt: userData.created_at,
              lastLogin: new Date().toISOString()
            },
            token: tokenData.access_token,
            expiresIn: 3600
          }

          // Salvar token no localStorage
          localStorage.setItem('auth_token', tokenData.access_token)
          localStorage.setItem('user_data', JSON.stringify(data.user))
          
          dispatch({ type: 'LOGIN_SUCCESS', payload: data })
          return
        }
      }

      // Se chegou até aqui, credenciais inválidas
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || 'Credenciais inválidas')
      } catch {
        dispatch({ type: 'LOGIN_ERROR', payload: 'Erro de conexão' })
      }
  }

  const logout = () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_data')
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
