import { AuthGuard } from '@/components/auth/auth-guard'
import { SimuladoForm } from '@/components/simulado/simulado-form'
import { Card } from '@/components/ui/card'

export default function GeradorSimuladoPage() {
  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Gerar Simulado
        </h1>
        
        <Card className="p-6">
          <SimuladoForm />
        </Card>
      </div>
    </AuthGuard>
  )
}
