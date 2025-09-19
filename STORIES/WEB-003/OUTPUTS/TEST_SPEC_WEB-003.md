# TEST_SPEC_WEB-003: Especificações de Teste - Tela de Geração de Simulado

## 1. Casos Felizes e de Erro

### **Simulado Form Tests**

#### Casos Felizes
- **Geração de simulado bem-sucedida**
  - Input: Banca válida + edital válido + configurações válidas
  - Expected: Preview gerado, simulado criado, redirect para realização
  - Assertions: Preview exibido, simulado criado, redirecionamento correto

- **Seleção de banca e edital**
  - Input: Banca selecionada + edital selecionado
  - Expected: Editais filtrados por banca, configurações habilitadas
  - Assertions: Editais corretos, formulário habilitado

- **Configuração de questões**
  - Input: Número de questões + tempo limite + dificuldade
  - Expected: Validação passa, preview atualizado
  - Assertions: Validação OK, preview correto

- **Preview do simulado**
  - Input: Configurações válidas
  - Expected: Preview exibido com todas as informações
  - Assertions: Preview completo, informações corretas

#### Casos de Erro
- **Banca não selecionada**
  - Input: Formulário sem banca
  - Expected: Erro de validação
  - Assertions: Erro exibido, submit desabilitado

- **Edital não selecionado**
  - Input: Banca selecionada mas sem edital
  - Expected: Erro de validação
  - Assertions: Erro exibido, submit desabilitado

- **Configurações inválidas**
  - Input: Número de questões inválido
  - Expected: Erro de validação
  - Assertions: Erro específico, submit desabilitado

- **Falha na geração**
  - Input: Configurações válidas mas API falha
  - Expected: Erro de geração
  - Assertions: Erro exibido, retry disponível

### **Banca Selector Tests**

#### Casos Felizes
- **Carregamento de bancas**
  - Input: Página carregada
  - Expected: Lista de bancas carregada
  - Assertions: Bancas exibidas, loading removido

- **Seleção de banca**
  - Input: Banca selecionada
  - Expected: Banca selecionada, editais carregados
  - Assertions: Banca selecionada, editais carregando

- **Filtro de bancas**
  - Input: Busca por nome de banca
  - Expected: Bancas filtradas
  - Assertions: Resultados corretos, busca funcional

#### Casos de Erro
- **Falha no carregamento**
  - Input: API de bancas falha
  - Expected: Erro de carregamento
  - Assertions: Erro exibido, retry disponível

- **Bancas vazias**
  - Input: Nenhuma banca disponível
  - Expected: Mensagem de banca vazia
  - Assertions: Mensagem exibida, estado correto

### **Edital Selector Tests**

#### Casos Felizes
- **Carregamento de editais**
  - Input: Banca selecionada
  - Expected: Editais da banca carregados
  - Assertions: Editais exibidos, loading removido

- **Seleção de edital**
  - Input: Edital selecionado
  - Expected: Edital selecionado, configurações habilitadas
  - Assertions: Edital selecionado, formulário habilitado

- **Filtro de editais**
  - Input: Filtros aplicados
  - Expected: Editais filtrados
  - Assertions: Resultados corretos, filtros funcionais

#### Casos de Erro
- **Falha no carregamento**
  - Input: API de editais falha
  - Expected: Erro de carregamento
  - Assertions: Erro exibido, retry disponível

- **Editais vazios**
  - Input: Nenhum edital disponível
  - Expected: Mensagem de edital vazio
  - Assertions: Mensagem exibida, estado correto

### **Question Config Tests**

#### Casos Felizes
- **Configuração válida**
  - Input: Número de questões + tempo + dificuldade válidos
  - Expected: Validação passa
  - Assertions: Sem erros, configuração válida

- **Validação em tempo real**
  - Input: Campos alterados
  - Expected: Validação atualizada
  - Assertions: Validação em tempo real, feedback imediato

#### Casos de Erro
- **Número de questões inválido**
  - Input: Número fora do range
  - Expected: Erro de validação
  - Assertions: Erro específico, submit desabilitado

- **Tempo limite inválido**
  - Input: Tempo fora do range
  - Expected: Erro de validação
  - Assertions: Erro específico, submit desabilitado

### **Simulado Preview Tests**

#### Casos Felizes
- **Preview exibido**
  - Input: Configurações válidas
  - Expected: Preview com todas as informações
  - Assertions: Preview completo, informações corretas

- **Confirmação de geração**
  - Input: Botão de gerar clicado
  - Expected: Geração iniciada
  - Assertions: Geração iniciada, loading exibido

#### Casos de Erro
- **Preview inválido**
  - Input: Configurações inválidas
  - Expected: Preview não exibido
  - Assertions: Preview oculto, erro exibido

### **Generation Progress Tests**

#### Casos Felizes
- **Progresso exibido**
  - Input: Geração em andamento
  - Expected: Progresso visual
  - Assertions: Progress bar, status atualizado

- **Geração concluída**
  - Input: Geração finalizada
  - Expected: Simulado pronto
  - Assertions: Simulado criado, redirect executado

#### Casos de Erro
- **Falha na geração**
  - Input: Geração falha
  - Expected: Erro exibido
  - Assertions: Erro exibido, retry disponível

- **Timeout na geração**
  - Input: Geração demora muito
  - Expected: Timeout exibido
  - Assertions: Timeout exibido, retry disponível

## 2. Estratégias de Mocks

### **Simulado Service Mocks**

#### Generate Simulado Mock
```javascript
// __mocks__/services/simulado-service.js
export const mockGenerateSimulado = jest.fn().mockResolvedValue({
  simulado: {
    id: 'sim_123456',
    title: 'Simulado CESPE 2024',
    description: 'Simulado baseado no edital CESPE 2024',
    banca: {
      id: 'banca_123',
      name: 'CESPE',
      code: 'CESPE'
    },
    edital: {
      id: 'edital_456',
      title: 'Concurso X 2024',
      year: 2024
    },
    totalQuestions: 50,
    timeLimit: 120,
    difficulty: 'medium',
    topics: ['matemática', 'português'],
    status: 'ready',
    createdAt: '2024-01-15T10:30:00Z'
  },
  questions: [
    {
      id: 'q1',
      question: 'Qual é a capital do Brasil?',
      alternatives: {
        A: 'São Paulo',
        B: 'Rio de Janeiro',
        C: 'Brasília',
        D: 'Belo Horizonte',
        E: 'Salvador'
      },
      correctAnswer: 'C',
      difficulty: 'easy',
      topic: 'conhecimentos gerais',
      order: 1
    }
  ],
  estimatedTime: 120,
  generationId: 'gen_123456'
})

export const mockGenerateSimuladoError = jest.fn().mockRejectedValue({
  message: 'Erro na geração do simulado',
  code: 'GENERATION_ERROR'
})
```

#### Get Simulado Mock
```javascript
export const mockGetSimulado = jest.fn().mockResolvedValue({
  id: 'sim_123456',
  title: 'Simulado CESPE 2024',
  description: 'Simulado baseado no edital CESPE 2024',
  banca: {
    id: 'banca_123',
    name: 'CESPE',
    code: 'CESPE'
  },
  edital: {
    id: 'edital_456',
    title: 'Concurso X 2024',
    year: 2024
  },
  totalQuestions: 50,
  timeLimit: 120,
  difficulty: 'medium',
  topics: ['matemática', 'português'],
  status: 'ready',
  createdAt: '2024-01-15T10:30:00Z'
})

export const mockGetSimuladoError = jest.fn().mockRejectedValue({
  message: 'Simulado não encontrado',
  code: 'SIMULADO_NOT_FOUND'
})
```

### **Banca Service Mocks**

```javascript
// __mocks__/services/banca-service.js
export const mockGetBancas = jest.fn().mockResolvedValue({
  bancas: [
    {
      id: 'banca_123',
      name: 'CESPE',
      code: 'CESPE',
      description: 'Centro de Seleção e de Promoção de Eventos',
      logo: 'https://example.com/cespe-logo.png',
      website: 'https://www.cespe.unb.br',
      isActive: true,
      characteristics: {
        questionStyle: 'multiple_choice',
        answerFormat: 'A-E',
        timePerQuestion: 2,
        difficultyDistribution: {
          easy: 20,
          medium: 60,
          hard: 20
        },
        commonTopics: ['português', 'matemática', 'conhecimentos gerais']
      },
      createdAt: '2024-01-15T10:30:00Z'
    }
  ],
  total: 1,
  page: 1,
  limit: 10
})

export const mockGetBancasError = jest.fn().mockRejectedValue({
  message: 'Erro ao carregar bancas',
  code: 'BANCAS_LOAD_ERROR'
})
```

### **Edital Service Mocks**

```javascript
// __mocks__/services/edital-service.js
export const mockGetEditais = jest.fn().mockResolvedValue({
  editais: [
    {
      id: 'edital_456',
      title: 'Concurso X 2024',
      description: 'Concurso público para cargo X',
      bancaId: 'banca_123',
      year: 2024,
      month: 6,
      examType: 'concurso',
      subjects: ['português', 'matemática', 'conhecimentos gerais'],
      totalQuestions: 100,
      timeLimit: 240,
      isActive: true,
      publishedAt: '2024-01-15T10:30:00Z',
      examDate: '2024-06-15T09:00:00Z',
      createdAt: '2024-01-15T10:30:00Z'
    }
  ],
  total: 1,
  page: 1,
  limit: 10
})

export const mockGetEditaisError = jest.fn().mockRejectedValue({
  message: 'Erro ao carregar editais',
  code: 'EDITAIS_LOAD_ERROR'
})
```

### **Generation Service Mocks**

```javascript
// __mocks__/services/generation-service.js
export const mockGetGenerationStatus = jest.fn().mockResolvedValue({
  id: 'gen_123456',
  status: 'processing',
  progress: 65,
  currentStep: 'Gerando questões de matemática',
  estimatedTimeRemaining: 45,
  error: null,
  createdAt: '2024-01-15T10:30:00Z',
  updatedAt: '2024-01-15T10:32:00Z'
})

export const mockGetGenerationStatusError = jest.fn().mockRejectedValue({
  message: 'Erro ao obter status da geração',
  code: 'GENERATION_STATUS_ERROR'
})
```

### **Router Mocks**

```javascript
// __mocks__/next/navigation.js
export const mockRouter = {
  push: jest.fn(),
  replace: jest.fn(),
  back: jest.fn(),
  forward: jest.fn(),
  refresh: jest.fn(),
  pathname: '/simulado/generate',
  query: {},
  asPath: '/simulado/generate',
}

export const useRouter = () => mockRouter
export const usePathname = () => mockRouter.pathname
export const useSearchParams = () => new URLSearchParams()
```

## 3. Timeouts e Re-tentativas

### **API Timeouts**
- **Geração de simulado**: 30 segundos
- **Carregamento de bancas**: 10 segundos
- **Carregamento de editais**: 10 segundos
- **Status da geração**: 5 segundos
- **Retry strategy**: 3 tentativas com backoff exponencial

### **Component Timeouts**
- **Loading states**: 10 segundos máximo
- **Form validation**: 500ms debounce
- **Generation progress**: Polling a cada 2 segundos
- **Auto-refresh**: 30 segundos para dados estáticos

### **Navigation Timeouts**
- **Redirect após geração**: 2 segundos
- **Redirect para simulado**: 1 segundo
- **Fallback routes**: Imediato

## 4. Critérios de Cobertura por Arquivo

### **src/components/simulado/simulado-form.tsx**
- **Cobertura mínima**: 95%
- **Casos críticos**: Validação, submit, error handling, loading states
- **Testes**: Form validation, submit flow, error display, loading states

### **src/components/simulado/banca-selector.tsx**
- **Cobertura mínima**: 90%
- **Casos críticos**: Carregamento, seleção, error handling
- **Testes**: Loading states, selection, error handling

### **src/components/simulado/edital-selector.tsx**
- **Cobertura mínima**: 90%
- **Casos críticos**: Filtro por banca, seleção, error handling
- **Testes**: Filtering, selection, error handling

### **src/components/simulado/question-config.tsx**
- **Cobertura mínima**: 95%
- **Casos críticos**: Validação, configuração, error display
- **Testes**: Validation, configuration, error display

### **src/components/simulado/simulado-preview.tsx**
- **Cobertura mínima**: 90%
- **Casos críticos**: Preview display, confirmação, error handling
- **Testes**: Preview display, confirmation, error handling

### **src/hooks/use-simulado.ts**
- **Cobertura mínima**: 95%
- **Casos críticos**: Geração, carregamento, error handling
- **Testes**: Generation, loading, error handling

### **src/hooks/use-banca.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Carregamento, cache, error handling
- **Testes**: Loading, caching, error handling

### **src/hooks/use-edital.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Filtro por banca, carregamento, error handling
- **Testes**: Filtering, loading, error handling

### **src/services/simulado-service.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Todas as operações, error handling
- **Testes**: All operations, error handling

### **src/services/banca-service.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Carregamento, cache, error handling
- **Testes**: Loading, caching, error handling

### **src/services/edital-service.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Filtros, carregamento, error handling
- **Testes**: Filtering, loading, error handling

## 5. Plano de Testes Exploratórios

### **Sessão 1: Fluxo de Geração (2h)**
- **Objetivo**: Verificar fluxo completo de geração
- **Cenários**:
  - Seleção de banca e edital
  - Configuração de questões
  - Preview do simulado
  - Geração e redirecionamento

### **Sessão 2: Validação de Formulários (1h)**
- **Objetivo**: Verificar validação de formulários
- **Cenários**:
  - Campos obrigatórios
  - Validação de range
  - Validação em tempo real
  - Mensagens de erro

### **Sessão 3: Estados de Loading (1h)**
- **Objetivo**: Verificar estados de loading
- **Cenários**:
  - Carregamento de bancas
  - Carregamento de editais
  - Geração de simulado
  - Progress tracking

### **Sessão 4: Error Handling (1h)**
- **Objetivo**: Verificar tratamento de erros
- **Cenários**:
  - Falhas de API
  - Timeouts
  - Erros de validação
  - Estados de fallback

### **Sessão 5: Responsividade (1h)**
- **Objetivo**: Verificar responsividade
- **Cenários**:
  - Mobile layout
  - Tablet layout
  - Desktop layout
  - Breakpoints

### **Sessão 6: Performance (1h)**
- **Objetivo**: Verificar performance
- **Cenários**:
  - Carregamento inicial
  - Filtros e busca
  - Geração de simulado
  - Navegação

## 6. Testes de Integração

### **Fluxo Completo de Geração**
- **Setup**: Usuário autenticado
- **Steps**: Seleção → Configuração → Preview → Geração → Redirect
- **Assertions**: Fluxo completo, simulado criado, redirecionamento correto

### **Filtro de Editais por Banca**
- **Setup**: Bancas e editais carregados
- **Steps**: Seleção de banca → Filtro de editais
- **Assertions**: Editais filtrados corretamente

### **Validação de Configurações**
- **Setup**: Formulário preenchido
- **Steps**: Alteração de campos → Validação
- **Assertions**: Validação em tempo real, erros exibidos

### **Geração com Progress Tracking**
- **Setup**: Configurações válidas
- **Steps**: Geração → Progress tracking → Conclusão
- **Assertions**: Progress atualizado, simulado criado

## 7. Testes de Performance

### **Métricas de Carregamento**
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3.5s
- **Cumulative Layout Shift**: < 0.1

### **Testes de Carga**
- **Usuários simultâneos**: 50
- **Gerações por minuto**: 100
- **Tempo de resposta**: < 3s
- **Taxa de erro**: < 2%

## 8. Testes de Segurança

### **Validação de Inputs**
- **Sanitização**: Inputs sanitizados
- **Validação**: Validação rigorosa
- **XSS**: Proteção contra XSS
- **CSRF**: Tokens CSRF

### **Autorização**
- **Autenticação**: Usuário autenticado
- **Autorização**: Permissões adequadas
- **Rate limiting**: Limitação de requisições
- **Session management**: Gerenciamento de sessão

---

**Este documento define especificações completas de teste para a tela de geração de simulado WEB-003, incluindo casos felizes, erros, mocks, timeouts, cobertura e plano de testes exploratórios.**
