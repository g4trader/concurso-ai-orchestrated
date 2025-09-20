'use client'

import { Card } from '@/components/ui/card'

interface SimuladoTimerProps {
  timeRemaining: number
  totalTime: number
  onTimeUp?: () => void
}

export function SimuladoTimer({ timeRemaining, totalTime }: SimuladoTimerProps) {
  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`
  }

  const progress = ((totalTime - timeRemaining) / totalTime) * 100
  const isWarning = timeRemaining <= 300 // 5 minutos
  const isCritical = timeRemaining <= 60 // 1 minuto

  const getTimerColor = () => {
    if (isCritical) return 'text-red-600 bg-red-50 border-red-200'
    if (isWarning) return 'text-yellow-600 bg-yellow-50 border-yellow-200'
    return 'text-blue-600 bg-blue-50 border-blue-200'
  }

  const getProgressColor = () => {
    if (isCritical) return 'bg-red-500'
    if (isWarning) return 'bg-yellow-500'
    return 'bg-blue-500'
  }

  return (
    <Card className={`p-4 border-2 ${getTimerColor()}`}>
      <div className="text-center">
        <div className="text-2xl font-bold mb-2">
          {formatTime(timeRemaining)}
        </div>
        <div className="text-sm text-gray-600 mb-3">
          Tempo restante
        </div>
        
        <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
          <div
            className={`h-2 rounded-full transition-all duration-1000 ${getProgressColor()}`}
            style={{ width: `${progress}%` }}
          />
        </div>
        
        <div className="text-xs text-gray-500">
          {Math.round(progress)}% concluído
        </div>
      </div>
    </Card>
  )
}
