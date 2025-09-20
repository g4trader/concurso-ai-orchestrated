import { Card } from '@/components/ui/card'

export function ProgressChart() {
  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4">
        Progresso Mensal
      </h3>
      <div className="space-y-4">
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Taxa de Acerto</span>
            <span>78%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-green-600 h-2 rounded-full" style={{ width: '78%' }}></div>
          </div>
        </div>
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Questões Respondidas</span>
            <span>240</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-blue-600 h-2 rounded-full" style={{ width: '60%' }}></div>
          </div>
        </div>
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Simulados Completos</span>
            <span>12</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-purple-600 h-2 rounded-full" style={{ width: '40%' }}></div>
          </div>
        </div>
      </div>
    </Card>
  )
}
