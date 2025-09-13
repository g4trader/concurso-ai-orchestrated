# HISTÓRIA CEB‑001: Crawler Cebraspe — listar e baixar PDFs

**Contexto:** Iniciar a coleta de documentos públicos (editais/provas/gabaritos) da banca Cebraspe.  
**Usuário:** Pipeline de ingestão (downstream: parser/IA).  
**Valor:** Base inicial para análise de editais e geração de simulados.

**Escopo (IN):** descoberta de URLs; catálogo de PDFs; metadados (título, ano, tipo, link); deduplicação por hash; logs JSON.  
**Escopo (OUT):** OCR e parsing semântico (histórias futuras).

**Critérios de Aceite (Gherkin)**  
- Dado o domínio público da Cebraspe, quando executo a rotina, então novos PDFs são catalogados e metadados salvos em `index.json`.  
- Dado que executo novamente, então documentos já processados são ignorados por hash.

**Métricas:** taxa de erro <3%; 0 duplicatas por execução incremental.  
**Dependências:** nenhuma.

**DoR:** critérios definidos; paths públicos mapeados.  
**DoD:** arquitetura, scaffolds, specs de testes, docs e review gerados nesta história.
