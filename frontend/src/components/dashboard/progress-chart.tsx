'use client'

import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { useAuth } from '@/hooks/use-auth'

interface ProgressData {
  accuracyRate: number
  questionsAnswered: number
  simuladosCompleted: number
  timeSpent: number
}

export function ProgressChart() {
  const { state } = useAuth()
  const [progressData, setProgressData] = useState<ProgressData | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const loadProgressData = async () => {
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
          setProgressData({
            accuracyRate: data.average_score || 0,
            questionsAnswered: data.total_questions_answered || 0,
            simuladosCompleted: data.total_simulados || 0,
            timeSpent: data.time_spent_total || 0
          })
        }
      } catch (error) {
        console.error('Erro ao carregar dados de progresso:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadProgressData()
  }, [state.token])

  if (isLoading) {
    return (
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Progresso</h3>
        <div className="space-y-4">
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-2 bg-gray-200 rounded"></div>
          </div>
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-2 bg-gray-200 rounded"></div>
          </div>
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-2 bg-gray-200 rounded"></div>
          </div>
        </div>
      </Card>
    )
  }

  const data = progressData || {
    accuracyRate: 0,
    questionsAnswered: 0,
    simuladosCompleted: 0,
    timeSpent: 0
  }

  // Calcular percentuais para as barras de progresso
  const accuracyPercentage = Math.min(data.accuracyRate, 100)
  const questionsPercentage = Math.min((data.questionsAnswered / 100) * 100, 100) // Meta: 100 questões
  const simuladosPercentage = Math.min((data.simuladosCompleted / 20) * 100, 100) // Meta: 20 simulados

  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4">
        Seu Progresso
      </h3>
      <div className="space-y-4">
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Taxa de Acerto</span>
            <span>{data.accuracyRate.toFixed(1)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-green-600 h-2 rounded-full transition-all duration-500" 
              style={{ width: `${accuracyPercentage}%` }}
            ></div>
          </div>
        </div>
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Questões Respondidas</span>
            <span>{data.questionsAnswered}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all duration-500" 
              style={{ width: `${questionsPercentage}%` }}
            ></div>
          </div>
        </div>
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Simulados Completos</span>
            <span>{data.simuladosCompleted}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-purple-600 h-2 rounded-full transition-all duration-500" 
              style={{ width: `${simuladosPercentage}%` }}
            ></div>
          </div>
        </div>
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Tempo de Estudo</span>
            <span>{Math.round(data.timeSpent / 60)}min</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-orange-600 h-2 rounded-full transition-all duration-500" 
              style={{ width: `${Math.min((data.timeSpent / 3600) * 100, 100)}%` }}
            ></div>
          </div>
        </div>
      </div>
    </Card>
  )
}
