import { AuthGuard } from '@/components/auth/auth-guard'
import { StatsCard } from '@/components/dashboard/stats-card'
import { RecentSimulados } from '@/components/dashboard/recent-simulados'
import { ProgressChart } from '@/components/dashboard/progress-chart'

export default function DashboardPage() {
  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Dashboard
        </h1>
        
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <StatsCard
            title="Simulados Realizados"
            value="12"
            change="+2 esta semana"
          />
          <StatsCard
            title="Taxa de Acerto"
            value="78%"
            change="+5% este mês"
          />
          <StatsCard
            title="Tempo Médio"
            value="45min"
            change="-3min por simulado"
          />
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          <RecentSimulados />
          <ProgressChart />
        </div>
      </div>
    </AuthGuard>
  )
}
