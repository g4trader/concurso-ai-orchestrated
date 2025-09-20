import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function NotFound() {
  return (
    <div className="container mx-auto px-4 py-8 text-center">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        404 - Página não encontrada
      </h1>
      <p className="text-xl text-gray-600 mb-8">
        A página que você está procurando não existe.
      </p>
      <Link href="/">
        <Button>
          Voltar ao início
        </Button>
      </Link>
    </div>
  )
}
