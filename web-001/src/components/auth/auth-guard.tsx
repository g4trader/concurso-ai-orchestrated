'use client'

import { useAuth } from '@/hooks/use-auth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { Spinner } from '@/components/ui/spinner'

interface AuthGuardProps {
  children: React.ReactNode
}

export function AuthGuard({ children }: AuthGuardProps) {
  const { state } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!state.isLoading && !state.isAuthenticated) {
      router.push('/login')
    }
  }, [state.isLoading, state.isAuthenticated, router])

  if (state.isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Spinner size="lg" />
      </div>
    )
  }

  if (!state.isAuthenticated) {
    return null
  }

  return <>{children}</>
}
