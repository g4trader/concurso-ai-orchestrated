# HISTÓRIA IA‑1: Pipeline de ingestão — parse→chunk→embed→index (+rerank)

**Contexto:** Estruturar conteúdo para RAG (editais/provas) com embeddings e reranker local.  
**Usuário:** Motor de geração.  
**Valor:** Recuperação precisa de contexto por banca/tópico.

**Escopo (IN):** blueprint do pipeline (PyMuPDF/Tesseract), chunking com metadados (banca/ano/tópico), embeddings (bge‑m3), FAISS, reranker (bge‑reranker‑large).  
**Escopo (OUT):** execução real (apenas scaffolds/contratos).

**Critérios:** Dado um PDF de exemplo, especificar como ele se transforma em chunks com IDs e metadados; definir a API para `query(topico, banca)` retornar top‑k trechos.
