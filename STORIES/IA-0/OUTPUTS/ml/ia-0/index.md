# Index - IA-0

## Objetivo
Sistema de indexação para modelos e configurações do Ollama.

## Funções

### `index_models() -> list`
```python
def index_models() -> list:
    """
    Lista todos os modelos disponíveis no Ollama.
    
    Returns:
        list: Lista de modelos com metadados
    """
    pass
```

### `get_model_info(model: str) -> dict`
```python
def get_model_info(model: str) -> dict:
    """
    Obtém informações detalhadas de um modelo.
    
    Args:
        model: Nome do modelo
    
    Returns:
        dict: Informações do modelo
    """
    pass
```

## Exemplos de Uso

### Python
```python
from ml.ia_0.index import index_models, get_model_info

# Listar modelos
models = index_models()

# Obter info do modelo
info = get_model_info("qwen2-7b")
```

### cURL
```bash
# Listar modelos
curl http://localhost:8000/ml/models

# Info do modelo
curl http://localhost:8000/ml/models/qwen2-7b
```
