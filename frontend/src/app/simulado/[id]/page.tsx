'use client'

import { useState, useEffect, useCallback } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { AuthGuard } from '@/components/auth/auth-guard'
import { SimuladoTimer } from '@/components/simulado/simulado-timer'
import { QuestionCard } from '@/components/simulado/question-card'
import { SimuladoNavigation } from '@/components/simulado/simulado-navigation'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Alert } from '@/components/ui/alert'

interface Question {
  id: string
  text: string
  options: string[]
  correctAnswer: number
  explanation?: string
  subject: string
}

interface Simulado {
  id: string
  title: string
  questions: Question[]
  timeLimit: number
  totalQuestions: number
}

export default function SimuladoPage() {
  const params = useParams()
  const router = useRouter()
  const [simulado, setSimulado] = useState<Simulado | null>(null)
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<{ [key: string]: number }>({})
  const [timeRemaining, setTimeRemaining] = useState(0)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  // Sem mais dados mock - apenas dados reais da API

  const handleSubmit = useCallback(async () => {
    setIsSubmitted(true)
    
    try {
      const { apiClient } = await import('@/lib/api')
      
      // Submeter simulado via API real - SEM FALLBACKS
      const response = await apiClient.submitSimulado(
        simulado!.id,
        answers,
        simulado!.time_limit * 60 - timeRemaining
      )
      
      if (response.data) {
        // Redirecionar para resultados
        router.push(`/resultados/${simulado!.id}`)
      } else {
        // ERRO: Falha ao submeter simulado
        console.error('Erro ao submeter simulado:', response.error)
        alert('Erro ao submeter simulado. Tente novamente.')
        setIsSubmitted(false)
      }
    } catch (error) {
      // ERRO: Falha na conexão
      console.error('Erro de conexão ao submeter simulado:', error)
      alert('Erro de conexão. Verifique se o backend está funcionando.')
      setIsSubmitted(false)
    }
  }, [simulado, answers, timeRemaining, router])

  useEffect(() => {
    // Carregar simulado real da API - SEM FALLBACKS MOCK
    const loadSimulado = async () => {
      setIsLoading(true)
      
      try {
        const { apiClient } = await import('@/lib/api')
        const response = await apiClient.getSimulado(parseInt(params.id as string))
        
        if (response.data) {
          setSimulado(response.data)
          setTimeRemaining(response.data.time_limit * 60) // Converter para segundos
        } else {
          // ERRO: Simulado não encontrado
          console.error('Simulado não encontrado:', response.error)
          setSimulado(null)
        }
      } catch (error) {
        // ERRO: Falha na conexão com API
        console.error('Erro ao carregar simulado:', error)
        setSimulado(null)
      }
      
      setIsLoading(false)
    }

    loadSimulado()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params.id])

  useEffect(() => {
    if (timeRemaining > 0 && !isSubmitted) {
      const timer = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            handleSubmit()
            return 0
          }
          return prev - 1
        })
      }, 1000)

      return () => clearInterval(timer)
    }
  }, [timeRemaining, isSubmitted, handleSubmit])

  const handleAnswerSelect = (questionId: string, answerIndex: number) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answerIndex
    }))
  }

  const handleNext = () => {
    if (currentQuestion < simulado!.totalQuestions - 1) {
      setCurrentQuestion(prev => prev + 1)
    }
  }

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1)
    }
  }

  // const formatTime = (seconds: number) => {
  //   const hours = Math.floor(seconds / 3600)
  //   const minutes = Math.floor((seconds % 3600) / 60)
  //   const secs = seconds % 60
  //   
  //   if (hours > 0) {
  //     return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  //   }
  //   return `${minutes}:${secs.toString().padStart(2, '0')}`
  // }

  if (isLoading) {
    return (
      <AuthGuard>
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-center min-h-[400px]">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Carregando simulado...</p>
            </div>
          </div>
        </div>
      </AuthGuard>
    )
  }

  if (!simulado) {
    return (
      <AuthGuard>
        <div className="container mx-auto px-4 py-8">
          <Alert variant="destructive">
            Simulado não encontrado.
          </Alert>
        </div>
      </AuthGuard>
    )
  }

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            {simulado.title}
          </h1>
          <div className="flex items-center gap-4 text-sm text-gray-600">
            <span>Questão {currentQuestion + 1} de {simulado.totalQuestions}</span>
            <span>•</span>
            <span>{simulado.questions[currentQuestion].subject}</span>
          </div>
        </div>

        <div className="grid lg:grid-cols-4 gap-6">
          <div className="lg:col-span-3">
            <Card className="p-6">
              <QuestionCard
                question={simulado.questions[currentQuestion]}
                selectedAnswer={answers[simulado.questions[currentQuestion].id]}
                onAnswerSelect={(answerIndex) => 
                  handleAnswerSelect(simulado.questions[currentQuestion].id, answerIndex)
                }
                isSubmitted={isSubmitted}
              />
            </Card>

            <div className="mt-6 flex justify-between">
              <Button
                variant="outline"
                onClick={handlePrevious}
                disabled={currentQuestion === 0}
              >
                ← Anterior
              </Button>
              
              <div className="flex gap-3">
                {currentQuestion === simulado.totalQuestions - 1 ? (
                  <Button
                    onClick={handleSubmit}
                    disabled={isSubmitted}
                    className="bg-green-600 hover:bg-green-700"
                  >
                    Finalizar Simulado
                  </Button>
                ) : (
                  <Button onClick={handleNext}>
                    Próxima →
                  </Button>
                )}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <SimuladoTimer
              timeRemaining={timeRemaining}
              totalTime={simulado.timeLimit * 60}
              onTimeUp={handleSubmit}
            />

            <SimuladoNavigation
              questions={simulado.questions}
              currentQuestion={currentQuestion}
              answers={answers}
              onQuestionSelect={setCurrentQuestion}
            />
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}
