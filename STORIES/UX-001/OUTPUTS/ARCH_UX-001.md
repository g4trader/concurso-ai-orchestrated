# ARCH_UX-001: Sistema de Feedback do Usuário (Reportar Erro na Questão)

## 1. Diagrama (entrada→processamento→saída)

```mermaid
graph TD
    A[Usuário identifica problema] --> B[Clique em "Reportar Problema"]
    B --> C[Modal de Feedback]
    C --> D[Seleção de Categoria]
    D --> E[Comentário do Usuário]
    E --> F[Validação do Formulário]
    F --> G[Salvamento Local]
    G --> H[Envio para API]
    H --> I[Confirmação de Recebimento]
    I --> J[Fechamento do Modal]
    
    K[Estados do Formulário] --> L[Formulário Vazio]
    L --> M[Formulário Preenchido]
    M --> N[Formulário Validado]
    N --> O[Formulário Enviado]
    
    P[Armazenamento Local] --> Q[Salvamento de Rascunho]
    Q --> R[Recuperação de Rascunho]
    R --> S[Limpeza de Rascunho]
    
    T[Error Handling] --> U[Falha na Validação]
    U --> V[Falha no Envio]
    V --> W[Retry Mechanism]
    W --> X[Fallback Options]
    
    Y[Responsive Design] --> Z[Mobile Layout]
    Z --> AA[Tablet Layout]
    AA --> BB[Desktop Layout]
    
    CC[API Integration] --> DD[Placeholder API]
    DD --> EE[Evento JSON Estruturado]
    EE --> FF[Log de Feedback]
    
    GG[Categories] --> HH[Erro na Questão]
    HH --> II[Questão Ambígua]
    II --> JJ[Alternativa Incorreta]
    JJ --> KK[Outro Problema]
```

## 2. Pastas/arquivos a criar

```
/ux-001/
├── src/
│   ├── components/
│   │   ├── feedback/
│   │   │   ├── feedback-button.tsx
│   │   │   ├── feedback-modal.tsx
│   │   │   ├── feedback-form.tsx
│   │   │   ├── feedback-category-selector.tsx
│   │   │   ├── feedback-comment.tsx
│   │   │   ├── feedback-submit.tsx
│   │   │   ├── feedback-success.tsx
│   │   │   └── feedback-error.tsx
│   │   ├── ui/
│   │   │   ├── button.tsx
│   │   │   ├── modal.tsx
│   │   │   ├── input.tsx
│   │   │   ├── textarea.tsx
│   │   │   ├── select.tsx
│   │   │   ├── checkbox.tsx
│   │   │   ├── radio.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── alert.tsx
│   │   │   └── spinner.tsx
│   │   └── layout/
│   │       ├── header.tsx
│   │       ├── sidebar.tsx
│   │       └── footer.tsx
│   ├── hooks/
│   │   ├── use-feedback.ts
│   │   ├── use-draft.ts
│   │   ├── use-modal.ts
│   │   └── use-validation.ts
│   ├── services/
│   │   ├── feedback-service.ts
│   │   ├── draft-service.ts
│   │   ├── api-client.ts
│   │   └── storage-service.ts
│   ├── utils/
│   │   ├── validators.ts
│   │   ├── formatters.ts
│   │   ├── constants.ts
│   │   └── helpers.ts
│   ├── types/
│   │   ├── feedback.ts
│   │   ├── api.ts
│   │   └── common.ts
│   ├── pages/
│   │   ├── feedback/
│   │   │   ├── index.tsx
│   │   │   └── success.tsx
│   │   └── _app.tsx
│   └── contexts/
│       ├── feedback-context.tsx
│       └── feedback-provider.tsx
├── tests/
│   ├── components/
│   │   ├── feedback/
│   │   │   ├── feedback-button.test.tsx
│   │   │   ├── feedback-modal.test.tsx
│   │   │   ├── feedback-form.test.tsx
│   │   │   ├── feedback-category-selector.test.tsx
│   │   │   └── feedback-comment.test.tsx
│   │   └── ui/
│   │       ├── button.test.tsx
│   │       ├── modal.test.tsx
│   │       └── input.test.tsx
│   ├── hooks/
│   │   ├── use-feedback.test.ts
│   │   ├── use-draft.test.ts
│   │   └── use-modal.test.ts
│   ├── services/
│   │   ├── feedback-service.test.ts
│   │   ├── draft-service.test.ts
│   │   └── api-client.test.ts
│   └── utils/
│       ├── validators.test.ts
│       ├── formatters.test.ts
│       └── helpers.test.ts
├── docs/
│   ├── FEEDBACK_SYSTEM.md
│   ├── API_CONTRACTS.md
│   └── USER_GUIDE.md
├── .env.example
├── package.json
└── README.md
```

## 3. Contratos (schemas/DTOs) com exemplos

### Feedback Types
```typescript
// types/feedback.ts
export interface FeedbackRequest {
  questionId: string;
  userId: string;
  category: FeedbackCategory;
  comment: string;
  metadata: FeedbackMetadata;
  timestamp: string;
  userAgent: string;
  sessionId: string;
}

export interface FeedbackCategory {
  id: string;
  name: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  icon: string;
}

export interface FeedbackMetadata {
  questionText: string;
  questionOptions: string[];
  selectedAnswer?: string;
  correctAnswer?: string;
  timeSpent: number;
  difficulty: 'easy' | 'medium' | 'hard';
  topic: string;
  banca: string;
  edital: string;
  simuladoId: string;
  browserInfo: BrowserInfo;
  deviceInfo: DeviceInfo;
}

export interface BrowserInfo {
  name: string;
  version: string;
  os: string;
  language: string;
  timezone: string;
}

export interface DeviceInfo {
  type: 'desktop' | 'tablet' | 'mobile';
  screen: {
    width: number;
    height: number;
  };
  userAgent: string;
}

export interface FeedbackResponse {
  success: boolean;
  feedbackId: string;
  message: string;
  timestamp: string;
  status: 'pending' | 'reviewed' | 'resolved' | 'rejected';
}

export interface FeedbackDraft {
  questionId: string;
  category?: FeedbackCategory;
  comment: string;
  lastSaved: string;
  isDirty: boolean;
}

export interface FeedbackEvent {
  type: 'feedback_submitted' | 'feedback_draft_saved' | 'feedback_modal_opened' | 'feedback_modal_closed';
  payload: any;
  timestamp: string;
  sessionId: string;
}
```

### API Types
```typescript
// types/api.ts
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ApiError;
  timestamp: string;
}

export interface ApiError {
  code: string;
  message: string;
  details?: any;
  field?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

export interface ValidationError {
  field: string;
  message: string;
  code: string;
}
```

### Common Types
```typescript
// types/common.ts
export interface BaseEntity {
  id: string;
  createdAt: string;
  updatedAt: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
}

export interface Question {
  id: string;
  text: string;
  options: QuestionOption[];
  correctAnswer: string;
  explanation?: string;
  topic: string;
  difficulty: 'easy' | 'medium' | 'hard';
  banca: string;
  edital: string;
}

export interface QuestionOption {
  id: string;
  text: string;
  letter: 'A' | 'B' | 'C' | 'D' | 'E';
}
```

## 4. Decisões/Trade-offs

### **Modal vs Página Dedicada**
- **Modal**: Melhor UX, mantém contexto da questão
- **Trade-off**: Espaço limitado vs funcionalidade completa
- **Decisão**: Modal com scroll interno para formulário

### **Armazenamento de Rascunho**
- **LocalStorage vs SessionStorage**: LocalStorage para persistência
- **Trade-off**: Persistência vs Privacidade
- **Decisão**: LocalStorage com TTL de 7 dias

### **Validação de Formulário**
- **Client-side vs Server-side**: Client-side para UX
- **Trade-off**: Performance vs Segurança
- **Decisão**: Validação híbrida (client + server)

### **Categorização de Feedback**
- **Categorias fixas vs dinâmicas**: Categorias fixas inicialmente
- **Trade-off**: Simplicidade vs Flexibilidade
- **Decisão**: Categorias fixas com possibilidade de expansão

### **API Placeholder**
- **Mock vs Real API**: Placeholder com estrutura real
- **Trade-off**: Desenvolvimento vs Integração
- **Decisão**: Placeholder que simula API real

### **Error Handling**
- **Global vs Component**: Error boundary global
- **Trade-off**: Consistência vs Flexibilidade
- **Decisão**: Error boundary com fallbacks específicos

### **Responsividade**
- **Mobile-first vs Desktop-first**: Mobile-first
- **Trade-off**: Desenvolvimento vs Acessibilidade
- **Decisão**: Mobile-first com breakpoints

### **Performance**
- **Lazy loading vs Eager loading**: Lazy loading para modal
- **Trade-off**: UX vs Performance
- **Decisão**: Lazy loading com skeleton

## 5. Checklist por etapas (P/M/G) e Riscos & Mitigações

### **Setup Inicial (P)**
- [ ] Configurar estrutura de pastas
- [ ] Configurar TypeScript types
- [ ] Configurar bibliotecas de UI
- [ ] Configurar variáveis de ambiente

**Riscos:**
- **Dependências pesadas**: Bibliotecas de UI podem impactar bundle
- **Configuração complexa**: Múltiplas bibliotecas

**Mitigações:**
- Tree shaking para otimização
- Lazy loading de componentes
- Documentação clara

### **Componentes de Feedback (P)**
- [ ] Implementar FeedbackButton
- [ ] Implementar FeedbackModal
- [ ] Implementar FeedbackForm
- [ ] Implementar FeedbackCategorySelector
- [ ] Implementar FeedbackComment

**Riscos:**
- **UX confusa**: Modal muito complexo
- **Performance**: Re-renders desnecessários

**Mitigações:**
- Design simples e intuitivo
- Memoização de componentes
- Otimização de re-renders

### **Formulário e Validação (M)**
- [ ] Implementar validação de formulário
- [ ] Implementar estados de loading
- [ ] Implementar error handling
- [ ] Implementar success states

**Riscos:**
- **Validação incorreta**: Lógica de validação complexa
- **UX ruim**: Estados de loading confusos

**Mitigações:**
- Testes unitários rigorosos
- Estados de loading claros
- Feedback visual adequado

### **Armazenamento Local (M)**
- [ ] Implementar salvamento de rascunho
- [ ] Implementar recuperação de rascunho
- [ ] Implementar limpeza de rascunho
- [ ] Implementar sincronização

**Riscos:**
- **Limite de storage**: LocalStorage limitado
- **Sincronização**: Dados inconsistentes

**Mitigações:**
- Compressão de dados
- Versionamento de dados
- Validação de integridade

### **API Integration (M)**
- [ ] Implementar placeholder API
- [ ] Implementar envio de feedback
- [ ] Implementar retry mechanism
- [ ] Implementar error handling

**Riscos:**
- **API não disponível**: Placeholder não funcional
- **Timeout**: Requisições demoradas

**Mitigações:**
- Placeholder robusto
- Timeout configurável
- Retry com backoff

### **Responsividade (G)**
- [ ] Implementar mobile layout
- [ ] Implementar tablet layout
- [ ] Implementar desktop layout
- [ ] Implementar touch interactions

**Riscos:**
- **Layout quebrado**: Modal em mobile
- **Touch**: Interações touch inadequadas

**Mitigações:**
- Testes em múltiplos dispositivos
- Modal responsivo
- Touch-friendly interactions

### **Testing (G)**
- [ ] Implementar testes unitários
- [ ] Implementar testes de integração
- [ ] Implementar testes E2E
- [ ] Implementar testes de acessibilidade

**Riscos:**
- **Cobertura baixa**: Componentes complexos
- **Testes lentos**: Modal e formulários

**Mitigações:**
- Coverage thresholds
- Mock de dependências
- Testes paralelos

### **Performance (G)**
- [ ] Implementar lazy loading
- [ ] Implementar code splitting
- [ ] Implementar caching
- [ ] Implementar optimization

**Riscos:**
- **Bundle size**: Bibliotecas pesadas
- **Memory usage**: Modal não fechado

**Mitigações:**
- Dynamic imports
- Memory management
- Performance monitoring

### **Acessibilidade (G)**
- [ ] Implementar ARIA labels
- [ ] Implementar keyboard navigation
- [ ] Implementar screen reader support
- [ ] Implementar focus management

**Riscos:**
- **Acessibilidade**: Modal não acessível
- **Keyboard**: Navegação por teclado

**Mitigações:**
- Testes de acessibilidade
- ARIA guidelines
- Keyboard navigation

---

**Este documento define a arquitetura completa do sistema de feedback UX-001, incluindo estrutura, contratos, decisões técnicas e plano de implementação com mitigação de riscos.**
