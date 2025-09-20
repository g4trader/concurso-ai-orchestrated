# TEST_SPEC_IA-3: Especificações de Teste - Avaliação Offline

## 1. Casos Felizes e de Erro

### **Topic Hit Rate Service Tests**

#### Casos Felizes
- **Cálculo de hit rate bem-sucedido**
  - Input: Simulados gerados + dataset held-out
  - Expected: Hit rate calculado corretamente
  - Assertions: Score entre 0-1, breakdown por tópico

- **Hit rate alto**
  - Input: Simulados com tópicos bem alinhados
  - Expected: Hit rate > 0.8
  - Assertions: Score alto, poucos misses

- **Hit rate médio**
  - Input: Simulados com alinhamento parcial
  - Expected: Hit rate entre 0.5-0.8
  - Assertions: Score médio, alguns misses

- **Breakdown por tópico**
  - Input: Múltiplos tópicos
  - Expected: Breakdown detalhado por tópico
  - Assertions: Cada tópico tem score individual

#### Casos de Erro
- **Dataset vazio**
  - Input: Dataset held-out vazio
  - Expected: ValueError
  - Assertions: Erro específico, mensagem clara

- **Simulados vazios**
  - Input: Lista vazia de simulados
  - Expected: ValueError
  - Assertions: Erro específico, validação de entrada

- **Tópicos não encontrados**
  - Input: Tópicos inexistentes no dataset
  - Expected: Warning + fallback
  - Assertions: Warning registrado, fallback executado

- **Classificação falha**
  - Input: Dados malformados para classificação
  - Expected: ClassificationError
  - Assertions: Erro de classificação, fallback tentado

### **Style Match Service Tests**

#### Casos Felizes
- **Análise de estilo bem-sucedida**
  - Input: Simulados + dataset de referência
  - Expected: Style match calculado
  - Assertions: Score entre 0-1, breakdown por aspecto

- **Estilo consistente**
  - Input: Simulados com estilo consistente
  - Expected: Style match > 0.8
  - Assertions: Score alto, consistência verificada

- **Estilo variado**
  - Input: Simulados com estilo variado
  - Expected: Style match entre 0.3-0.7
  - Assertions: Score médio, variação detectada

- **Análise por aspecto**
  - Input: Múltiplos aspectos de estilo
  - Expected: Breakdown por aspecto
  - Assertions: Cada aspecto tem score individual

#### Casos de Erro
- **Referência de estilo ausente**
  - Input: Sem dataset de referência
  - Expected: ReferenceError
  - Assertions: Erro específico, referência necessária

- **Análise de estilo falha**
  - Input: Dados inadequados para análise
  - Expected: AnalysisError
  - Assertions: Erro de análise, fallback tentado

- **Aspectos não configurados**
  - Input: Aspectos de estilo não definidos
  - Expected: ConfigurationError
  - Assertions: Erro de configuração, aspectos padrão

- **Timeout de análise**
  - Input: Análise muito complexa
  - Expected: TimeoutError
  - Assertions: Timeout respeitado, análise cancelada

### **Answerability Service Tests**

#### Casos Felizes
- **Verificação de answerability bem-sucedida**
  - Input: Questões + critérios de resposta
  - Expected: Answerability calculada
  - Assertions: Score entre 0-1, breakdown por critério

- **Questões bem formuladas**
  - Input: Questões claras e respondíveis
  - Expected: Answerability > 0.9
  - Assertions: Score alto, questões válidas

- **Questões problemáticas**
  - Input: Questões mal formuladas
  - Expected: Answerability < 0.5
  - Assertions: Score baixo, problemas detectados

- **Verificação por critério**
  - Input: Múltiplos critérios
  - Expected: Breakdown por critério
  - Assertions: Cada critério tem score individual

#### Casos de Erro
- **Critérios não definidos**
  - Input: Sem critérios de answerability
  - Expected: CriteriaError
  - Assertions: Erro específico, critérios necessários

- **Verificação falha**
  - Input: Dados inadequados para verificação
  - Expected: VerificationError
  - Assertions: Erro de verificação, fallback tentado

- **Questões malformadas**
  - Input: Questões com estrutura inválida
  - Expected: ValidationError
  - Assertions: Erro de validação, estrutura verificada

- **Timeout de verificação**
  - Input: Verificação muito complexa
  - Expected: TimeoutError
  - Assertions: Timeout respeitado, verificação cancelada

### **Metrics Aggregator Service Tests**

#### Casos Felizes
- **Agregação bem-sucedida**
  - Input: Múltiplas métricas
  - Expected: Métricas agregadas
  - Assertions: Score geral calculado, pesos aplicados

- **Agregação ponderada**
  - Input: Métricas + pesos configurados
  - Expected: Agregação ponderada
  - Assertions: Pesos respeitados, score ponderado

- **Agregação simples**
  - Input: Métricas sem pesos
  - Expected: Média simples
  - Assertions: Média calculada, pesos iguais

- **Múltiplas agregações**
  - Input: Diferentes métodos de agregação
  - Expected: Agregações múltiplas
  - Assertions: Cada método aplicado, resultados consistentes

#### Casos de Erro
- **Métricas vazias**
  - Input: Lista vazia de métricas
  - Expected: ValueError
  - Assertions: Erro específico, métricas necessárias

- **Pesos inválidos**
  - Input: Pesos que não somam 1.0
  - Expected: WeightError
  - Assertions: Erro de pesos, normalização tentada

- **Métricas incompatíveis**
  - Input: Métricas com escalas diferentes
  - Expected: CompatibilityError
  - Assertions: Erro de compatibilidade, normalização tentada

- **Agregação falha**
  - Input: Dados inadequados para agregação
  - Expected: AggregationError
  - Assertions: Erro de agregação, fallback tentado

### **Gap Analysis Service Tests**

#### Casos Felizes
- **Análise de gaps bem-sucedida**
  - Input: Métricas + thresholds
  - Expected: Gaps identificados
  - Assertions: Gaps classificados, recomendações geradas

- **Gaps críticos identificados**
  - Input: Métricas abaixo dos thresholds
  - Expected: Gaps críticos detectados
  - Assertions: Gaps críticos, impacto alto

- **Gaps moderados identificados**
  - Input: Métricas próximas aos thresholds
  - Expected: Gaps moderados detectados
  - Assertions: Gaps moderados, impacto médio

- **Análise por categoria**
  - Input: Múltiplas categorias de gaps
  - Expected: Gaps por categoria
  - Assertions: Cada categoria analisada, gaps específicos

#### Casos de Erro
- **Thresholds não definidos**
  - Input: Sem thresholds configurados
  - Expected: ThresholdError
  - Assertions: Erro específico, thresholds necessários

- **Métricas insuficientes**
  - Input: Poucas métricas para análise
  - Expected: InsufficientDataError
  - Assertions: Erro de dados insuficientes, análise cancelada

- **Análise falha**
  - Input: Dados inadequados para análise
  - Expected: AnalysisError
  - Assertions: Erro de análise, fallback tentado

- **Timeout de análise**
  - Input: Análise muito complexa
  - Expected: TimeoutError
  - Assertions: Timeout respeitado, análise cancelada

### **Report Generator Service Tests**

#### Casos Felizes
- **Geração de relatório bem-sucedida**
  - Input: Resultados de avaliação
  - Expected: Relatório gerado
  - Assertions: Relatório completo, formato correto

- **Relatório Markdown**
  - Input: Configuração Markdown
  - Expected: Relatório em Markdown
  - Assertions: Formato Markdown, estrutura correta

- **Relatório com gráficos**
  - Input: Configuração com gráficos
  - Expected: Relatório com gráficos
  - Assertions: Gráficos incluídos, visualização correta

- **Relatório completo**
  - Input: Todos os componentes
  - Expected: Relatório completo
  - Assertions: Todas as seções incluídas, conteúdo completo

#### Casos de Erro
- **Resultados vazios**
  - Input: Sem resultados de avaliação
  - Expected: EmptyResultsError
  - Assertions: Erro específico, resultados necessários

- **Template não encontrado**
  - Input: Template inexistente
  - Expected: TemplateError
  - Assertions: Erro de template, template padrão usado

- **Geração falha**
  - Input: Dados inadequados para geração
  - Expected: GenerationError
  - Assertions: Erro de geração, fallback tentado

- **Timeout de geração**
  - Input: Geração muito complexa
  - Expected: TimeoutError
  - Assertions: Timeout respeitado, geração cancelada

### **Benchmark Service Tests**

#### Casos Felizes
- **Benchmark bem-sucedido**
  - Input: Múltiplas avaliações
  - Expected: Benchmark executado
  - Assertions: Score geral calculado, tendências identificadas

- **Benchmark comparativo**
  - Input: Avaliações de diferentes períodos
  - Expected: Comparação temporal
  - Assertions: Tendências calculadas, evolução identificada

- **Benchmark agregado**
  - Input: Múltiplas métricas
  - Expected: Agregação de métricas
  - Assertions: Métricas agregadas, scores consistentes

- **Benchmark com baseline**
  - Input: Avaliações + baseline
  - Expected: Comparação com baseline
  - Assertions: Baseline respeitado, comparação válida

#### Casos de Erro
- **Avaliações insuficientes**
  - Input: Poucas avaliações para benchmark
  - Expected: InsufficientDataError
  - Assertions: Erro de dados insuficientes, benchmark cancelado

- **Baseline inválido**
  - Input: Baseline malformado
  - Expected: BaselineError
  - Assertions: Erro de baseline, baseline padrão usado

- **Benchmark falha**
  - Input: Dados inadequados para benchmark
  - Expected: BenchmarkError
  - Assertions: Erro de benchmark, fallback tentado

- **Timeout de benchmark**
  - Input: Benchmark muito complexo
  - Expected: TimeoutError
  - Assertions: Timeout respeitado, benchmark cancelado

## 2. Estratégias de Mocks

### **Rede/IO Mocks**

#### Topic Hit Rate Service
```python
@pytest.fixture
def mock_topic_classifier():
    with patch('src.services.topic_hit_rate_service.TopicClassifier') as mock_classifier:
        mock_classifier.return_value.classify.return_value = {
            "topic": "Direito Constitucional",
            "confidence": 0.95,
            "category": "legal"
        }
        yield mock_classifier

@pytest.fixture
def mock_dataset_loader():
    with patch('src.services.topic_hit_rate_service.DatasetLoader') as mock_loader:
        mock_loader.return_value.load_held_out.return_value = {
            "banca": "CESPE",
            "ano": 2023,
            "questoes": [
                {
                    "questao_id": "real_001",
                    "topico": "Direito Constitucional",
                    "pergunta": "Sobre os princípios fundamentais..."
                }
            ]
        }
        yield mock_loader
```

#### Style Match Service
```python
@pytest.fixture
def mock_style_analyzer():
    with patch('src.services.style_match_service.StyleAnalyzer') as mock_analyzer:
        mock_analyzer.return_value.analyze.return_value = {
            "linguagem_formal": 0.85,
            "estrutura_questao": 0.90,
            "nivel_dificuldade": 0.75,
            "overall_score": 0.83
        }
        yield mock_analyzer

@pytest.fixture
def mock_style_reference():
    with patch('src.services.style_match_service.StyleReference') as mock_reference:
        mock_reference.return_value.get_patterns.return_value = {
            "CESPE": {
                "linguagem_formal": 0.9,
                "estrutura_questao": 0.85,
                "nivel_dificuldade": 0.8
            }
        }
        yield mock_reference
```

#### Answerability Service
```python
@pytest.fixture
def mock_answerability_checker():
    with patch('src.services.answerability_service.AnswerabilityChecker') as mock_checker:
        mock_checker.return_value.check.return_value = {
            "clareza_pergunta": 0.95,
            "alternativas_validas": 0.90,
            "justificativa_coerente": 0.88,
            "overall_score": 0.91
        }
        yield mock_checker

@pytest.fixture
def mock_criteria_validator():
    with patch('src.services.answerability_service.CriteriaValidator') as mock_validator:
        mock_validator.return_value.validate.return_value = {
            "is_valid": True,
            "criteria_met": ["clareza", "alternativas", "justificativa"],
            "score": 0.91
        }
        yield mock_validator
```

#### Metrics Aggregator Service
```python
@pytest.fixture
def mock_metrics_aggregator():
    with patch('src.services.metrics_aggregator_service.MetricsAggregator') as mock_aggregator:
        mock_aggregator.return_value.aggregate.return_value = {
            "overall_score": 0.84,
            "weighted_scores": {
                "topic_hit_rate": 0.85,
                "style_match": 0.75,
                "answerability": 0.92
            },
            "aggregation_method": "weighted_average"
        }
        yield mock_aggregator
```

#### Gap Analysis Service
```python
@pytest.fixture
def mock_gap_analyzer():
    with patch('src.services.gap_analysis_service.GapAnalyzer') as mock_analyzer:
        mock_analyzer.return_value.analyze.return_value = {
            "critical_gaps": [
                {
                    "gap_type": "topic_coverage",
                    "description": "Baixa cobertura em Direito Tributário",
                    "impact": "high",
                    "recommendation": "Aumentar contextos de Direito Tributário"
                }
            ],
            "moderate_gaps": [
                {
                    "gap_type": "style_consistency",
                    "description": "Inconsistência no nível de formalidade",
                    "impact": "medium",
                    "recommendation": "Refinar prompts de estilo"
                }
            ]
        }
        yield mock_analyzer
```

#### Report Generator Service
```python
@pytest.fixture
def mock_report_generator():
    with patch('src.services.report_generator_service.ReportGenerator') as mock_generator:
        mock_generator.return_value.generate.return_value = {
            "report_id": "report_123456",
            "status": "generated",
            "report_path": "/reports/evaluation_report_2024-01-15.md",
            "sections": ["executive_summary", "metrics_analysis", "gap_analysis", "recommendations"]
        }
        yield mock_generator
```

#### Benchmark Service
```python
@pytest.fixture
def mock_benchmark_runner():
    with patch('src.services.benchmark_service.BenchmarkRunner') as mock_runner:
        mock_runner.return_value.run.return_value = {
            "benchmark_id": "bench_123456",
            "status": "completed",
            "overall_score": 0.84,
            "performance_trends": {
                "improvement_rate": 0.05,
                "consistency_score": 0.88,
                "reliability_score": 0.90
            }
        }
        yield mock_runner
```

### **File System Mocks**

```python
@pytest.fixture
def mock_file_system():
    with patch('os.path.exists') as mock_exists, \
         patch('builtins.open', mock_open(read_data="test data")):
        mock_exists.return_value = True
        yield
```

### **Cache Mocks**

```python
@pytest.fixture
def mock_cache():
    with patch('redis.Redis') as mock_redis:
        mock_redis.return_value.get.return_value = None
        mock_redis.return_value.set.return_value = True
        yield mock_redis
```

## 3. Timeouts e Re-tentativas

### **Topic Hit Rate Service**
- **Classificação timeout**: 10 segundos
- **Cálculo timeout**: 5 segundos
- **Retry strategy**: 2 tentativas com backoff exponencial
- **Fallback**: Classificação genérica se específica falhar

### **Style Match Service**
- **Análise timeout**: 15 segundos
- **Comparação timeout**: 8 segundos
- **Retry strategy**: 2 tentativas com backoff exponencial
- **Fallback**: Análise básica se completa falhar

### **Answerability Service**
- **Verificação timeout**: 10 segundos
- **Validação timeout**: 5 segundos
- **Retry strategy**: 2 tentativas com backoff exponencial
- **Fallback**: Verificação básica se completa falhar

### **Metrics Aggregator Service**
- **Agregação timeout**: 5 segundos
- **Retry strategy**: 1 tentativa
- **Fallback**: Agregação simples se ponderada falhar

### **Gap Analysis Service**
- **Análise timeout**: 20 segundos
- **Retry strategy**: 1 tentativa
- **Fallback**: Análise básica se completa falhar

### **Report Generator Service**
- **Geração timeout**: 30 segundos
- **Retry strategy**: 1 tentativa
- **Fallback**: Relatório básico se completo falhar

### **Benchmark Service**
- **Benchmark timeout**: 60 segundos
- **Retry strategy**: 1 tentativa
- **Fallback**: Benchmark básico se completo falhar

## 4. Critérios de Cobertura por Arquivo

### **src/main.py**
- **Cobertura mínima**: 80%
- **Casos críticos**: Inicialização da app, configuração CORS
- **Testes**: Health check, configuração de rotas

### **src/config/settings.py**
- **Cobertura mínima**: 90%
- **Casos críticos**: Todas as configurações, validações
- **Testes**: Valores padrão, variáveis de ambiente

### **src/services/topic_hit_rate_service.py**
- **Cobertura mínima**: 85%
- **Casos críticos**: Classificação, cálculo, breakdown
- **Testes**: Hit rate alto/médio/baixo, erros, fallbacks

### **src/services/style_match_service.py**
- **Cobertura mínima**: 85%
- **Casos críticos**: Análise, comparação, breakdown
- **Testes**: Estilo consistente/variado, erros, fallbacks

### **src/services/answerability_service.py**
- **Cobertura mínima**: 85%
- **Casos críticos**: Verificação, validação, breakdown
- **Testes**: Questões válidas/inválidas, erros, fallbacks

### **src/services/metrics_aggregator_service.py**
- **Cobertura mínima**: 90%
- **Casos críticos**: Agregação, pesos, métodos
- **Testes**: Agregação ponderada/simples, erros, fallbacks

### **src/services/gap_analysis_service.py**
- **Cobertura mínima**: 80%
- **Casos críticos**: Análise, classificação, recomendações
- **Testes**: Gaps críticos/moderados, erros, fallbacks

### **src/services/report_generator_service.py**
- **Cobertura mínima**: 80%
- **Casos críticos**: Geração, templates, formatação
- **Testes**: Relatórios completos/básicos, erros, fallbacks

### **src/services/benchmark_service.py**
- **Cobertura mínima**: 85%
- **Casos críticos**: Benchmark, comparação, tendências
- **Testes**: Benchmarks completos/básicos, erros, fallbacks

### **src/api/routes.py**
- **Cobertura mínima**: 80%
- **Casos críticos**: Todos os endpoints, validações, erros
- **Testes**: Avaliação, benchmark, relatório, health, métricas

### **src/models/request.py**
- **Cobertura mínima**: 90%
- **Casos críticos**: Validações Pydantic, enums
- **Testes**: Validações, tipos, campos obrigatórios

### **src/models/response.py**
- **Cobertura mínima**: 90%
- **Casos críticos**: Serialização, tipos de dados
- **Testes**: Serialização, validações

### **src/evaluators/topic_evaluator.py**
- **Cobertura mínima**: 85%
- **Casos críticos**: Classificação, cálculo, validação
- **Testes**: Tópicos válidos/inválidos, erros, fallbacks

### **src/evaluators/style_evaluator.py**
- **Cobertura mínima**: 85%
- **Casos críticos**: Análise, comparação, validação
- **Testes**: Estilos válidos/inválidos, erros, fallbacks

### **src/evaluators/answerability_evaluator.py**
- **Cobertura mínima**: 85%
- **Casos críticos**: Verificação, validação, critérios
- **Testes**: Questões válidas/inválidas, erros, fallbacks

## 5. Testes de Integração

### **Pipeline Completo**
- **Avaliação → Métricas → Análise → Relatório**
- **Benchmark → Comparação → Tendências → Performance**
- **Health Check → All Services**
- **Metrics → Performance Data**

### **Testes de Performance**
- **Avaliação de 100 simulados**
- **Benchmark de 50 avaliações**
- **Geração de relatório completo**
- **Concurrent requests (5 users)**

### **Testes de Resilência**
- **Service failures**
- **Network timeouts**
- **Memory pressure**
- **Cache failures**

## 6. Testes de Segurança

### **Input Validation**
- **Evaluation request security**
- **SQL injection prevention**
- **Path traversal prevention**
- **XSS prevention**

### **Authentication/Authorization**
- **API key validation**
- **Rate limiting**
- **CORS validation**
- **Input sanitization**

## 7. Testes de Monitoramento

### **Logging**
- **Structured logging**
- **Error tracking**
- **Performance metrics**
- **Audit trail**

### **Health Checks**
- **Service availability**
- **Resource usage**
- **Dependency health**
- **Performance degradation**

---

**Este documento define especificações completas de teste para o sistema de avaliação offline IA-3, incluindo casos felizes, erros, mocks, timeouts e critérios de cobertura.**
