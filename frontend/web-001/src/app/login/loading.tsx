import { Spinner } from '@/components/ui/spinner'

export default function LoginLoading() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-md mx-auto">
        <div className="flex items-center justify-center p-6">
          <Spinner size="lg" />
        </div>
      </div>
    </div>
  )
}
