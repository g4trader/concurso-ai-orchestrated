'use client'

interface ResultsChartProps {
  score: number
}

export function ResultsChart({ score }: ResultsChartProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return '#10B981' // green-500
    if (score >= 60) return '#F59E0B' // yellow-500
    return '#EF4444' // red-500
  }

  const getScoreMessage = (score: number) => {
    if (score >= 90) return 'Excelente'
    if (score >= 80) return 'Muito Bom'
    if (score >= 60) return 'Bom'
    if (score >= 40) return 'Regular'
    return 'Precisa Melhorar'
  }

  return (
    <div className="space-y-6">
      {/* Gráfico Circular Simples */}
      <div className="flex justify-center">
        <div className="relative w-32 h-32">
          <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 36 36">
            {/* Círculo de fundo */}
            <path
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none"
              stroke="#E5E7EB"
              strokeWidth="2"
            />
            {/* Círculo de progresso */}
            <path
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none"
              stroke={getScoreColor(score)}
              strokeWidth="2"
              strokeDasharray={`${score}, 100`}
              strokeLinecap="round"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div className="text-2xl font-bold" style={{ color: getScoreColor(score) }}>
                {score}%
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Informações do Score */}
      <div className="text-center">
        <div className="text-lg font-semibold text-gray-900 mb-2">
          {getScoreMessage(score)}
        </div>
        <div className="text-sm text-gray-600">
          {score >= 80 
            ? 'Parabéns! Você está no caminho certo.'
            : score >= 60
            ? 'Bom resultado! Continue estudando.'
            : 'Foque nos pontos fracos e tente novamente.'
          }
        </div>
      </div>

      {/* Barra de Progresso */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm text-gray-600">
          <span>Progresso</span>
          <span>{score}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="h-2 rounded-full transition-all duration-1000"
            style={{ 
              width: `${score}%`,
              backgroundColor: getScoreColor(score)
            }}
          />
        </div>
      </div>

      {/* Comparação com Meta */}
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">Meta de Aprovação</span>
          <span className="text-sm text-gray-600">80%</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Seu Resultado</span>
          <span className={`text-sm font-medium ${score >= 80 ? 'text-green-600' : 'text-red-600'}`}>
            {score}%
          </span>
        </div>
        {score >= 80 ? (
          <div className="mt-2 text-xs text-green-600">
            ✅ Meta atingida!
          </div>
        ) : (
          <div className="mt-2 text-xs text-red-600">
            ❌ Meta não atingida. Faltam {80 - score} pontos.
          </div>
        )}
      </div>
    </div>
  )
}
