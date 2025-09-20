import { AuthGuard } from '@/components/auth/auth-guard'
import { SimuladoForm } from '@/components/simulado/simulado-form'
import { Card } from '@/components/ui/card'
import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function GeradorSimuladoPage() {
  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Gerar Simulado
          </h1>
          <Link href="/dashboard">
            <Button variant="outline">
              ← Voltar ao Dashboard
            </Button>
          </Link>
        </div>
        
        <div className="grid lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <Card className="p-6">
              <div className="mb-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  Configurações do Simulado
                </h2>
                <p className="text-gray-600">
                  Personalize seu simulado de acordo com suas necessidades de estudo.
                </p>
              </div>
              <SimuladoForm />
            </Card>
          </div>
          
          <div className="space-y-6">
            <Card className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                💡 Dicas para um Bom Simulado
              </h3>
              <ul className="space-y-3 text-sm text-gray-600">
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  Escolha um número de questões adequado ao seu tempo disponível
                </li>
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  Defina um tempo limite realista para simular condições reais
                </li>
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  Selecione matérias que você está estudando atualmente
                </li>
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  Revise os resultados para identificar pontos de melhoria
                </li>
              </ul>
            </Card>
            
            <Card className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                📊 Estatísticas Rápidas
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Simulados realizados:</span>
                  <span className="font-medium">12</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Taxa de acerto:</span>
                  <span className="font-medium text-green-600">78%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Tempo médio:</span>
                  <span className="font-medium">45min</span>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}
