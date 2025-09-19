# TEST_SPEC_WEB-004: Especificações de Teste - Relatório Pós-Simulado

## 1. Casos Felizes e de Erro

### **Results Summary Tests**

#### Casos Felizes
- **Exibição de resumo completo**
  - Input: Resultados válidos do simulado
  - Expected: Resumo com pontuação, acertos, tempo
  - Assertions: Dados corretos, layout responsivo, badges corretos

- **Cálculo de progresso**
  - Input: 35 acertos de 50 questões
  - Expected: Progress bar em 70%
  - Assertions: Progress bar correta, porcentagem exata

- **Exibição de badges**
  - Input: Resultados com diferentes tipos de resposta
  - Expected: Badges coloridos corretos
  - Assertions: Cores corretas, textos corretos

#### Casos de Erro
- **Resultados vazios**
  - Input: Resultados sem dados
  - Expected: Mensagem de erro ou estado vazio
  - Assertions: Erro exibido, fallback adequado

- **Dados corrompidos**
  - Input: Resultados com campos inválidos
  - Expected: Tratamento de erro
  - Assertions: Erro tratado, dados sanitizados

### **Results Table Tests**

#### Casos Felizes
- **Exibição de tabela completa**
  - Input: Lista de resultados de questões
  - Expected: Tabela com todas as colunas
  - Assertions: Dados corretos, formatação adequada

- **Ordenação por coluna**
  - Input: Clique em cabeçalho de coluna
  - Expected: Dados ordenados corretamente
  - Assertions: Ordenação ascendente/descendente, ícones corretos

- **Filtro por status**
  - Input: Seleção de filtro (corretas/incorretas)
  - Expected: Tabela filtrada
  - Assertions: Apenas resultados filtrados exibidos

- **Paginação**
  - Input: Muitos resultados
  - Expected: Paginação funcional
  - Assertions: Navegação entre páginas, contadores corretos

#### Casos de Erro
- **Tabela vazia**
  - Input: Sem resultados
  - Expected: Mensagem de tabela vazia
  - Assertions: Mensagem exibida, estado adequado

- **Erro de carregamento**
  - Input: Falha na API
  - Expected: Erro de carregamento
  - Assertions: Erro exibido, retry disponível

### **Performance Chart Tests**

#### Casos Felizes
- **Gráfico de pizza por tópico**
  - Input: Dados de performance por tópico
  - Expected: Gráfico de pizza renderizado
  - Assertions: Dados corretos, cores adequadas, tooltips funcionais

- **Gráfico de barras por dificuldade**
  - Input: Dados de performance por dificuldade
  - Expected: Gráfico de barras renderizado
  - Assertions: Barras corretas, legendas adequadas

- **Responsividade dos gráficos**
  - Input: Diferentes tamanhos de tela
  - Expected: Gráficos responsivos
  - Assertions: Redimensionamento correto, legibilidade mantida

#### Casos de Erro
- **Dados insuficientes**
  - Input: Poucos dados para gráfico
  - Expected: Mensagem ou gráfico simplificado
  - Assertions: Fallback adequado, UX mantida

- **Erro de renderização**
  - Input: Dados malformados
  - Expected: Erro tratado
  - Assertions: Erro exibido, gráfico não quebrado

### **Export Tests**

#### Casos Felizes
- **Exportação Markdown**
  - Input: Resultados válidos + opções de export
  - Expected: Arquivo Markdown gerado
  - Assertions: Formato correto, conteúdo completo

- **Exportação PDF**
  - Input: Resultados + opções PDF
  - Expected: PDF gerado
  - Assertions: PDF válido, layout correto

- **Exportação JSON**
  - Input: Resultados + opções JSON
  - Expected: JSON válido
  - Assertions: Estrutura correta, dados completos

- **Download automático**
  - Input: Exportação bem-sucedida
  - Expected: Download iniciado
  - Assertions: Arquivo baixado, nome correto

#### Casos de Erro
- **Falha na exportação**
  - Input: Erro na API de export
  - Expected: Erro exibido
  - Assertions: Mensagem clara, retry disponível

- **Timeout na exportação**
  - Input: Exportação demora muito
  - Expected: Timeout tratado
  - Assertions: Timeout exibido, cancelamento disponível

### **Analytics Tests**

#### Casos Felizes
- **Análise de performance**
  - Input: Dados de simulado
  - Expected: Análise completa gerada
  - Assertions: Métricas corretas, insights relevantes

- **Identificação de pontos fracos**
  - Input: Resultados com erros
  - Expected: Pontos fracos identificados
  - Assertions: Identificação correta, recomendações adequadas

- **Geração de recomendações**
  - Input: Análise de performance
  - Expected: Recomendações personalizadas
  - Assertions: Recomendações relevantes, priorização correta

#### Casos de Erro
- **Análise falha**
  - Input: Dados insuficientes
  - Expected: Análise parcial ou erro
  - Assertions: Fallback adequado, dados disponíveis

- **Recomendações vazias**
  - Input: Performance perfeita
  - Expected: Mensagem de parabéns
  - Assertions: Mensagem positiva, sugestões gerais

## 2. Estratégias de Mocks

### **Results Service Mocks**

#### Get Results Mock
```javascript
// __mocks__/services/results-service.js
export const mockGetResults = jest.fn().mockResolvedValue({
  id: 'result_123456',
  simuladoId: 'sim_789012',
  userId: 'user_345678',
  totalQuestions: 50,
  correctAnswers: 35,
  wrongAnswers: 12,
  unansweredQuestions: 3,
  score: 70.0,
  timeSpent: 7200,
  averageTimePerQuestion: 144.0,
  submittedAt: '2024-01-15T12:30:00Z',
  completedAt: '2024-01-15T12:35:00Z',
  results: [
    {
      questionId: 'q1',
      question: 'Qual é a capital do Brasil?',
      selectedAnswer: 'C',
      correctAnswer: 'C',
      isCorrect: true,
      timeSpent: 30,
      topic: 'conhecimentos gerais',
      difficulty: 'easy',
      order: 1,
      explanation: 'Brasília é a capital do Brasil desde 1960'
    }
  ],
  performance: {
    overallScore: 70.0,
    scoreByTopic: [
      {
        topic: 'matemática',
        totalQuestions: 15,
        correctAnswers: 12,
        score: 80.0,
        averageTime: 120.0,
        accuracy: 0.8
      }
    ],
    scoreByDifficulty: [
      {
        difficulty: 'easy',
        totalQuestions: 20,
        correctAnswers: 18,
        score: 90.0,
        averageTime: 60.0,
        accuracy: 0.9
      }
    ],
    timeAnalysis: {
      totalTime: 7200,
      averageTimePerQuestion: 144.0,
      fastestQuestion: 15,
      slowestQuestion: 300,
      timeDistribution: [
        {
          range: '0-30s',
          count: 5,
          percentage: 10.0
        }
      ],
      timeEfficiency: 75.0
    },
    accuracyRate: 0.7,
    completionRate: 0.94,
    improvementAreas: ['matemática', 'física'],
    strengths: ['português', 'história']
  },
  weakPoints: [
    {
      topic: 'matemática',
      difficulty: 'hard',
      accuracy: 0.4,
      averageTime: 200.0,
      questions: [],
      recommendations: ['Estudar álgebra', 'Praticar geometria']
    }
  ],
  recommendations: [
    {
      type: 'study',
      priority: 'high',
      title: 'Focar em matemática',
      description: 'Sua performance em matemática está abaixo da média',
      actionItems: ['Revisar álgebra', 'Praticar exercícios'],
      resources: ['Livro de matemática', 'Vídeo aulas']
    }
  ]
})

export const mockGetResultsError = jest.fn().mockRejectedValue({
  message: 'Resultados não encontrados',
  code: 'RESULTS_NOT_FOUND'
})
```

#### Analyze Results Mock
```javascript
export const mockAnalyzeResults = jest.fn().mockResolvedValue({
  overallScore: 70.0,
  scoreByTopic: [
    {
      topic: 'matemática',
      totalQuestions: 15,
      correctAnswers: 12,
      score: 80.0,
      averageTime: 120.0,
      accuracy: 0.8
    }
  ],
  scoreByDifficulty: [
    {
      difficulty: 'easy',
      totalQuestions: 20,
      correctAnswers: 18,
      score: 90.0,
      averageTime: 60.0,
      accuracy: 0.9
    }
  ],
  timeAnalysis: {
    totalTime: 7200,
    averageTimePerQuestion: 144.0,
    fastestQuestion: 15,
    slowestQuestion: 300,
    timeDistribution: [
      {
        range: '0-30s',
        count: 5,
        percentage: 10.0
      }
    ],
    timeEfficiency: 75.0
  },
  accuracyRate: 0.7,
  completionRate: 0.94,
  improvementAreas: ['matemática', 'física'],
  strengths: ['português', 'história']
})

export const mockAnalyzeResultsError = jest.fn().mockRejectedValue({
  message: 'Erro na análise de resultados',
  code: 'ANALYSIS_ERROR'
})
```

### **Export Service Mocks**

```javascript
// __mocks__/services/export-service.js
export const mockExportResults = jest.fn().mockResolvedValue({
  success: true,
  data: '# Relatório de Resultados\n\n## Resumo\n\n- **Pontuação**: 70/100\n- **Acertos**: 35/50\n- **Tempo**: 2h 00min\n\n## Análise por Tópico\n\n| Tópico | Acertos | Total | % |\n|--------|---------|-------|---|\n| Matemática | 12 | 15 | 80% |\n| Português | 18 | 20 | 90% |\n\n## Recomendações\n\n1. Focar em matemática\n2. Praticar exercícios\n\n## Pontos Fracos\n\n- Álgebra básica\n- Geometria plana',
  filename: 'relatorio_simulado_20240115.md',
  size: 1024
})

export const mockExportResultsError = jest.fn().mockRejectedValue({
  message: 'Erro na exportação',
  code: 'EXPORT_ERROR'
})
```

### **Chart Library Mocks**

```javascript
// __mocks__/recharts.js
export const ResponsiveContainer = ({ children }) => children
export const PieChart = ({ children }) => <div data-testid="pie-chart">{children}</div>
export const Pie = ({ children }) => <div data-testid="pie">{children}</div>
export const Cell = ({ children }) => <div data-testid="cell">{children}</div>
export const BarChart = ({ children }) => <div data-testid="bar-chart">{children}</div>
export const Bar = ({ children }) => <div data-testid="bar">{children}</div>
export const XAxis = () => <div data-testid="x-axis" />
export const YAxis = () => <div data-testid="y-axis" />
export const CartesianGrid = () => <div data-testid="cartesian-grid" />
export const Tooltip = () => <div data-testid="tooltip" />
export const Legend = () => <div data-testid="legend" />
```

### **File Download Mocks**

```javascript
// __mocks__/utils/download.js
export const mockDownloadFile = jest.fn().mockImplementation((data, filename) => {
  // Simula download de arquivo
  const blob = new Blob([data], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
})
```

## 3. Timeouts e Re-tentativas

### **API Timeouts**
- **Carregamento de resultados**: 10 segundos
- **Análise de performance**: 15 segundos
- **Exportação de relatório**: 30 segundos
- **Geração de gráficos**: 5 segundos
- **Retry strategy**: 3 tentativas com backoff exponencial

### **Component Timeouts**
- **Loading states**: 10 segundos máximo
- **Chart rendering**: 5 segundos
- **Export processing**: 30 segundos
- **Auto-refresh**: 60 segundos para dados estáticos

### **User Interaction Timeouts**
- **Export download**: 2 segundos
- **Chart interaction**: 500ms debounce
- **Table sorting**: 300ms debounce
- **Filter application**: 500ms debounce

## 4. Critérios de Cobertura por Arquivo

### **src/components/results/results-summary.tsx**
- **Cobertura mínima**: 95%
- **Casos críticos**: Cálculos, exibição, loading states
- **Testes**: Cálculos corretos, layout responsivo, estados de loading

### **src/components/results/results-table.tsx**
- **Cobertura mínima**: 90%
- **Casos críticos**: Ordenação, filtros, paginação
- **Testes**: Ordenação funcional, filtros corretos, paginação

### **src/components/results/performance-chart.tsx**
- **Cobertura mínima**: 85%
- **Casos críticos**: Renderização, responsividade, dados
- **Testes**: Gráficos renderizados, dados corretos, responsividade

### **src/hooks/use-results.ts**
- **Cobertura mínima**: 95%
- **Casos críticos**: Carregamento, análise, error handling
- **Testes**: Carregamento correto, análise funcional, tratamento de erros

### **src/hooks/use-export.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Exportação, download, error handling
- **Testes**: Exportação funcional, download correto, tratamento de erros

### **src/services/results-service.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Todas as operações, error handling
- **Testes**: Operações corretas, tratamento de erros

### **src/services/export-service.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Exportação, formatação, error handling
- **Testes**: Exportação funcional, formatação correta, tratamento de erros

### **src/utils/calculations.ts**
- **Cobertura mínima**: 95%
- **Casos críticos**: Cálculos de performance, análise de tempo
- **Testes**: Cálculos corretos, edge cases, validações

### **src/utils/formatters.ts**
- **Cobertura mínima**: 90%
- **Casos críticos**: Formatação de dados, exportação
- **Testes**: Formatação correta, exportação funcional

## 5. Plano de Testes Exploratórios

### **Sessão 1: Visualização de Resultados (2h)**
- **Objetivo**: Verificar exibição completa de resultados
- **Cenários**:
  - Resumo de resultados
  - Tabela detalhada
  - Gráficos de performance
  - Análise de tempo

### **Sessão 2: Interatividade (1h)**
- **Objetivo**: Verificar funcionalidades interativas
- **Cenários**:
  - Ordenação de tabela
  - Filtros de resultados
  - Interação com gráficos
  - Navegação entre seções

### **Sessão 3: Exportação (1h)**
- **Objetivo**: Verificar funcionalidades de exportação
- **Cenários**:
  - Exportação Markdown
  - Exportação PDF
  - Exportação JSON
  - Download de arquivos

### **Sessão 4: Responsividade (1h)**
- **Objetivo**: Verificar responsividade
- **Cenários**:
  - Mobile layout
  - Tablet layout
  - Desktop layout
  - Print styles

### **Sessão 5: Performance (1h)**
- **Objetivo**: Verificar performance
- **Cenários**:
  - Carregamento de dados
  - Renderização de gráficos
  - Exportação de arquivos
  - Navegação

### **Sessão 6: Error Handling (1h)**
- **Objetivo**: Verificar tratamento de erros
- **Cenários**:
  - Falhas de API
  - Dados corrompidos
  - Timeouts
  - Estados de fallback

## 6. Testes de Integração

### **Fluxo Completo de Resultados**
- **Setup**: Simulado concluído
- **Steps**: Carregamento → Análise → Exibição → Exportação
- **Assertions**: Fluxo completo, dados corretos, exportação funcional

### **Análise de Performance**
- **Setup**: Resultados carregados
- **Steps**: Análise → Identificação de pontos fracos → Recomendações
- **Assertions**: Análise correta, pontos fracos identificados, recomendações relevantes

### **Exportação de Relatório**
- **Setup**: Resultados e análise completos
- **Steps**: Seleção de formato → Geração → Download
- **Assertions**: Formato correto, conteúdo completo, download funcional

### **Interação com Gráficos**
- **Setup**: Gráficos renderizados
- **Steps**: Hover → Tooltip → Zoom → Filtro
- **Assertions**: Interações funcionais, dados corretos, UX adequada

## 7. Testes de Performance

### **Métricas de Carregamento**
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3.5s
- **Cumulative Layout Shift**: < 0.1

### **Testes de Carga**
- **Resultados simultâneos**: 100
- **Exportações por minuto**: 50
- **Tempo de resposta**: < 2s
- **Taxa de erro**: < 1%

### **Testes de Memória**
- **Uso de memória**: < 100MB
- **Vazamentos de memória**: 0
- **Garbage collection**: Eficiente
- **Performance**: Estável

## 8. Testes de Segurança

### **Validação de Dados**
- **Sanitização**: Dados sanitizados
- **Validação**: Validação rigorosa
- **XSS**: Proteção contra XSS
- **CSRF**: Tokens CSRF

### **Exportação Segura**
- **Validação de formato**: Formatos válidos
- **Tamanho de arquivo**: Limites adequados
- **Conteúdo**: Conteúdo seguro
- **Download**: Download seguro

### **Autorização**
- **Autenticação**: Usuário autenticado
- **Autorização**: Permissões adequadas
- **Rate limiting**: Limitação de requisições
- **Session management**: Gerenciamento de sessão

---

**Este documento define especificações completas de teste para o relatório pós-simulado WEB-004, incluindo casos felizes, erros, mocks, timeouts, cobertura e plano de testes exploratórios.**
