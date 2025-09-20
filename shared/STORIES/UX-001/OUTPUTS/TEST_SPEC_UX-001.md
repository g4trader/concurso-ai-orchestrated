# TEST_SPEC_UX-001: Especificações de Teste - Sistema de Feedback do Usuário

## 1. Casos Felizes e de Erro

### **Feedback Button Tests**

#### Casos Felizes
- **Exibição do botão**
  - Input: Questão válida com dados completos
  - Expected: Botão "Reportar Problema" visível
  - Assertions: Botão renderizado, ícone correto, texto adequado

- **Abertura do modal**
  - Input: Clique no botão de feedback
  - Expected: Modal de feedback aberto
  - Assertions: Modal visível, dados da questão carregados

- **Responsividade do botão**
  - Input: Diferentes tamanhos de tela
  - Expected: Botão adaptado ao layout
  - Assertions: Texto completo em desktop, abreviado em mobile

#### Casos de Erro
- **Dados incompletos**
  - Input: Questão sem dados obrigatórios
  - Expected: Botão desabilitado ou erro
  - Assertions: Estado adequado, mensagem de erro

- **Modal não abre**
  - Input: Erro na abertura do modal
  - Expected: Erro tratado
  - Assertions: Erro exibido, fallback adequado

### **Feedback Modal Tests**

#### Casos Felizes
- **Abertura do modal**
  - Input: Clique no botão de feedback
  - Expected: Modal aberto com formulário
  - Assertions: Modal visível, formulário carregado, dados corretos

- **Carregamento de rascunho**
  - Input: Rascunho salvo anteriormente
  - Expected: Rascunho carregado no formulário
  - Assertions: Dados preenchidos, estado correto

- **Fechamento do modal**
  - Input: Clique em fechar ou cancelar
  - Expected: Modal fechado
  - Assertions: Modal oculto, estado limpo

#### Casos de Erro
- **Erro ao carregar rascunho**
  - Input: Rascunho corrompido
  - Expected: Erro tratado
  - Assertions: Erro exibido, formulário vazio

- **Modal não fecha**
  - Input: Erro no fechamento
  - Expected: Erro tratado
  - Assertions: Erro exibido, modal ainda visível

### **Feedback Form Tests**

#### Casos Felizes
- **Preenchimento do formulário**
  - Input: Dados válidos do formulário
  - Expected: Formulário preenchido
  - Assertions: Campos preenchidos, validação OK

- **Seleção de categoria**
  - Input: Clique em categoria
  - Expected: Categoria selecionada
  - Assertions: Categoria marcada, prioridade correta

- **Validação em tempo real**
  - Input: Digitação no campo comentário
  - Expected: Validação em tempo real
  - Assertions: Contador de caracteres, validação visual

- **Auto-save de rascunho**
  - Input: Formulário preenchido
  - Expected: Rascunho salvo automaticamente
  - Assertions: Rascunho salvo, confirmação visual

#### Casos de Erro
- **Validação de campos obrigatórios**
  - Input: Formulário incompleto
  - Expected: Erro de validação
  - Assertions: Erro exibido, campos destacados

- **Comentário muito curto**
  - Input: Comentário com menos de 10 caracteres
  - Expected: Erro de validação
  - Assertions: Erro exibido, botão desabilitado

- **Comentário muito longo**
  - Input: Comentário com mais de 1000 caracteres
  - Expected: Erro de validação
  - Assertions: Erro exibido, botão desabilitado

### **Category Selector Tests**

#### Casos Felizes
- **Exibição de categorias**
  - Input: Modal aberto
  - Expected: Lista de categorias exibida
  - Assertions: Categorias visíveis, ícones corretos

- **Seleção de categoria**
  - Input: Clique em categoria
  - Expected: Categoria selecionada
  - Assertions: Categoria marcada, prioridade exibida

- **Prioridades visuais**
  - Input: Categorias com diferentes prioridades
  - Expected: Cores e badges corretos
  - Assertions: Cores adequadas, badges corretos

#### Casos de Erro
- **Categoria não selecionada**
  - Input: Tentativa de envio sem categoria
  - Expected: Erro de validação
  - Assertions: Erro exibido, formulário não enviado

- **Categoria inválida**
  - Input: Categoria corrompida
  - Expected: Erro tratado
  - Assertions: Erro exibido, fallback adequado

### **Feedback Submission Tests**

#### Casos Felizes
- **Envio bem-sucedido**
  - Input: Formulário válido e completo
  - Expected: Feedback enviado
  - Assertions: Sucesso exibido, modal fechado

- **Confirmação de envio**
  - Input: Feedback enviado
  - Expected: Confirmação visual
  - Assertions: Mensagem de sucesso, toast exibido

- **Limpeza de rascunho**
  - Input: Feedback enviado com sucesso
  - Expected: Rascunho limpo
  - Assertions: Rascunho removido, estado limpo

#### Casos de Erro
- **Falha no envio**
  - Input: Erro na API
  - Expected: Erro tratado
  - Assertions: Erro exibido, retry disponível

- **Timeout no envio**
  - Input: Envio demora muito
  - Expected: Timeout tratado
  - Assertions: Timeout exibido, cancelamento disponível

- **Dados corrompidos**
  - Input: Dados inválidos
  - Expected: Erro de validação
  - Assertions: Erro exibido, dados sanitizados

### **Draft Management Tests**

#### Casos Felizes
- **Salvamento de rascunho**
  - Input: Formulário preenchido
  - Expected: Rascunho salvo
  - Assertions: Rascunho salvo, confirmação visual

- **Recuperação de rascunho**
  - Input: Modal aberto com rascunho
  - Expected: Rascunho carregado
  - Assertions: Dados preenchidos, estado correto

- **Limpeza de rascunho**
  - Input: Feedback enviado
  - Expected: Rascunho limpo
  - Assertions: Rascunho removido, estado limpo

#### Casos de Erro
- **Rascunho corrompido**
  - Input: Rascunho com dados inválidos
  - Expected: Erro tratado
  - Assertions: Erro exibido, formulário vazio

- **Falha no salvamento**
  - Input: Erro no localStorage
  - Expected: Erro tratado
  - Assertions: Erro exibido, fallback adequado

- **Rascunho expirado**
  - Input: Rascunho antigo
  - Expected: Rascunho limpo
  - Assertions: Rascunho removido, formulário vazio

## 2. Estratégias de Mocks

### **Feedback Service Mocks**

#### Submit Feedback Mock
```javascript
// __mocks__/services/feedback-service.js
export const mockSubmitFeedback = jest.fn().mockResolvedValue({
  success: true,
  feedbackId: 'fb_abc123def456',
  message: 'Feedback enviado com sucesso. Obrigado pela sua contribuição!',
  timestamp: '2024-01-15T14:30:05Z',
  status: 'pending'
})

export const mockSubmitFeedbackError = jest.fn().mockRejectedValue({
  message: 'Erro ao enviar feedback',
  code: 'FEEDBACK_SUBMISSION_ERROR'
})
```

#### Get Categories Mock
```javascript
export const mockGetCategories = jest.fn().mockResolvedValue([
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
])
```

### **Draft Service Mocks**

```javascript
// __mocks__/services/draft-service.js
export const mockGetDraft = jest.fn().mockResolvedValue({
  questionId: 'q_123456',
  category: {
    id: 'error_in_question',
    name: 'Erro na Questão',
    description: 'A questão contém um erro factual ou técnico',
    priority: 'high',
    icon: 'alert-triangle'
  },
  comment: 'A alternativa B está incorreta. A resposta correta deveria ser A.',
  lastSaved: '2024-01-15T14:25:00Z',
  isDirty: false
})

export const mockSaveDraft = jest.fn().mockResolvedValue(undefined)

export const mockClearDraft = jest.fn().mockResolvedValue(undefined)

export const mockGetDraftError = jest.fn().mockRejectedValue({
  message: 'Erro ao carregar rascunho',
  code: 'DRAFT_LOAD_ERROR'
})
```

### **Local Storage Mocks**

```javascript
// __mocks__/utils/localStorage.js
export const mockLocalStorage = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
  length: 0,
  key: jest.fn()
}

// Mock localStorage for tests
Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage,
  writable: true
})
```

### **API Client Mocks**

```javascript
// __mocks__/services/api-client.js
export const mockApiClient = {
  post: jest.fn(),
  get: jest.fn(),
  put: jest.fn(),
  delete: jest.fn()
}

export const mockApiResponse = (data, status = 200) => ({
  data,
  status,
  statusText: 'OK',
  headers: {},
  config: {}
})

export const mockApiError = (message, status = 500) => ({
  message,
  status,
  response: {
    data: { error: message },
    status,
    statusText: 'Internal Server Error'
  }
})
```

### **Toast Notifications Mock**

```javascript
// __mocks__/react-hot-toast.js
export const toast = {
  success: jest.fn(),
  error: jest.fn(),
  loading: jest.fn(),
  dismiss: jest.fn(),
  promise: jest.fn()
}

export default toast
```

## 3. Timeouts e Re-tentativas

### **API Timeouts**
- **Envio de feedback**: 10 segundos
- **Carregamento de categorias**: 5 segundos
- **Salvamento de rascunho**: 2 segundos
- **Recuperação de rascunho**: 1 segundo
- **Retry strategy**: 3 tentativas com backoff exponencial

### **Component Timeouts**
- **Modal opening**: 1 segundo máximo
- **Form validation**: 500ms debounce
- **Auto-save**: 30 segundos
- **Toast display**: 5 segundos

### **User Interaction Timeouts**
- **Button click**: 300ms debounce
- **Form submission**: 2 segundos
- **Draft save**: 1 segundo
- **Modal close**: 500ms

## 4. Critérios de Cobertura por Arquivo

### **src/components/feedback/feedback-button.tsx**
- **Cobertura mínima**: 95%
- **Casos críticos**: Renderização, clique, abertura do modal
- **Testes**: Botão renderizado, modal aberto, dados corretos

### **src/components/feedback/feedback-modal.tsx**
- **Cobertura mínima**: 90%
- **Casos críticos**: Abertura, fechamento, carregamento de rascunho
- **Testes**: Modal funcional, rascunho carregado, estados corretos

### **src/components/feedback/feedback-form.tsx**
- **Cobertura mínima**: 95%
- **Casos críticos**: Validação, envio, auto-save
- **Testes**: Validação correta, envio funcional, auto-save

### **src/components/feedback/feedback-category-selector.tsx**
- **Cobertura mínima**: 90%
- **Casos críticos**: Seleção, validação, prioridades
- **Testes**: Seleção funcional, validação correta, prioridades

### **src/hooks/use-feedback.ts**
- **Cobertura mínima**: 95%
- **Casos críticos**: Envio, error handling, estados
- **Testes**: Envio correto, tratamento de erros, estados

### **src/hooks/use-draft.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Salvamento, recuperação, limpeza
- **Testes**: Operações corretas, tratamento de erros

### **src/services/feedback-service.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Todas as operações, error handling
- **Testes**: Operações corretas, tratamento de erros

### **src/services/draft-service.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: LocalStorage, TTL, error handling
- **Testes**: Operações corretas, TTL funcional, tratamento de erros

### **src/utils/validators.ts**
- **Cobertura mínima**: 95%
- **Casos críticos**: Validação de formulário, comentários
- **Testes**: Validação correta, edge cases, sanitização

## 5. Plano de Testes Exploratórios

### **Sessão 1: Fluxo de Feedback (2h)**
- **Objetivo**: Verificar fluxo completo de feedback
- **Cenários**:
  - Abertura do modal
  - Preenchimento do formulário
  - Seleção de categoria
  - Envio do feedback
  - Confirmação de sucesso

### **Sessão 2: Gerenciamento de Rascunhos (1h)**
- **Objetivo**: Verificar funcionalidades de rascunho
- **Cenários**:
  - Salvamento automático
  - Recuperação de rascunho
  - Limpeza de rascunho
  - Expiração de rascunho

### **Sessão 3: Validação e Error Handling (1h)**
- **Objetivo**: Verificar validação e tratamento de erros
- **Cenários**:
  - Validação de campos
  - Tratamento de erros de API
  - Timeouts e retry
  - Estados de erro

### **Sessão 4: Responsividade (1h)**
- **Objetivo**: Verificar responsividade
- **Cenários**:
  - Mobile layout
  - Tablet layout
  - Desktop layout
  - Touch interactions

### **Sessão 5: Performance (1h)**
- **Objetivo**: Verificar performance
- **Cenários**:
  - Carregamento do modal
  - Auto-save de rascunho
  - Envio de feedback
  - Memory usage

### **Sessão 6: Acessibilidade (1h)**
- **Objetivo**: Verificar acessibilidade
- **Cenários**:
  - Navegação por teclado
  - Screen reader
  - ARIA labels
  - Focus management

## 6. Testes de Integração

### **Fluxo Completo de Feedback**
- **Setup**: Questão carregada
- **Steps**: Abertura → Preenchimento → Envio → Confirmação
- **Assertions**: Fluxo completo, dados corretos, confirmação

### **Gerenciamento de Rascunhos**
- **Setup**: Modal aberto
- **Steps**: Preenchimento → Auto-save → Fechamento → Reabertura
- **Assertions**: Rascunho salvo, recuperado, limpo

### **Validação de Formulário**
- **Setup**: Formulário vazio
- **Steps**: Preenchimento → Validação → Correção → Envio
- **Assertions**: Validação correta, correção funcional, envio

### **Error Handling**
- **Setup**: Erro simulado
- **Steps**: Erro → Retry → Sucesso
- **Assertions**: Erro tratado, retry funcional, sucesso

## 7. Testes de Performance

### **Métricas de Carregamento**
- **Modal Opening**: < 500ms
- **Form Validation**: < 100ms
- **Auto-save**: < 200ms
- **Feedback Submission**: < 2s

### **Testes de Carga**
- **Feedbacks simultâneos**: 50
- **Auto-save por minuto**: 100
- **Tempo de resposta**: < 1s
- **Taxa de erro**: < 1%

### **Testes de Memória**
- **Uso de memória**: < 50MB
- **Vazamentos de memória**: 0
- **Garbage collection**: Eficiente
- **Performance**: Estável

## 8. Testes de Segurança

### **Validação de Dados**
- **Sanitização**: Dados sanitizados
- **Validação**: Validação rigorosa
- **XSS**: Proteção contra XSS
- **CSRF**: Tokens CSRF

### **Armazenamento Local**
- **Dados sensíveis**: Não armazenados
- **TTL**: Expiração adequada
- **Criptografia**: Dados criptografados
- **Limpeza**: Limpeza adequada

### **API Security**
- **Validação**: Validação de entrada
- **Rate limiting**: Limitação de requisições
- **Authentication**: Autenticação adequada
- **Authorization**: Autorização adequada

---

**Este documento define especificações completas de teste para o sistema de feedback UX-001, incluindo casos felizes, erros, mocks, timeouts, cobertura e plano de testes exploratórios.**
