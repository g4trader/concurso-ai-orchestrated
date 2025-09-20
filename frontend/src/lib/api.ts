// API client para conectar com o backend real

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 
  (typeof window !== 'undefined' && window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://concurso-ai-backend-609095880025.us-central1.run.app')

export interface ApiResponse<T> {
  data?: T
  error?: string
  message?: string
}

export class ApiClient {
  private baseURL: string
  private token: string | null = null

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
    this.token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP ${response.status}`)
      }

      const data = await response.json()
      return { data }
    } catch (error) {
      return { 
        error: error instanceof Error ? error.message : 'Erro desconhecido' 
      }
    }
  }

  // Auth endpoints
  async login(email: string, password: string) {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)

    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || 'Erro no login')
    }

    const data = await response.json()
    this.token = data.access_token
    
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', data.access_token)
    }

    return data
  }

  async register(name: string, email: string, password: string) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password }),
    })
  }

  async getCurrentUser() {
    return this.request('/auth/me')
  }

  // Simulado endpoints
  async createSimulado(config: {
    title: string
    config: {
      banca: string
      subjects: string[]
      num_questions: number
      time_limit: number
      level: string
    }
    time_limit: number
    total_questions: number
  }) {
    return this.request('/simulados/', {
      method: 'POST',
      body: JSON.stringify(config),
    })
  }

  async getSimulados() {
    return this.request('/simulados/')
  }

  async getSimulado(id: number) {
    return this.request(`/simulados/${id}`)
  }

  async startSimulado(id: number) {
    return this.request(`/simulados/${id}/start`, {
      method: 'POST',
    })
  }

  async submitSimulado(id: number, answers: Record<string, number>, timeSpent: number, questions?: any[]) {
    // Calcular subject_scores baseado nas questões
    const subjectScores: Record<string, { correct: number; total: number }> = {}
    
    if (questions) {
      questions.forEach(question => {
        const subject = question.subject
        if (!subjectScores[subject]) {
          subjectScores[subject] = { correct: 0, total: 0 }
        }
        subjectScores[subject].total++
        
        // Verificar se a resposta está correta
        const userAnswer = answers[question.id]
        if (userAnswer === question.correct_answer) {
          subjectScores[subject].correct++
        }
      })
    }

    return this.request(`/simulados/${id}/submit`, {
      method: 'POST',
      body: JSON.stringify({
        simulado_id: id,
        answers,
        time_spent: timeSpent,
        subject_scores: subjectScores
      }),
    })
  }

  async getSimuladoResult(id: number) {
    return this.request(`/simulados/${id}/result`)
  }

  // Dashboard endpoints
  async getDashboardStats() {
    return this.request('/dashboard/stats')
  }

  async getRecentResults() {
    return this.request('/dashboard/results')
  }

  // Utility methods
  setToken(token: string) {
    this.token = token
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token)
    }
  }

  clearToken() {
    this.token = null
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token')
    }
  }

  isAuthenticated() {
    return !!this.token
  }
}

// Export singleton instance
export const apiClient = new ApiClient()
