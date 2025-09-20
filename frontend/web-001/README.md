# WEB-001: Protótipo Web Next.js

## Visão Geral
Este é o protótipo base da aplicação web para a plataforma Concurso AI, desenvolvido com Next.js 14 e App Router.

## Funcionalidades
- ✅ Layout responsivo com Header e Footer
- ✅ Sistema de autenticação (mock)
- ✅ Dashboard com estatísticas
- ✅ Página de geração de simulados
- ✅ Página de resultados
- ✅ Componentes UI reutilizáveis
- ✅ Tratamento de erros e loading states

## Tecnologias
- **Next.js 14** com App Router
- **TypeScript** para tipagem
- **Tailwind CSS** para estilização
- **Lucide React** para ícones

## Como Executar

1. **Instalar dependências:**
   ```bash
   npm install
   ```

2. **Configurar variáveis de ambiente:**
   ```bash
   cp env.example .env.local
   ```

3. **Executar em desenvolvimento:**
   ```bash
   npm run dev
   ```

4. **Acessar a aplicação:**
   - Frontend: http://localhost:3000
   - Backend APIs: http://localhost:8000

## Estrutura do Projeto

```
src/
├── app/                    # App Router do Next.js
│   ├── dashboard/         # Página do dashboard
│   ├── gerador-simulado/  # Página de geração de simulados
│   ├── login/             # Página de login
│   ├── resultados/        # Página de resultados
│   ├── globals.css        # Estilos globais
│   ├── layout.tsx         # Layout principal
│   ├── page.tsx           # Página inicial
│   └── ...
├── components/            # Componentes reutilizáveis
│   ├── auth/             # Componentes de autenticação
│   ├── dashboard/        # Componentes do dashboard
│   ├── layout/           # Header, Footer
│   ├── resultados/       # Componentes de resultados
│   ├── simulado/         # Componentes de simulados
│   └── ui/               # Componentes UI base
├── hooks/                # Hooks customizados
├── types/                # Tipos TypeScript
└── lib/                  # Utilitários
```

## Rotas Disponíveis

### Páginas Públicas
- `/` - Página inicial
- `/login` - Login de usuário

### Páginas Protegidas (requer autenticação)
- `/dashboard` - Dashboard principal
- `/gerador-simulado` - Gerar novos simulados
- `/resultados` - Ver resultados de simulados

## Componentes UI

- **Button** - Botão com variantes (default, outline, ghost, destructive)
- **Card** - Container com bordas e sombra
- **Input** - Campo de entrada de texto
- **Alert** - Mensagens de feedback
- **Spinner** - Indicador de carregamento

## Autenticação

O sistema de autenticação está implementado como mock:
- Login com email/senha
- Contexto de autenticação global
- Proteção de rotas com AuthGuard
- Estado de loading e erro

## Próximos Passos

1. **Integração com APIs** - Conectar com os serviços backend
2. **Autenticação real** - Implementar JWT/OAuth
3. **Bancos de dados** - Conectar com PostgreSQL/Redis
4. **Testes** - Adicionar testes unitários e e2e
5. **Deploy** - Configurar para produção

## Variáveis de Ambiente

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Concurso AI

# Authentication
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3000
```
