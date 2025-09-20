import { AuthGuard } from '@/components/auth/auth-guard'
import { ScoreDisplay } from '@/components/resultados/score-display'
import { QuestionReview } from '@/components/resultados/question-review'
import { PerformanceChart } from '@/components/resultados/performance-chart'

export default function ResultadosPage() {
  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Resultados
        </h1>
        
        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-1">
            <ScoreDisplay />
          </div>
          <div className="lg:col-span-2">
            <PerformanceChart />
          </div>
        </div>

        <QuestionReview />
      </div>
    </AuthGuard>
  )
}
