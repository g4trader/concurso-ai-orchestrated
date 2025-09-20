'use client'

import { useState, useEffect } from 'react'
import { AuthGuard } from '@/components/auth/auth-guard'
import { StatsCard } from '@/components/dashboard/stats-card'
import { RecentSimulados } from '@/components/dashboard/recent-simulados'
import { ProgressChart } from '@/components/dashboard/progress-chart'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/hooks/use-auth'

interface DashboardStats {
  total_simulados: number
  average_score: number
  average_time_spent: number
  ranking_position: number
  recent_simulados: any[]
  progress_data: { [key: string]: number }
}

export default function DashboardPage() {
  const { state } = useAuth()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadDashboardData = async () => {
      if (!state.token) return
      
      setIsLoading(true)
      setError(null)
      
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 
          (typeof window !== 'undefined' && window.location.hostname === 'localhost' 
            ? 'http://localhost:8000' 
            : 'https://concurso-ai-backend.railway.app')

        const response = await fetch(`${apiUrl}/dashboard/stats`, {
          headers: {
            'Authorization': `Bearer ${state.token}`
          }
        })
        
        if (response.ok) {
          const data = await response.json()
          setStats(data)
        } else {
          setError('Erro ao carregar dados do dashboard')
        }
      } catch (error) {
        setError('Erro de conexão')
      } finally {
        setIsLoading(false)
      }
    }

    loadDashboardData()
  }, [state.token])

  if (isLoading) {
    return (
      <AuthGuard>
        <div className="container mx-auto px-4 py-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">Carregando Dashboard...</h1>
            <p>Buscando seus dados. Aguarde um momento.</p>
          </div>
        </div>
      </AuthGuard>
    )
  }

  if (error) {
    return (
      <AuthGuard>
        <div className="container mx-auto px-4 py-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">Erro no Dashboard</h1>
            <p className="text-red-600 mb-4">{error}</p>
            <Button onClick={() => window.location.reload()}>
              Tentar Novamente
            </Button>
          </div>
        </div>
      </AuthGuard>
    )
  }

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Dashboard
            </h1>
            <p className="text-gray-600 mt-1">
              Bem-vindo, {state.user?.name || state.user?.email}!
            </p>
          </div>
          <div className="flex gap-3">
            <Link href="/gerador-simulado">
              <Button className="bg-primary-600 hover:bg-primary-700">
                Novo Simulado
              </Button>
            </Link>
            <Link href="/resultados">
              <Button variant="outline">
                Ver Resultados
              </Button>
            </Link>
          </div>
        </div>
        
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Simulados Realizados"
            value={stats?.total_simulados?.toString() || "0"}
            change="Dados em tempo real"
            icon="📊"
          />
          <StatsCard
            title="Taxa de Acerto"
            value={`${stats?.average_score?.toFixed(1) || "0"}%`}
            change="Média geral"
            icon="🎯"
          />
          <StatsCard
            title="Tempo Médio"
            value={`${Math.round((stats?.average_time_spent || 0) / 60)}min`}
            change="Por simulado"
            icon="⏱️"
          />
          <StatsCard
            title="Ranking"
            value={`#${stats?.ranking_position || "N/A"}`}
            change="Posição atual"
            icon="🏆"
          />
        </div>

        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2">
            <RecentSimulados />
          </div>
          <div>
            <ProgressChart />
          </div>
        </div>

        {/* Seção de Ações Rápidas */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Ações Rápidas
          </h2>
          <div className="grid md:grid-cols-3 gap-4">
            <Link href="/gerador-simulado">
              <div className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors">
                <div className="text-2xl mb-2">📝</div>
                <h3 className="font-medium text-gray-900">Criar Simulado</h3>
                <p className="text-sm text-gray-600">Gere um novo simulado personalizado</p>
              </div>
            </Link>
            <Link href="/resultados">
              <div className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors">
                <div className="text-2xl mb-2">📈</div>
                <h3 className="font-medium text-gray-900">Ver Resultados</h3>
                <p className="text-sm text-gray-600">Analise seu desempenho</p>
              </div>
            </Link>
            <div className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors">
              <div className="text-2xl mb-2">📚</div>
              <h3 className="font-medium text-gray-900">Estudar</h3>
              <p className="text-sm text-gray-600">Acesse materiais de estudo</p>
            </div>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}
