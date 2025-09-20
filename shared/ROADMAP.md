# Roadmap — IA Concursos (MVP → Beta)

## Sprint 1 — Fundamentos da Coleta
- CEB-001: Crawler Cebraspe — listar/baixar PDFs
- CEB-002: Parser OCR — extrair texto/metadados
**Marco:** Base inicial com PDFs + TXT + metadados

## Sprint 2 — Simulados Inteligentes
- SIM-001: Motor de Simulados — geração no estilo da banca
**Marco:** API que retorna simulado de 20 questões com gabarito

## Sprint 3 — Personalização do Estudo
- PLN-001: Plano de Estudos Inteligente
- SR-001: Spaced Repetition (revisões automatizadas)
**Marco:** Ciclo completo de estudo (plano + revisões + simulados)

## Sprint 4 — Go-to-Market Beta
- Frontend mínimo + onboarding (história futura)
**Marco:** Primeiros usuários beta navegando no MVP

## Sprint 4 — Frontend & Go‑to‑Market (MVP)
- WEB-001: Protótipo Web — shell do app (Next.js)
- WEB-002: Autenticação simples (e-mail/senha)
- WEB-003: Tela de geração de simulado
- WEB-004: Relatório pós-simulado
- UX-001: Feedback do usuário
- OPS-001: Deploy mínimo (Vercel/Cloud Run)
- OPS-002: Observabilidade básica (logs + uptime)
**Marco:** MVP acessível com experiência ponta‑a‑ponta para beta testers.

# 📌 Roadmap Completo até o MVP

Este quadro resume todas as sprints (S1–S4), histórias e marcos principais.

| Sprint | Objetivo                          | Histórias Principais                                                                                       | Marco de Entrega                                     |
|--------|-----------------------------------|-------------------------------------------------------------------------------------------------------------|------------------------------------------------------|
| **S1** | Fundamentos da Coleta             | CEB-001 (Crawler editais Cebraspe), CEB-002 (Crawler provas Cebraspe), FGV-001 (Crawler editais FGV), FGV-002 (Crawler provas FGV) | Coleta inicial estruturada de 2 bancas               |
| **S2** | Camada IA — Infra & Ingestão      | IA-0 (Infra IA: Ollama + modelos), IA-1 (Pipeline parse→chunk→embed→index + rerank)                          | Infra IA e pipeline de ingestão especificados        |
| **S3** | Camada IA — Geração & Avaliação   | IA-2 (Geração condicionada banca+edital com validação), IA-3 (Avaliação offline: topic-hit, style match, answerability) | Motor de geração validado e métricas de qualidade    |
| **S4** | Frontend & Go‑to‑Market (MVP)     | WEB-001 (Protótipo Web), WEB-002 (Autenticação simples), WEB-003 (Tela de simulado), WEB-004 (Relatório), UX-001 (Feedback), OPS-001 (Deploy), OPS-002 (Observabilidade) | MVP completo acessível para beta testers             |

---

## 🛤️ Linha do Tempo (estimada)

- **S1**: Semanas 1–2 → Crawlers e coleta inicial  
- **S2**: Semanas 3–4 → Infra IA e ingestão de conteúdo  
- **S3**: Semanas 5–7 → Geração de questões e avaliação offline  
- **S4**: Semanas 8–10 → Frontend, deploy e MVP com beta fechado  

---

## 🎯 Meta Final
Ter um **MVP navegável**, com:
- Editais e provas processados (2 bancas mínimas).  
- Simulados gerados com estilo e probabilidade da banca.  
- Interface web com login, simulado e relatório.  
- Deploy acessível para testadores.
