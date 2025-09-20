'use client'

import { Card } from '@/components/ui/card'

interface Question {
  id: string
  text: string
  options: string[]
  correctAnswer: number
  explanation?: string
  subject: string
}

interface SimuladoNavigationProps {
  questions: Question[]
  currentQuestion: number
  answers: { [key: string]: number }
  onQuestionSelect: (index: number) => void
}

export function SimuladoNavigation({ 
  questions, 
  currentQuestion, 
  answers, 
  onQuestionSelect 
}: SimuladoNavigationProps) {
  const getQuestionStatus = (index: number) => {
    const questionId = questions[index].id
    if (answers[questionId] !== undefined) {
      return 'answered'
    }
    return 'unanswered'
  }

  const getQuestionStyle = (index: number) => {
    const status = getQuestionStatus(index)
    const isCurrent = index === currentQuestion
    
    if (isCurrent) {
      return 'bg-blue-500 text-white border-blue-500'
    }
    
    if (status === 'answered') {
      return 'bg-green-100 text-green-800 border-green-300'
    }
    
    return 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
  }

  const answeredCount = Object.keys(answers).length
  const totalQuestions = questions.length

  return (
    <Card className="p-4">
      <div className="mb-4">
        <h3 className="font-semibold text-gray-900 mb-2">
          Navegação
        </h3>
        <div className="text-sm text-gray-600">
          {answeredCount} de {totalQuestions} questões respondidas
        </div>
      </div>

      <div className="grid grid-cols-5 gap-2 mb-4">
        {questions.map((_, index) => (
          <button
            key={index}
            onClick={() => onQuestionSelect(index)}
            className={`w-8 h-8 rounded-full border-2 text-sm font-medium transition-all ${getQuestionStyle(index)}`}
            title={`Questão ${index + 1}${getQuestionStatus(index) === 'answered' ? ' (respondida)' : ''}`}
          >
            {index + 1}
          </button>
        ))}
      </div>

      <div className="space-y-2 text-xs">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
          <span className="text-gray-600">Atual</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-100 border border-green-300 rounded-full"></div>
          <span className="text-gray-600">Respondida</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-white border border-gray-300 rounded-full"></div>
          <span className="text-gray-600">Não respondida</span>
        </div>
      </div>
    </Card>
  )
}
