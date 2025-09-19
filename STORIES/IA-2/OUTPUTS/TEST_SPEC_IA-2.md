# TEST_SPEC_IA-2: Especificações de Teste - Geração Condicionada

## 1. Casos Felizes e de Erro

### **Prompt Engineering Service Tests**

#### Casos Felizes
- **Template CESPE válido**
  - Input: Contextos + edital CESPE + tópico
  - Expected: Prompt específico para CESPE gerado
  - Assertions: Prompt contém características CESPE, template correto

- **Template FGV válido**
  - Input: Contextos + edital FGV + tópico
  - Expected: Prompt específico para FGV gerado
  - Assertions: Prompt contém características FGV, template correto

- **Template genérico**
  - Input: Contextos + edital desconhecido + tópico
  - Expected: Prompt genérico gerado
  - Assertions: Prompt genérico, sem características específicas

- **Cache de prompt**
  - Input: Mesmo contexto + edital + tópico
  - Expected: Prompt do cache retornado
  - Assertions: Tempo de resposta reduzido, prompt idêntico

#### Casos de Erro
- **Template não encontrado**
  - Input: Banca inexistente
  - Expected: Template genérico usado
  - Assertions: Fallback para genérico, log de warning

- **Contextos vazios**
  - Input: Lista vazia de contextos
  - Expected: ValueError
  - Assertions: Erro específico, mensagem clara

- **Edital malformado**
  - Input: Edital sem campos obrigatórios
  - Expected: ValidationError
  - Assertions: Validação de campos obrigatórios

- **Cache corrompido**
  - Input: Cache inválido
  - Expected: Cache ignorado, prompt regenerado
  - Assertions: Fallback para geração, cache limpo

### **LLM Generation Service Tests**

#### Casos Felizes
- **Geração bem-sucedida**
  - Input: Prompt válido + contexto
  - Expected: Questão JSON estruturada
  - Assertions: Estrutura correta, campos obrigatórios presentes

- **Geração com timeout**
  - Input: Prompt complexo
  - Expected: Questão gerada dentro do timeout
  - Assertions: Tempo respeitado, questão válida

- **Fallback para modelo menor**
  - Input: Modelo principal indisponível
  - Expected: Modelo menor usado
  - Assertions: Fallback executado, questão gerada

- **Retry bem-sucedido**
  - Input: Falha temporária
  - Expected: Retry executado com sucesso
  - Assertions: Retry funcionando, questão gerada

#### Casos de Erro
- **Modelo não carregado**
  - Input: Modelo inexistente
  - Expected: ModelNotFoundError
  - Assertions: Erro específico, fallback tentado

- **Timeout de geração**
  - Input: Prompt muito complexo
  - Expected: TimeoutError
  - Assertions: Timeout respeitado, erro tratado

- **Resposta malformada**
  - Input: LLM retorna JSON inválido
  - Expected: ParsingError
  - Assertions: Erro de parsing, retry tentado

- **Memória insuficiente**
  - Input: Modelo muito grande
  - Expected: MemoryError
  - Assertions: Erro de memória, fallback para modelo menor

### **Validation Service Tests**

#### Casos Felizes
- **Validação bem-sucedida**
  - Input: Questão válida
  - Expected: Validação aprovada
  - Assertions: Todos os checks passaram, scores adequados

- **Validação com warnings**
  - Input: Questão com problemas menores
  - Expected: Validação aprovada com warnings
  - Assertions: Warnings registrados, validação aprovada

- **Validação configurável**
  - Input: Questão + nível de validação
  - Expected: Validação conforme nível
  - Assertions: Nível respeitado, checks apropriados

#### Casos de Erro
- **Questão inválida**
  - Input: Questão malformada
  - Expected: ValidationError
  - Assertions: Erro específico, detalhes do problema

- **Alternativas inválidas**
  - Input: Alternativas malformadas
  - Expected: ValidationError
  - Assertions: Erro de alternativas, validação falhou

- **Gabarito inválido**
  - Input: Gabarito inexistente
  - Expected: ValidationError
  - Assertions: Erro de gabarito, validação falhou

- **Justificativa vazia**
  - Input: Justificativa vazia
  - Expected: ValidationError
  - Assertions: Erro de justificativa, validação falhou

### **Self-Consistency Service Tests**

#### Casos Felizes
- **Consistência verificada**
  - Input: Questão + justificativa
  - Expected: Consistência confirmada
  - Assertions: Score alto, consistência verificada

- **Verificação 2x**
  - Input: Questão para verificação dupla
  - Expected: Duas verificações executadas
  - Assertions: 2x verificações, resultados consistentes

- **Timeout respeitado**
  - Input: Verificação complexa
  - Expected: Verificação dentro do timeout
  - Assertions: Timeout respeitado, verificação concluída

#### Casos de Erro
- **Inconsistência detectada**
  - Input: Questão + justificativa inconsistente
  - Expected: Inconsistência detectada
  - Assertions: Score baixo, inconsistência identificada

- **Timeout de verificação**
  - Input: Verificação muito complexa
  - Expected: TimeoutError
  - Assertions: Timeout respeitado, erro tratado

- **Fallback para 1x**
  - Input: Verificação 2x falha
  - Expected: Fallback para 1x
  - Assertions: Fallback executado, verificação 1x

### **Anti-Plagiarism Service Tests**

#### Casos Felizes
- **Plágio não detectado**
  - Input: Questão original + contextos
  - Expected: Baixo score de plágio
  - Assertions: Score baixo, plágio não detectado

- **Cache de verificação**
  - Input: Questão já verificada
  - Expected: Resultado do cache
  - Assertions: Cache hit, tempo reduzido

- **Whitelist funcionando**
  - Input: Questão de fonte confiável
  - Expected: Verificação bypassada
  - Assertions: Whitelist respeitada, verificação bypassada

#### Casos de Erro
- **Plágio detectado**
  - Input: Questão copiada + contextos
  - Expected: Alto score de plágio
  - Assertions: Score alto, plágio detectado

- **Timeout de verificação**
  - Input: Verificação complexa
  - Expected: TimeoutError
  - Assertions: Timeout respeitado, erro tratado

- **Cache inválido**
  - Input: Cache corrompido
  - Expected: Cache ignorado, verificação executada
  - Assertions: Fallback para verificação, cache limpo

### **Quality Assessment Service Tests**

#### Casos Felizes
- **Avaliação bem-sucedida**
  - Input: Questão válida
  - Expected: Scores de qualidade
  - Assertions: Scores calculados, métricas válidas

- **Múltiplas métricas**
  - Input: Questão para avaliação completa
  - Expected: Todas as métricas calculadas
  - Assertions: Todas as métricas presentes, scores válidos

- **Cache de avaliação**
  - Input: Questão já avaliada
  - Expected: Resultado do cache
  - Assertions: Cache hit, tempo reduzido

#### Casos de Erro
- **Questão inválida**
  - Input: Questão malformada
  - Expected: ValidationError
  - Assertions: Erro de validação, avaliação falhou

- **Métrica não disponível**
  - Input: Questão + métrica indisponível
  - Expected: Métrica ignorada
  - Assertions: Métrica ignorada, outras calculadas

- **Timeout de avaliação**
  - Input: Avaliação complexa
  - Expected: TimeoutError
  - Assertions: Timeout respeitado, erro tratado

### **Batch Processor Service Tests**

#### Casos Felizes
- **Processamento em lote**
  - Input: Lista de requests
  - Expected: Todas as questões processadas
  - Assertions: Todas processadas, resultados válidos

- **Processamento paralelo**
  - Input: Múltiplas questões
  - Expected: Processamento paralelo
  - Assertions: Paralelismo respeitado, tempo reduzido

- **Filtro de qualidade**
  - Input: Questões com scores variados
  - Expected: Questões filtradas por qualidade
  - Assertions: Filtro aplicado, apenas questões de qualidade

#### Casos de Erro
- **Request inválido**
  - Input: Request malformado
  - Expected: Request ignorado
  - Assertions: Request ignorado, outros processados

- **Timeout de lote**
  - Input: Lote muito grande
  - Expected: TimeoutError
  - Assertions: Timeout respeitado, erro tratado

- **Falha em cascata**
  - Input: Múltiplas falhas
  - Expected: Falhas isoladas
  - Assertions: Falhas não afetam outras, isolamento

## 2. Estratégias de Mocks

### **Rede/IO Mocks**

#### LLM Generation Service
```python
@pytest.fixture
def mock_ollama():
    with patch('ollama.Client') as mock_client:
        mock_response = {
            "model": "llama-3.1-8b",
            "response": '{"question": "Qual é o princípio fundamental?", "alternatives": {"A": "...", "B": "...", "C": "..."}, "correct_answer": "B", "justification": "..."}',
            "done": True
        }
        mock_client.return_value.generate.return_value = mock_response
        yield mock_client

@pytest.fixture
def mock_openai():
    with patch('openai.OpenAI') as mock_client:
        mock_response = {
            "choices": [{
                "message": {
                    "content": '{"question": "Qual é o princípio fundamental?", "alternatives": {"A": "...", "B": "...", "C": "..."}, "correct_answer": "B", "justification": "..."}'
                }
            }]
        }
        mock_client.return_value.chat.completions.create.return_value = mock_response
        yield mock_client
```

#### Validation Service
```python
@pytest.fixture
def mock_validation():
    with patch('src.services.validation_service.ValidationService') as mock_service:
        mock_result = {
            "is_valid": True,
            "scores": {
                "plausibility": 0.95,
                "consistency": 0.92,
                "plagiarism": 0.05,
                "quality": 0.94
            },
            "checks": {
                "uniqueness": {"passed": True, "score": 1.0},
                "consistency": {"passed": True, "score": 0.92},
                "plagiarism": {"passed": True, "score": 0.05},
                "quality": {"passed": True, "score": 0.94}
            }
        }
        mock_service.return_value.validate_question.return_value = mock_result
        yield mock_service
```

#### Self-Consistency Service
```python
@pytest.fixture
def mock_consistency():
    with patch('src.services.self_consistency_service.SelfConsistencyService') as mock_service:
        mock_result = {
            "score": 0.92,
            "consistent": True,
            "checks_performed": 2,
            "details": "Justificativa coerente com resposta"
        }
        mock_service.return_value.check_consistency.return_value = mock_result
        yield mock_service
```

#### Anti-Plagiarism Service
```python
@pytest.fixture
def mock_plagiarism():
    with patch('src.services.anti_plagiarism_service.AntiPlagiarismService') as mock_service:
        mock_result = {
            "score": 0.05,
            "plagiarized": False,
            "similar_chunks": [],
            "details": "Baixo risco de plágio"
        }
        mock_service.return_value.check_plagiarism.return_value = mock_result
        yield mock_service
```

#### Quality Assessment Service
```python
@pytest.fixture
def mock_quality():
    with patch('src.services.quality_assessment_service.QualityAssessmentService') as mock_service:
        mock_result = {
            "plausibility": 0.95,
            "consistency": 0.92,
            "clarity": 0.88,
            "difficulty": 0.75,
            "overall": 0.90
        }
        mock_service.return_value.assess_quality.return_value = mock_result
        yield mock_service
```

### **File System Mocks**

```python
@pytest.fixture
def mock_file_system():
    with patch('os.path.exists') as mock_exists, \
         patch('builtins.open', mock_open(read_data="template content")):
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

### **Prompt Engineering Service**
- **Template loading timeout**: 5 segundos
- **Cache timeout**: 1 segundo
- **Retry strategy**: 2 tentativas com backoff exponencial
- **Fallback**: Template genérico se específico falhar

### **LLM Generation Service**
- **Generation timeout**: 30 segundos
- **Model loading timeout**: 60 segundos
- **Retry strategy**: 3 tentativas com backoff exponencial
- **Fallback**: Modelo menor se principal falhar

### **Validation Service**
- **Validation timeout**: 10 segundos
- **Retry strategy**: 2 tentativas
- **Fallback**: Validação básica se completa falhar

### **Self-Consistency Service**
- **Consistency check timeout**: 10 segundos
- **Retry strategy**: 1 tentativa
- **Fallback**: 1x check se 2x falhar

### **Anti-Plagiarism Service**
- **Plagiarism check timeout**: 5 segundos
- **Retry strategy**: 1 tentativa
- **Fallback**: Bypass se verificação falhar

### **Quality Assessment Service**
- **Assessment timeout**: 5 segundos
- **Retry strategy**: 1 tentativa
- **Fallback**: Métricas básicas se completas falharem

### **Batch Processor Service**
- **Batch timeout**: 300 segundos
- **Per-question timeout**: 30 segundos
- **Retry strategy**: 2 tentativas por questão
- **Fallback**: Questões individuais se lote falhar

## 4. Critérios de Cobertura por Arquivo

### **src/main.py**
- **Cobertura mínima**: 80%
- **Casos críticos**: Inicialização da app, configuração CORS
- **Testes**: Health check, configuração de rotas

### **src/config/settings.py**
- **Cobertura mínima**: 90%
- **Casos críticos**: Todas as configurações, validações
- **Testes**: Valores padrão, variáveis de ambiente

### **src/services/prompt_engineering_service.py**
- **Cobertura mínima**: 85%
- **Casos críticos**: Templates por banca, cache, fallback
- **Testes**: CESPE, FGV, genérico, cache, erros

### **src/services/llm_generation_service.py**
- **Cobertura mínima**: 80%
- **Casos críticos**: Geração, timeout, fallback, retry
- **Testes**: Geração, timeout, fallback, retry, erros

### **src/services/validation_service.py**
- **Cobertura mínima**: 85%
- **Casos críticos**: Validação completa, níveis, erros
- **Testes**: Validação, níveis, erros, warnings

### **src/services/self_consistency_service.py**
- **Cobertura mínima**: 80%
- **Casos críticos**: Verificação 2x, timeout, fallback
- **Testes**: 2x check, timeout, fallback, inconsistência

### **src/services/anti_plagiarism_service.py**
- **Cobertura mínima**: 75%
- **Casos críticos**: Detecção, cache, whitelist
- **Testes**: Detecção, cache, whitelist, timeout

### **src/services/quality_assessment_service.py**
- **Cobertura mínima**: 80%
- **Casos críticos**: Múltiplas métricas, cache, timeout
- **Testes**: Métricas, cache, timeout, erros

### **src/services/batch_processor_service.py**
- **Cobertura mínima**: 85%
- **Casos críticos**: Processamento paralelo, filtros, erros
- **Testes**: Paralelo, filtros, erros, timeout

### **src/api/routes.py**
- **Cobertura mínima**: 80%
- **Casos críticos**: Todos os endpoints, validações, erros
- **Testes**: Geração, lote, validação, health, métricas

### **src/models/request.py**
- **Cobertura mínima**: 90%
- **Casos críticos**: Validações Pydantic, enums
- **Testes**: Validações, tipos, campos obrigatórios

### **src/models/response.py**
- **Cobertura mínima**: 90%
- **Casos críticos**: Serialização, tipos de dados
- **Testes**: Serialização, validações

## 5. Testes de Integração

### **Pipeline Completo**
- **Geração → Validação → Consistência → Plágio → Qualidade**
- **Lote → Processamento Paralelo → Filtros → Resultados**
- **Health Check → All Services**
- **Metrics → Performance Data**

### **Testes de Performance**
- **Geração de 100 questões**
- **Validação de 1000 questões**
- **Processamento em lote (50 questões)**
- **Concurrent requests (10 users)**

### **Testes de Resilência**
- **Service failures**
- **Network timeouts**
- **Memory pressure**
- **Cache failures**

## 6. Testes de Segurança

### **Input Validation**
- **Question generation security**
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

**Este documento define especificações completas de teste para o sistema de geração condicionada IA-2, incluindo casos felizes, erros, mocks, timeouts e critérios de cobertura.**
