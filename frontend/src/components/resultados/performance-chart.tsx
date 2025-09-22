'use client'

import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { useAuth } from '@/hooks/use-auth'

interface PerformanceData {
  subjects: { [key: string]: number }
  recentScores: number[]
  monthlyProgress: { [key: string]: number }
}

export function PerformanceChart() {
  const { state } = useAuth()
  const [performanceData, setPerformanceData] = useState<PerformanceData | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const loadPerformanceData = async () => {
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
          setPerformanceData({
            subjects: data.subjects_performance || {},
            recentScores: [], // TODO: Implementar histórico de pontuações
            monthlyProgress: {} // TODO: Implementar progresso mensal
          })
        }
      } catch (error) {
        console.error('Erro ao carregar dados de performance:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadPerformanceData()
  }, [state.token])

  if (isLoading) {
    return (
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Performance por Disciplina</h3>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="h-4 bg-gray-200 rounded mb-2"></div>
              <div className="h-2 bg-gray-200 rounded"></div>
            </div>
          ))}
        </div>
      </Card>
    )
  }

  const data = performanceData || {
    subjects: {},
    recentScores: [],
    monthlyProgress: {}
  }

  const subjects = Object.entries(data.subjects)
  const hasData = subjects.length > 0

  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4">
        Performance por Disciplina
      </h3>
      
      {!hasData ? (
        <div className="text-center py-8">
          <div className="text-4xl mb-2">📊</div>
          <p className="text-gray-500 mb-4">Nenhum dado de performance disponível</p>
          <p className="text-sm text-gray-400">
            Complete alguns simulados para ver sua performance por disciplina
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {subjects.map(([subject, score]) => {
            const percentage = Math.min(score, 100)
            const getColor = (score: number) => {
              if (score >= 70) return 'bg-green-500'
              if (score >= 50) return 'bg-yellow-500'
              return 'bg-red-500'
            }

            return (
              <div key={subject}>
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm font-medium text-gray-700">
                    {subject}
                  </span>
                  <span className="text-sm text-gray-600">
                    {score.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`${getColor(score)} h-2 rounded-full transition-all duration-500`}
                    style={{ width: `${percentage}%` }}
                  ></div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Seção de Insights */}
      {hasData && (
        <div className="mt-6 pt-4 border-t border-gray-200">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Insights</h4>
          <div className="space-y-2 text-sm text-gray-600">
            {(() => {
              const bestSubject = subjects.reduce((best, [subject, score]) => 
                score > best.score ? { subject, score } : best, 
                { subject: '', score: 0 }
              )
              const worstSubject = subjects.reduce((worst, [subject, score]) => 
                score < worst.score ? { subject, score } : worst, 
                { subject: '', score: 100 }
              )

              return (
                <>
                  {bestSubject.score > 0 && (
                    <p>
                      <span className="font-medium">Melhor disciplina:</span> {bestSubject.subject} ({bestSubject.score.toFixed(1)}%)
                    </p>
                  )}
                  {worstSubject.score < 100 && (
                    <p>
                      <span className="font-medium">Foque em:</span> {worstSubject.subject} ({worstSubject.score.toFixed(1)}%)
                    </p>
                  )}
                </>
              )
            })()}
          </div>
        </div>
      )}
    </Card>
  )
}