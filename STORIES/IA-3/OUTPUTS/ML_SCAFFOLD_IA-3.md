# ML_SCAFFOLD_IA-3: Pipeline de IA para Avaliação Offline

## Estrutura de /ml/ia-3/

### 1. preprocess.md
```markdown
# Preprocessamento de Dados para Avaliação Offline

## Objetivo
Preparar e limpar dados de entrada para o pipeline de avaliação offline.

## Funções Principais

### preprocess_generated_simulados(simulados: List[Dict]) -> List[Dict]
- Limpar e normalizar simulados gerados
- Extrair metadados relevantes
- Validar estrutura dos dados
- Retornar simulados processados

### preprocess_held_out_dataset(dataset: Dict) -> Dict
- Limpar e normalizar dataset held-out
- Extrair metadados de validação
- Validar completude dos dados
- Retornar dataset estruturado

### preprocess_evaluation_config(config: Dict) -> Dict
- Normalizar configurações de avaliação
- Validar métricas solicitadas
- Extrair thresholds configurados
- Retornar configuração estruturada

## Exemplos de Uso

### Python
```python
from ml.ia3.preprocess import preprocess_generated_simulados, preprocess_held_out_dataset

# Preprocessar simulados gerados
simulados = [
    {
        "simulado_id": "sim_001",
        "banca": "CESPE",
        "ano": 2023,
        "questoes": [...]
    }
]
processed_simulados = preprocess_generated_simulados(simulados)

# Preprocessar dataset held-out
dataset = {
    "banca": "CESPE",
    "ano": 2023,
    "questoes_reais": [...]
}
processed_dataset = preprocess_held_out_dataset(dataset)
```

### cURL
```bash
curl -X POST http://localhost:8003/api/v1/preprocess/simulados \
  -H "Content-Type: application/json" \
  -d '{
    "simulados": [
      {
        "simulado_id": "sim_001",
        "banca": "CESPE",
        "ano": 2023,
        "questoes": [...]
      }
    ]
  }'
```
```

### 2. index.md
```markdown
# Indexação e Recuperação de Dados de Avaliação

## Objetivo
Indexar dados de avaliação para recuperação eficiente durante o processamento.

## Funções Principais

### index_evaluation_data(simulados: List[Dict], dataset: Dict) -> str
- Indexar simulados e dataset held-out
- Criar índices por banca, ano, tópico
- Retornar ID do índice criado

### retrieve_evaluation_data(index_id: str, filters: Dict) -> Dict
- Buscar dados de avaliação por filtros
- Aplicar filtros por banca, ano, tópico
- Retornar dados filtrados

### update_evaluation_index(index_id: str, new_data: Dict) -> bool
- Atualizar índice existente com novos dados
- Manter consistência dos índices
- Retornar status da atualização

## Exemplos de Uso

### Python
```python
from ml.ia3.index import index_evaluation_data, retrieve_evaluation_data

# Indexar dados de avaliação
simulados = [...]
dataset = {...}
index_id = index_evaluation_data(simulados, dataset)

# Recuperar dados de avaliação
filters = {"banca": "CESPE", "ano": 2023}
evaluation_data = retrieve_evaluation_data(index_id, filters)
```

### cURL
```bash
curl -X POST http://localhost:8003/api/v1/index/evaluation \
  -H "Content-Type: application/json" \
  -d '{
    "simulados": [...],
    "dataset": {...},
    "filters": {
      "banca": "CESPE",
      "ano": 2023
    }
  }'
```
```

### 3. rerank.md
```markdown
# Reranking de Dados para Avaliação

## Objetivo
Rerankear dados de avaliação para otimizar o processamento de métricas.

## Funções Principais

### rerank_evaluation_data(data: Dict, criteria: str) -> Dict
- Rerankear dados por critério específico
- Aplicar algoritmo de reranking
- Retornar dados ordenados

### calculate_relevance_score(data: Dict, criteria: str) -> float
- Calcular score de relevância para critério
- Usar algoritmo de similaridade
- Retornar score normalizado (0-1)

### filter_by_relevance(data: Dict, threshold: float) -> Dict
- Filtrar dados por threshold de relevância
- Manter apenas dados relevantes
- Retornar dados filtrados

## Exemplos de Uso

### Python
```python
from ml.ia3.rerank import rerank_evaluation_data, calculate_relevance_score

# Rerankear dados de avaliação
data = {...}
criteria = "topic_relevance"
reranked_data = rerank_evaluation_data(data, criteria)

# Calcular score de relevância
score = calculate_relevance_score(data, criteria)
```

### cURL
```bash
curl -X POST http://localhost:8003/api/v1/rerank/evaluation \
  -H "Content-Type: application/json" \
  -d '{
    "data": {...},
    "criteria": "topic_relevance",
    "threshold": 0.7
  }'
```
```

### 4. generate.md
```markdown
# Geração de Métricas de Avaliação

## Objetivo
Gerar métricas de avaliação usando algoritmos de análise.

## Funções Principais

### generate_topic_hit_rate(simulados: List[Dict], dataset: Dict) -> Dict
- Calcular topic hit rate
- Comparar tópicos entre simulados e dataset
- Retornar métricas de hit rate

### generate_style_match(simulados: List[Dict], dataset: Dict) -> Dict
- Calcular style match
- Analisar consistência de estilo
- Retornar métricas de style match

### generate_answerability(simulados: List[Dict], dataset: Dict) -> Dict
- Calcular answerability
- Verificar capacidade de resposta
- Retornar métricas de answerability

## Exemplos de Uso

### Python
```python
from ml.ia3.generate import generate_topic_hit_rate, generate_style_match

# Gerar topic hit rate
simulados = [...]
dataset = {...}
hit_rate = generate_topic_hit_rate(simulados, dataset)

# Gerar style match
style_match = generate_style_match(simulados, dataset)
```

### cURL
```bash
curl -X POST http://localhost:8003/api/v1/generate/metrics \
  -H "Content-Type: application/json" \
  -d '{
    "simulados": [...],
    "dataset": {...},
    "metrics": ["topic_hit_rate", "style_match", "answerability"]
  }'
```
```

### 5. validate.md
```markdown
# Validação de Métricas de Avaliação

## Objetivo
Validar métricas de avaliação para garantir qualidade e consistência.

## Funções Principais

### validate_topic_hit_rate(metrics: Dict) -> Dict
- Validar métricas de topic hit rate
- Verificar consistência dos dados
- Retornar status de validação

### validate_style_match(metrics: Dict) -> Dict
- Validar métricas de style match
- Verificar precisão da análise
- Retornar status de validação

### validate_answerability(metrics: Dict) -> Dict
- Validar métricas de answerability
- Verificar critérios de resposta
- Retornar status de validação

## Exemplos de Uso

### Python
```python
from ml.ia3.validate import validate_topic_hit_rate, validate_style_match

# Validar topic hit rate
hit_rate_metrics = {...}
validation = validate_topic_hit_rate(hit_rate_metrics)

# Validar style match
style_metrics = {...}
validation = validate_style_match(style_metrics)
```

### cURL
```bash
curl -X POST http://localhost:8003/api/v1/validate/metrics \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": {
      "topic_hit_rate": {...},
      "style_match": {...},
      "answerability": {...}
    }
  }'
```
```

### 6. evaluate.md
```markdown
# Avaliação de Performance do Sistema

## Objetivo
Avaliar performance do sistema de avaliação usando métricas objetivas.

## Funções Principais

### evaluate_topic_hit_rate_performance(metrics: Dict) -> float
- Avaliar performance de topic hit rate
- Calcular score de performance
- Retornar score (0-1)

### evaluate_style_match_performance(metrics: Dict) -> float
- Avaliar performance de style match
- Calcular score de performance
- Retornar score (0-1)

### evaluate_answerability_performance(metrics: Dict) -> float
- Avaliar performance de answerability
- Calcular score de performance
- Retornar score (0-1)

### evaluate_overall_performance(metrics: Dict) -> Dict
- Avaliar performance geral
- Combinar múltiplas métricas
- Retornar scores detalhados

## Exemplos de Uso

### Python
```python
from ml.ia3.evaluate import evaluate_topic_hit_rate_performance, evaluate_overall_performance

# Avaliar performance de topic hit rate
hit_rate_metrics = {...}
performance = evaluate_topic_hit_rate_performance(hit_rate_metrics)

# Avaliar performance geral
all_metrics = {...}
overall_performance = evaluate_overall_performance(all_metrics)
```

### cURL
```bash
curl -X POST http://localhost:8003/api/v1/evaluate/performance \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": {
      "topic_hit_rate": {...},
      "style_match": {...},
      "answerability": {...}
    }
  }'
```
```

## Contratos de Função (Assinaturas)

### Preprocessamento
```python
def preprocess_generated_simulados(simulados: List[Dict[str, Any]]) -> List[Dict[str, Any]]
def preprocess_held_out_dataset(dataset: Dict[str, Any]) -> Dict[str, Any]
def preprocess_evaluation_config(config: Dict[str, Any]) -> Dict[str, Any]
```

### Indexação
```python
def index_evaluation_data(simulados: List[Dict[str, Any]], dataset: Dict[str, Any]) -> str
def retrieve_evaluation_data(index_id: str, filters: Dict[str, Any]) -> Dict[str, Any]
def update_evaluation_index(index_id: str, new_data: Dict[str, Any]) -> bool
```

### Reranking
```python
def rerank_evaluation_data(data: Dict[str, Any], criteria: str) -> Dict[str, Any]
def calculate_relevance_score(data: Dict[str, Any], criteria: str) -> float
def filter_by_relevance(data: Dict[str, Any], threshold: float) -> Dict[str, Any]
```

### Geração
```python
def generate_topic_hit_rate(simulados: List[Dict[str, Any]], dataset: Dict[str, Any]) -> Dict[str, Any]
def generate_style_match(simulados: List[Dict[str, Any]], dataset: Dict[str, Any]) -> Dict[str, Any]
def generate_answerability(simulados: List[Dict[str, Any]], dataset: Dict[str, Any]) -> Dict[str, Any]
```

### Validação
```python
def validate_topic_hit_rate(metrics: Dict[str, Any]) -> Dict[str, Any]
def validate_style_match(metrics: Dict[str, Any]) -> Dict[str, Any]
def validate_answerability(metrics: Dict[str, Any]) -> Dict[str, Any]
```

### Avaliação
```python
def evaluate_topic_hit_rate_performance(metrics: Dict[str, Any]) -> float
def evaluate_style_match_performance(metrics: Dict[str, Any]) -> float
def evaluate_answerability_performance(metrics: Dict[str, Any]) -> float
def evaluate_overall_performance(metrics: Dict[str, Any]) -> Dict[str, Any]
```

## Exemplos de Chamadas para Futura API

### Avaliação de Simulados
```bash
curl -X POST http://localhost:8003/api/v1/evaluate/simulados \
  -H "Content-Type: application/json" \
  -d '{
    "evaluation_id": "eval_123456",
    "generated_simulados": [
      {
        "simulado_id": "sim_001",
        "banca": "CESPE",
        "ano": 2023,
        "topico": "Direito Constitucional",
        "questoes": [
          {
            "questao_id": "q_001",
            "pergunta": "Qual é o princípio fundamental da Constituição Federal?",
            "alternativas": {
              "A": "Princípio da legalidade",
              "B": "Princípio da separação dos poderes",
              "C": "Princípio da igualdade"
            },
            "resposta_correta": "B",
            "justificativa": "O princípio da separação dos poderes..."
          }
        ]
      }
    ],
    "held_out_dataset": {
      "banca": "CESPE",
      "ano": 2023,
      "topico": "Direito Constitucional",
      "questoes_reais": [
        {
          "questao_id": "real_001",
          "pergunta": "Sobre os princípios fundamentais...",
          "alternativas": {...},
          "resposta_correta": "B"
        }
      ]
    },
    "evaluation_config": {
      "metrics": ["topic_hit_rate", "style_match", "answerability"],
      "thresholds": {
        "topic_hit_rate": 0.8,
        "style_match": 0.7,
        "answerability": 0.9
      }
    }
  }'
```

### Benchmark de Avaliação
```bash
curl -X POST http://localhost:8003/api/v1/benchmark/evaluation \
  -H "Content-Type: application/json" \
  -d '{
    "benchmark_id": "bench_789012",
    "evaluation_requests": [
      {
        "evaluation_id": "eval_001",
        "generated_simulados": [...],
        "held_out_dataset": {...}
      }
    ],
    "benchmark_config": {
      "metrics": ["topic_hit_rate", "style_match", "answerability"],
      "aggregation_method": "weighted_average",
      "weights": {
        "topic_hit_rate": 0.4,
        "style_match": 0.3,
        "answerability": 0.3
      }
    }
  }'
```

### Geração de Relatório
```bash
curl -X POST http://localhost:8003/api/v1/report/generate \
  -H "Content-Type: application/json" \
  -d '{
    "report_id": "report_345678",
    "evaluation_results": [...],
    "benchmark_results": [...],
    "report_config": {
      "format": "markdown",
      "include_charts": true,
      "include_recommendations": true,
      "include_gap_analysis": true
    }
  }'
```

### Validação de Métricas
```bash
curl -X POST http://localhost:8003/api/v1/validate/metrics \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": {
      "topic_hit_rate": {
        "score": 0.85,
        "details": {
          "total_questions": 100,
          "topic_matches": 85,
          "topic_miss": 15
        }
      },
      "style_match": {
        "score": 0.75,
        "details": {
          "total_questions": 100,
          "style_matches": 75,
          "style_miss": 25
        }
      },
      "answerability": {
        "score": 0.92,
        "details": {
          "total_questions": 100,
          "answerable": 92,
          "unanswerable": 8
        }
      }
    }
  }'
```

### Avaliação de Performance
```bash
curl -X POST http://localhost:8003/api/v1/evaluate/performance \
  -H "Content-Type: application/json" \
  -d '{
    "metrics": {
      "topic_hit_rate": {...},
      "style_match": {...},
      "answerability": {...}
    },
    "evaluation_config": {
      "check_consistency": true,
      "check_accuracy": true,
      "check_reliability": true,
      "consistency_threshold": 0.8,
      "accuracy_threshold": 0.9,
      "reliability_threshold": 0.85
    }
  }'
```

---

**Este documento define o pipeline de ML para avaliação offline IA-3, incluindo estrutura, contratos e exemplos de uso.**
