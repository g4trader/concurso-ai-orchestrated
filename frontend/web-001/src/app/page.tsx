import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Concurso AI
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Simulados inteligentes para concursos públicos
        </p>
        <div className="space-x-4">
          <Link href="/login">
            <Button size="lg">
              Entrar
            </Button>
          </Link>
          <Link href="/dashboard">
            <Button variant="outline" size="lg">
              Dashboard
            </Button>
          </Link>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-2">
            Simulados Personalizados
          </h3>
          <p className="text-gray-600">
            Questões geradas por IA baseadas no seu perfil de estudo
          </p>
        </Card>
        
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-2">
            Análise de Performance
          </h3>
          <p className="text-gray-600">
            Relatórios detalhados do seu progresso e pontos de melhoria
          </p>
        </Card>
        
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-2">
            Múltiplas Bancas
          </h3>
          <p className="text-gray-600">
            CESPE, FGV, VUNESP e outras bancas organizadoras
          </p>
        </Card>
      </div>
    </div>
  )
}
