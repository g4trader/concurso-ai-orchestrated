# FE_SCAFFOLD_WEB-003: Frontend Scaffolding - Tela de Geração de Simulado

## Estrutura de Arquivos Criados

### 1. Configuração Base

#### package.json
```json
{
  "name": "concurso-ai-simulado",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "dependencies": {
    "next": "14.0.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@types/node": "20.0.0",
    "@types/react": "18.2.0",
    "@types/react-dom": "18.2.0",
    "typescript": "5.0.0",
    "tailwindcss": "3.3.0",
    "autoprefixer": "10.4.0",
    "postcss": "8.4.0",
    "lucide-react": "0.292.0",
    "clsx": "2.0.0",
    "tailwind-merge": "2.0.0",
    "react-hook-form": "7.47.0",
    "@hookform/resolvers": "3.3.0",
    "zod": "3.22.0",
    "axios": "1.6.0",
    "js-cookie": "3.0.5",
    "@types/js-cookie": "3.0.6",
    "react-query": "3.39.0",
    "swr": "2.2.0",
    "framer-motion": "10.16.0"
  },
  "devDependencies": {
    "eslint": "8.0.0",
    "eslint-config-next": "14.0.0",
    "@testing-library/react": "13.4.0",
    "@testing-library/jest-dom": "6.0.0",
    "jest": "29.0.0",
    "jest-environment-jsdom": "29.0.0"
  }
}
```

### 2. Componentes de Simulado

#### src/components/simulado/simulado-form.tsx
```typescript
'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { BancaSelector } from './banca-selector'
import { EditalSelector } from './edital-selector'
import { QuestionConfig } from './question-config'
import { SimuladoPreview } from './simulado-preview'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Alert } from '@/components/ui/alert'
import { Spinner } from '@/components/ui/spinner'

const simuladoSchema = z.object({
  bancaId: z.string().min(1, 'Selecione uma banca'),
  editalId: z.string().min(1, 'Selecione um edital'),
  totalQuestions: z.number().min(1).max(100),
  timeLimit: z.number().min(30).max(300),
  difficulty: z.enum(['easy', 'medium', 'hard']),
  topics: z.array(z.string()).optional(),
  customInstructions: z.string().optional(),
})

type SimuladoFormData = z.infer<typeof simuladoSchema>

export function SimuladoForm() {
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [preview, setPreview] = useState<SimuladoPreview | null>(null)

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<SimuladoFormData>({
    resolver: zodResolver(simuladoSchema),
  })

  const onSubmit = async (data: SimuladoFormData) => {
    setIsGenerating(true)
    setError(null)
    
    try {
      // Gerar preview
      const previewData = await generatePreview(data)
      setPreview(previewData)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setIsGenerating(false)
    }
  }

  const onGenerate = async () => {
    if (!preview) return
    
    setIsGenerating(true)
    setError(null)
    
    try {
      // Gerar simulado
      const simulado = await generateSimulado(preview)
      // Redirecionar para o simulado
      router.push(`/simulado/take/${simulado.id}`)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {error && (
        <Alert variant="destructive">
          {error}
        </Alert>
      )}
      
      <Card className="p-6">
        <h2 className="text-2xl font-bold mb-6">Configurar Simulado</h2>
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <BancaSelector
            {...register('bancaId')}
            error={errors.bancaId?.message}
          />
          
          <EditalSelector
            bancaId={watch('bancaId')}
            {...register('editalId')}
            error={errors.editalId?.message}
          />
          
          <QuestionConfig
            {...register('totalQuestions')}
            {...register('timeLimit')}
            {...register('difficulty')}
            errors={{
              totalQuestions: errors.totalQuestions?.message,
              timeLimit: errors.timeLimit?.message,
              difficulty: errors.difficulty?.message,
            }}
          />
          
          <Button
            type="submit"
            className="w-full"
            disabled={isGenerating}
          >
            {isGenerating ? (
              <>
                <Spinner size="sm" className="mr-2" />
                Gerando Preview...
              </>
            ) : (
              'Gerar Preview'
            )}
          </Button>
        </form>
      </Card>
      
      {preview && (
        <SimuladoPreview
          preview={preview}
          onGenerate={onGenerate}
          isGenerating={isGenerating}
        />
      )}
    </div>
  )
}
```

#### src/components/simulado/banca-selector.tsx
```typescript
'use client'

import { useState, useEffect } from 'react'
import { Select } from '@/components/ui/select'
import { Spinner } from '@/components/ui/spinner'
import { useBancas } from '@/hooks/use-banca'

interface BancaSelectorProps {
  value?: string
  onChange?: (value: string) => void
  error?: string
}

export function BancaSelector({ value, onChange, error }: BancaSelectorProps) {
  const { bancas, isLoading, error: fetchError } = useBancas()

  if (isLoading) {
    return (
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          Banca Organizadora
        </label>
        <div className="flex items-center justify-center p-4">
          <Spinner size="sm" />
        </div>
      </div>
    )
  }

  if (fetchError) {
    return (
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          Banca Organizadora
        </label>
        <div className="text-red-600 text-sm">
          Erro ao carregar bancas: {fetchError}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">
        Banca Organizadora
      </label>
      <Select
        value={value}
        onValueChange={onChange}
        placeholder="Selecione uma banca"
      >
        {bancas?.map((banca) => (
          <Select.Item key={banca.id} value={banca.id}>
            <div className="flex items-center space-x-2">
              {banca.logo && (
                <img
                  src={banca.logo}
                  alt={banca.name}
                  className="w-6 h-6 rounded"
                />
              )}
              <span>{banca.name}</span>
              <span className="text-gray-500">({banca.code})</span>
            </div>
          </Select.Item>
        ))}
      </Select>
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
    </div>
  )
}
```

#### src/components/simulado/edital-selector.tsx
```typescript
'use client'

import { useState, useEffect } from 'react'
import { Select } from '@/components/ui/select'
import { Spinner } from '@/components/ui/spinner'
import { useEditais } from '@/hooks/use-edital'

interface EditalSelectorProps {
  bancaId?: string
  value?: string
  onChange?: (value: string) => void
  error?: string
}

export function EditalSelector({ 
  bancaId, 
  value, 
  onChange, 
  error 
}: EditalSelectorProps) {
  const { editais, isLoading, error: fetchError } = useEditais(bancaId)

  if (!bancaId) {
    return (
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          Edital
        </label>
        <div className="text-gray-500 text-sm">
          Selecione uma banca primeiro
        </div>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          Edital
        </label>
        <div className="flex items-center justify-center p-4">
          <Spinner size="sm" />
        </div>
      </div>
    )
  }

  if (fetchError) {
    return (
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          Edital
        </label>
        <div className="text-red-600 text-sm">
          Erro ao carregar editais: {fetchError}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">
        Edital
      </label>
      <Select
        value={value}
        onValueChange={onChange}
        placeholder="Selecione um edital"
      >
        {editais?.map((edital) => (
          <Select.Item key={edital.id} value={edital.id}>
            <div className="space-y-1">
              <div className="font-medium">{edital.title}</div>
              <div className="text-sm text-gray-500">
                {edital.year} • {edital.examType} • {edital.totalQuestions} questões
              </div>
            </div>
          </Select.Item>
        ))}
      </Select>
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
    </div>
  )
}
```

#### src/components/simulado/question-config.tsx
```typescript
'use client'

import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { Label } from '@/components/ui/label'

interface QuestionConfigProps {
  totalQuestions?: number
  timeLimit?: number
  difficulty?: string
  onTotalQuestionsChange?: (value: number) => void
  onTimeLimitChange?: (value: number) => void
  onDifficultyChange?: (value: string) => void
  errors?: {
    totalQuestions?: string
    timeLimit?: string
    difficulty?: string
  }
}

export function QuestionConfig({
  totalQuestions,
  timeLimit,
  difficulty,
  onTotalQuestionsChange,
  onTimeLimitChange,
  onDifficultyChange,
  errors,
}: QuestionConfigProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="space-y-2">
        <Label htmlFor="totalQuestions">Número de Questões</Label>
        <Input
          id="totalQuestions"
          type="number"
          min="1"
          max="100"
          value={totalQuestions}
          onChange={(e) => onTotalQuestionsChange?.(Number(e.target.value))}
          placeholder="50"
        />
        {errors?.totalQuestions && (
          <p className="text-sm text-red-600">{errors.totalQuestions}</p>
        )}
      </div>
      
      <div className="space-y-2">
        <Label htmlFor="timeLimit">Tempo Limite (min)</Label>
        <Input
          id="timeLimit"
          type="number"
          min="30"
          max="300"
          value={timeLimit}
          onChange={(e) => onTimeLimitChange?.(Number(e.target.value))}
          placeholder="120"
        />
        {errors?.timeLimit && (
          <p className="text-sm text-red-600">{errors.timeLimit}</p>
        )}
      </div>
      
      <div className="space-y-2">
        <Label htmlFor="difficulty">Dificuldade</Label>
        <Select
          value={difficulty}
          onValueChange={onDifficultyChange}
          placeholder="Selecione a dificuldade"
        >
          <Select.Item value="easy">Fácil</Select.Item>
          <Select.Item value="medium">Médio</Select.Item>
          <Select.Item value="hard">Difícil</Select.Item>
        </Select>
        {errors?.difficulty && (
          <p className="text-sm text-red-600">{errors.difficulty}</p>
        )}
      </div>
    </div>
  )
}
```

#### src/components/simulado/simulado-preview.tsx
```typescript
'use client'

import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Spinner } from '@/components/ui/spinner'
import { SimuladoPreview as SimuladoPreviewType } from '@/types/simulado'

interface SimuladoPreviewProps {
  preview: SimuladoPreviewType
  onGenerate: () => void
  isGenerating: boolean
}

export function SimuladoPreview({ 
  preview, 
  onGenerate, 
  isGenerating 
}: SimuladoPreviewProps) {
  return (
    <Card className="p-6">
      <h3 className="text-xl font-bold mb-4">Preview do Simulado</h3>
      
      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-medium text-gray-700">Banca</h4>
            <p className="text-lg">{preview.banca.name}</p>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-700">Edital</h4>
            <p className="text-lg">{preview.edital.title}</p>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-700">Questões</h4>
            <p className="text-lg">{preview.totalQuestions}</p>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-700">Tempo Limite</h4>
            <p className="text-lg">{preview.timeLimit} minutos</p>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-700">Dificuldade</h4>
            <Badge variant="secondary">
              {preview.difficulty === 'easy' && 'Fácil'}
              {preview.difficulty === 'medium' && 'Médio'}
              {preview.difficulty === 'hard' && 'Difícil'}
            </Badge>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-700">Tempo Estimado</h4>
            <p className="text-lg">{preview.estimatedTime} minutos</p>
          </div>
        </div>
        
        {preview.topics && preview.topics.length > 0 && (
          <div>
            <h4 className="font-medium text-gray-700 mb-2">Tópicos</h4>
            <div className="flex flex-wrap gap-2">
              {preview.topics.map((topic) => (
                <Badge key={topic} variant="outline">
                  {topic}
                </Badge>
              ))}
            </div>
          </div>
        )}
        
        <div className="pt-4 border-t">
          <Button
            onClick={onGenerate}
            className="w-full"
            disabled={isGenerating}
          >
            {isGenerating ? (
              <>
                <Spinner size="sm" className="mr-2" />
                Gerando Simulado...
              </>
            ) : (
              'Gerar Simulado'
            )}
          </Button>
        </div>
      </div>
    </Card>
  )
}
```

### 3. Hooks de Simulado

#### src/hooks/use-simulado.ts
```typescript
'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Simulado, SimuladoGenerationRequest } from '@/types/simulado'
import { simuladoService } from '@/services/simulado-service'

export function useSimulado() {
  const [simulado, setSimulado] = useState<Simulado | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const generateSimulado = async (request: SimuladoGenerationRequest) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await simuladoService.generateSimulado(request)
      setSimulado(response.simulado)
      return response
    } catch (err: any) {
      setError(err.message)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const getSimulado = async (id: string) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const simulado = await simuladoService.getSimulado(id)
      setSimulado(simulado)
      return simulado
    } catch (err: any) {
      setError(err.message)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const submitSimulado = async (id: string, responses: any[]) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const results = await simuladoService.submitSimulado(id, responses)
      return results
    } catch (err: any) {
      setError(err.message)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  return {
    simulado,
    isLoading,
    error,
    generateSimulado,
    getSimulado,
    submitSimulado,
    clearError: () => setError(null),
  }
}
```

#### src/hooks/use-banca.ts
```typescript
'use client'

import { useState, useEffect } from 'react'
import { Banca } from '@/types/banca'
import { bancaService } from '@/services/banca-service'

export function useBancas() {
  const [bancas, setBancas] = useState<Banca[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchBancas = async () => {
      setIsLoading(true)
      setError(null)
      
      try {
        const response = await bancaService.getBancas()
        setBancas(response.bancas)
      } catch (err: any) {
        setError(err.message)
      } finally {
        setIsLoading(false)
      }
    }

    fetchBancas()
  }, [])

  return {
    bancas,
    isLoading,
    error,
    refetch: () => {
      setIsLoading(true)
      setError(null)
      // Refetch logic
    },
  }
}
```

#### src/hooks/use-edital.ts
```typescript
'use client'

import { useState, useEffect } from 'react'
import { Edital } from '@/types/edital'
import { editalService } from '@/services/edital-service'

export function useEditais(bancaId?: string) {
  const [editais, setEditais] = useState<Edital[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!bancaId) {
      setEditais([])
      return
    }

    const fetchEditais = async () => {
      setIsLoading(true)
      setError(null)
      
      try {
        const response = await editalService.getEditais({ bancaId })
        setEditais(response.editais)
      } catch (err: any) {
        setError(err.message)
      } finally {
        setIsLoading(false)
      }
    }

    fetchEditais()
  }, [bancaId])

  return {
    editais,
    isLoading,
    error,
    refetch: () => {
      setIsLoading(true)
      setError(null)
      // Refetch logic
    },
  }
}
```

### 4. Serviços

#### src/services/simulado-service.ts
```typescript
import { apiClient } from './api-client'
import { 
  Simulado, 
  SimuladoGenerationRequest, 
  SimuladoGenerationResponse,
  SimuladoResults 
} from '@/types/simulado'

export const simuladoService = {
  async generateSimulado(request: SimuladoGenerationRequest): Promise<SimuladoGenerationResponse> {
    const response = await apiClient.post('/simulados/generate', request)
    return response.data
  },

  async getSimulado(id: string): Promise<Simulado> {
    const response = await apiClient.get(`/simulados/${id}`)
    return response.data
  },

  async getSimuladoQuestions(id: string): Promise<any[]> {
    const response = await apiClient.get(`/simulados/${id}/questions`)
    return response.data
  },

  async submitSimulado(id: string, responses: any[]): Promise<SimuladoResults> {
    const response = await apiClient.post(`/simulados/${id}/submit`, { responses })
    return response.data
  },

  async getSimuladoResults(id: string): Promise<SimuladoResults> {
    const response = await apiClient.get(`/simulados/${id}/results`)
    return response.data
  },
}
```

#### src/services/banca-service.ts
```typescript
import { apiClient } from './api-client'
import { Banca, BancaListResponse } from '@/types/banca'

export const bancaService = {
  async getBancas(params?: any): Promise<BancaListResponse> {
    const response = await apiClient.get('/bancas', { params })
    return response.data
  },

  async getBanca(id: string): Promise<Banca> {
    const response = await apiClient.get(`/bancas/${id}`)
    return response.data
  },
}
```

#### src/services/edital-service.ts
```typescript
import { apiClient } from './api-client'
import { Edital, EditalListResponse, EditalFilter } from '@/types/edital'

export const editalService = {
  async getEditais(filter?: EditalFilter): Promise<EditalListResponse> {
    const response = await apiClient.get('/editais', { params: filter })
    return response.data
  },

  async getEdital(id: string): Promise<Edital> {
    const response = await apiClient.get(`/editais/${id}`)
    return response.data
  },
}
```

### 5. Tipos TypeScript

#### src/types/simulado.ts
```typescript
export interface Simulado {
  id: string
  title: string
  description: string
  banca: Banca
  edital: Edital
  totalQuestions: number
  timeLimit: number
  difficulty: 'easy' | 'medium' | 'hard'
  topics: string[]
  status: 'draft' | 'generating' | 'ready' | 'in_progress' | 'completed' | 'expired'
  createdAt: string
  userId: string
}

export interface SimuladoGenerationRequest {
  bancaId: string
  editalId: string
  totalQuestions: number
  timeLimit: number
  difficulty: 'easy' | 'medium' | 'hard'
  topics?: string[]
  customInstructions?: string
}

export interface SimuladoGenerationResponse {
  simulado: Simulado
  questions: Question[]
  estimatedTime: number
  generationId: string
}

export interface SimuladoPreview {
  banca: Banca
  edital: Edital
  totalQuestions: number
  timeLimit: number
  difficulty: 'easy' | 'medium' | 'hard'
  topics: string[]
  estimatedTime: number
  availableQuestions: number
}
```

### 6. Páginas

#### src/pages/simulado/generate/index.tsx
```typescript
import { SimuladoForm } from '@/components/simulado/simulado-form'
import { AuthGuard } from '@/components/auth/auth-guard'

export default function GenerateSimuladoPage() {
  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        <div className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="py-6">
              <h1 className="text-2xl font-bold text-gray-900">
                Gerar Simulado
              </h1>
              <p className="text-gray-600">
                Configure e gere seu simulado personalizado
              </p>
            </div>
          </div>
        </div>
        
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <SimuladoForm />
        </div>
      </div>
    </AuthGuard>
  )
}
```

### 7. Variáveis de Ambiente

#### .env.example
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8002
NEXT_PUBLIC_APP_NAME=Concurso AI

# Simulado Configuration
NEXT_PUBLIC_MAX_QUESTIONS=100
NEXT_PUBLIC_MIN_QUESTIONS=1
NEXT_PUBLIC_MAX_TIME_LIMIT=300
NEXT_PUBLIC_MIN_TIME_LIMIT=30

# Development
NODE_ENV=development
```

### 8. README de Rotas

#### ROUTES.md
```markdown
# Rotas da Aplicação - Geração de Simulado

## Páginas Públicas
- `/simulado/generate` - Página de geração de simulado

## Páginas Protegidas (requer autenticação)
- `/simulado/take/[id]` - Realizar simulado
- `/simulado/results/[id]` - Ver resultados

## Componentes de Simulado
- `SimuladoForm` - Formulário de configuração
- `BancaSelector` - Seletor de banca
- `EditalSelector` - Seletor de edital
- `QuestionConfig` - Configuração de questões
- `SimuladoPreview` - Preview do simulado
- `GenerationProgress` - Progresso da geração

## Hooks de Simulado
- `useSimulado` - Hook principal de simulado
- `useBancas` - Hook para bancas
- `useEditais` - Hook para editais
- `useQuestions` - Hook para questões

## Serviços
- `simuladoService` - Serviço de simulados
- `bancaService` - Serviço de bancas
- `editalService` - Serviço de editais
- `questionService` - Serviço de questões

## Variáveis de Ambiente
- `NEXT_PUBLIC_API_URL` - URL base da API
- `NEXT_PUBLIC_APP_NAME` - Nome da aplicação
- `NEXT_PUBLIC_MAX_QUESTIONS` - Máximo de questões
- `NEXT_PUBLIC_MIN_QUESTIONS` - Mínimo de questões
- `NEXT_PUBLIC_MAX_TIME_LIMIT` - Tempo limite máximo
- `NEXT_PUBLIC_MIN_TIME_LIMIT` - Tempo limite mínimo

## Fluxo de Geração
1. Usuário acessa página de geração
2. Seleciona banca e edital
3. Configura questões e tempo
4. Visualiza preview
5. Confirma geração
6. Simulado é gerado
7. Redirecionamento para realização
```

---

**Este documento define o scaffolding completo do frontend WEB-003, incluindo componentes de simulado, hooks, serviços, tipos e páginas.**
