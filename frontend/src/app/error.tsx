'use client'

import { useEffect } from 'react'
import { Alert } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div className="container mx-auto px-4 py-8">
      <Alert variant="destructive">
        <h2 className="text-lg font-semibold mb-2">
          Algo deu errado!
        </h2>
        <p className="mb-4">
          Ocorreu um erro inesperado. Tente novamente.
        </p>
        <Button onClick={reset}>
          Tentar novamente
        </Button>
      </Alert>
    </div>
  )
}
