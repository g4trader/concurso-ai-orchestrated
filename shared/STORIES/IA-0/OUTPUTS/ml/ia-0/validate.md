# Validate - IA-0

## Objetivo
Sistema de validação de respostas e qualidade dos modelos.

## Funções

### `validate_response(response: str, prompt: str) -> dict`
```python
def validate_response(response: str, prompt: str) -> dict:
    """
    Valida qualidade e relevância da resposta.
    
    Args:
        response: Texto da resposta
        prompt: Prompt original
    
    Returns:
        dict: Resultado da validação
    """
    pass
```

### `check_quality_metrics(response: str) -> dict`
```python
def check_quality_metrics(response: str) -> dict:
    """
    Verifica métricas de qualidade da resposta.
    
    Args:
        response: Texto da resposta
    
    Returns:
        dict: Métricas de qualidade
    """
    pass
```

## Exemplos de Uso

### Python
```python
from ml.ia_0.validate import validate_response

# Validar resposta
validation = validate_response(
    response="Texto gerado...",
    prompt="Gere uma questão de português"
)
```

### cURL
```bash
curl -X POST http://localhost:8000/ml/validate \
  -H "Content-Type: application/json" \
  -d '{
    "response": "Texto gerado...",
    "prompt": "Gere uma questão de português"
  }'
```
