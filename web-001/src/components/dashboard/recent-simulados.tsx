import { Card } from '@/components/ui/card'

export function RecentSimulados() {
  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4">
        Simulados Recentes
      </h3>
      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <div>
            <p className="font-medium">CESPE - Direito Constitucional</p>
            <p className="text-sm text-gray-500">15/01/2024</p>
          </div>
          <span className="text-sm bg-green-100 text-green-800 px-2 py-1 rounded">
            78%
          </span>
        </div>
        <div className="flex justify-between items-center">
          <div>
            <p className="font-medium">FGV - Administração Pública</p>
            <p className="text-sm text-gray-500">12/01/2024</p>
          </div>
          <span className="text-sm bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
            65%
          </span>
        </div>
        <div className="flex justify-between items-center">
          <div>
            <p className="font-medium">VUNESP - Português</p>
            <p className="text-sm text-gray-500">10/01/2024</p>
          </div>
          <span className="text-sm bg-green-100 text-green-800 px-2 py-1 rounded">
            82%
          </span>
        </div>
      </div>
    </Card>
  )
}
