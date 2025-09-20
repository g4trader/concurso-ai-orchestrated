'use client'

import Link from 'next/link'
import { useAuth } from '@/hooks/use-auth'
import { LogoutButton } from '@/components/auth/logout-button'

export function Header() {
  const { state } = useAuth()
  const { user, isAuthenticated } = state

  return (
    <header className="bg-white border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="text-xl font-bold text-primary-600">
            Concurso AI
          </Link>
          
          <nav className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Link href="/dashboard" className="text-gray-700 hover:text-primary-600">
                  Dashboard
                </Link>
                <Link href="/gerador-simulado" className="text-gray-700 hover:text-primary-600">
                  Simulados
                </Link>
                <span className="text-gray-600">
                  Olá, {user?.name}
                </span>
                <LogoutButton />
              </>
            ) : (
              <Link href="/login" className="text-gray-700 hover:text-primary-600">
                Entrar
              </Link>
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}
