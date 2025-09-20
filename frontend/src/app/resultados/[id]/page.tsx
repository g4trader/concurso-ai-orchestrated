'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { AuthGuard } from '@/components/auth/auth-guard'
import { ResultsChart } from '@/components/results/results-chart'
import { SubjectAnalysis } from '@/components/results/subject-analysis'
import { Recommendations } from '@/components/results/recommendations'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import Link from 'next/link'

interface SimuladoResult {
  id: string
  simulado_id: string
  user_id: number
  answers: { [key: string]: number }
  score: number
  correct_answers: number
  total_questions: number
  time_spent: number
  submitted_at: string
  simulado_title: string
  subject_performance: { [subject: string]: { correct: number; total: number } }
  recommendations: string[]
}

export default function ResultadosPage() {
  const params = useParams()
  const [result, setResult] = useState<SimuladoResult | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadResults = async () => {
      setIsLoading(true)
      setError(null)
      
      try {
        const { apiClient } = await import('@/lib/api')
        const response = await apiClient.getSimuladoResult(parseInt(params.id as string))

        if (response.data) {
          setResult(response.data as SimuladoResult)
        } else {
          setError(response.error || 'Resultado não encontrado')
        }
      } catch (error) {
        console.error('Erro ao carregar resultados:', error)
        setError('Erro de conexão. Verifique se o backend está funcionando.')
      } finally {
        setIsLoading(false)
      }
    }

    loadResults()
  }, [params.id])

  if (isLoading) {
    return (
      <AuthGuard>
        <div className="container mx-auto px-4 py-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Carregando Resultados...</h1>
          <p>Analisando seu desempenho. Aguarde um momento.</p>
        </div>
      </AuthGuard>
    )
  }

  if (error || !result) {
    return (
      <AuthGuard>
        <div className="container mx-auto px-4 py-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Erro ao Carregar Resultados</h1>
          <p className="text-red-600 mb-4">{error || 'Resultado não encontrado'}</p>
          <div className="space-x-4">
            <Link href="/dashboard">
              <Button>Voltar ao Dashboard</Button>
            </Link>
            <Link href="/gerador-simulado">
              <Button variant="outline">Gerar Novo Simulado</Button>
            </Link>
          </div>
        </div>
      </AuthGuard>
    )
  }

  const scorePercentage = (result.correct_answers / result.total_questions) * 100

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Resultados do Simulado
          </h1>
          <Link href="/dashboard">
            <Button variant="outline">
              Voltar ao Dashboard
            </Button>
          </Link>
        </div>

        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            {result.simulado_title}
          </h2>
          <p className="text-gray-600">
            Finalizado em {new Date(result.submitted_at).toLocaleDateString('pt-BR')} às {new Date(result.submitted_at).toLocaleTimeString('pt-BR')}
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          <Card className="p-6 text-center">
            <h2 className="text-xl font-semibold text-gray-700 mb-2">Sua Pontuação</h2>
            <p className="text-5xl font-bold text-primary-600">{scorePercentage.toFixed(1)}%</p>
            <p className="text-lg text-gray-600 mt-2">
              {result.correct_answers} de {result.total_questions} questões corretas
            </p>
          </Card>

          <Card className="p-6 lg:col-span-2">
            <ResultsChart score={scorePercentage} />
          </Card>
        </div>

        <div className="grid lg:grid-cols-2 gap-6 mb-8">
          <SubjectAnalysis subjectScores={result.subject_performance || {}} />
          <Recommendations recommendations={result.recommendations} />
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card className="p-6 text-center">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Tempo Gasto</h3>
            <p className="text-2xl font-bold text-blue-600">
              {Math.floor(result.time_spent / 60)}min {result.time_spent % 60}s
            </p>
          </Card>
          
          <Card className="p-6 text-center">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Taxa de Acerto</h3>
            <p className="text-2xl font-bold text-green-600">
              {scorePercentage.toFixed(1)}%
            </p>
          </Card>
          
          <Card className="p-6 text-center">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Questões</h3>
            <p className="text-2xl font-bold text-purple-600">
              {result.total_questions}
            </p>
          </Card>
        </div>

        <div className="text-center">
          <div className="space-x-4">
            <Link href="/gerador-simulado">
              <Button size="lg" className="bg-primary-600 hover:bg-primary-700">
                Gerar Novo Simulado
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button size="lg" variant="outline">
                Ver Todos os Resultados
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}