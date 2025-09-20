'use client'

interface Question {
  id: string
  text: string
  options: string[]
  correctAnswer: number
  explanation?: string
  subject: string
}

interface QuestionCardProps {
  question: Question
  selectedAnswer?: number
  onAnswerSelect: (answerIndex: number) => void
  isSubmitted?: boolean
}

export function QuestionCard({ 
  question, 
  selectedAnswer, 
  onAnswerSelect, 
  isSubmitted = false 
}: QuestionCardProps) {
  const getOptionStyle = (index: number) => {
    if (isSubmitted) {
      if (index === question.correctAnswer) {
        return 'bg-green-100 border-green-500 text-green-800'
      }
      if (index === selectedAnswer && index !== question.correctAnswer) {
        return 'bg-red-100 border-red-500 text-red-800'
      }
      return 'bg-gray-100 border-gray-300 text-gray-600'
    }
    
    if (selectedAnswer === index) {
      return 'bg-blue-100 border-blue-500 text-blue-800'
    }
    
    return 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
  }

  const getOptionLabel = (index: number) => {
    const labels = ['A', 'B', 'C', 'D', 'E']
    return labels[index] || String.fromCharCode(65 + index)
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          {question.text}
        </h2>
        
        <div className="space-y-3">
          {question.options.map((option, index) => (
            <label
              key={index}
              className={`flex items-start p-4 border-2 rounded-lg cursor-pointer transition-all ${
                !isSubmitted ? 'hover:shadow-md' : ''
              } ${getOptionStyle(index)}`}
            >
              <input
                type="radio"
                name={`question-${question.id}`}
                value={index}
                checked={selectedAnswer === index}
                onChange={() => onAnswerSelect(index)}
                disabled={isSubmitted}
                className="sr-only"
              />
              
              <div className="flex items-start w-full">
                <div className={`flex-shrink-0 w-8 h-8 rounded-full border-2 flex items-center justify-center text-sm font-bold mr-3 ${
                  isSubmitted
                    ? index === question.correctAnswer
                      ? 'bg-green-500 border-green-500 text-white'
                      : index === selectedAnswer
                      ? 'bg-red-500 border-red-500 text-white'
                      : 'bg-gray-300 border-gray-300 text-gray-600'
                    : selectedAnswer === index
                    ? 'bg-blue-500 border-blue-500 text-white'
                    : 'bg-white border-gray-300 text-gray-600'
                }`}>
                  {getOptionLabel(index)}
                </div>
                
                <div className="flex-1">
                  <p className="text-sm leading-relaxed">
                    {option}
                  </p>
                </div>
              </div>
            </label>
          ))}
        </div>
      </div>

      {isSubmitted && question.explanation && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-semibold text-blue-900 mb-2">
            💡 Explicação
          </h3>
          <p className="text-blue-800 text-sm">
            {question.explanation}
          </p>
        </div>
      )}
    </div>
  )
}
