# FE_SCAFFOLD_UX-001: Frontend Scaffolding - Sistema de Feedback do Usuário

## Estrutura de Arquivos Criados

### 1. Configuração Base

#### package.json
```json
{
  "name": "concurso-ai-feedback",
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
    "react-hook-form": "7.48.0",
    "@hookform/resolvers": "3.3.0",
    "zod": "3.22.0",
    "axios": "1.6.0",
    "js-cookie": "3.0.5",
    "@types/js-cookie": "3.0.6",
    "react-query": "3.39.0",
    "swr": "2.2.0",
    "framer-motion": "10.16.0",
    "react-hot-toast": "2.4.0",
    "uuid": "9.0.1",
    "@types/uuid": "9.0.7"
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

### 2. Componentes de Feedback

#### src/components/feedback/feedback-button.tsx
```typescript
'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { FeedbackModal } from './feedback-modal'
import { AlertTriangle, MessageSquare } from 'lucide-react'

interface FeedbackButtonProps {
  questionId: string
  questionText: string
  questionOptions: string[]
  selectedAnswer?: string
  correctAnswer?: string
  timeSpent: number
  difficulty: 'easy' | 'medium' | 'hard'
  topic: string
  banca: string
  edital: string
  simuladoId: string
  className?: string
}

export function FeedbackButton({
  questionId,
  questionText,
  questionOptions,
  selectedAnswer,
  correctAnswer,
  timeSpent,
  difficulty,
  topic,
  banca,
  edital,
  simuladoId,
  className
}: FeedbackButtonProps) {
  const [isModalOpen, setIsModalOpen] = useState(false)

  const handleOpenModal = () => {
    setIsModalOpen(true)
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
  }

  return (
    <>
      <Button
        variant="outline"
        size="sm"
        onClick={handleOpenModal}
        className={`flex items-center gap-2 ${className}`}
      >
        <AlertTriangle size={16} />
        <span className="hidden sm:inline">Reportar Problema</span>
        <span className="sm:hidden">Reportar</span>
      </Button>

      <FeedbackModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        questionId={questionId}
        questionText={questionText}
        questionOptions={questionOptions}
        selectedAnswer={selectedAnswer}
        correctAnswer={correctAnswer}
        timeSpent={timeSpent}
        difficulty={difficulty}
        topic={topic}
        banca={banca}
        edital={edital}
        simuladoId={simuladoId}
      />
    </>
  )
}
```

#### src/components/feedback/feedback-modal.tsx
```typescript
'use client'

import { useEffect } from 'react'
import { Modal } from '@/components/ui/modal'
import { FeedbackForm } from './feedback-form'
import { FeedbackSuccess } from './feedback-success'
import { FeedbackError } from './feedback-error'
import { useFeedback } from '@/hooks/use-feedback'
import { useDraft } from '@/hooks/use-draft'
import { FeedbackRequest } from '@/types/feedback'

interface FeedbackModalProps {
  isOpen: boolean
  onClose: () => void
  questionId: string
  questionText: string
  questionOptions: string[]
  selectedAnswer?: string
  correctAnswer?: string
  timeSpent: number
  difficulty: 'easy' | 'medium' | 'hard'
  topic: string
  banca: string
  edital: string
  simuladoId: string
}

export function FeedbackModal({
  isOpen,
  onClose,
  questionId,
  questionText,
  questionOptions,
  selectedAnswer,
  correctAnswer,
  timeSpent,
  difficulty,
  topic,
  banca,
  edital,
  simuladoId
}: FeedbackModalProps) {
  const { 
    submitFeedback, 
    isSubmitting, 
    isSuccess, 
    isError, 
    error,
    resetState 
  } = useFeedback()
  
  const { 
    loadDraft, 
    saveDraft, 
    clearDraft, 
    draft 
  } = useDraft(questionId)

  useEffect(() => {
    if (isOpen) {
      loadDraft()
    }
  }, [isOpen, loadDraft])

  useEffect(() => {
    if (isSuccess) {
      clearDraft()
      // Auto-close modal after 2 seconds
      setTimeout(() => {
        onClose()
        resetState()
      }, 2000)
    }
  }, [isSuccess, clearDraft, onClose, resetState])

  const handleSubmit = async (data: Partial<FeedbackRequest>) => {
    const feedbackData: FeedbackRequest = {
      questionId,
      userId: 'current-user-id', // TODO: Get from auth context
      category: data.category!,
      comment: data.comment!,
      metadata: {
        questionText,
        questionOptions,
        selectedAnswer,
        correctAnswer,
        timeSpent,
        difficulty,
        topic,
        banca,
        edital,
        simuladoId,
        browserInfo: {
          name: navigator.userAgent.includes('Chrome') ? 'Chrome' : 'Other',
          version: '120.0.0.0',
          os: navigator.platform,
          language: navigator.language,
          timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
        },
        deviceInfo: {
          type: window.innerWidth < 768 ? 'mobile' : window.innerWidth < 1024 ? 'tablet' : 'desktop',
          screen: {
            width: window.innerWidth,
            height: window.innerHeight
          },
          userAgent: navigator.userAgent
        }
      },
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      sessionId: 'current-session-id' // TODO: Get from session context
    }

    await submitFeedback(feedbackData)
  }

  const handleSaveDraft = (data: Partial<FeedbackRequest>) => {
    saveDraft(data)
  }

  const handleClose = () => {
    resetState()
    onClose()
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="Reportar Problema na Questão"
      size="md"
    >
      <div className="space-y-4">
        {isError && (
          <FeedbackError 
            error={error} 
            onRetry={() => resetState()} 
          />
        )}
        
        {isSuccess ? (
          <FeedbackSuccess />
        ) : (
          <FeedbackForm
            initialData={draft}
            onSubmit={handleSubmit}
            onSaveDraft={handleSaveDraft}
            isSubmitting={isSubmitting}
            questionText={questionText}
            questionOptions={questionOptions}
          />
        )}
      </div>
    </Modal>
  )
}
```

#### src/components/feedback/feedback-form.tsx
```typescript
'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { FeedbackCategorySelector } from './feedback-category-selector'
import { useDraft } from '@/hooks/use-draft'
import { FeedbackRequest, FeedbackCategory } from '@/types/feedback'
import { Save, Send, AlertCircle } from 'lucide-react'

const feedbackSchema = z.object({
  category: z.object({
    id: z.string(),
    name: z.string(),
    description: z.string(),
    priority: z.enum(['low', 'medium', 'high']),
    icon: z.string()
  }),
  comment: z.string()
    .min(10, 'Comentário deve ter pelo menos 10 caracteres')
    .max(1000, 'Comentário deve ter no máximo 1000 caracteres')
})

type FeedbackFormData = z.infer<typeof feedbackSchema>

interface FeedbackFormProps {
  initialData?: Partial<FeedbackRequest>
  onSubmit: (data: FeedbackFormData) => Promise<void>
  onSaveDraft: (data: Partial<FeedbackRequest>) => void
  isSubmitting: boolean
  questionText: string
  questionOptions: string[]
}

export function FeedbackForm({
  initialData,
  onSubmit,
  onSaveDraft,
  isSubmitting,
  questionText,
  questionOptions
}: FeedbackFormProps) {
  const { saveDraft } = useDraft()
  const [isDraftSaved, setIsDraftSaved] = useState(false)

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors, isValid, isDirty }
  } = useForm<FeedbackFormData>({
    resolver: zodResolver(feedbackSchema),
    defaultValues: {
      category: initialData?.category,
      comment: initialData?.comment || ''
    }
  })

  const watchedValues = watch()

  // Auto-save draft every 30 seconds
  useEffect(() => {
    if (isDirty && watchedValues.comment.length > 0) {
      const timer = setTimeout(() => {
        onSaveDraft(watchedValues)
        setIsDraftSaved(true)
        setTimeout(() => setIsDraftSaved(false), 2000)
      }, 30000)

      return () => clearTimeout(timer)
    }
  }, [watchedValues, isDirty, onSaveDraft])

  const handleFormSubmit = async (data: FeedbackFormData) => {
    await onSubmit(data)
  }

  const handleSaveDraft = () => {
    onSaveDraft(watchedValues)
    setIsDraftSaved(true)
    setTimeout(() => setIsDraftSaved(false), 2000)
  }

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      <div className="space-y-4">
        <div>
          <h3 className="text-sm font-medium text-gray-900 mb-2">
            Questão
          </h3>
          <div className="p-3 bg-gray-50 rounded-md text-sm text-gray-700">
            {questionText}
          </div>
        </div>

        <div>
          <h3 className="text-sm font-medium text-gray-900 mb-2">
            Alternativas
          </h3>
          <div className="space-y-1">
            {questionOptions.map((option, index) => (
              <div key={index} className="text-sm text-gray-600">
                {option}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div>
        <FeedbackCategorySelector
          onCategorySelect={(category) => setValue('category', category)}
          selectedCategory={watchedValues.category}
          error={errors.category?.message}
        />
      </div>

      <div>
        <label htmlFor="comment" className="block text-sm font-medium text-gray-900 mb-2">
          Comentário *
        </label>
        <Textarea
          id="comment"
          {...register('comment')}
          placeholder="Descreva o problema encontrado na questão..."
          rows={4}
          className={errors.comment ? 'border-red-300' : ''}
        />
        {errors.comment && (
          <p className="mt-1 text-sm text-red-600 flex items-center gap-1">
            <AlertCircle size={14} />
            {errors.comment.message}
          </p>
        )}
        <p className="mt-1 text-xs text-gray-500">
          {watchedValues.comment?.length || 0}/1000 caracteres
        </p>
      </div>

      <div className="flex items-center justify-between pt-4 border-t">
        <div className="flex items-center gap-2">
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={handleSaveDraft}
            disabled={!isDirty || isSubmitting}
          >
            <Save size={16} />
            Salvar Rascunho
          </Button>
          {isDraftSaved && (
            <span className="text-xs text-green-600">Rascunho salvo!</span>
          )}
        </div>

        <div className="flex items-center gap-2">
          <Button
            type="button"
            variant="outline"
            onClick={() => window.history.back()}
            disabled={isSubmitting}
          >
            Cancelar
          </Button>
          <Button
            type="submit"
            disabled={!isValid || isSubmitting}
            className="flex items-center gap-2"
          >
            {isSubmitting ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Enviando...
              </>
            ) : (
              <>
                <Send size={16} />
                Enviar Feedback
              </>
            )}
          </Button>
        </div>
      </div>
    </form>
  )
}
```

#### src/components/feedback/feedback-category-selector.tsx
```typescript
'use client'

import { useState } from 'react'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { FeedbackCategory } from '@/types/feedback'
import { 
  AlertTriangle, 
  HelpCircle, 
  XCircle, 
  MessageSquare,
  FileText,
  Bug
} from 'lucide-react'

const FEEDBACK_CATEGORIES: FeedbackCategory[] = [
  {
    id: 'error_in_question',
    name: 'Erro na Questão',
    description: 'A questão contém um erro factual ou técnico',
    priority: 'high',
    icon: 'alert-triangle'
  },
  {
    id: 'ambiguous_question',
    name: 'Questão Ambígua',
    description: 'A questão pode ter mais de uma interpretação',
    priority: 'medium',
    icon: 'help-circle'
  },
  {
    id: 'incorrect_alternative',
    name: 'Alternativa Incorreta',
    description: 'Uma das alternativas está incorreta',
    priority: 'high',
    icon: 'x-circle'
  },
  {
    id: 'poor_question_quality',
    name: 'Qualidade da Questão',
    description: 'A questão tem problemas de redação ou clareza',
    priority: 'medium',
    icon: 'file-text'
  },
  {
    id: 'technical_issue',
    name: 'Problema Técnico',
    description: 'Problema técnico com a exibição ou funcionalidade',
    priority: 'low',
    icon: 'bug'
  },
  {
    id: 'other',
    name: 'Outro',
    description: 'Outro tipo de problema não listado',
    priority: 'low',
    icon: 'message-square'
  }
]

const getIcon = (iconName: string) => {
  const icons = {
    'alert-triangle': AlertTriangle,
    'help-circle': HelpCircle,
    'x-circle': XCircle,
    'file-text': FileText,
    'bug': Bug,
    'message-square': MessageSquare
  }
  return icons[iconName as keyof typeof icons] || MessageSquare
}

const getPriorityColor = (priority: string) => {
  switch (priority) {
    case 'high':
      return 'bg-red-100 text-red-800 border-red-200'
    case 'medium':
      return 'bg-yellow-100 text-yellow-800 border-yellow-200'
    case 'low':
      return 'bg-green-100 text-green-800 border-green-200'
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200'
  }
}

interface FeedbackCategorySelectorProps {
  onCategorySelect: (category: FeedbackCategory) => void
  selectedCategory?: FeedbackCategory
  error?: string
}

export function FeedbackCategorySelector({
  onCategorySelect,
  selectedCategory,
  error
}: FeedbackCategorySelectorProps) {
  const [selectedId, setSelectedId] = useState(selectedCategory?.id || '')

  const handleCategoryChange = (categoryId: string) => {
    setSelectedId(categoryId)
    const category = FEEDBACK_CATEGORIES.find(cat => cat.id === categoryId)
    if (category) {
      onCategorySelect(category)
    }
  }

  return (
    <div className="space-y-3">
      <Label className="text-sm font-medium text-gray-900">
        Categoria do Problema *
      </Label>
      
      <RadioGroup
        value={selectedId}
        onValueChange={handleCategoryChange}
        className="space-y-3"
      >
        {FEEDBACK_CATEGORIES.map((category) => {
          const Icon = getIcon(category.icon)
          const isSelected = selectedId === category.id
          
          return (
            <div
              key={category.id}
              className={`flex items-start space-x-3 p-3 rounded-lg border-2 cursor-pointer transition-colors ${
                isSelected
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <RadioGroupItem
                value={category.id}
                id={category.id}
                className="mt-1"
              />
              <div className="flex-1 min-w-0">
                <Label
                  htmlFor={category.id}
                  className="flex items-center gap-2 cursor-pointer"
                >
                  <Icon size={16} className="text-gray-600" />
                  <span className="font-medium text-gray-900">
                    {category.name}
                  </span>
                  <Badge
                    variant="outline"
                    className={`text-xs ${getPriorityColor(category.priority)}`}
                  >
                    {category.priority === 'high' ? 'Alta' :
                     category.priority === 'medium' ? 'Média' : 'Baixa'}
                  </Badge>
                </Label>
                <p className="mt-1 text-sm text-gray-600">
                  {category.description}
                </p>
              </div>
            </div>
          )
        })}
      </RadioGroup>
      
      {error && (
        <p className="text-sm text-red-600 flex items-center gap-1">
          <AlertTriangle size={14} />
          {error}
        </p>
      )}
    </div>
  )
}
```

### 3. Hooks de Feedback

#### src/hooks/use-feedback.ts
```typescript
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { FeedbackRequest, FeedbackResponse } from '@/types/feedback'
import { feedbackService } from '@/services/feedback-service'
import toast from 'react-hot-toast'

export function useFeedback() {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSuccess, setIsSuccess] = useState(false)
  const [isError, setIsError] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const submitFeedback = async (feedback: FeedbackRequest): Promise<void> => {
    setIsSubmitting(true)
    setIsError(false)
    setError(null)
    
    try {
      const response = await feedbackService.submitFeedback(feedback)
      
      if (response.success) {
        setIsSuccess(true)
        toast.success('Feedback enviado com sucesso!')
      } else {
        throw new Error(response.message || 'Erro ao enviar feedback')
      }
    } catch (err: any) {
      setIsError(true)
      setError(err.message)
      toast.error('Erro ao enviar feedback. Tente novamente.')
      throw err
    } finally {
      setIsSubmitting(false)
    }
  }

  const resetState = () => {
    setIsSubmitting(false)
    setIsSuccess(false)
    setIsError(false)
    setError(null)
  }

  return {
    submitFeedback,
    isSubmitting,
    isSuccess,
    isError,
    error,
    resetState
  }
}
```

#### src/hooks/use-draft.ts
```typescript
'use client'

import { useState, useEffect } from 'react'
import { FeedbackRequest } from '@/types/feedback'
import { draftService } from '@/services/draft-service'

export function useDraft(questionId: string) {
  const [draft, setDraft] = useState<Partial<FeedbackRequest> | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadDraft = async () => {
    setIsLoading(true)
    setError(null)
    
    try {
      const draftData = await draftService.getDraft(questionId)
      setDraft(draftData)
    } catch (err: any) {
      setError(err.message)
      console.error('Erro ao carregar rascunho:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const saveDraft = async (data: Partial<FeedbackRequest>) => {
    try {
      await draftService.saveDraft(questionId, data)
      setDraft(data)
    } catch (err: any) {
      console.error('Erro ao salvar rascunho:', err)
    }
  }

  const clearDraft = async () => {
    try {
      await draftService.clearDraft(questionId)
      setDraft(null)
    } catch (err: any) {
      console.error('Erro ao limpar rascunho:', err)
    }
  }

  return {
    draft,
    isLoading,
    error,
    loadDraft,
    saveDraft,
    clearDraft
  }
}
```

### 4. Serviços

#### src/services/feedback-service.ts
```typescript
import { apiClient } from './api-client'
import { FeedbackRequest, FeedbackResponse } from '@/types/feedback'

export const feedbackService = {
  async submitFeedback(feedback: FeedbackRequest): Promise<FeedbackResponse> {
    const response = await apiClient.post('/feedback', feedback)
    return response.data
  },

  async getFeedback(feedbackId: string): Promise<FeedbackResponse> {
    const response = await apiClient.get(`/feedback/${feedbackId}`)
    return response.data
  },

  async getFeedbacks(params?: {
    page?: number
    limit?: number
    status?: string
    category?: string
  }): Promise<{ data: FeedbackResponse[]; pagination: any }> {
    const response = await apiClient.get('/feedback', { params })
    return response.data
  },

  async updateFeedbackStatus(
    feedbackId: string, 
    status: string, 
    adminComment?: string
  ): Promise<FeedbackResponse> {
    const response = await apiClient.put(`/feedback/${feedbackId}/status`, {
      status,
      admin_comment: adminComment
    })
    return response.data
  },

  async getCategories(): Promise<any[]> {
    const response = await apiClient.get('/feedback/categories')
    return response.data
  },

  async getAnalytics(period?: string): Promise<any> {
    const response = await apiClient.get('/feedback/analytics', {
      params: { period }
    })
    return response.data
  }
}
```

#### src/services/draft-service.ts
```typescript
import { FeedbackRequest } from '@/types/feedback'

const DRAFT_KEY_PREFIX = 'feedback_draft_'
const DRAFT_TTL = 7 * 24 * 60 * 60 * 1000 // 7 days

export const draftService = {
  async getDraft(questionId: string): Promise<Partial<FeedbackRequest> | null> {
    try {
      const key = `${DRAFT_KEY_PREFIX}${questionId}`
      const draftData = localStorage.getItem(key)
      
      if (!draftData) return null
      
      const { data, timestamp } = JSON.parse(draftData)
      
      // Check if draft is expired
      if (Date.now() - timestamp > DRAFT_TTL) {
        this.clearDraft(questionId)
        return null
      }
      
      return data
    } catch (error) {
      console.error('Erro ao carregar rascunho:', error)
      return null
    }
  },

  async saveDraft(questionId: string, data: Partial<FeedbackRequest>): Promise<void> {
    try {
      const key = `${DRAFT_KEY_PREFIX}${questionId}`
      const draftData = {
        data,
        timestamp: Date.now()
      }
      
      localStorage.setItem(key, JSON.stringify(draftData))
    } catch (error) {
      console.error('Erro ao salvar rascunho:', error)
      throw error
    }
  },

  async clearDraft(questionId: string): Promise<void> {
    try {
      const key = `${DRAFT_KEY_PREFIX}${questionId}`
      localStorage.removeItem(key)
    } catch (error) {
      console.error('Erro ao limpar rascunho:', error)
      throw error
    }
  },

  async clearAllDrafts(): Promise<void> {
    try {
      const keys = Object.keys(localStorage)
      const draftKeys = keys.filter(key => key.startsWith(DRAFT_KEY_PREFIX))
      
      draftKeys.forEach(key => {
        localStorage.removeItem(key)
      })
    } catch (error) {
      console.error('Erro ao limpar todos os rascunhos:', error)
      throw error
    }
  }
}
```

### 5. Tipos TypeScript

#### src/types/feedback.ts
```typescript
export interface FeedbackRequest {
  questionId: string
  userId: string
  category: FeedbackCategory
  comment: string
  metadata: FeedbackMetadata
  timestamp: string
  userAgent: string
  sessionId: string
}

export interface FeedbackCategory {
  id: string
  name: string
  description: string
  priority: 'low' | 'medium' | 'high'
  icon: string
}

export interface FeedbackMetadata {
  questionText: string
  questionOptions: string[]
  selectedAnswer?: string
  correctAnswer?: string
  timeSpent: number
  difficulty: 'easy' | 'medium' | 'hard'
  topic: string
  banca: string
  edital: string
  simuladoId: string
  browserInfo: BrowserInfo
  deviceInfo: DeviceInfo
}

export interface BrowserInfo {
  name: string
  version: string
  os: string
  language: string
  timezone: string
}

export interface DeviceInfo {
  type: 'desktop' | 'tablet' | 'mobile'
  screen: {
    width: number
    height: number
  }
  userAgent: string
}

export interface FeedbackResponse {
  success: boolean
  feedbackId: string
  message: string
  timestamp: string
  status: 'pending' | 'reviewed' | 'resolved' | 'rejected'
}

export interface FeedbackDraft {
  questionId: string
  category?: FeedbackCategory
  comment: string
  lastSaved: string
  isDirty: boolean
}

export interface FeedbackEvent {
  type: 'feedback_submitted' | 'feedback_draft_saved' | 'feedback_modal_opened' | 'feedback_modal_closed'
  payload: any
  timestamp: string
  sessionId: string
}
```

### 6. Páginas

#### src/pages/feedback/index.tsx
```typescript
import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import { FeedbackButton } from '@/components/feedback/feedback-button'
import { useFeedback } from '@/hooks/use-feedback'
import { AuthGuard } from '@/components/auth/auth-guard'

export default function FeedbackPage() {
  const router = useRouter()
  const { questionId } = router.query
  const [question, setQuestion] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (questionId && typeof questionId === 'string') {
      // TODO: Load question data from API
      setQuestion({
        id: questionId,
        text: 'Qual é o prazo para recurso em processo administrativo?',
        options: [
          'A) 30 dias',
          'B) 60 dias',
          'C) 90 dias',
          'D) 120 dias',
          'E) 180 dias'
        ],
        selectedAnswer: 'A',
        correctAnswer: 'B',
        timeSpent: 45,
        difficulty: 'medium',
        topic: 'direito administrativo',
        banca: 'CESPE',
        edital: 'MPU_2024',
        simuladoId: 'sim_345678'
      })
      setIsLoading(false)
    }
  }, [questionId])

  if (isLoading) {
    return (
      <AuthGuard>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </AuthGuard>
    )
  }

  if (!question) {
    return (
      <AuthGuard>
        <div className="min-h-screen bg-gray-50">
          <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-900">
                Questão não encontrada
              </h1>
            </div>
          </div>
        </div>
      </AuthGuard>
    )
  }

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="bg-white shadow rounded-lg p-6">
            <div className="space-y-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Questão #{question.id}
                </h1>
                <p className="text-gray-600">
                  {question.topic} • {question.banca} • {question.edital}
                </p>
              </div>

              <div className="space-y-4">
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">
                    Enunciado
                  </h2>
                  <p className="text-gray-700 mt-2">
                    {question.text}
                  </p>
                </div>

                <div>
                  <h2 className="text-lg font-semibold text-gray-900">
                    Alternativas
                  </h2>
                  <div className="space-y-2 mt-2">
                    {question.options.map((option: string, index: number) => (
                      <div key={index} className="text-gray-700">
                        {option}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t">
                  <div className="text-sm text-gray-600">
                    <p>Tempo gasto: {question.timeSpent}s</p>
                    <p>Dificuldade: {question.difficulty}</p>
                    <p>Resposta selecionada: {question.selectedAnswer}</p>
                    <p>Resposta correta: {question.correctAnswer}</p>
                  </div>

                  <FeedbackButton
                    questionId={question.id}
                    questionText={question.text}
                    questionOptions={question.options}
                    selectedAnswer={question.selectedAnswer}
                    correctAnswer={question.correctAnswer}
                    timeSpent={question.timeSpent}
                    difficulty={question.difficulty}
                    topic={question.topic}
                    banca={question.banca}
                    edital={question.edital}
                    simuladoId={question.simuladoId}
                  />
                </div>
              </div>
            </div>
          </div>
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
NEXT_PUBLIC_API_URL=http://localhost:8004
NEXT_PUBLIC_APP_NAME=Concurso AI Feedback

# Feedback Configuration
NEXT_PUBLIC_MAX_COMMENT_LENGTH=1000
NEXT_PUBLIC_MIN_COMMENT_LENGTH=10
NEXT_PUBLIC_DRAFT_AUTO_SAVE_INTERVAL=30000
NEXT_PUBLIC_DRAFT_TTL=604800000

# Development
NODE_ENV=development
```

### 8. README de Rotas

#### ROUTES.md
```markdown
# Rotas da Aplicação - Sistema de Feedback

## Páginas Protegidas (requer autenticação)
- `/feedback/[questionId]` - Página de feedback para questão específica
- `/feedback/success` - Página de sucesso após envio

## Componentes de Feedback
- `FeedbackButton` - Botão para abrir modal de feedback
- `FeedbackModal` - Modal principal de feedback
- `FeedbackForm` - Formulário de feedback
- `FeedbackCategorySelector` - Seletor de categoria
- `FeedbackComment` - Campo de comentário
- `FeedbackSubmit` - Botão de envio
- `FeedbackSuccess` - Tela de sucesso
- `FeedbackError` - Tela de erro

## Hooks de Feedback
- `useFeedback` - Hook principal de feedback
- `useDraft` - Hook para rascunhos
- `useModal` - Hook para modal
- `useValidation` - Hook para validação

## Serviços
- `feedbackService` - Serviço de feedback
- `draftService` - Serviço de rascunhos
- `apiClient` - Cliente de API
- `storageService` - Serviço de armazenamento

## Variáveis de Ambiente
- `NEXT_PUBLIC_API_URL` - URL base da API
- `NEXT_PUBLIC_APP_NAME` - Nome da aplicação
- `NEXT_PUBLIC_MAX_COMMENT_LENGTH` - Tamanho máximo do comentário
- `NEXT_PUBLIC_MIN_COMMENT_LENGTH` - Tamanho mínimo do comentário
- `NEXT_PUBLIC_DRAFT_AUTO_SAVE_INTERVAL` - Intervalo de auto-save
- `NEXT_PUBLIC_DRAFT_TTL` - TTL do rascunho

## Fluxo de Feedback
1. Usuário identifica problema na questão
2. Clica em "Reportar Problema"
3. Modal de feedback é aberto
4. Seleciona categoria do problema
5. Escreve comentário detalhado
6. Rascunho é salvo automaticamente
7. Usuário envia feedback
8. Confirmação de recebimento
9. Modal é fechado
10. Feedback é processado pelo sistema

## Categorias de Feedback
- **Erro na Questão** (Alta prioridade) - Erro factual ou técnico
- **Questão Ambígua** (Média prioridade) - Múltiplas interpretações
- **Alternativa Incorreta** (Alta prioridade) - Alternativa com erro
- **Qualidade da Questão** (Média prioridade) - Problemas de redação
- **Problema Técnico** (Baixa prioridade) - Problema de exibição
- **Outro** (Baixa prioridade) - Outros problemas

## Funcionalidades
- **Auto-save** de rascunhos a cada 30 segundos
- **Validação** em tempo real do formulário
- **Categorização** automática por prioridade
- **Metadados** completos da questão
- **Responsividade** para todos os dispositivos
- **Acessibilidade** com ARIA labels
- **Error handling** robusto
- **Loading states** adequados
```

---

**Este documento define o scaffolding completo do frontend UX-001, incluindo componentes de feedback, hooks, serviços, tipos e páginas.**
