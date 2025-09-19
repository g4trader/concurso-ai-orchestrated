# TEST_SPEC_WEB-002: Especificações de Teste - Autenticação Simples

## 1. Casos Felizes e de Erro

### **Login Form Tests**

#### Casos Felizes
- **Login bem-sucedido com credenciais válidas**
  - Input: Email válido + senha válida
  - Expected: Login realizado, token armazenado, redirect para dashboard
  - Assertions: Token salvo, usuário autenticado, redirecionamento correto

- **Login com "Lembrar de mim" ativado**
  - Input: Credenciais válidas + rememberMe=true
  - Expected: Token com expiração estendida
  - Assertions: Token com expiração de 30 dias, persistência mantida

- **Validação de campos em tempo real**
  - Input: Email inválido + senha válida
  - Expected: Erro de validação exibido
  - Assertions: Mensagem de erro específica, submit desabilitado

- **Formulário limpo após login**
  - Input: Login bem-sucedido
  - Expected: Campos limpos, estado resetado
  - Assertions: Campos vazios, sem erros, estado inicial

#### Casos de Erro
- **Credenciais inválidas**
  - Input: Email/senha incorretos
  - Expected: Mensagem de erro de credenciais
  - Assertions: Erro exibido, formulário mantido, sem redirecionamento

- **Email não encontrado**
  - Input: Email inexistente
  - Expected: Erro "Email não encontrado"
  - Assertions: Mensagem específica, formulário mantido

- **Conta desativada**
  - Input: Credenciais de conta inativa
  - Expected: Erro "Conta desativada"
  - Assertions: Mensagem específica, sem login

- **Rate limiting**
  - Input: Múltiplas tentativas de login
  - Expected: Erro de rate limiting
  - Assertions: Mensagem de bloqueio temporário

- **Timeout de rede**
  - Input: Resposta lenta da API
  - Expected: Timeout após 10s
  - Assertions: Erro de timeout, estado resetado

### **Logout Button Tests**

#### Casos Felizes
- **Logout bem-sucedido**
  - Input: Usuário autenticado clica em logout
  - Expected: Token removido, redirect para login
  - Assertions: Token limpo, estado resetado, redirecionamento

- **Logout com token inválido**
  - Input: Token expirado/inválido
  - Expected: Logout local realizado
  - Assertions: Estado limpo, redirecionamento

- **Logout em múltiplas abas**
  - Input: Logout em uma aba
  - Expected: Sincronização entre abas
  - Assertions: Todas as abas redirecionadas

#### Casos de Erro
- **Falha na API de logout**
  - Input: Erro na API de logout
  - Expected: Logout local realizado
  - Assertions: Estado limpo, redirecionamento mantido

- **Token corrompido**
  - Input: Token malformado
  - Expected: Logout local realizado
  - Assertions: Estado limpo, sem erros

### **Auth Guard Tests**

#### Casos Felizes
- **Acesso autorizado**
  - Input: Usuário autenticado acessa rota protegida
  - Expected: Acesso permitido
  - Assertions: Conteúdo renderizado, sem redirecionamento

- **Token válido**
  - Input: Token válido e não expirado
  - Expected: Acesso permitido
  - Assertions: Conteúdo renderizado

- **Token refresh automático**
  - Input: Token próximo do vencimento
  - Expected: Refresh automático
  - Assertions: Novo token, acesso mantido

#### Casos de Erro
- **Acesso não autorizado**
  - Input: Usuário não autenticado
  - Expected: Redirect para login
  - Assertions: Redirecionamento, sem conteúdo

- **Token expirado**
  - Input: Token expirado
  - Expected: Redirect para login
  - Assertions: Redirecionamento, token limpo

- **Token inválido**
  - Input: Token malformado
  - Expected: Redirect para login
  - Assertions: Redirecionamento, estado limpo

### **Password Input Tests**

#### Casos Felizes
- **Toggle de visibilidade**
  - Input: Clique no ícone de olho
  - Expected: Alternância entre texto/senha
  - Assertions: Tipo de input alterado, ícone atualizado

- **Validação de senha**
  - Input: Senha com menos de 8 caracteres
  - Expected: Erro de validação
  - Assertions: Mensagem específica, submit desabilitado

- **Senha forte**
  - Input: Senha com 8+ caracteres
  - Expected: Validação passa
  - Assertions: Sem erros, submit habilitado

#### Casos de Erro
- **Senha vazia**
  - Input: Campo senha vazio
  - Expected: Erro de campo obrigatório
  - Assertions: Mensagem específica, submit desabilitado

- **Senha com caracteres especiais**
  - Input: Senha com caracteres inválidos
  - Expected: Erro de validação
  - Assertions: Mensagem específica, validação falha

### **Token Service Tests**

#### Casos Felizes
- **Armazenamento de token**
  - Input: Token válido
  - Expected: Token salvo em cookies
  - Assertions: Cookie criado, valor correto

- **Recuperação de token**
  - Input: Token armazenado
  - Expected: Token recuperado
  - Assertions: Valor correto, sem erros

- **Limpeza de tokens**
  - Input: Comando de limpeza
  - Expected: Tokens removidos
  - Assertions: Cookies removidos, estado limpo

#### Casos de Erro
- **Token corrompido**
  - Input: Token malformado
  - Expected: Token ignorado
  - Assertions: Fallback para null, sem erros

- **Storage indisponível**
  - Input: Cookies desabilitados
  - Expected: Fallback para localStorage
  - Assertions: Fallback funcional, sem erros

### **API Client Tests**

#### Casos Felizes
- **Requisição com token**
  - Input: Requisição autenticada
  - Expected: Header Authorization adicionado
  - Assertions: Header correto, requisição enviada

- **Refresh automático de token**
  - Input: Token expirado
  - Expected: Refresh automático
  - Assertions: Novo token, requisição retry

- **Interceptação de resposta**
  - Input: Resposta da API
  - Expected: Dados processados
  - Assertions: Dados corretos, sem erros

#### Casos de Erro
- **Token expirado**
  - Input: Token expirado
  - Expected: Refresh automático
  - Assertions: Novo token, requisição retry

- **Refresh falha**
  - Input: Refresh token inválido
  - Expected: Redirect para login
  - Assertions: Redirecionamento, estado limpo

- **Timeout de requisição**
  - Input: Requisição lenta
  - Expected: Timeout após 10s
  - Assertions: Erro de timeout, estado resetado

## 2. Estratégias de Mocks

### **Auth Service Mocks**

#### Login Mock
```javascript
// __mocks__/services/auth-service.js
export const mockLogin = jest.fn().mockResolvedValue({
  user: {
    id: '123e4567-e89b-12d3-a456-426614174000',
    email: 'test@example.com',
    name: 'Test User',
    avatar: 'https://example.com/avatar.jpg',
    createdAt: '2024-01-15T10:30:00Z',
    lastLogin: '2024-01-15T10:30:00Z',
    isActive: true,
  },
  token: 'mock-jwt-token',
  refreshToken: 'mock-refresh-token',
  expiresIn: 3600,
  tokenType: 'Bearer',
})

export const mockLoginError = jest.fn().mockRejectedValue({
  message: 'Credenciais inválidas',
  code: 'INVALID_CREDENTIALS',
})
```

#### Logout Mock
```javascript
export const mockLogout = jest.fn().mockResolvedValue({
  message: 'Logout realizado com sucesso',
  success: true,
})

export const mockLogoutError = jest.fn().mockRejectedValue({
  message: 'Erro no logout',
  code: 'LOGOUT_ERROR',
})
```

#### Refresh Token Mock
```javascript
export const mockRefreshToken = jest.fn().mockResolvedValue({
  token: 'new-mock-jwt-token',
  refreshToken: 'new-mock-refresh-token',
  expiresIn: 3600,
})

export const mockRefreshTokenError = jest.fn().mockRejectedValue({
  message: 'Token de refresh inválido',
  code: 'INVALID_REFRESH_TOKEN',
})
```

### **Token Service Mocks**

```javascript
// __mocks__/services/token-service.js
const mockTokens = {
  token: null,
  refreshToken: null,
}

export const mockTokenService = {
  getToken: jest.fn(() => mockTokens.token),
  setToken: jest.fn((token) => { mockTokens.token = token }),
  getRefreshToken: jest.fn(() => mockTokens.refreshToken),
  setRefreshToken: jest.fn((refreshToken) => { mockTokens.refreshToken = refreshToken }),
  clearTokens: jest.fn(() => { 
    mockTokens.token = null
    mockTokens.refreshToken = null
  }),
  isTokenExpired: jest.fn((token) => {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return payload.exp * 1000 < Date.now()
    } catch {
      return true
    }
  }),
}
```

### **API Client Mocks**

```javascript
// __mocks__/services/api-client.js
export const mockApiClient = {
  post: jest.fn(),
  get: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
  interceptors: {
    request: { use: jest.fn() },
    response: { use: jest.fn() },
  },
}

// Mock successful responses
mockApiClient.post.mockResolvedValue({
  data: { success: true },
  status: 200,
  statusText: 'OK',
})

mockApiClient.get.mockResolvedValue({
  data: { success: true },
  status: 200,
  statusText: 'OK',
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
  pathname: '/',
  query: {},
  asPath: '/',
}

export const useRouter = () => mockRouter
export const usePathname = () => mockRouter.pathname
export const useSearchParams = () => new URLSearchParams()
```

### **Cookies Mocks**

```javascript
// __mocks__/js-cookie.js
const mockCookies = {}

export default {
  get: jest.fn((key) => mockCookies[key] || undefined),
  set: jest.fn((key, value) => { mockCookies[key] = value }),
  remove: jest.fn((key) => { delete mockCookies[key] }),
}
```

## 3. Timeouts e Re-tentativas

### **API Timeouts**
- **Login timeout**: 10 segundos
- **Logout timeout**: 5 segundos
- **Refresh token timeout**: 5 segundos
- **Get user info timeout**: 5 segundos
- **Retry strategy**: 3 tentativas com backoff exponencial

### **Component Timeouts**
- **Loading states**: 5 segundos máximo
- **Form validation**: 500ms debounce
- **Token refresh**: 30 segundos antes do vencimento
- **Auto-logout**: 30 minutos de inatividade

### **Navigation Timeouts**
- **Redirect after login**: 1 segundo
- **Redirect after logout**: 500ms
- **Route protection**: Imediato
- **Fallback routes**: Imediato

## 4. Critérios de Cobertura por Arquivo

### **src/components/auth/login-form.tsx**
- **Cobertura mínima**: 95%
- **Casos críticos**: Validação, submit, error handling, loading states
- **Testes**: Form validation, submit flow, error display, loading states

### **src/components/auth/logout-button.tsx**
- **Cobertura mínima**: 90%
- **Casos críticos**: Logout flow, loading states, error handling
- **Testes**: Logout functionality, loading states, error handling

### **src/components/auth/auth-guard.tsx**
- **Cobertura mínima**: 95%
- **Casos críticos**: Authentication check, redirect logic, loading states
- **Testes**: Auth check, redirect logic, loading states, error handling

### **src/components/auth/protected-route.tsx**
- **Cobertura mínima**: 90%
- **Casos críticos**: Route protection, redirect logic
- **Testes**: Route protection, redirect logic, error handling

### **src/components/auth/password-input.tsx**
- **Cobertura mínima**: 95%
- **Casos críticos**: Toggle visibility, validation, error display
- **Testes**: Toggle functionality, validation, error display

### **src/hooks/use-auth.ts**
- **Cobertura mínima**: 95%
- **Casos críticos**: Login, logout, token refresh, state management
- **Testes**: All auth flows, state management, error handling

### **src/hooks/use-login.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Login flow, error handling, loading states
- **Testes**: Login functionality, error handling, loading states

### **src/hooks/use-logout.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Logout flow, error handling, loading states
- **Testes**: Logout functionality, error handling, loading states

### **src/hooks/use-token.ts**
- **Cobertura mínima**: 95%
- **Casos críticos**: Token management, storage operations
- **Testes**: Token operations, storage operations, error handling

### **src/services/auth-service.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: All API calls, error handling
- **Testes**: All API methods, error handling, response processing

### **src/services/token-service.ts**
- **Cobertura mínima**: 95%
- **Casos críticos**: Token storage, retrieval, validation
- **Testes**: All token operations, storage operations, validation

### **src/services/api-client.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Request/response interceptors, error handling
- **Testes**: Interceptors, error handling, token refresh

## 5. Plano de Testes Exploratórios

### **Sessão 1: Fluxo de Login (2h)**
- **Objetivo**: Verificar fluxo completo de login
- **Cenários**:
  - Login com credenciais válidas
  - Login com credenciais inválidas
  - Validação de campos
  - Estados de loading
  - Redirecionamento após login

### **Sessão 2: Fluxo de Logout (1h)**
- **Objetivo**: Verificar fluxo completo de logout
- **Cenários**:
  - Logout normal
  - Logout com token inválido
  - Logout em múltiplas abas
  - Limpeza de estado
  - Redirecionamento após logout

### **Sessão 3: Proteção de Rotas (1.5h)**
- **Objetivo**: Verificar proteção de rotas
- **Cenários**:
  - Acesso a rotas protegidas
  - Redirecionamento para login
  - Token expirado
  - Token inválido
  - Refresh automático

### **Sessão 4: Gerenciamento de Tokens (1.5h)**
- **Objetivo**: Verificar gerenciamento de tokens
- **Cenários**:
  - Armazenamento de tokens
  - Recuperação de tokens
  - Validação de tokens
  - Refresh automático
  - Limpeza de tokens

### **Sessão 5: Estados de Erro (1h)**
- **Objetivo**: Verificar tratamento de erros
- **Cenários**:
  - Erros de rede
  - Timeouts
  - Erros de validação
  - Erros de API
  - Estados de fallback

### **Sessão 6: Segurança (1h)**
- **Objetivo**: Verificar aspectos de segurança
- **Cenários**:
  - Armazenamento seguro de tokens
  - Proteção contra XSS
  - Proteção contra CSRF
  - Validação de inputs
  - Sanitização de dados

## 6. Testes de Integração

### **Fluxo Completo de Autenticação**
- **Setup**: Usuário não autenticado
- **Steps**: Acesso à rota protegida → Redirect para login → Login → Dashboard
- **Assertions**: Fluxo completo, tokens armazenados, redirecionamento correto

### **Fluxo de Logout**
- **Setup**: Usuário autenticado
- **Steps**: Dashboard → Logout → Login
- **Assertions**: Estado limpo, tokens removidos, redirecionamento correto

### **Refresh Automático de Token**
- **Setup**: Usuário com token próximo do vencimento
- **Steps**: Acesso à rota protegida → Refresh automático → Acesso mantido
- **Assertions**: Token renovado, acesso mantido, sem interrupção

### **Múltiplas Abas**
- **Setup**: Usuário logado em múltiplas abas
- **Steps**: Logout em uma aba → Verificar outras abas
- **Assertions**: Todas as abas redirecionadas, estado sincronizado

## 7. Testes de Performance

### **Métricas de Carregamento**
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3.5s
- **Cumulative Layout Shift**: < 0.1

### **Testes de Carga**
- **Usuários simultâneos**: 100
- **Logins por minuto**: 500
- **Tempo de resposta**: < 2s
- **Taxa de erro**: < 1%

## 8. Testes de Segurança

### **Autenticação**
- **Token storage**: Cookies seguros
- **Token validation**: Validação rigorosa
- **Password handling**: Hash seguro
- **Session management**: Timeout adequado

### **Proteção contra Ataques**
- **XSS**: Sanitização de inputs
- **CSRF**: Tokens CSRF
- **Brute force**: Rate limiting
- **Session hijacking**: Tokens seguros

---

**Este documento define especificações completas de teste para o sistema de autenticação WEB-002, incluindo casos felizes, erros, mocks, timeouts, cobertura e plano de testes exploratórios.**
