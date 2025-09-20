import { AuthGuard } from '@/components/auth/auth-guard'
import { StatsCard } from '@/components/dashboard/stats-card'
import { RecentSimulados } from '@/components/dashboard/recent-simulados'
import { ProgressChart } from '@/components/dashboard/progress-chart'
import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function DashboardPage() {
  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Dashboard
          </h1>
          <div className="flex gap-3">
            <Link href="/gerador-simulado">
              <Button className="bg-primary-600 hover:bg-primary-700">
                Novo Simulado
              </Button>
            </Link>
            <Link href="/resultados">
              <Button variant="outline">
                Ver Resultados
              </Button>
            </Link>
          </div>
        </div>
        
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Simulados Realizados"
            value="12"
            change="+2 esta semana"
            icon="📊"
          />
          <StatsCard
            title="Taxa de Acerto"
            value="78%"
            change="+5% este mês"
            icon="🎯"
          />
          <StatsCard
            title="Tempo Médio"
            value="45min"
            change="-3min por simulado"
            icon="⏱️"
          />
          <StatsCard
            title="Ranking"
            value="#15"
            change="+3 posições"
            icon="🏆"
          />
        </div>

        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2">
            <RecentSimulados />
          </div>
          <div>
            <ProgressChart />
          </div>
        </div>

        {/* Seção de Ações Rápidas */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Ações Rápidas
          </h2>
          <div className="grid md:grid-cols-3 gap-4">
            <Link href="/gerador-simulado">
              <div className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors">
                <div className="text-2xl mb-2">📝</div>
                <h3 className="font-medium text-gray-900">Criar Simulado</h3>
                <p className="text-sm text-gray-600">Gere um novo simulado personalizado</p>
              </div>
            </Link>
            <Link href="/resultados">
              <div className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors">
                <div className="text-2xl mb-2">📈</div>
                <h3 className="font-medium text-gray-900">Ver Resultados</h3>
                <p className="text-sm text-gray-600">Analise seu desempenho</p>
              </div>
            </Link>
            <div className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors">
              <div className="text-2xl mb-2">📚</div>
              <h3 className="font-medium text-gray-900">Estudar</h3>
              <p className="text-sm text-gray-600">Acesse materiais de estudo</p>
            </div>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}
