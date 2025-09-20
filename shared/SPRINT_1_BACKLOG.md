# 📋 Sprint 1 — Backlog

**Objetivo:** Fundamentos da Coleta

**Marco:** Base inicial com PDFs + TXT + metadados

## Histórias

### CEB-001

- [STORY.md](STORIES/CEB-001/STORY.md)

- [ORDER.yml](STORIES/CEB-001/ORDER.yml)

**Critérios extraídos:**

**Critérios de Aceite (Gherkin)**
- Dado o domínio público da Cebraspe, quando executo a rotina, então novos PDFs são catalogados e metadados salvos em `index.json`.
- Dado que executo novamente, então documentos já processados são ignorados por hash.


### CEB-002

- [STORY.md](STORIES/CEB-002/STORY.md)

- [ORDER.yml](STORIES/CEB-002/ORDER.yml)

**Critérios extraídos:**

**Critérios:** Dado um lote misto de PDFs, quando executo o parser, então arquivos `.txt` e JSON de metadados são gerados; charset UTF‑8 válido.

