'use client'

interface SubjectScores {
  [subject: string]: {
    correct: number
    total: number
  }
}

interface RecommendationsProps {
  score: number
  subjectScores: SubjectScores
  timeSpent: number
}

export function Recommendations({ score, subjectScores, timeSpent }: RecommendationsProps) {
  const getWeakSubjects = () => {
    return Object.entries(subjectScores)
      .filter(([, data]) => data.total > 0)
      .map(([subject, data]) => ({
        subject,
        score: Math.round((data.correct / data.total) * 100)
      }))
      .filter(item => item.score < 70)
      .sort((a, b) => a.score - b.score)
      .slice(0, 3)
  }

  const getStrongSubjects = () => {
    return Object.entries(subjectScores)
      .filter(([, data]) => data.total > 0)
      .map(([subject, data]) => ({
        subject,
        score: Math.round((data.correct / data.total) * 100)
      }))
      .filter(item => item.score >= 80)
      .sort((a, b) => b.score - a.score)
      .slice(0, 2)
  }

  const getTimeRecommendation = () => {
    const avgTimePerQuestion = timeSpent / Object.values(subjectScores).reduce((sum, data) => sum + data.total, 0)
    
    if (avgTimePerQuestion > 120) { // Mais de 2 minutos por questão
      return {
        type: 'speed',
        message: 'Você está gastando muito tempo por questão. Pratique mais para aumentar a velocidade.',
        icon: '⏰'
      }
    } else if (avgTimePerQuestion < 60) { // Menos de 1 minuto por questão
      return {
        type: 'accuracy',
        message: 'Você está respondendo muito rápido. Tome mais tempo para ler e analisar as questões.',
        icon: '🎯'
      }
    } else {
      return {
        type: 'balanced',
        message: 'Seu tempo por questão está equilibrado. Continue assim!',
        icon: '⚖️'
      }
    }
  }

  const weakSubjects = getWeakSubjects()
  const strongSubjects = getStrongSubjects()
  const timeRec = getTimeRecommendation()

  return (
    <div className="space-y-6">
      {/* Recomendação Geral */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <div className="text-2xl">🎯</div>
          <div>
            <h3 className="font-semibold text-blue-900 mb-2">
              Recomendação Geral
            </h3>
            <p className="text-blue-800 text-sm">
              {score >= 80 
                ? 'Excelente desempenho! Continue mantendo esse nível e foque em consolidar seus conhecimentos.'
                : score >= 60
                ? 'Bom resultado! Continue estudando e foque especialmente nas matérias com menor desempenho.'
                : 'Seu resultado indica que é necessário intensificar os estudos. Foque nas matérias básicas primeiro.'
              }
            </p>
          </div>
        </div>
      </div>

      {/* Matérias que Precisam de Atenção */}
      {weakSubjects.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <div className="text-2xl">⚠️</div>
            <div>
              <h3 className="font-semibold text-red-900 mb-2">
                Matérias que Precisam de Mais Atenção
              </h3>
              <ul className="space-y-2 text-red-800 text-sm">
                {weakSubjects.map((item, index) => (
                  <li key={item.subject} className="flex items-center gap-2">
                    <span className="font-medium">{index + 1}.</span>
                    <span>{item.subject}</span>
                    <span className="text-red-600 font-medium">({item.score}%)</span>
                  </li>
                ))}
              </ul>
              <p className="text-red-700 text-xs mt-2">
                💡 Dedique mais tempo de estudo a essas matérias nos próximos simulados.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Matérias de Força */}
      {strongSubjects.length > 0 && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <div className="text-2xl">✅</div>
            <div>
              <h3 className="font-semibold text-green-900 mb-2">
                Suas Matérias de Força
              </h3>
              <ul className="space-y-2 text-green-800 text-sm">
                {strongSubjects.map((item, index) => (
                  <li key={item.subject} className="flex items-center gap-2">
                    <span className="font-medium">{index + 1}.</span>
                    <span>{item.subject}</span>
                    <span className="text-green-600 font-medium">({item.score}%)</span>
                  </li>
                ))}
              </ul>
              <p className="text-green-700 text-xs mt-2">
                🎉 Continue mantendo esse excelente desempenho nessas matérias!
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Recomendação de Tempo */}
      <div className={`border rounded-lg p-4 ${
        timeRec.type === 'speed' ? 'bg-yellow-50 border-yellow-200' :
        timeRec.type === 'accuracy' ? 'bg-blue-50 border-blue-200' :
        'bg-green-50 border-green-200'
      }`}>
        <div className="flex items-start gap-3">
          <div className="text-2xl">{timeRec.icon}</div>
          <div>
            <h3 className={`font-semibold mb-2 ${
              timeRec.type === 'speed' ? 'text-yellow-900' :
              timeRec.type === 'accuracy' ? 'text-blue-900' :
              'text-green-900'
            }`}>
              Análise de Tempo
            </h3>
            <p className={`text-sm ${
              timeRec.type === 'speed' ? 'text-yellow-800' :
              timeRec.type === 'accuracy' ? 'text-blue-800' :
              'text-green-800'
            }`}>
              {timeRec.message}
            </p>
            <p className={`text-xs mt-2 ${
              timeRec.type === 'speed' ? 'text-yellow-700' :
              timeRec.type === 'accuracy' ? 'text-blue-700' :
              'text-green-700'
            }`}>
              Tempo médio por questão: {Math.round(timeSpent / Object.values(subjectScores).reduce((sum, data) => sum + data.total, 0))} segundos
            </p>
          </div>
        </div>
      </div>

      {/* Próximos Passos */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <div className="text-2xl">📚</div>
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">
              Próximos Passos Recomendados
            </h3>
            <ul className="space-y-2 text-gray-700 text-sm">
              <li className="flex items-start gap-2">
                <span className="text-primary-600">1.</span>
                <span>Faça um novo simulado focando nas matérias com menor desempenho</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary-600">2.</span>
                <span>Revise os conteúdos das questões que você errou</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary-600">3.</span>
                <span>Pratique mais questões da mesma banca e matéria</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary-600">4.</span>
                <span>Mantenha um cronograma regular de estudos</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
