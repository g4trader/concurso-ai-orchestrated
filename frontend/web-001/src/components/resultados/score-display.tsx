import { Card } from '@/components/ui/card'

export function ScoreDisplay() {
  return (
    <Card className="p-6 text-center">
      <h3 className="text-lg font-semibold mb-4">
        Resultado do Simulado
      </h3>
      <div className="text-4xl font-bold text-green-600 mb-2">
        78%
      </div>
      <p className="text-gray-600 mb-4">
        16 de 20 questões corretas
      </p>
      <div className="space-y-2">
        <div className="flex justify-between">
          <span>Acertos:</span>
          <span className="font-medium">16</span>
        </div>
        <div className="flex justify-between">
          <span>Erros:</span>
          <span className="font-medium">4</span>
        </div>
        <div className="flex justify-between">
          <span>Tempo:</span>
          <span className="font-medium">42min</span>
        </div>
      </div>
    </Card>
  )
}
