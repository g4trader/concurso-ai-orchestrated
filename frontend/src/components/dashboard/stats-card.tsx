import { Card } from '@/components/ui/card'

interface StatsCardProps {
  title: string
  value: string
  change: string
  icon?: string
}

export function StatsCard({ title, value, change, icon }: StatsCardProps) {
  return (
    <Card className="p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-gray-500">
          {title}
        </h3>
        {icon && (
          <span className="text-2xl">{icon}</span>
        )}
      </div>
      <p className="text-2xl font-bold text-gray-900 mb-1">
        {value}
      </p>
      <p className="text-sm text-green-600">
        {change}
      </p>
    </Card>
  )
}
