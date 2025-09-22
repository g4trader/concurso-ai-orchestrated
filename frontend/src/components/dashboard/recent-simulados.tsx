'use client'

import { useState, useEffect } from 'react'
import { Card } from '@/components/ui/card'
import { useAuth } from '@/hooks/use-auth'
import Link from 'next/link'

interface RecentSimulado {
  id: number
  title: string
  config: {
    banca: string
    subjects: string[]
    level: string
  }
  created_at: string
  score?: number
  completed_at?: string
}

export function RecentSimulados() {
  const { state } = useAuth()
  const [recentSimulados, setRecentSimulados] = useState<RecentSimulado[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const loadRecentSimulados = async () => {
      if (!state.token) {
        setIsLoading(false)
        return
      }

      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 
          (typeof window !== 'undefined' && window.location.hostname === 'localhost' 
            ? 'http://localhost:8000' 
            : 'https://concurso-ai-backend-609095880025.us-central1.run.app')

        // Buscar simulados do usuário
        const simuladosResponse = await fetch(`${apiUrl}/simulados/?limit=5`, {
          headers: {
            'Authorization': `Bearer ${state.token}`
          }
        })
        
        if (simuladosResponse.ok) {
          const simulados = await simuladosResponse.json()
          
          // Buscar resultados para cada simulado
          const simuladosWithResults = await Promise.all(
            simulados.map(async (simulado: RecentSimulado) => {
              try {
                const resultResponse = await fetch(`${apiUrl}/simulados/${simulado.id}/result`, {
                  headers: {
                    'Authorization': `Bearer ${state.token}`
                  }
                })
                
                if (resultResponse.ok) {
                  const result = await resultResponse.json()
                  return {
                    ...simulado,
                    score: result.score,
                    completed_at: result.created_at
                  }
                }
              } catch (error) {
                console.error(`Erro ao buscar resultado do simulado ${simulado.id}:`, error)
              }
              
              return simulado
            })
          )
          
          setRecentSimulados(simuladosWithResults)
        }
      } catch (error) {
        console.error('Erro ao carregar simulados recentes:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadRecentSimulados()
  }, [state.token])

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }

  const getScoreColor = (score?: number) => {
    if (!score) return 'bg-gray-100 text-gray-800'
    if (score >= 70) return 'bg-green-100 text-green-800'
    if (score >= 50) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  const getScoreText = (score?: number) => {
    if (!score) return 'Não finalizado'
    return `${score}%`
  }

  if (isLoading) {
    return (
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Simulados Recentes</h3>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="h-4 bg-gray-200 rounded mb-1"></div>
              <div className="h-3 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </Card>
    )
  }

  return (
    <Card className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">
          Simulados Recentes
        </h3>
        <Link href="/resultados">
          <span className="text-sm text-primary-600 hover:text-primary-700 cursor-pointer">
            Ver todos
          </span>
        </Link>
      </div>
      
      {recentSimulados.length === 0 ? (
        <div className="text-center py-8">
          <div className="text-4xl mb-2">📝</div>
          <p className="text-gray-500 mb-4">Nenhum simulado encontrado</p>
          <Link href="/gerador-simulado">
            <span className="text-primary-600 hover:text-primary-700 font-medium cursor-pointer">
              Criar primeiro simulado
            </span>
          </Link>
        </div>
      ) : (
        <div className="space-y-3">
          {recentSimulados.map((simulado) => (
            <Link key={simulado.id} href={`/resultados/${simulado.id}`}>
              <div className="flex justify-between items-center p-3 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors">
                <div className="flex-1">
                  <p className="font-medium text-gray-900">
                    {simulado.config.banca} - {simulado.config.subjects.join(', ')}
                  </p>
                  <p className="text-sm text-gray-500">
                    {formatDate(simulado.created_at)} • {simulado.config.level}
                  </p>
                </div>
                <span className={`text-sm px-2 py-1 rounded ${getScoreColor(simulado.score)}`}>
                  {getScoreText(simulado.score)}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </Card>
  )
}
