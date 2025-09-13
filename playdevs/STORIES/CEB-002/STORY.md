# HISTÓRIA CEB‑002: Parser OCR — extrair texto e metadados

**Contexto:** Transformar PDFs em texto pesquisável com fallback para OCR.  
**Usuário:** Módulo de IA e busca.  
**Valor:** Texto limpo e metadados para extração de conteúdo programático e indexação.

**Escopo (IN):** OCR para PDFs imagem; extração para PDFs texto; normalização; salvamento `.txt` + JSON; classificação (edital/prova/gabarito/retificação).  
**Escopo (OUT):** extração semântica de tópicos (história futura).

**Critérios:** Dado um lote misto de PDFs, quando executo o parser, então arquivos `.txt` e JSON de metadados são gerados; charset UTF‑8 válido.

**Métricas:** taxa de sucesso OCR ≥95%; tempo razoável por doc.  
**Dependências:** CEB‑001.

**DoR/DoD:** como CEB‑001.
