import { LoginForm } from '@/components/auth/login-form'
import { Card } from '@/components/ui/card'

export default function LoginPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-md mx-auto">
        <Card className="p-6">
          <h1 className="text-2xl font-bold text-center mb-6">
            Entrar
          </h1>
          <LoginForm />
        </Card>
      </div>
    </div>
  )
}
