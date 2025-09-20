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

interface Question {
  id: string
  text: string
  options: string[]
  correctAnswer: number
  explanation?: string
  subject: string
}

interface SimuladoResult {
  id: string
  title: string
  questions: Question[]
  answers: { [key: string]: number }
  timeSpent: number
  submittedAt: string
  score: number
  correctAnswers: number
  totalQuestions: number
  subjectScores: { [subject: string]: { correct: number; total: number } }
}

export default function ResultadosPage() {
  const params = useParams()
  const [result, setResult] = useState<SimuladoResult | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const loadResult = async () => {
      setIsLoading(true)
      
      // Carregar dados do simulado do localStorage
      const simuladoData = localStorage.getItem(`simulado_${params.id}`)
      const simuladoConfig = localStorage.getItem(`simulado_config_${params.id}`)
      
      if (!simuladoData || !simuladoConfig) {
        setIsLoading(false)
        return
      }

      const answers = JSON.parse(simuladoData)
      // const config = JSON.parse(simuladoConfig) // Configuração não usada no momento

      // Mock data para demonstração
      const mockQuestions: Question[] = [
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

      // Calcular resultados
      let correctAnswers = 0
      const subjectScores: { [subject: string]: { correct: number; total: number } } = {}

      mockQuestions.forEach(question => {
        const userAnswer = answers.answers[question.id]
        const isCorrect = userAnswer === question.correctAnswer
        
        if (isCorrect) {
          correctAnswers++
        }

        if (!subjectScores[question.subject]) {
          subjectScores[question.subject] = { correct: 0, total: 0 }
        }
        
        subjectScores[question.subject].total++
        if (isCorrect) {
          subjectScores[question.subject].correct++
        }
      })

      const score = Math.round((correctAnswers / mockQuestions.length) * 100)

      const simuladoResult: SimuladoResult = {
        id: params.id as string,
        title: 'Simulado CESPE - Direito Constitucional',
        questions: mockQuestions,
        answers: answers.answers,
        timeSpent: answers.timeSpent,
        submittedAt: answers.submittedAt,
        score,
        correctAnswers,
        totalQuestions: mockQuestions.length,
        subjectScores
      }

      setResult(simuladoResult)
      setIsLoading(false)
    }

    loadResult()
  }, [params.id])

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60
    
    if (hours > 0) {
      return `${hours}h ${minutes}m ${secs}s`
    }
    return `${minutes}m ${secs}s`
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreMessage = (score: number) => {
    if (score >= 90) return 'Excelente! Continue assim!'
    if (score >= 80) return 'Muito bom! Pequenos ajustes e você estará perfeito.'
    if (score >= 60) return 'Bom resultado! Há espaço para melhorias.'
    if (score >= 40) return 'Resultado regular. Foque nos pontos fracos.'
    return 'Resultado abaixo do esperado. Revise o conteúdo e tente novamente.'
  }

  if (isLoading) {
    return (
      <AuthGuard>
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-center min-h-[400px]">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Carregando resultados...</p>
            </div>
          </div>
        </div>
      </AuthGuard>
    )
  }

  if (!result) {
    return (
      <AuthGuard>
        <div className="container mx-auto px-4 py-8">
          <Card className="p-6 text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">
              Resultados não encontrados
            </h1>
            <p className="text-gray-600 mb-6">
              Não foi possível carregar os resultados deste simulado.
            </p>
            <Link href="/dashboard">
              <Button>Voltar ao Dashboard</Button>
            </Link>
          </Card>
        </div>
      </AuthGuard>
    )
  }

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Resultados do Simulado
              </h1>
              <p className="text-gray-600">{result.title}</p>
            </div>
            <Link href="/dashboard">
              <Button variant="outline">← Voltar ao Dashboard</Button>
            </Link>
          </div>
        </div>

        {/* Score Principal */}
        <Card className="p-8 mb-8 text-center">
          <div className="mb-4">
            <div className={`text-6xl font-bold ${getScoreColor(result.score)}`}>
              {result.score}%
            </div>
            <div className="text-xl text-gray-600 mt-2">
              {result.correctAnswers} de {result.totalQuestions} questões corretas
            </div>
          </div>
          
          <div className="text-lg text-gray-700 mb-4">
            {getScoreMessage(result.score)}
          </div>
          
          <div className="flex justify-center gap-8 text-sm text-gray-600">
            <div>
              <span className="font-medium">Tempo gasto:</span> {formatTime(result.timeSpent)}
            </div>
            <div>
              <span className="font-medium">Finalizado em:</span> {new Date(result.submittedAt).toLocaleString()}
            </div>
          </div>
        </Card>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Gráfico de Performance */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              📊 Performance Geral
            </h2>
            <ResultsChart score={result.score} />
          </Card>

          {/* Análise por Matéria */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              📚 Análise por Matéria
            </h2>
            <SubjectAnalysis subjectScores={result.subjectScores} />
          </Card>
        </div>

        {/* Recomendações */}
        <Card className="p-6 mt-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            💡 Recomendações de Estudo
          </h2>
          <Recommendations 
            score={result.score}
            subjectScores={result.subjectScores}
            timeSpent={result.timeSpent}
          />
        </Card>

        {/* Ações */}
        <div className="flex justify-center gap-4 mt-8">
          <Link href="/gerador-simulado">
            <Button className="bg-primary-600 hover:bg-primary-700">
              Fazer Novo Simulado
            </Button>
          </Link>
          <Button variant="outline">
            📄 Exportar Resultados
          </Button>
        </div>
      </div>
    </AuthGuard>
  )
}
