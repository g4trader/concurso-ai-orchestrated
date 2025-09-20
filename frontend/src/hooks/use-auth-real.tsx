'use client'

import { createContext, useContext, useReducer, useEffect, ReactNode } from 'react'
import { apiClient } from '@/lib/api'

interface User {
  id: number
  name: string
  email: string
  is_active: boolean
  created_at: string
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: User }
  | { type: 'LOGIN_FAILURE'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'CLEAR_ERROR' }

const initialState: AuthState = {
  user: null,
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
        user: action.payload,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      }
    case 'LOGIN_FAILURE':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload,
      }
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      }
    case 'CLEAR_ERROR':
      return { ...state, error: null }
    default:
      return state
  }
}

interface AuthContextType {
  state: AuthState
  login: (credentials: { email: string; password: string }) => Promise<void>
  register: (data: { name: string; email: string; password: string }) => Promise<void>
  logout: () => void
  clearError: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, initialState)

  useEffect(() => {
    // Check for existing token on mount
    const token = localStorage.getItem('access_token')
    if (token) {
      // Verify token with backend
      apiClient.getCurrentUser()
        .then(response => {
          if (response.data) {
            dispatch({ type: 'LOGIN_SUCCESS', payload: response.data })
          } else {
            // Token is invalid, clear it
            apiClient.clearToken()
            dispatch({ type: 'LOGOUT' })
          }
        })
        .catch(() => {
          // Token is invalid, clear it
          apiClient.clearToken()
          dispatch({ type: 'LOGOUT' })
        })
    }
  }, [])

  const login = async (credentials: { email: string; password: string }) => {
    dispatch({ type: 'LOGIN_START' })

    try {
      // Try real API first
      const response = await apiClient.login(credentials.email, credentials.password)
      
      if (response.access_token) {
        // Get user data
        const userResponse = await apiClient.getCurrentUser()
        if (userResponse.data) {
          dispatch({ type: 'LOGIN_SUCCESS', payload: userResponse.data })
          return
        }
      }
      
      dispatch({ type: 'LOGIN_FAILURE', payload: 'Credenciais inválidas' })
    } catch {
      dispatch({ type: 'LOGIN_FAILURE', payload: 'Erro de conexão. Verifique se o backend está rodando.' })
    }
  }

  const register = async (data: { name: string; email: string; password: string }) => {
    dispatch({ type: 'LOGIN_START' })

    try {
      const response = await apiClient.register(data.name, data.email, data.password)
      
      if (response.data) {
        // Auto-login after registration
        await login({ email: data.email, password: data.password })
      } else {
        dispatch({ type: 'LOGIN_FAILURE', payload: response.error || 'Erro no registro' })
      }
    } catch {
      dispatch({ type: 'LOGIN_FAILURE', payload: 'Erro de conexão. Verifique se o backend está rodando.' })
    }
  }

  const logout = () => {
    apiClient.clearToken()
    dispatch({ type: 'LOGOUT' })
  }

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' })
  }

  return (
    <AuthContext.Provider value={{ state, login, register, logout, clearError }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
