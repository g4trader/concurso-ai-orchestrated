# Evaluate - IA-0

## Objetivo
Sistema de avaliação de performance e qualidade dos modelos.

## Funções

### `evaluate_model(model: str, test_cases: list) -> dict`
```python
def evaluate_model(model: str, test_cases: list) -> dict:
    """
    Avalia performance de um modelo com casos de teste.
    
    Args:
        model: Nome do modelo
        test_cases: Lista de casos de teste
    
    Returns:
        dict: Resultados da avaliação
    """
    pass
```

### `benchmark_models(models: list, test_cases: list) -> dict`
```python
def benchmark_models(models: list, test_cases: list) -> dict:
    """
    Compara performance entre modelos.
    
    Args:
        models: Lista de modelos
        test_cases: Lista de casos de teste
    
    Returns:
        dict: Comparação de performance
    """
    pass
```

## Exemplos de Uso

### Python
```python
from ml.ia_0.evaluate import evaluate_model

# Avaliar modelo
results = evaluate_model(
    model="qwen2-7b",
    test_cases=["teste1", "teste2"]
)
```

### cURL
```bash
curl -X POST http://localhost:8000/ml/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2-7b",
    "test_cases": ["teste1", "teste2"]
  }'
```
