'use client'

import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { useAuth } from '@/hooks/use-auth'
import { Button } from '@/components/ui/button'

interface SimuladoResult {
  id: number
  simulado_id: number
  score: number
  correct_answers: number
  total_questions: number
  time_spent: number
  created_at: string
  answers: { [key: string]: number }
  subject_scores: { [key: string]: { correct: number; total: number } }
}

interface Question {
  id: string
  text: string
  options: string[]
  correct_answer: number
  explanation?: string
  subject: string
}

export function QuestionReview() {
  const { state } = useAuth()
  const [recentResults, setRecentResults] = useState<SimuladoResult[]>([])
  const [selectedResult, setSelectedResult] = useState<SimuladoResult | null>(null)
  const [questions, setQuestions] = useState<Question[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const loadRecentResults = async () => {
      if (!state.token) {
        setIsLoading(false)
        return
      }

      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 
          (typeof window !== 'undefined' && window.location.hostname === 'localhost' 
            ? 'http://localhost:8000' 
            : 'https://concurso-ai-backend-609095880025.us-central1.run.app')

        const response = await fetch(`${apiUrl}/dashboard/results?limit=5`, {
          headers: {
            'Authorization': `Bearer ${state.token}`
          }
        })
        
        if (response.ok) {
          const results = await response.json()
          setRecentResults(results)
          if (results.length > 0) {
            setSelectedResult(results[0])
            await loadQuestions(results[0].simulado_id)
          }
        }
      } catch (error) {
        console.error('Erro ao carregar resultados recentes:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadRecentResults()
  }, [state.token])

  const loadQuestions = async (simuladoId: number) => {
    if (!state.token) return

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 
        (typeof window !== 'undefined' && window.location.hostname === 'localhost' 
          ? 'http://localhost:8000' 
          : 'https://concurso-ai-backend-609095880025.us-central1.run.app')

      const response = await fetch(`${apiUrl}/simulados/${simuladoId}`, {
        headers: {
          'Authorization': `Bearer ${state.token}`
        }
      })
      
      if (response.ok) {
        const simulado = await response.json()
        setQuestions(simulado.questions || [])
      }
    } catch (error) {
      console.error('Erro ao carregar questões:', error)
    }
  }

  const handleResultSelect = async (result: SimuladoResult) => {
    setSelectedResult(result)
    await loadQuestions(result.simulado_id)
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return `${minutes}m ${remainingSeconds}s`
  }

  if (isLoading) {
    return (
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Revisão de Questões</h3>
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded"></div>
        </div>
      </Card>
    )
  }

  if (recentResults.length === 0) {
    return (
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Revisão de Questões</h3>
        <div className="text-center py-8">
          <div className="text-4xl mb-2">📝</div>
          <p className="text-gray-500 mb-4">Nenhum resultado encontrado</p>
          <p className="text-sm text-gray-400">
            Complete alguns simulados para revisar suas respostas
          </p>
        </div>
      </Card>
    )
  }

  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4">Revisão de Questões</h3>
      
      {/* Seletor de Resultados */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Selecione um simulado para revisar:
        </label>
        <div className="space-y-2">
          {recentResults.map((result) => (
            <button
              key={result.id}
              onClick={() => handleResultSelect(result)}
              className={`w-full text-left p-3 rounded-lg border transition-colors ${
                selectedResult?.id === result.id
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200 hover:bg-gray-50'
              }`}
            >
              <div className="flex justify-between items-center">
                <div>
                  <p className="font-medium">Simulado #{result.simulado_id}</p>
                  <p className="text-sm text-gray-500">
                    {formatDate(result.created_at)} • {formatTime(result.time_spent)}
                  </p>
                </div>
                <div className="text-right">
                  <p className={`font-semibold ${
                    result.score >= 70 ? 'text-green-600' : 
                    result.score >= 50 ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {result.score}%
                  </p>
                  <p className="text-sm text-gray-500">
                    {result.correct_answers}/{result.total_questions}
                  </p>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Revisão das Questões */}
      {selectedResult && questions.length > 0 && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h4 className="font-medium">Questões do Simulado #{selectedResult.simulado_id}</h4>
            <span className="text-sm text-gray-500">
              {selectedResult.correct_answers}/{selectedResult.total_questions} corretas
            </span>
          </div>
          
          <div className="space-y-4 max-h-96 overflow-y-auto">
            {questions.map((question, index) => {
              const userAnswer = selectedResult.answers[question.id]
              const isCorrect = userAnswer === question.correct_answer
              
              return (
                <div key={question.id} className="border rounded-lg p-4">
                  <div className="flex items-start justify-between mb-3">
                    <span className="text-sm font-medium text-gray-500">
                      Questão {index + 1}
                    </span>
                    <span className={`text-sm px-2 py-1 rounded ${
                      isCorrect 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {isCorrect ? 'Correta' : 'Incorreta'}
                    </span>
                  </div>
                  
                  <p className="text-gray-900 mb-3">{question.text}</p>
                  
                  <div className="space-y-2">
                    {question.options.map((option, optionIndex) => {
                      const isUserAnswer = userAnswer === optionIndex
                      const isCorrectAnswer = question.correct_answer === optionIndex
                      
                      return (
                        <div
                          key={optionIndex}
                          className={`p-2 rounded text-sm ${
                            isCorrectAnswer
                              ? 'bg-green-50 border border-green-200 text-green-800'
                              : isUserAnswer
                              ? 'bg-red-50 border border-red-200 text-red-800'
                              : 'bg-gray-50 text-gray-700'
                          }`}
                        >
                          <span className="font-medium">
                            {String.fromCharCode(65 + optionIndex)}. 
                          </span>
                          {option}
                          {isCorrectAnswer && (
                            <span className="ml-2 text-xs">✓ Resposta correta</span>
                          )}
                          {isUserAnswer && !isCorrectAnswer && (
                            <span className="ml-2 text-xs">✗ Sua resposta</span>
                          )}
                        </div>
                      )
                    })}
                  </div>
                  
                  {question.explanation && (
                    <div className="mt-3 p-3 bg-blue-50 rounded text-sm text-blue-800">
                      <strong>Explicação:</strong> {question.explanation}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      )}
    </Card>
  )
}