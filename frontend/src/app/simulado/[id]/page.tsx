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

  // Mock data para demonstração
  const mockSimulado: Simulado = {
    id: params.id as string,
    title: 'Simulado CESPE - Direito Constitucional',
    timeLimit: 60, // 60 minutos
    totalQuestions: 5,
    questions: [
      {
        id: '1',
        text: 'A respeito dos direitos fundamentais, assinale a opção correta.',
        options: [
          'Os direitos fundamentais são absolutos e não admitem restrições.',
          'Os direitos fundamentais podem ser restringidos por lei, desde que respeitados os princípios da proporcionalidade e razoabilidade.',
          'Os direitos fundamentais só podem ser restringidos em caso de estado de sítio.',
          'Os direitos fundamentais não se aplicam às relações privadas.'
        ],
        correctAnswer: 1,
        explanation: 'Os direitos fundamentais podem ser restringidos por lei, desde que respeitados os princípios da proporcionalidade e razoabilidade.',
        subject: 'Direito Constitucional'
      },
      {
        id: '2',
        text: 'Sobre o controle de constitucionalidade no Brasil, é correto afirmar:',
        options: [
          'O controle de constitucionalidade é exercido apenas pelo Supremo Tribunal Federal.',
          'O controle de constitucionalidade pode ser exercido por qualquer juiz ou tribunal.',
          'O controle de constitucionalidade é exercido apenas pelo Poder Legislativo.',
          'O controle de constitucionalidade não existe no ordenamento jurídico brasileiro.'
        ],
        correctAnswer: 1,
        explanation: 'O controle de constitucionalidade pode ser exercido por qualquer juiz ou tribunal, sendo o STF o guardião da Constituição.',
        subject: 'Direito Constitucional'
      },
      {
        id: '3',
        text: 'A respeito do Poder Judiciário, assinale a opção correta.',
        options: [
          'O Poder Judiciário é composto apenas pelo Supremo Tribunal Federal.',
          'O Poder Judiciário é composto por tribunais e juízes, sendo o STF o órgão de cúpula.',
          'O Poder Judiciário não tem autonomia administrativa.',
          'O Poder Judiciário é subordinado ao Poder Executivo.'
        ],
        correctAnswer: 1,
        explanation: 'O Poder Judiciário é composto por tribunais e juízes, sendo o STF o órgão de cúpula do sistema judiciário.',
        subject: 'Direito Constitucional'
      },
      {
        id: '4',
        text: 'Sobre os princípios fundamentais da República Federativa do Brasil, é correto afirmar:',
        options: [
          'A República Federativa do Brasil é formada pela união indissolúvel dos Estados e Municípios.',
          'A República Federativa do Brasil é formada pela união indissolúvel dos Estados, Municípios e Distrito Federal.',
          'A República Federativa do Brasil é formada pela união dos Estados, que podem se separar.',
          'A República Federativa do Brasil não é uma federação.'
        ],
        correctAnswer: 1,
        explanation: 'A República Federativa do Brasil é formada pela união indissolúvel dos Estados, Municípios e Distrito Federal.',
        subject: 'Direito Constitucional'
      },
      {
        id: '5',
        text: 'A respeito da organização do Estado, assinale a opção correta.',
        options: [
          'O Brasil é um Estado unitário.',
          'O Brasil é uma federação com autonomia dos entes federativos.',
          'O Brasil é uma confederação.',
          'O Brasil não tem forma de Estado definida.'
        ],
        correctAnswer: 1,
        explanation: 'O Brasil é uma federação com autonomia dos entes federativos (União, Estados, Municípios e Distrito Federal).',
        subject: 'Direito Constitucional'
      }
    ]
  }

  const handleSubmit = useCallback(async () => {
    setIsSubmitted(true)
    
    try {
      const { apiClient } = await import('@/lib/api')
      
      // Submeter simulado via API real
      const response = await apiClient.submitSimulado(
        simulado!.id,
        answers,
        simulado!.timeLimit * 60 - timeRemaining
      )
      
      if (response.data) {
        // Redirecionar para resultados
        router.push(`/resultados/${simulado!.id}`)
      } else {
        // Fallback para localStorage se API falhar
        const simuladoData = {
          id: simulado!.id,
          answers,
          timeSpent: simulado!.timeLimit * 60 - timeRemaining,
          submittedAt: new Date().toISOString()
        }
        localStorage.setItem(`simulado_${simulado!.id}`, JSON.stringify(simuladoData))
        router.push(`/resultados/${simulado!.id}`)
      }
    } catch (error) {
      // Fallback para localStorage se API falhar
      const simuladoData = {
        id: simulado!.id,
        answers,
        timeSpent: simulado!.timeLimit * 60 - timeRemaining,
        submittedAt: new Date().toISOString()
      }
      localStorage.setItem(`simulado_${simulado!.id}`, JSON.stringify(simuladoData))
      router.push(`/resultados/${simulado!.id}`)
    }
  }, [simulado, answers, timeRemaining, router])

  useEffect(() => {
    // Carregar simulado real da API
    const loadSimulado = async () => {
      setIsLoading(true)
      
      try {
        const { apiClient } = await import('@/lib/api')
        const response = await apiClient.getSimulado(parseInt(params.id as string))
        
        if (response.data) {
          setSimulado(response.data)
          setTimeRemaining(response.data.time_limit * 60) // Converter para segundos
        } else {
          // Fallback para dados mock se API falhar
          setSimulado(mockSimulado)
          setTimeRemaining(mockSimulado.timeLimit * 60)
        }
      } catch (error) {
        // Fallback para dados mock se API falhar
        setSimulado(mockSimulado)
        setTimeRemaining(mockSimulado.timeLimit * 60)
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
