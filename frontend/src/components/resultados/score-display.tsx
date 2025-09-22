'use client'

import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { useAuth } from '@/hooks/use-auth'

interface ScoreData {
  totalSimulados: number
  averageScore: number
  bestScore: number
  totalQuestions: number
  correctAnswers: number
}

export function ScoreDisplay() {
  const { state } = useAuth()
  const [scoreData, setScoreData] = useState<ScoreData | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const loadScoreData = async () => {
      if (!state.token) {
        setIsLoading(false)
        return
      }

      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 
          (typeof window !== 'undefined' && window.location.hostname === 'localhost' 
            ? 'http://localhost:8000' 
            : 'https://concurso-ai-backend-609095880025.us-central1.run.app')

        const response = await fetch(`${apiUrl}/dashboard/stats`, {
          headers: {
            'Authorization': `Bearer ${state.token}`
          }
        })
        
        if (response.ok) {
          const data = await response.json()
          setScoreData({
            totalSimulados: data.total_simulados || 0,
            averageScore: data.average_score || 0,
            bestScore: data.best_score || 0,
            totalQuestions: data.total_questions_answered || 0,
            correctAnswers: Math.round((data.total_questions_answered || 0) * (data.average_score || 0) / 100)
          })
        }
      } catch (error) {
        console.error('Erro ao carregar dados de pontuação:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadScoreData()
  }, [state.token])

  if (isLoading) {
    return (
      <Card className="p-6">
        <div className="text-center">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded mb-4"></div>
            <div className="h-12 bg-gray-200 rounded mb-4"></div>
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
          </div>
        </div>
      </Card>
    )
  }

  const data = scoreData || {
    totalSimulados: 0,
    averageScore: 0,
    bestScore: 0,
    totalQuestions: 0,
    correctAnswers: 0
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreMessage = (score: number) => {
    if (score >= 80) return 'Excelente!'
    if (score >= 60) return 'Bom trabalho!'
    if (score >= 40) return 'Continue estudando!'
    return 'Vamos melhorar!'
  }

  return (
    <Card className="p-6">
      <div className="text-center">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Sua Pontuação Geral
        </h3>
        
        <div className="mb-6">
          <div className={`text-5xl font-bold ${getScoreColor(data.averageScore)} mb-2`}>
            {data.averageScore.toFixed(1)}%
          </div>
          <p className="text-gray-600">{getScoreMessage(data.averageScore)}</p>
        </div>

        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Simulados Realizados</span>
            <span className="font-semibold">{data.totalSimulados}</span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Melhor Pontuação</span>
            <span className={`font-semibold ${getScoreColor(data.bestScore)}`}>
              {data.bestScore}%
            </span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Questões Respondidas</span>
            <span className="font-semibold">{data.totalQuestions}</span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Acertos</span>
            <span className="font-semibold text-green-600">
              {data.correctAnswers}/{data.totalQuestions}
            </span>
          </div>
        </div>

        {data.totalSimulados === 0 && (
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <p className="text-blue-800 text-sm">
              Faça seu primeiro simulado para ver suas estatísticas!
            </p>
          </div>
        )}
      </div>
    </Card>
  )
}