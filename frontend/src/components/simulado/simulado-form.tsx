// import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export function SimuladoForm() {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">
        Configurar Simulado
      </h2>
      
      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Banca
          </label>
          <select className="w-full h-10 px-3 border border-gray-300 rounded-md">
            <option>CESPE</option>
            <option>FGV</option>
            <option>VUNESP</option>
            <option>FCC</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Tópico
          </label>
          <Input placeholder="Ex: Direito Constitucional" />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Número de Questões
          </label>
          <Input type="number" defaultValue="20" />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Tempo Limite (minutos)
          </label>
          <Input type="number" defaultValue="60" />
        </div>
      </div>
      
      <Button className="w-full" size="lg">
        Gerar Simulado
      </Button>
    </div>
  )
}
