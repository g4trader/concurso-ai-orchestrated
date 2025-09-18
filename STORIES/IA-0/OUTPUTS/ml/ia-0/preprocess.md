# Preprocess - IA-0

## Objetivo
Pré-processamento de prompts para otimização de inferência com modelos Ollama.

## Funções

### `preprocess_prompt(prompt: str, model: str) -> dict`
```python
def preprocess_prompt(prompt: str, model: str) -> dict:
    """
    Pré-processa prompt para otimização específica do modelo.
    
    Args:
        prompt: Texto do prompt
        model: Nome do modelo (qwen2-7b, llama3.1-8b)
    
    Returns:
        dict: Prompt processado com metadados
    """
    pass
```

### `validate_prompt(prompt: str) -> bool`
```python
def validate_prompt(prompt: str) -> bool:
    """
    Valida se prompt está dentro dos limites do modelo.
    
    Args:
        prompt: Texto do prompt
    
    Returns:
        bool: True se válido
    """
    pass
```

## Exemplos de Uso

### Python
```python
from ml.ia_0.preprocess import preprocess_prompt

# Pré-processar prompt
processed = preprocess_prompt(
    prompt="Gere uma questão de português",
    model="qwen2-7b"
)
```

### cURL
```bash
curl -X POST http://localhost:8000/ml/preprocess \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Gere uma questão de português",
    "model": "qwen2-7b"
  }'
```
