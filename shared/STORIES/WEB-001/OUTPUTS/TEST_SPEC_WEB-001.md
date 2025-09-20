# TEST_SPEC_WEB-001: Especificações de Teste - Protótipo Web Next.js

## 1. Casos Felizes e de Erro

### **Layout e Navegação Tests**

#### Casos Felizes
- **Layout principal renderiza corretamente**
  - Input: Aplicação carregada
  - Expected: Header, main content, footer visíveis
  - Assertions: Estrutura HTML correta, componentes renderizados

- **Navegação entre páginas**
  - Input: Clique em links de navegação
  - Expected: Páginas carregam corretamente
  - Assertions: URL atualizada, conteúdo da página correto

- **Header responsivo**
  - Input: Diferentes tamanhos de tela
  - Expected: Header adapta-se ao tamanho
  - Assertions: Layout responsivo, menu mobile funcional

- **Footer sempre visível**
  - Input: Scroll em qualquer página
  - Expected: Footer permanece no final
  - Assertions: Posicionamento correto, conteúdo visível

#### Casos de Erro
- **Página não encontrada**
  - Input: URL inexistente
  - Expected: Página 404 renderizada
  - Assertions: Mensagem de erro, botão de retorno

- **Erro de carregamento**
  - Input: Falha na renderização
  - Expected: Error boundary ativado
  - Assertions: Mensagem de erro, botão de retry

- **Navegação quebrada**
  - Input: Links malformados
  - Expected: Fallback para página inicial
  - Assertions: Redirecionamento correto, sem crash

### **Página de Login Tests**

#### Casos Felizes
- **Formulário de login renderiza**
  - Input: Acesso à página de login
  - Expected: Formulário com campos email/senha
  - Assertions: Campos visíveis, botão de submit

- **Login bem-sucedido**
  - Input: Credenciais válidas
  - Expected: Redirecionamento para dashboard
  - Assertions: Estado de autenticação atualizado, token salvo

- **Validação de campos**
  - Input: Campos preenchidos corretamente
  - Expected: Validação passa
  - Assertions: Sem mensagens de erro, submit habilitado

- **Estado de loading**
  - Input: Submit do formulário
  - Expected: Spinner de loading
  - Assertions: Botão desabilitado, indicador visual

#### Casos de Erro
- **Credenciais inválidas**
  - Input: Email/senha incorretos
  - Expected: Mensagem de erro
  - Assertions: Erro exibido, formulário não submetido

- **Campos obrigatórios vazios**
  - Input: Campos em branco
  - Expected: Validação falha
  - Assertions: Mensagens de erro, submit desabilitado

- **Email malformado**
  - Input: Email inválido
  - Expected: Erro de validação
  - Assertions: Mensagem específica, campo destacado

- **Timeout de login**
  - Input: Resposta lenta da API
  - Expected: Timeout após 30s
  - Assertions: Erro de timeout, estado resetado

### **Dashboard Tests**

#### Casos Felizes
- **Dashboard carrega para usuário autenticado**
  - Input: Usuário logado acessa dashboard
  - Expected: Estatísticas e componentes carregam
  - Assertions: Cards de stats, gráficos, dados mockados

- **Estatísticas exibidas**
  - Input: Dados de simulados
  - Expected: Cards com números corretos
  - Assertions: Valores corretos, formatação adequada

- **Gráficos renderizam**
  - Input: Dados de performance
  - Expected: Gráficos visíveis
  - Assertions: Elementos SVG, dados plotados

- **Simulados recentes listados**
  - Input: Lista de simulados
  - Expected: Cards de simulados recentes
  - Assertions: Títulos, datas, status corretos

#### Casos de Erro
- **Acesso sem autenticação**
  - Input: Usuário não logado
  - Expected: Redirecionamento para login
  - Assertions: AuthGuard ativado, redirect correto

- **Dados não carregam**
  - Input: API retorna erro
  - Expected: Estado de erro exibido
  - Assertions: Mensagem de erro, botão de retry

- **Gráficos falham**
  - Input: Dados malformados
  - Expected: Fallback para texto
  - Assertions: Mensagem de fallback, sem crash

### **Gerador de Simulado Tests**

#### Casos Felizes
- **Formulário de simulado renderiza**
  - Input: Acesso à página
  - Expected: Formulário com campos
  - Assertions: Campos visíveis, opções de banca

- **Seleção de banca**
  - Input: Seleção de banca (CESPE, FGV, etc.)
  - Expected: Opções atualizadas
  - Assertions: Dropdown funcional, valores corretos

- **Configuração de simulado**
  - Input: Preenchimento do formulário
  - Expected: Validação passa
  - Assertions: Campos válidos, submit habilitado

- **Geração de simulado**
  - Input: Submit do formulário
  - Expected: Redirecionamento para simulado
  - Assertions: Simulado criado, página carregada

#### Casos de Erro
- **Campos obrigatórios vazios**
  - Input: Formulário incompleto
  - Expected: Validação falha
  - Assertions: Mensagens de erro, submit desabilitado

- **Banca inválida**
  - Input: Banca não suportada
  - Expected: Erro de validação
  - Assertions: Mensagem específica, opção inválida

- **Falha na geração**
  - Input: Erro na API
  - Expected: Mensagem de erro
  - Assertions: Erro exibido, formulário mantido

### **Página de Resultados Tests**

#### Casos Felizes
- **Resultados exibidos**
  - Input: Simulado completado
  - Expected: Score e análise exibidos
  - Assertions: Pontuação correta, gráficos visíveis

- **Review de questões**
  - Input: Clique em questão
  - Expected: Detalhes da questão
  - Assertions: Pergunta, resposta, explicação

- **Gráfico de performance**
  - Input: Dados de resultado
  - Expected: Gráfico renderizado
  - Assertions: Elementos visuais, dados corretos

- **Exportação de resultados**
  - Input: Botão de exportar
  - Expected: Download iniciado
  - Assertions: Arquivo gerado, download funcional

#### Casos de Erro
- **Resultados não encontrados**
  - Input: ID de simulado inválido
  - Expected: Mensagem de erro
  - Assertions: Erro 404, botão de retorno

- **Dados corrompidos**
  - Input: Dados malformados
  - Expected: Fallback para dados padrão
  - Assertions: Mensagem de aviso, dados básicos

### **Componentes UI Tests**

#### Casos Felizes
- **Button renderiza corretamente**
  - Input: Props de button
  - Expected: Botão com estilo correto
  - Assertions: Classes CSS, texto, estado

- **Button com loading**
  - Input: Prop loading=true
  - Expected: Spinner visível
  - Assertions: Spinner renderizado, botão desabilitado

- **Card com conteúdo**
  - Input: Children no Card
  - Expected: Conteúdo renderizado
  - Assertions: Estrutura HTML, estilos aplicados

- **Spinner animado**
  - Input: Componente Spinner
  - Expected: Animação de rotação
  - Assertions: CSS animation, tamanho correto

#### Casos de Erro
- **Button com props inválidas**
  - Input: Props malformadas
  - Expected: Fallback para props padrão
  - Assertions: Componente não quebra, estilos padrão

- **Card sem conteúdo**
  - Input: Children vazio
  - Expected: Card vazio renderizado
  - Assertions: Estrutura mantida, sem crash

## 2. Estratégias de Mocks

### **API Mocks**

#### Auth API
```javascript
// __mocks__/api/auth.js
export const mockLogin = jest.fn().mockResolvedValue({
  user: {
    id: '1',
    email: 'test@example.com',
    name: 'Test User',
  },
  token: 'mock-jwt-token',
  expiresIn: 3600,
})

export const mockLogout = jest.fn().mockResolvedValue({})

export const mockGetUser = jest.fn().mockResolvedValue({
  id: '1',
  email: 'test@example.com',
  name: 'Test User',
})
```

#### Simulado API
```javascript
// __mocks__/api/simulado.js
export const mockGetSimulados = jest.fn().mockResolvedValue({
  data: [
    {
      id: '1',
      title: 'Simulado CESPE 2023',
      banca: 'CESPE',
      totalQuestions: 50,
      status: 'completed',
    },
  ],
  pagination: {
    page: 1,
    limit: 10,
    total: 1,
    totalPages: 1,
  },
})

export const mockCreateSimulado = jest.fn().mockResolvedValue({
  id: '2',
  title: 'Novo Simulado',
  banca: 'FGV',
  totalQuestions: 30,
  status: 'draft',
})

export const mockGetQuestions = jest.fn().mockResolvedValue([
  {
    id: '1',
    question: 'Qual é a capital do Brasil?',
    alternatives: {
      A: 'São Paulo',
      B: 'Rio de Janeiro',
      C: 'Brasília',
      D: 'Belo Horizonte',
      E: 'Salvador',
    },
    correctAnswer: 'C',
  },
])
```

#### Results API
```javascript
// __mocks__/api/results.js
export const mockGetResults = jest.fn().mockResolvedValue({
  simuladoId: '1',
  score: 85,
  totalQuestions: 50,
  correctAnswers: 42,
  timeSpent: 2700,
  responses: [
    {
      questionId: '1',
      selectedAnswer: 'C',
      isCorrect: true,
      timeSpent: 45,
    },
  ],
  completedAt: '2024-01-15T10:30:00Z',
})
```

### **Router Mocks**

```javascript
// __mocks__/next/router.js
export const mockRouter = {
  push: jest.fn(),
  replace: jest.fn(),
  back: jest.fn(),
  pathname: '/',
  query: {},
  asPath: '/',
}

export const useRouter = () => mockRouter
```

### **Local Storage Mocks**

```javascript
// __mocks__/localStorage.js
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
}

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
})
```

### **Window Mocks**

```javascript
// __mocks__/window.js
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
})
```

## 3. Timeouts e Re-tentativas

### **API Timeouts**
- **Login timeout**: 30 segundos
- **Simulado generation timeout**: 60 segundos
- **Results loading timeout**: 15 segundos
- **Retry strategy**: 3 tentativas com backoff exponencial

### **Component Timeouts**
- **Loading states**: 5 segundos máximo
- **Error boundaries**: Imediato
- **Form validation**: 500ms debounce
- **Auto-save**: 2 segundos após mudança

### **Navigation Timeouts**
- **Page transitions**: 3 segundos
- **Route changes**: 1 segundo
- **Redirects**: 500ms
- **Fallback routes**: Imediato

## 4. Critérios de Cobertura por Arquivo

### **src/app/layout.tsx**
- **Cobertura mínima**: 90%
- **Casos críticos**: Renderização, providers, metadata
- **Testes**: Layout structure, AuthProvider, metadata

### **src/app/page.tsx**
- **Cobertura mínima**: 85%
- **Casos críticos**: Links, cards, apresentação
- **Testes**: Homepage content, navigation links, responsive

### **src/app/login/page.tsx**
- **Cobertura mínima**: 90%
- **Casos críticos**: Formulário, validação, estados
- **Testes**: Form rendering, validation, error states

### **src/app/dashboard/page.tsx**
- **Cobertura mínima**: 85%
- **Casos críticos**: AuthGuard, componentes, dados
- **Testes**: Authentication, component rendering, data display

### **src/components/ui/button.tsx**
- **Cobertura mínima**: 95%
- **Casos críticos**: Variantes, estados, acessibilidade
- **Testes**: All variants, loading state, disabled state, accessibility

### **src/components/ui/card.tsx**
- **Cobertura mínima**: 90%
- **Casos críticos**: Renderização, estilos, children
- **Testes**: Basic rendering, styling, content display

### **src/components/layout/header.tsx**
- **Cobertura mínima**: 85%
- **Casos críticos**: Navegação, autenticação, responsividade
- **Testes**: Navigation links, auth state, responsive behavior

### **src/hooks/use-auth.tsx**
- **Cobertura mínima**: 90%
- **Casos críticos**: Login, logout, estado, persistência
- **Testes**: Login flow, logout, state management, persistence

### **src/lib/utils.ts**
- **Cobertura mínima**: 95%
- **Casos críticos**: Todas as funções utilitárias
- **Testes**: All utility functions, edge cases, error handling

## 5. Plano de Testes Exploratórios

### **Sessão 1: Navegação e Layout (2h)**
- **Objetivo**: Verificar navegação e layout responsivo
- **Cenários**:
  - Navegação entre todas as páginas
  - Teste em diferentes tamanhos de tela
  - Verificação de acessibilidade
  - Teste de performance de carregamento

### **Sessão 2: Autenticação (1.5h)**
- **Objetivo**: Testar fluxo completo de autenticação
- **Cenários**:
  - Login com credenciais válidas/inválidas
  - Logout e limpeza de sessão
  - Persistência de autenticação
  - Redirecionamentos após auth

### **Sessão 3: Dashboard e Dados (2h)**
- **Objetivo**: Verificar exibição e interação com dados
- **Cenários**:
  - Carregamento de estatísticas
  - Interação com gráficos
  - Lista de simulados recentes
  - Estados de loading/error

### **Sessão 4: Formulários e Validação (1.5h)**
- **Objetivo**: Testar formulários e validações
- **Cenários**:
  - Formulário de login
  - Formulário de gerador de simulado
  - Validações de campo
  - Estados de submit

### **Sessão 5: Estados de Erro (1h)**
- **Objetivo**: Verificar tratamento de erros
- **Cenários**:
  - Páginas não encontradas
  - Erros de API
  - Timeouts
  - Estados de fallback

### **Sessão 6: Performance e Acessibilidade (1h)**
- **Objetivo**: Verificar performance e acessibilidade
- **Cenários**:
  - Tempo de carregamento
  - Uso de teclado
  - Screen readers
  - Contraste de cores

## 6. Testes de Integração

### **Fluxo Completo de Login**
- **Setup**: Usuário não autenticado
- **Steps**: Acesso à página → Login → Dashboard
- **Assertions**: Redirecionamento correto, estado atualizado

### **Fluxo de Geração de Simulado**
- **Setup**: Usuário autenticado
- **Steps**: Dashboard → Gerador → Configuração → Criação
- **Assertions**: Simulado criado, redirecionamento correto

### **Fluxo de Resultados**
- **Setup**: Simulado completado
- **Steps**: Acesso aos resultados → Visualização → Review
- **Assertions**: Dados corretos, navegação funcional

## 7. Testes de Performance

### **Métricas de Carregamento**
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3.5s
- **Cumulative Layout Shift**: < 0.1

### **Testes de Carga**
- **Usuários simultâneos**: 100
- **Páginas por minuto**: 1000
- **Tempo de resposta**: < 2s
- **Taxa de erro**: < 1%

## 8. Testes de Acessibilidade

### **WCAG 2.1 AA Compliance**
- **Contraste de cores**: Mínimo 4.5:1
- **Navegação por teclado**: Todas as funcionalidades
- **Screen readers**: Compatibilidade
- **Alt text**: Todas as imagens

### **Ferramentas de Teste**
- **axe-core**: Testes automatizados
- **Lighthouse**: Auditoria completa
- **WAVE**: Verificação de acessibilidade
- **Manual testing**: Verificação humana

---

**Este documento define especificações completas de teste para o protótipo web WEB-001, incluindo casos felizes, erros, mocks, timeouts, cobertura e plano de testes exploratórios.**
