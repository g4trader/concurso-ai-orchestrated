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
