import { NextRequest, NextResponse } from 'next/server'

// Credenciais padrão para demonstração
const DEFAULT_CREDENTIALS = {
  email: 'admin@concursoai.com',
  password: 'admin123'
}

export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json()

    // Verificar credenciais
    if (email === DEFAULT_CREDENTIALS.email && password === DEFAULT_CREDENTIALS.password) {
      const user = {
        id: '1',
        name: 'Administrador',
        email: 'admin@concursoai.com',
        role: 'admin',
        lastLogin: new Date().toISOString()
      }

      return NextResponse.json({
        user,
        token: 'demo-token-12345'
      })
    }

    // Credenciais inválidas
    return NextResponse.json(
      { error: 'Credenciais inválidas' },
      { status: 401 }
    )
  } catch {
    return NextResponse.json(
      { error: 'Erro interno do servidor' },
      { status: 500 }
    )
  }
}
