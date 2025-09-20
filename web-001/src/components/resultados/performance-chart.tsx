import { Card } from '@/components/ui/card'

export function PerformanceChart() {
  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4">
        Performance por Tópico
      </h3>
      <div className="space-y-4">
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Direito Constitucional</span>
            <span>85%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-green-600 h-2 rounded-full" style={{ width: '85%' }}></div>
          </div>
        </div>
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Administração Pública</span>
            <span>70%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-yellow-600 h-2 rounded-full" style={{ width: '70%' }}></div>
          </div>
        </div>
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Português</span>
            <span>65%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-red-600 h-2 rounded-full" style={{ width: '65%' }}></div>
          </div>
        </div>
      </div>
    </Card>
  )
}
