# HISTÓRIA IA‑0: Infra IA — Inferência local com Ollama e modelos open-weights

**Contexto:** Precisamos de um serviço local de LLM gratuito para geração (Qwen2‑7B, Llama‑3.1‑8B).  
**Usuário:** Motor de geração de questões.  
**Valor:** Custos previsíveis, independência de API externa.

**Escopo (IN):** definir arquitetura de serviço `/llm/generate`, roteamento por modelo, parâmetros (temperature, max_tokens), política de logs; scaffolds de endpoints e contratos.  
**Escopo (OUT):** instalação real do Ollama (será implementada em sprint posterior).

**Critérios:** Dado um prompt de teste, o contrato do endpoint/CLI proposto aceita `model`, `prompt`, `params` e retorna `text`.  
**Métricas:** latência-alvo documentada; fallback entre modelos documentado.
