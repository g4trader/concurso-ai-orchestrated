# Rerank - IA-0

## Objetivo
Sistema de reranking para otimização de respostas dos modelos.

## Funções

### `rerank_responses(responses: list, query: str) -> list`
```python
def rerank_responses(responses: list, query: str) -> list:
    """
    Rerank respostas baseado na relevância da query.
    
    Args:
        responses: Lista de respostas
        query: Query original
    
    Returns:
        list: Respostas rerankeadas
    """
    pass
```

### `score_response(response: str, query: str) -> float`
```python
def score_response(response: str, query: str) -> float:
    """
    Calcula score de relevância de uma resposta.
    
    Args:
        response: Texto da resposta
        query: Query original
    
    Returns:
        float: Score de relevância (0-1)
    """
    pass
```

## Exemplos de Uso

### Python
```python
from ml.ia_0.rerank import rerank_responses

# Rerankear respostas
ranked = rerank_responses(
    responses=["resposta1", "resposta2"],
    query="questão de português"
)
```

### cURL
```bash
curl -X POST http://localhost:8000/ml/rerank \
  -H "Content-Type: application/json" \
  -d '{
    "responses": ["resposta1", "resposta2"],
    "query": "questão de português"
  }'
```
