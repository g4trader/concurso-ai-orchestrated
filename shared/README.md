# Concurso-AI Orchestrated

Este repositório contém a **orquestração completa de histórias e prompts** para desenvolver um
MVP de plataforma de estudos para concursos públicos usando **instâncias de IA no Cursor**.

## 📂 Estrutura

- `playdevs/ROADMAP.md` → visão geral dos marcos até o Go-to-Market Beta
- `playdevs/SPRINT_PLAN.yml` → sprint atual com histórias e ordem
- `playdevs/STORIES/{ID}/` → cada história (STORY.md, ORDER.yml, PROMPTS/, OUTPUTS/)
- `playdevs/TEMPLATES/` → prompts reutilizáveis por papel

## 🚀 Como usar no Cursor

1. Clone este repositório no Cursor (pode ser fork do GitHub).
2. Abra `playdevs/SPRINT_PLAN.yml` para ver a lista de histórias da sprint.
3. Entre em uma pasta de história, ex.: `playdevs/STORIES/CEB-001/`.
4. Siga o arquivo `ORDER.yml`:
   - Cada passo indica: **papel** (Arquiteta, Backend, QA…), **entrada**, **prompt** a usar, **output esperado**.
   - Abra o prompt em `PROMPTS/` e execute na instância de IA correspondente.
   - Salve o resultado no arquivo/pasta de `OUTPUTS/` indicado.
5. Continue até o último passo (Reviewer).

## 🛠 Fluxo de Trabalho

- Cada história gera um conjunto de artefatos em `OUTPUTS/`.
- Depois de revisado, abra um **PR** para integrar ao branch `main`.
- O PR deve conter:
  - STORY.md (imutável)
  - ORDER.yml (imutável)
  - Saídas em OUTPUTS/ (geradas na sprint)
- O merge depende de aprovação da etapa **Reviewer**.

## 📌 Status Atual

- Sprint 1 foca em coleta e parsing (CEB-001 e CEB-002).
- As demais histórias já estão mapeadas (SIM-001, PLN-001, SR-001).

---

📖 Veja também: [CONTRIBUTING.md](CONTRIBUTING.md)
