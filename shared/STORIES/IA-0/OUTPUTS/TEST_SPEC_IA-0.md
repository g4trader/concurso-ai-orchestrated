# TEST_SPEC_IA-0: Especificações de Teste - Infraestrutura IA

## 1. Visão Geral

Este documento define as especificações de teste para a infraestrutura IA-0, incluindo testes unitários, integração e end-to-end para o serviço de inferência com Ollama.

## 2. Estratégia de Testes

### 2.1 Tipos de Teste
- **Unitários**: Testes isolados de funções e classes
- **Integração**: Testes de comunicação entre componentes
- **End-to-End**: Testes completos do fluxo de geração
- **Performance**: Testes de latência e throughput
- **Resilência**: Testes de falhas e recuperação

### 2.2 Ferramentas
- **pytest**: Framework de testes
- **pytest-asyncio**: Testes assíncronos
- **pytest-httpx**: Mock de requisições HTTP
- **pytest-mock**: Mock de dependências
- **pytest-cov**: Cobertura de código

## 3. Casos de Teste - Casos Felizes

### 3.1 Health Check
```python
def test_health_check_success():
    """Teste de health check com Ollama disponível"""
    # Given: Ollama está rodando
    # When: Chamar /api/v1/health
    # Then: Retornar status "healthy"
    # And: ollama_connected = True
    # And: models_available não vazio
    # And: uptime > 0
```

### 3.2 Listagem de Modelos
```python
def test_list_models_success():
    """Teste de listagem de modelos com sucesso"""
    # Given: Ollama com modelos carregados
    # When: Chamar /api/v1/models
    # Then: Retornar lista de ModelInfo
    # And: Cada modelo tem name, size, modified_at, digest
    # And: Status 200
```

### 3.3 Geração de Questão
```python
def test_generate_question_success():
    """Teste de geração de questão com sucesso"""
    # Given: Prompt válido e modelo disponível
    # When: POST /api/v1/generate
    # Then: Retornar QuestionResponse
    # And: question não vazio
    # And: alternatives com 4 opções
    # And: correct_answer válido
    # And: explanation não vazio
    # And: processing_time > 0
    # And: timestamp atual
```

### 3.4 Geração em Lote
```python
def test_generate_batch_success():
    """Teste de geração em lote com sucesso"""
    # Given: Lista de prompts válidos
    # When: POST /api/v1/generate/batch
    # Then: Retornar lista de resultados
    # And: Cada resultado tem success=True
    # And: data contém QuestionResponse
```

## 4. Casos de Teste - Casos de Erro

### 4.1 Ollama Indisponível
```python
def test_ollama_unavailable():
    """Teste com Ollama indisponível"""
    # Given: Ollama não está rodando
    # When: Chamar qualquer endpoint
    # Then: Retornar status 500
    # And: ErrorResponse com detalhes
    # And: Log de erro registrado
```

### 4.2 Modelo Não Encontrado
```python
def test_model_not_found():
    """Teste com modelo inexistente"""
    # Given: Modelo não disponível
    # When: POST /api/v1/generate com modelo inválido
    # Then: Retornar status 400
    # And: ErrorResponse com "Model not available"
    # And: Lista de modelos disponíveis
```

### 4.3 Prompt Inválido
```python
def test_invalid_prompt():
    """Teste com prompt inválido"""
    # Given: Prompt vazio ou muito longo
    # When: POST /api/v1/generate
    # Then: Retornar status 422
    # And: ValidationError com detalhes
```

### 4.4 Timeout de Requisição
```python
def test_request_timeout():
    """Teste de timeout de requisição"""
    # Given: Ollama com resposta lenta
    # When: POST /api/v1/generate
    # Then: Retornar status 500
    # And: ErrorResponse com "Request timeout"
    # And: Log de timeout
```

## 5. Estratégias de Mock

### 5.1 Mock de Rede/IO
```python
@pytest.fixture
def mock_ollama_response():
    """Mock de resposta do Ollama"""
    return {
        "response": '{"question": "Test question", "alternatives": ["A) A", "B) B", "C) C", "D) D"], "correct_answer": "A", "explanation": "Test explanation"}',
        "done": True,
        "context": [],
        "total_duration": 1200000000,
        "load_duration": 100000000,
        "prompt_eval_count": 10,
        "prompt_eval_duration": 500000000,
        "eval_count": 50,
        "eval_duration": 600000000
    }

@pytest.fixture
def mock_httpx_client():
    """Mock do cliente HTTP"""
    with httpx.Client() as client:
        yield client
```

### 5.2 Mock de Modelo
```python
@pytest.fixture
def mock_ollama_service():
    """Mock do serviço Ollama"""
    service = Mock(spec=OllamaService)
    service.list_models.return_value = [
        ModelInfo(name="qwen2:7b", size="4.1GB", modified_at="2024-01-15", digest="sha256:abc123")
    ]
    service.generate_question.return_value = QuestionResponse(
        question="Test question",
        alternatives=["A) A", "B) B", "C) C", "D) D"],
        correct_answer="A",
        explanation="Test explanation",
        model_used="qwen2:7b",
        processing_time=1.2,
        timestamp=datetime.now()
    )
    return service
```

### 5.3 Mock de Configurações
```python
@pytest.fixture
def mock_settings():
    """Mock das configurações"""
    settings = Mock()
    settings.OLLAMA_HOST = "http://localhost:11434"
    settings.OLLAMA_TIMEOUT = 30
    settings.DEFAULT_MODEL = "qwen2:7b"
    settings.API_HOST = "0.0.0.0"
    settings.API_PORT = 8000
    return settings
```

## 6. Timeouts e Re-tentativas

### 6.1 Configuração de Timeouts
```python
# Configurações de timeout
OLLAMA_TIMEOUT = 30  # segundos
REQUEST_TIMEOUT = 60  # segundos
HEALTH_CHECK_TIMEOUT = 5  # segundos

# Configurações de retry
MAX_RETRIES = 3
RETRY_DELAY = 1  # segundo
BACKOFF_FACTOR = 2
```

### 6.2 Testes de Timeout
```python
def test_ollama_timeout():
    """Teste de timeout do Ollama"""
    # Given: Ollama com resposta lenta (>30s)
    # When: POST /api/v1/generate
    # Then: Timeout após 30s
    # And: Retornar status 500
    # And: ErrorResponse com timeout

def test_retry_mechanism():
    """Teste de mecanismo de retry"""
    # Given: Ollama com falhas intermitentes
    # When: POST /api/v1/generate
    # Then: Tentar 3 vezes
    # And: Delay exponencial entre tentativas
    # And: Sucesso na terceira tentativa
```

## 7. Critérios de Cobertura por Arquivo

### 7.1 src/main.py
- **Cobertura mínima**: 90%
- **Testes obrigatórios**:
  - Inicialização da aplicação
  - Configuração de CORS
  - Inclusão de rotas
  - Eventos de startup/shutdown

### 7.2 src/config/settings.py
- **Cobertura mínima**: 95%
- **Testes obrigatórios**:
  - Carregamento de variáveis de ambiente
  - Valores padrão
  - Conversão de tipos
  - Validação de configurações

### 7.3 src/models/request.py
- **Cobertura mínima**: 95%
- **Testes obrigatórios**:
  - Validação de QuestionRequest
  - Validação de BatchQuestionRequest
  - Validação de ModelRequest
  - Campos obrigatórios e opcionais

### 7.4 src/models/response.py
- **Cobertura mínima**: 95%
- **Testes obrigatórios**:
  - Serialização de QuestionResponse
  - Serialização de HealthResponse
  - Serialização de ModelInfo
  - Serialização de ErrorResponse

### 7.5 src/services/ollama_service.py
- **Cobertura mínima**: 85%
- **Testes obrigatórios**:
  - list_models() - sucesso e erro
  - generate_question() - sucesso e erro
  - generate_questions_batch() - sucesso e erro
  - _prepare_prompt() - formatação
  - _extract_question_data() - parsing JSON
  - Tratamento de exceções
  - Timeouts e retries

### 7.6 src/services/health_check.py
- **Cobertura mínima**: 90%
- **Testes obrigatórios**:
  - check_health() - Ollama disponível
  - check_health() - Ollama indisponível
  - get_metrics() - métricas corretas
  - Tratamento de exceções

### 7.7 src/api/routes.py
- **Cobertura mínima**: 85%
- **Testes obrigatórios**:
  - GET / - endpoint raiz
  - GET /health - health check
  - GET /models - listagem de modelos
  - POST /generate - geração de questão
  - POST /generate/batch - geração em lote
  - GET /metrics - métricas
  - Tratamento de erros HTTP

### 7.8 src/utils/logger.py
- **Cobertura mínima**: 80%
- **Testes obrigatórios**:
  - setup_logging() - configuração
  - get_logger() - criação de logger
  - Formatação de logs
  - Níveis de log

## 8. Testes de Performance

### 8.1 Latência
```python
def test_generation_latency():
    """Teste de latência de geração"""
    # Given: Prompt padrão
    # When: POST /api/v1/generate
    # Then: processing_time < 5s
    # And: Latência consistente

def test_batch_latency():
    """Teste de latência em lote"""
    # Given: 10 prompts
    # When: POST /api/v1/generate/batch
    # Then: Tempo total < 30s
    # And: Paralelização eficiente
```

### 8.2 Throughput
```python
def test_concurrent_requests():
    """Teste de requisições concorrentes"""
    # Given: 10 requisições simultâneas
    # When: POST /api/v1/generate
    # Then: Todas completadas com sucesso
    # And: Sem deadlocks
    # And: Performance degradada mas funcional
```

## 9. Testes de Resilência

### 9.1 Falhas de Rede
```python
def test_network_failure():
    """Teste de falha de rede"""
    # Given: Rede instável
    # When: POST /api/v1/generate
    # Then: Retry automático
    # And: Fallback para erro após 3 tentativas
    # And: Log de falhas
```

### 9.2 Falhas de Modelo
```python
def test_model_failure():
    """Teste de falha de modelo"""
    # Given: Modelo corrompido
    # When: POST /api/v1/generate
    # Then: Detectar falha
    # And: Retornar erro específico
    # And: Sugerir modelo alternativo
```

## 10. Configuração de Testes

### 10.1 pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=85
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    performance: Performance tests
    slow: Slow tests
```

### 10.2 conftest.py
```python
import pytest
import asyncio
from httpx import AsyncClient
from src.main import app

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def client():
    """Create test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def sample_question_request():
    """Sample question request for tests"""
    return {
        "prompt": "Gere uma questão sobre matemática básica",
        "model": "qwen2:7b",
        "temperature": 0.7,
        "max_tokens": 1000
    }
```

## 11. Execução de Testes

### 11.1 Comandos de Teste
```bash
# Executar todos os testes
pytest

# Executar testes unitários
pytest -m unit

# Executar testes de integração
pytest -m integration

# Executar testes de performance
pytest -m performance

# Executar com cobertura
pytest --cov=src --cov-report=html

# Executar testes específicos
pytest tests/test_ollama_service.py::test_generate_question_success
```

### 11.2 CI/CD Integration
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

## 12. Critérios de Aceite

### 12.1 Cobertura Mínima
- **Cobertura geral**: ≥85%
- **Cobertura de serviços**: ≥85%
- **Cobertura de APIs**: ≥85%
- **Cobertura de modelos**: ≥95%

### 12.2 Performance
- **Latência de geração**: <5s
- **Latência de health check**: <1s
- **Throughput**: >10 req/min
- **Disponibilidade**: >99%

### 12.3 Qualidade
- **Todos os testes passando**: 100%
- **Sem warnings**: 0
- **Código limpo**: Aprovado por linters
- **Documentação**: 100% dos métodos documentados

## 13. Monitoramento e Alertas

### 13.1 Métricas de Teste
- Taxa de sucesso dos testes
- Tempo de execução dos testes
- Cobertura de código
- Performance dos testes

### 13.2 Alertas
- Falha em testes críticos
- Degradação de performance
- Redução de cobertura
- Falhas de integração

---

**Este documento define as especificações completas de teste para a infraestrutura IA-0, garantindo qualidade, confiabilidade e performance do serviço de inferência com Ollama.**
