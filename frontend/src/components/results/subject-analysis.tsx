'use client'

interface SubjectScores {
  [subject: string]: {
    correct: number
    total: number
  }
}

interface SubjectAnalysisProps {
  subjectScores: SubjectScores
}

export function SubjectAnalysis({ subjectScores }: SubjectAnalysisProps) {
  const getSubjectScore = (subject: string) => {
    const data = subjectScores[subject]
    if (!data || data.total === 0) return 0
    return Math.round((data.correct / data.total) * 100)
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50'
    if (score >= 60) return 'text-yellow-600 bg-yellow-50'
    return 'text-red-600 bg-red-50'
  }

  const getScoreIcon = (score: number) => {
    if (score >= 80) return '✅'
    if (score >= 60) return '⚠️'
    return '❌'
  }

  const subjects = Object.keys(subjectScores)
  const sortedSubjects = subjects.sort((a, b) => getSubjectScore(b) - getSubjectScore(a))

  if (subjects.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        <p>Nenhuma análise de matéria disponível.</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {sortedSubjects.map(subject => {
        const score = getSubjectScore(subject)
        const data = subjectScores[subject]
        
        return (
          <div key={subject} className="border rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <span className="text-lg">{getScoreIcon(score)}</span>
                <h3 className="font-medium text-gray-900">{subject}</h3>
              </div>
              <div className={`px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(score)}`}>
                {score}%
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm text-gray-600">
                <span>Acertos</span>
                <span>{data.correct} de {data.total}</span>
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all duration-1000 ${
                    score >= 80 ? 'bg-green-500' : score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${score}%` }}
                />
              </div>
              
              <div className="text-xs text-gray-500">
                {score >= 80 
                  ? 'Excelente desempenho nesta matéria!'
                  : score >= 60
                  ? 'Bom desempenho, mas há espaço para melhorias.'
                  : 'Foque mais nesta matéria nos próximos estudos.'
                }
              </div>
            </div>
          </div>
        )
      })}

      {/* Resumo Geral */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-medium text-blue-900 mb-2">
          📊 Resumo por Matéria
        </h4>
        <div className="space-y-1 text-sm text-blue-800">
          <div className="flex justify-between">
            <span>Matéria com melhor desempenho:</span>
            <span className="font-medium">
              {sortedSubjects[0]} ({getSubjectScore(sortedSubjects[0])}%)
            </span>
          </div>
          <div className="flex justify-between">
            <span>Matéria que precisa de mais atenção:</span>
            <span className="font-medium">
              {sortedSubjects[sortedSubjects.length - 1]} ({getSubjectScore(sortedSubjects[sortedSubjects.length - 1])}%)
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
