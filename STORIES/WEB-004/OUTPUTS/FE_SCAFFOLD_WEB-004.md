# FE_SCAFFOLD_WEB-004: Frontend Scaffolding - Relatório Pós-Simulado

## Estrutura de Arquivos Criados

### 1. Configuração Base

#### package.json
```json
{
  "name": "concurso-ai-results",
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
    "chart.js": "4.4.0",
    "react-chartjs-2": "5.2.0",
    "recharts": "2.8.0",
    "axios": "1.6.0",
    "js-cookie": "3.0.5",
    "@types/js-cookie": "3.0.6",
    "react-query": "3.39.0",
    "swr": "2.2.0",
    "framer-motion": "10.16.0",
    "html2canvas": "1.4.1",
    "jspdf": "2.5.1"
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

### 2. Componentes de Resultados

#### src/components/results/results-summary.tsx
```typescript
'use client'

import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { SimuladoResults } from '@/types/results'

interface ResultsSummaryProps {
  results: SimuladoResults
  isLoading?: boolean
}

export function ResultsSummary({ results, isLoading }: ResultsSummaryProps) {
  if (isLoading) {
    return (
      <Card className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      </Card>
    )
  }

  return (
    <Card className="p-6">
      <div className="space-y-6">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">
            Resultado do Simulado
          </h2>
          <p className="text-gray-600 mt-2">
            {results.simuladoId} • {new Date(results.completedAt).toLocaleDateString()}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">
              {results.score.toFixed(1)}%
            </div>
            <div className="text-sm text-gray-600">Pontuação</div>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">
              {results.correctAnswers}/{results.totalQuestions}
            </div>
            <div className="text-sm text-gray-600">Acertos</div>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">
              {Math.floor(results.timeSpent / 60)}min
            </div>
            <div className="text-sm text-gray-600">Tempo</div>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span>Progresso</span>
              <span>{results.correctAnswers}/{results.totalQuestions}</span>
            </div>
            <Progress 
              value={(results.correctAnswers / results.totalQuestions) * 100} 
              className="h-2"
            />
          </div>

          <div className="flex flex-wrap gap-2 justify-center">
            <Badge variant="secondary">
              {results.correctAnswers} Corretas
            </Badge>
            <Badge variant="destructive">
              {results.wrongAnswers} Incorretas
            </Badge>
            {results.unansweredQuestions > 0 && (
              <Badge variant="outline">
                {results.unansweredQuestions} Não respondidas
              </Badge>
            )}
          </div>
        </div>
      </div>
    </Card>
  )
}
```

#### src/components/results/results-table.tsx
```typescript
'use client'

import { useState } from 'react'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Table } from '@/components/ui/table'
import { QuestionResult } from '@/types/results'
import { ChevronDown, ChevronUp, Filter } from 'lucide-react'

interface ResultsTableProps {
  results: QuestionResult[]
  isLoading?: boolean
}

export function ResultsTable({ results, isLoading }: ResultsTableProps) {
  const [sortBy, setSortBy] = useState<'order' | 'topic' | 'difficulty' | 'time'>('order')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc')
  const [filterBy, setFilterBy] = useState<'all' | 'correct' | 'incorrect' | 'unanswered'>('all')

  if (isLoading) {
    return (
      <Card className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded"></div>
          <div className="space-y-2">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-12 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </Card>
    )
  }

  const filteredResults = results.filter(result => {
    if (filterBy === 'all') return true
    if (filterBy === 'correct') return result.isCorrect
    if (filterBy === 'incorrect') return !result.isCorrect && result.selectedAnswer !== null
    if (filterBy === 'unanswered') return result.selectedAnswer === null
    return true
  })

  const sortedResults = [...filteredResults].sort((a, b) => {
    let aValue: any, bValue: any
    
    switch (sortBy) {
      case 'order':
        aValue = a.order
        bValue = b.order
        break
      case 'topic':
        aValue = a.topic
        bValue = b.topic
        break
      case 'difficulty':
        const difficultyOrder = { easy: 1, medium: 2, hard: 3 }
        aValue = difficultyOrder[a.difficulty]
        bValue = difficultyOrder[b.difficulty]
        break
      case 'time':
        aValue = a.timeSpent
        bValue = b.timeSpent
        break
      default:
        aValue = a.order
        bValue = b.order
    }

    if (sortOrder === 'asc') {
      return aValue > bValue ? 1 : -1
    } else {
      return aValue < bValue ? 1 : -1
    }
  })

  const handleSort = (column: typeof sortBy) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(column)
      setSortOrder('asc')
    }
  }

  return (
    <Card className="p-6">
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-semibold">Detalhes das Questões</h3>
          
          <div className="flex gap-2">
            <select
              value={filterBy}
              onChange={(e) => setFilterBy(e.target.value as any)}
              className="px-3 py-1 border rounded text-sm"
            >
              <option value="all">Todas</option>
              <option value="correct">Corretas</option>
              <option value="incorrect">Incorretas</option>
              <option value="unanswered">Não respondidas</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th 
                  className="text-left p-2 cursor-pointer hover:bg-gray-50"
                  onClick={() => handleSort('order')}
                >
                  <div className="flex items-center gap-1">
                    Questão
                    {sortBy === 'order' && (
                      sortOrder === 'asc' ? <ChevronUp size={16} /> : <ChevronDown size={16} />
                    )}
                  </div>
                </th>
                <th 
                  className="text-left p-2 cursor-pointer hover:bg-gray-50"
                  onClick={() => handleSort('topic')}
                >
                  <div className="flex items-center gap-1">
                    Tópico
                    {sortBy === 'topic' && (
                      sortOrder === 'asc' ? <ChevronUp size={16} /> : <ChevronDown size={16} />
                    )}
                  </div>
                </th>
                <th 
                  className="text-left p-2 cursor-pointer hover:bg-gray-50"
                  onClick={() => handleSort('difficulty')}
                >
                  <div className="flex items-center gap-1">
                    Dificuldade
                    {sortBy === 'difficulty' && (
                      sortOrder === 'asc' ? <ChevronUp size={16} /> : <ChevronDown size={16} />
                    )}
                  </div>
                </th>
                <th className="text-left p-2">Resposta</th>
                <th 
                  className="text-left p-2 cursor-pointer hover:bg-gray-50"
                  onClick={() => handleSort('time')}
                >
                  <div className="flex items-center gap-1">
                    Tempo
                    {sortBy === 'time' && (
                      sortOrder === 'asc' ? <ChevronUp size={16} /> : <ChevronDown size={16} />
                    )}
                  </div>
                </th>
                <th className="text-left p-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {sortedResults.map((result) => (
                <tr key={result.questionId} className="border-b hover:bg-gray-50">
                  <td className="p-2 font-medium">#{result.order}</td>
                  <td className="p-2">{result.topic}</td>
                  <td className="p-2">
                    <Badge 
                      variant={
                        result.difficulty === 'easy' ? 'secondary' :
                        result.difficulty === 'medium' ? 'default' : 'destructive'
                      }
                    >
                      {result.difficulty === 'easy' ? 'Fácil' :
                       result.difficulty === 'medium' ? 'Médio' : 'Difícil'}
                    </Badge>
                  </td>
                  <td className="p-2">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-sm">
                        {result.selectedAnswer || '—'}
                      </span>
                      {result.selectedAnswer && (
                        <span className="text-gray-500 text-sm">
                          ({result.correctAnswer})
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="p-2">{result.timeSpent}s</td>
                  <td className="p-2">
                    {result.selectedAnswer === null ? (
                      <Badge variant="outline">Não respondida</Badge>
                    ) : result.isCorrect ? (
                      <Badge variant="secondary" className="bg-green-100 text-green-800">
                        Correta
                      </Badge>
                    ) : (
                      <Badge variant="destructive">Incorreta</Badge>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Card>
  )
}
```

#### src/components/results/performance-chart.tsx
```typescript
'use client'

import { Card } from '@/components/ui/card'
import { PerformanceAnalysis } from '@/types/results'
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

interface PerformanceChartProps {
  performance: PerformanceAnalysis
  isLoading?: boolean
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

export function PerformanceChart({ performance, isLoading }: PerformanceChartProps) {
  if (isLoading) {
    return (
      <Card className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-1/3"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </Card>
    )
  }

  const topicData = performance.scoreByTopic.map(topic => ({
    name: topic.topic,
    value: topic.score,
    correct: topic.correctAnswers,
    total: topic.totalQuestions
  }))

  const difficultyData = performance.scoreByDifficulty.map(diff => ({
    name: diff.difficulty === 'easy' ? 'Fácil' : diff.difficulty === 'medium' ? 'Médio' : 'Difícil',
    value: diff.score,
    correct: diff.correctAnswers,
    total: diff.totalQuestions
  }))

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Performance por Tópico</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={topicData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {topicData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </Card>

      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Performance por Dificuldade</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={difficultyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#8884d8" name="Pontuação (%)" />
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </div>
  )
}
```

### 3. Hooks de Resultados

#### src/hooks/use-results.ts
```typescript
'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { SimuladoResults } from '@/types/results'
import { resultsService } from '@/services/results-service'

export function useResults() {
  const [results, setResults] = useState<SimuladoResults | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const getResults = async (id: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const results = await resultsService.getResults(id)
      setResults(results)
      return results
    } catch (err: any) {
      setError(err.message)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const analyzeResults = async (id: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const analysis = await resultsService.analyzeResults(id)
      return analysis
    } catch (err: any) {
      setError(err.message)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const getPerformance = async (id: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const performance = await resultsService.getPerformance(id)
      return performance
    } catch (err: any) {
      setError(err.message)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const getWeakPoints = async (id: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const weakPoints = await resultsService.getWeakPoints(id)
      return weakPoints
    } catch (err: any) {
      setError(err.message)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const getRecommendations = async (id: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const recommendations = await resultsService.getRecommendations(id)
      return recommendations
    } catch (err: any) {
      setError(err.message)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  return {
    results,
    isLoading,
    error,
    getResults,
    analyzeResults,
    getPerformance,
    getWeakPoints,
    getRecommendations,
    clearError: () => setError(null),
  }
}
```

#### src/hooks/use-export.ts
```typescript
'use client'

import { useState } from 'react'
import { ExportOptions, ExportResult } from '@/types/export'
import { exportService } from '@/services/export-service'

export function useExport() {
  const [isExporting, setIsExporting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const exportResults = async (id: string, options: ExportOptions): Promise<ExportResult> => {
    setIsExporting(true)
    setError(null)
    
    try {
      const result = await exportService.exportResults(id, options)
      return result
    } catch (err: any) {
      setError(err.message)
      throw err
    } finally {
      setIsExporting(false)
    }
  }

  const downloadFile = (data: string | Blob, filename: string) => {
    const blob = data instanceof Blob ? data : new Blob([data], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  return {
    isExporting,
    error,
    exportResults,
    downloadFile,
    clearError: () => setError(null),
  }
}
```

### 4. Serviços

#### src/services/results-service.ts
```typescript
import { apiClient } from './api-client'
import { 
  SimuladoResults, 
  PerformanceAnalysis,
  WeakPoint,
  Recommendation
} from '@/types/results'

export const resultsService = {
  async getResults(id: string): Promise<SimuladoResults> {
    const response = await apiClient.get(`/results/${id}`)
    return response.data
  },

  async analyzeResults(id: string): Promise<PerformanceAnalysis> {
    const response = await apiClient.post(`/results/${id}/analyze`)
    return response.data
  },

  async getPerformance(id: string): Promise<PerformanceAnalysis> {
    const response = await apiClient.get(`/results/${id}/performance`)
    return response.data
  },

  async getWeakPoints(id: string): Promise<WeakPoint[]> {
    const response = await apiClient.get(`/results/${id}/weak-points`)
    return response.data
  },

  async getRecommendations(id: string): Promise<Recommendation[]> {
    const response = await apiClient.get(`/results/${id}/recommendations`)
    return response.data
  },

  async getChartData(id: string): Promise<any> {
    const response = await apiClient.get(`/results/${id}/charts`)
    return response.data
  },

  async saveDraft(id: string, draftData: any): Promise<void> {
    await apiClient.post(`/results/${id}/save`, { draft_data: draftData })
  },

  async shareResults(id: string): Promise<string> {
    const response = await apiClient.get(`/results/${id}/share`)
    return response.data.share_url
  },
}
```

#### src/services/export-service.ts
```typescript
import { apiClient } from './api-client'
import { ExportOptions, ExportResult } from '@/types/export'

export const exportService = {
  async exportResults(id: string, options: ExportOptions): Promise<ExportResult> {
    const response = await apiClient.post(`/results/${id}/export`, options)
    return response.data
  },

  async exportToMarkdown(id: string, options: ExportOptions): Promise<string> {
    const result = await this.exportResults(id, { ...options, format: 'markdown' })
    return result.data as string
  },

  async exportToPDF(id: string, options: ExportOptions): Promise<Blob> {
    const result = await this.exportResults(id, { ...options, format: 'pdf' })
    return result.data as Blob
  },

  async exportToJSON(id: string, options: ExportOptions): Promise<string> {
    const result = await this.exportResults(id, { ...options, format: 'json' })
    return result.data as string
  },

  async exportToCSV(id: string, options: ExportOptions): Promise<string> {
    const result = await this.exportResults(id, { ...options, format: 'csv' })
    return result.data as string
  },
}
```

### 5. Tipos TypeScript

#### src/types/results.ts
```typescript
export interface SimuladoResults {
  id: string
  simuladoId: string
  userId: string
  totalQuestions: number
  correctAnswers: number
  wrongAnswers: number
  unansweredQuestions: number
  score: number
  timeSpent: number
  averageTimePerQuestion: number
  submittedAt: string
  completedAt: string
  results: QuestionResult[]
  performance: PerformanceAnalysis
  weakPoints: WeakPoint[]
  recommendations: Recommendation[]
}

export interface QuestionResult {
  questionId: string
  question: string
  selectedAnswer: 'A' | 'B' | 'C' | 'D' | 'E' | null
  correctAnswer: 'A' | 'B' | 'C' | 'D' | 'E'
  isCorrect: boolean
  timeSpent: number
  topic: string
  difficulty: 'easy' | 'medium' | 'hard'
  order: number
  explanation?: string
}

export interface PerformanceAnalysis {
  overallScore: number
  scoreByTopic: TopicScore[]
  scoreByDifficulty: DifficultyScore[]
  timeAnalysis: TimeAnalysis
  accuracyRate: number
  completionRate: number
  improvementAreas: string[]
  strengths: string[]
}

export interface TopicScore {
  topic: string
  totalQuestions: number
  correctAnswers: number
  score: number
  averageTime: number
  accuracy: number
}

export interface DifficultyScore {
  difficulty: 'easy' | 'medium' | 'hard'
  totalQuestions: number
  correctAnswers: number
  score: number
  averageTime: number
  accuracy: number
}

export interface TimeAnalysis {
  totalTime: number
  averageTimePerQuestion: number
  fastestQuestion: number
  slowestQuestion: number
  timeDistribution: TimeDistribution[]
  timeEfficiency: number
}

export interface TimeDistribution {
  range: string
  count: number
  percentage: number
}

export interface WeakPoint {
  topic: string
  difficulty: 'easy' | 'medium' | 'hard'
  accuracy: number
  averageTime: number
  questions: QuestionResult[]
  recommendations: string[]
}

export interface Recommendation {
  type: 'study' | 'practice' | 'time_management' | 'strategy'
  priority: 'high' | 'medium' | 'low'
  title: string
  description: string
  actionItems: string[]
  resources?: string[]
}
```

### 6. Páginas

#### src/pages/results/[id]/index.tsx
```typescript
import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'
import { ResultsSummary } from '@/components/results/results-summary'
import { ResultsTable } from '@/components/results/results-table'
import { PerformanceChart } from '@/components/results/performance-chart'
import { WeakPoints } from '@/components/results/weak-points'
import { ResultsExport } from '@/components/results/results-export'
import { useResults } from '@/hooks/use-results'
import { AuthGuard } from '@/components/auth/auth-guard'
import { SimuladoResults } from '@/types/results'

export default function ResultsPage() {
  const router = useRouter()
  const { id } = router.query
  const { results, isLoading, error, getResults } = useResults()
  const [activeTab, setActiveTab] = useState<'summary' | 'details' | 'analysis' | 'export'>('summary')

  useEffect(() => {
    if (id && typeof id === 'string') {
      getResults(id)
    }
  }, [id, getResults])

  if (isLoading) {
    return (
      <AuthGuard>
        <div className="min-h-screen bg-gray-50">
          <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <div className="animate-pulse space-y-6">
              <div className="h-8 bg-gray-200 rounded w-1/3"></div>
              <div className="h-64 bg-gray-200 rounded"></div>
              <div className="h-64 bg-gray-200 rounded"></div>
            </div>
          </div>
        </div>
      </AuthGuard>
    )
  }

  if (error) {
    return (
      <AuthGuard>
        <div className="min-h-screen bg-gray-50">
          <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
              <div className="text-red-800">
                Erro ao carregar resultados: {error}
              </div>
            </div>
          </div>
        </div>
      </AuthGuard>
    )
  }

  if (!results) {
    return (
      <AuthGuard>
        <div className="min-h-screen bg-gray-50">
          <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-900">
                Resultados não encontrados
              </h1>
            </div>
          </div>
        </div>
      </AuthGuard>
    )
  }

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        <div className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="py-6">
              <h1 className="text-2xl font-bold text-gray-900">
                Resultados do Simulado
              </h1>
              <p className="text-gray-600">
                Análise detalhada do seu desempenho
              </p>
            </div>
          </div>
        </div>
        
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="space-y-6">
            {activeTab === 'summary' && (
              <>
                <ResultsSummary results={results} />
                <PerformanceChart performance={results.performance} />
              </>
            )}
            
            {activeTab === 'details' && (
              <ResultsTable results={results.results} />
            )}
            
            {activeTab === 'analysis' && (
              <WeakPoints weakPoints={results.weakPoints} />
            )}
            
            {activeTab === 'export' && (
              <ResultsExport results={results} />
            )}
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
NEXT_PUBLIC_API_URL=http://localhost:8003
NEXT_PUBLIC_APP_NAME=Concurso AI Results

# Results Configuration
NEXT_PUBLIC_MAX_EXPORT_SIZE=10485760
NEXT_PUBLIC_CHART_ANIMATION_DURATION=1000
NEXT_PUBLIC_EXPORT_TIMEOUT=30000

# Development
NODE_ENV=development
```

### 8. README de Rotas

#### ROUTES.md
```markdown
# Rotas da Aplicação - Relatório de Resultados

## Páginas Protegidas (requer autenticação)
- `/results/[id]` - Visualizar resultados do simulado
- `/results/[id]/print` - Versão para impressão
- `/results/[id]/export` - Exportar resultados

## Componentes de Resultados
- `ResultsSummary` - Resumo dos resultados
- `ResultsTable` - Tabela detalhada de questões
- `PerformanceChart` - Gráficos de performance
- `TimeAnalysis` - Análise de tempo
- `WeakPoints` - Identificação de pontos fracos
- `ResultsExport` - Exportação de resultados
- `ResultsShare` - Compartilhamento
- `ResultsPrint` - Versão para impressão

## Hooks de Resultados
- `useResults` - Hook principal de resultados
- `useCharts` - Hook para gráficos
- `useExport` - Hook para exportação
- `usePrint` - Hook para impressão
- `useAnalytics` - Hook para analytics

## Serviços
- `resultsService` - Serviço de resultados
- `analyticsService` - Serviço de analytics
- `exportService` - Serviço de exportação
- `storageService` - Serviço de armazenamento
- `shareService` - Serviço de compartilhamento

## Variáveis de Ambiente
- `NEXT_PUBLIC_API_URL` - URL base da API
- `NEXT_PUBLIC_APP_NAME` - Nome da aplicação
- `NEXT_PUBLIC_MAX_EXPORT_SIZE` - Tamanho máximo de exportação
- `NEXT_PUBLIC_CHART_ANIMATION_DURATION` - Duração da animação dos gráficos
- `NEXT_PUBLIC_EXPORT_TIMEOUT` - Timeout para exportação

## Fluxo de Resultados
1. Usuário completa simulado
2. Dados são processados
3. Análise de performance é gerada
4. Pontos fracos são identificados
5. Recomendações são criadas
6. Relatório é renderizado
7. Usuário pode exportar/compartilhar
```

---

**Este documento define o scaffolding completo do frontend WEB-004, incluindo componentes de resultados, hooks, serviços, tipos e páginas.**
