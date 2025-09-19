# ML_SCAFFOLD_IA-2: Pipeline de IA para Geração Condicionada

## Estrutura de /ml/ia-2/

### 1. preprocess.md
```markdown
# Preprocessamento de Dados para Geração de Questões

## Objetivo
Preparar e limpar dados de entrada para o pipeline de geração de questões.

## Funções Principais

### preprocess_contexts(contexts: List[Dict]) -> List[Dict]
- Limpar e normalizar textos dos chunks
- Extrair metadados relevantes
- Validar qualidade dos contextos
- Retornar contextos processados

### preprocess_edital_summary(edital: Dict) -> Dict
- Normalizar informações do edital
- Extrair características da banca
- Validar completude dos dados
- Retornar resumo estruturado

### preprocess_topic(topic: str) -> Dict
- Normalizar nome do tópico
- Mapear para taxonomia padrão
- Extrair subtópicos relacionados
- Retornar tópico estruturado

## Exemplos de Uso

### Python
```python
from ml.ia2.preprocess import preprocess_contexts, preprocess_edital_summary

# Preprocessar contextos
contexts = [
    {
        "chunk_id": "chunk_001",
        "text": "Os princípios fundamentais da Constituição Federal...",
        "metadata": {"banca": "CESPE", "ano": 2024}
    }
]
processed_contexts = preprocess_contexts(contexts)

# Preprocessar edital
edital = {
    "banca": "CESPE",
    "ano": 2024,
    "cargo": "Analista Judiciário",
    "topico": "Direito Constitucional"
}
processed_edital = preprocess_edital_summary(edital)
```

### cURL
```bash
curl -X POST http://localhost:8002/api/v1/preprocess/contexts \
  -H "Content-Type: application/json" \
  -d '{
    "contexts": [
      {
        "chunk_id": "chunk_001",
        "text": "Os princípios fundamentais...",
        "metadata": {"banca": "CESPE", "ano": 2024}
      }
    ]
  }'
```
```

### 2. index.md
```markdown
# Indexação e Recuperação de Contextos

## Objetivo
Indexar contextos para recuperação eficiente durante a geração de questões.

## Funções Principais

### index_contexts(contexts: List[Dict]) -> str
- Indexar contextos no sistema de busca
- Criar índices por banca, tópico, ano
- Retornar ID do índice criado

### retrieve_relevant_contexts(query: str, filters: Dict) -> List[Dict]
- Buscar contextos relevantes para a query
- Aplicar filtros por banca, tópico, ano
- Retornar contextos ordenados por relevância

### update_index(index_id: str, new_contexts: List[Dict]) -> bool
- Atualizar índice existente com novos contextos
- Manter consistência dos índices
- Retornar status da atualização

## Exemplos de Uso

### Python
```python
from ml.ia2.index import index_contexts, retrieve_relevant_contexts

# Indexar contextos
contexts = [...]
index_id = index_contexts(contexts)

# Recuperar contextos relevantes
query = "princípios fundamentais da constituição"
filters = {"banca": "CESPE", "topico": "Direito Constitucional"}
relevant_contexts = retrieve_relevant_contexts(query, filters)
```

### cURL
```bash
curl -X POST http://localhost:8002/api/v1/index/contexts \
  -H "Content-Type: application/json" \
  -d '{
    "contexts": [...],
    "filters": {
      "banca": "CESPE",
      "topico": "Direito Constitucional"
    }
  }'
```
```

### 3. rerank.md
```markdown
# Reranking de Contextos para Geração

## Objetivo
Rerankear contextos recuperados para otimizar a geração de questões.

## Funções Principais

### rerank_contexts(contexts: List[Dict], query: str) -> List[Dict]
- Rerankear contextos por relevância para a query
- Aplicar modelo de reranking
- Retornar contextos ordenados

### calculate_relevance_score(context: Dict, query: str) -> float
- Calcular score de relevância entre contexto e query
- Usar modelo de similaridade semântica
- Retornar score normalizado (0-1)

### filter_by_relevance(contexts: List[Dict], threshold: float) -> List[Dict]
- Filtrar contextos por threshold de relevância
- Manter apenas contextos relevantes
- Retornar contextos filtrados

## Exemplos de Uso

### Python
```python
from ml.ia2.rerank import rerank_contexts, calculate_relevance_score

# Rerankear contextos
contexts = [...]
query = "princípios fundamentais da constituição"
reranked_contexts = rerank_contexts(contexts, query)

# Calcular score de relevância
context = {"text": "Os princípios fundamentais..."}
score = calculate_relevance_score(context, query)
```

### cURL
```bash
curl -X POST http://localhost:8002/api/v1/rerank/contexts \
  -H "Content-Type: application/json" \
  -d '{
    "contexts": [...],
    "query": "princípios fundamentais da constituição",
    "threshold": 0.7
  }'
```
```

### 4. generate.md
```markdown
# Geração de Questões com LLM

## Objetivo
Gerar questões de múltipla escolha usando LLM com prompts condicionados.

## Funções Principais

### generate_question(contexts: List[Dict], edital: Dict, topic: str) -> Dict
- Gerar questão usando LLM
- Aplicar prompt específico da banca
- Retornar questão estruturada

### generate_batch_questions(requests: List[Dict]) -> List[Dict]
- Gerar múltiplas questões em paralelo
- Aplicar validação em lote
- Retornar questões geradas

### validate_generated_question(question: Dict) -> Dict
- Validar questão gerada
- Verificar formato e conteúdo
- Retornar status de validação

## Exemplos de Uso

### Python
```python
from ml.ia2.generate import generate_question, generate_batch_questions

# Gerar questão única
contexts = [...]
edital = {"banca": "CESPE", "ano": 2024}
topic = "Direito Constitucional"
question = generate_question(contexts, edital, topic)

# Gerar questões em lote
requests = [
    {"contexts": [...], "edital": {...}, "topic": "..."},
    {"contexts": [...], "edital": {...}, "topic": "..."}
]
questions = generate_batch_questions(requests)
```

### cURL
```bash
curl -X POST http://localhost:8002/api/v1/generate/question \
  -H "Content-Type: application/json" \
  -d '{
    "contexts": [...],
    "edital_summary": {
      "banca": "CESPE",
      "ano": 2024,
      "topico": "Direito Constitucional"
    },
    "topic": "Direito Constitucional"
  }'
```
```

### 5. validate.md
```markdown
# Validação de Questões Geradas

## Objetivo
Validar questões geradas para garantir qualidade e consistência.

## Funções Principais

### validate_question_format(question: Dict) -> Dict
- Validar formato da questão
- Verificar estrutura JSON
- Retornar status de validação

### validate_question_content(question: Dict) -> Dict
- Validar conteúdo da questão
- Verificar coerência e clareza
- Retornar score de qualidade

### validate_alternatives(alternatives: Dict) -> Dict
- Validar alternativas da questão
- Verificar unicidade do gabarito
- Retornar status de validação

### validate_justification(justification: str, correct_answer: str) -> Dict
- Validar justificativa da resposta
- Verificar coerência com resposta correta
- Retornar score de consistência

## Exemplos de Uso

### Python
```python
from ml.ia2.validate import validate_question_format, validate_question_content

# Validar formato
question = {
    "question": "Qual é o princípio fundamental?",
    "alternatives": {"A": "...", "B": "...", "C": "..."},
    "correct_answer": "B",
    "justification": "..."
}
format_validation = validate_question_format(question)

# Validar conteúdo
content_validation = validate_question_content(question)
```

### cURL
```bash
curl -X POST http://localhost:8002/api/v1/validate/question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Qual é o princípio fundamental?",
    "alternatives": {"A": "...", "B": "...", "C": "..."},
    "correct_answer": "B",
    "justification": "..."
  }'
```
```

### 6. evaluate.md
```markdown
# Avaliação de Qualidade das Questões

## Objetivo
Avaliar qualidade das questões geradas usando métricas objetivas.

## Funções Principais

### evaluate_plausibility(question: Dict) -> float
- Avaliar plausibilidade da questão
- Usar modelo de classificação
- Retornar score (0-1)

### evaluate_consistency(question: Dict) -> float
- Avaliar consistência da questão
- Verificar coerência interna
- Retornar score (0-1)

### evaluate_plagiarism(question: Dict, source_contexts: List[Dict]) -> float
- Avaliar risco de plágio
- Comparar com contextos fonte
- Retornar score (0-1)

### evaluate_overall_quality(question: Dict) -> Dict
- Avaliar qualidade geral
- Combinar múltiplas métricas
- Retornar scores detalhados

## Exemplos de Uso

### Python
```python
from ml.ia2.evaluate import evaluate_plausibility, evaluate_overall_quality

# Avaliar plausibilidade
question = {...}
plausibility_score = evaluate_plausibility(question)

# Avaliar qualidade geral
quality_scores = evaluate_overall_quality(question)
```

### cURL
```bash
curl -X POST http://localhost:8002/api/v1/evaluate/quality \
  -H "Content-Type: application/json" \
  -d '{
    "question": {...},
    "source_contexts": [...],
    "evaluation_config": {
      "check_plausibility": true,
      "check_consistency": true,
      "check_plagiarism": true
    }
  }'
```
```

## Contratos de Função (Assinaturas)

### Preprocessamento
```python
def preprocess_contexts(contexts: List[Dict[str, Any]]) -> List[Dict[str, Any]]
def preprocess_edital_summary(edital: Dict[str, Any]) -> Dict[str, Any]
def preprocess_topic(topic: str) -> Dict[str, Any]
```

### Indexação
```python
def index_contexts(contexts: List[Dict[str, Any]]) -> str
def retrieve_relevant_contexts(query: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]
def update_index(index_id: str, new_contexts: List[Dict[str, Any]]) -> bool
```

### Reranking
```python
def rerank_contexts(contexts: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]
def calculate_relevance_score(context: Dict[str, Any], query: str) -> float
def filter_by_relevance(contexts: List[Dict[str, Any]], threshold: float) -> List[Dict[str, Any]]
```

### Geração
```python
def generate_question(contexts: List[Dict[str, Any]], edital: Dict[str, Any], topic: str) -> Dict[str, Any]
def generate_batch_questions(requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]
def validate_generated_question(question: Dict[str, Any]) -> Dict[str, Any]
```

### Validação
```python
def validate_question_format(question: Dict[str, Any]) -> Dict[str, Any]
def validate_question_content(question: Dict[str, Any]) -> Dict[str, Any]
def validate_alternatives(alternatives: Dict[str, str]) -> Dict[str, Any]
def validate_justification(justification: str, correct_answer: str) -> Dict[str, Any]
```

### Avaliação
```python
def evaluate_plausibility(question: Dict[str, Any]) -> float
def evaluate_consistency(question: Dict[str, Any]) -> float
def evaluate_plagiarism(question: Dict[str, Any], source_contexts: List[Dict[str, Any]]) -> float
def evaluate_overall_quality(question: Dict[str, Any]) -> Dict[str, Any]
```

## Exemplos de Chamadas para Futura API

### Geração de Questão Única
```bash
curl -X POST http://localhost:8002/api/v1/generate/question \
  -H "Content-Type: application/json" \
  -d '{
    "contexts": [
      {
        "chunk_id": "chunk_001",
        "text": "Os princípios fundamentais da Constituição Federal...",
        "metadata": {
          "banca": "CESPE",
          "ano": 2024,
          "topico": "Direito Constitucional"
        }
      }
    ],
    "edital_summary": {
      "banca": "CESPE",
      "ano": 2024,
      "cargo": "Analista Judiciário",
      "orgao": "STF",
      "topico": "Direito Constitucional",
      "dificuldade": "intermediaria",
      "estilo": "conceitual"
    },
    "topic": "Direito Constitucional",
    "generation_config": {
      "num_questions": 1,
      "difficulty": "intermediaria",
      "style": "conceitual",
      "validation_level": "strict"
    }
  }'
```

### Geração em Lote
```bash
curl -X POST http://localhost:8002/api/v1/generate/batch \
  -H "Content-Type: application/json" \
  -d '{
    "batch_id": "batch_789012",
    "requests": [
      {
        "contexts": [...],
        "edital_summary": {...},
        "topic": "Direito Constitucional"
      },
      {
        "contexts": [...],
        "edital_summary": {...},
        "topic": "Direito Administrativo"
      }
    ],
    "batch_config": {
      "max_parallel": 5,
      "timeout_per_question": 30,
      "quality_threshold": 0.9,
      "validation_level": "strict"
    }
  }'
```

### Validação de Questão
```bash
curl -X POST http://localhost:8002/api/v1/validate/question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Qual é o princípio fundamental da Constituição Federal?",
    "alternatives": {
      "A": "Princípio da legalidade",
      "B": "Princípio da separação dos poderes",
      "C": "Princípio da igualdade",
      "D": "Princípio da dignidade da pessoa humana",
      "E": "Princípio da publicidade"
    },
    "correct_answer": "B",
    "justification": "O princípio da separação dos poderes está expressamente previsto no art. 2º da CF/88...",
    "source_chunks": ["chunk_001", "chunk_002"],
    "validation_config": {
      "check_consistency": true,
      "check_plagiarism": true,
      "check_quality": true,
      "consistency_threshold": 0.8,
      "plagiarism_threshold": 0.3,
      "quality_threshold": 0.9
    }
  }'
```

### Avaliação de Qualidade
```bash
curl -X POST http://localhost:8002/api/v1/evaluate/quality \
  -H "Content-Type: application/json" \
  -d '{
    "question": {...},
    "source_contexts": [...],
    "evaluation_config": {
      "check_plausibility": true,
      "check_consistency": true,
      "check_plagiarism": true,
      "plausibility_threshold": 0.9,
      "consistency_threshold": 0.8,
      "plagiarism_threshold": 0.3
    }
  }'
```

---

**Este documento define o pipeline de ML para geração condicionada IA-2, incluindo estrutura, contratos e exemplos de uso.**
