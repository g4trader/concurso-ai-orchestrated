/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configurações de imagem
  images: {
    domains: ['localhost', 'vercel.app', 'concurso-ai.vercel.app'],
    formats: ['image/webp', 'image/avif'],
  },
  
  // Variáveis de ambiente
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME || 'Concurso AI',
  },
  
  // Configurações de produção
  output: 'standalone',
  
  // Configurações de build
  experimental: {
    optimizeCss: true,
  },
  
  // Configurações de compressão
  compress: true,
  
  // Configurações de headers de segurança
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ]
  },
  
  // Configurações de redirecionamento
  async redirects() {
    return [
      {
        source: '/home',
        destination: '/',
        permanent: true,
      },
    ]
  },
}

module.exports = nextConfig
