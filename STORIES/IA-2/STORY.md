# HISTÓRIA IA‑2: Geração condicionada por banca+edital com validação automática

**Contexto:** Precisamos gerar questões plausíveis no estilo da banca e do edital atual.  
**Usuário:** Estudante (via simulados).  
**Valor:** Questões coerentes, gabarito único, justificativa e fontes (chunks).

**Escopo (IN):** prompts de sistema/tarefa; JSON de saída; validações automáticas (unicidade de gabarito, self‑consistency 2×, anti‑plágio leve).  
**Escopo (OUT):** geração em massa (apenas contrato e scaffolds).

**Critérios:** Dado {CONTEXTOS}+{RESUMO_EDITAL}+{TOPICO}, retorno JSON com pergunta, alternativas A‑E, correta, justificativa curta, ids dos chunks.  
**Métricas:** plausibilidade ≥90% (definição documentada); tempo alvo por questão.
