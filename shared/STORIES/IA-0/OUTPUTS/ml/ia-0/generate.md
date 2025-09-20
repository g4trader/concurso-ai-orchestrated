# Generate - IA-0

## Objetivo
Sistema de geração de texto usando modelos Ollama.

## Funções

### `generate_text(prompt: str, model: str, params: dict) -> dict`
```python
def generate_text(prompt: str, model: str, params: dict) -> dict:
    """
    Gera texto usando modelo Ollama.
    
    Args:
        prompt: Texto do prompt
        model: Nome do modelo
        params: Parâmetros de geração
    
    Returns:
        dict: Resposta com texto gerado
    """
    pass
```

### `generate_batch(prompts: list, model: str, params: dict) -> list`
```python
def generate_batch(prompts: list, model: str, params: dict) -> list:
    """
    Gera texto em lote para múltiplos prompts.
    
    Args:
        prompts: Lista de prompts
        model: Nome do modelo
        params: Parâmetros de geração
    
    Returns:
        list: Lista de respostas
    """
    pass
```

## Exemplos de Uso

### Python
```python
from ml.ia_0.generate import generate_text

# Gerar texto
response = generate_text(
    prompt="Gere uma questão de português",
    model="qwen2-7b",
    params={"temperature": 0.7, "max_tokens": 1000}
)
```

### cURL
```bash
curl -X POST http://localhost:8000/llm/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2-7b",
    "prompt": "Gere uma questão de português",
    "params": {
      "temperature": 0.7,
      "max_tokens": 1000
    }
  }'
```
