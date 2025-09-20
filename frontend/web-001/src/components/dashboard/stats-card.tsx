import { Card } from '@/components/ui/card'

interface StatsCardProps {
  title: string
  value: string
  change: string
}

export function StatsCard({ title, value, change }: StatsCardProps) {
  return (
    <Card className="p-6">
      <h3 className="text-sm font-medium text-gray-500 mb-2">
        {title}
      </h3>
      <p className="text-2xl font-bold text-gray-900 mb-1">
        {value}
      </p>
      <p className="text-sm text-green-600">
        {change}
      </p>
    </Card>
  )
}
