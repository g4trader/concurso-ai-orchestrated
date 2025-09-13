# Contribuindo — Concurso-AI

Obrigado por colaborar! Este projeto é guiado por **histórias de sprint** e **ordens de execução para instâncias de IA**.

## 🔀 Branching

- `main`: linha estável (somente merge via PR)
- `feature/{id}-{slug}`: branch por história (ex.: `feature/CEB-001-crawler`)
- `docs/{id}`: ajustes de documentação sem código

## 📦 Pull Requests

Cada PR deve incluir:

- Artefatos de **OUTPUTS/** gerados no Cursor (arquitetura, scaffolds, specs, docs, review)
- **NUNCA** alterar STORY.md ou ORDER.yml
- Revisão obrigatória da etapa **Reviewer** antes do merge

## ✅ Critérios de Aceite de PR

- Todos os arquivos de OUTPUTS/ presentes
- Nenhum secret ou credencial exposta
- Estrutura conforme ROOT_GUIDELINES (12-factor, logs JSON, etc.)
- Aprovação de pelo menos 1 maintainer

## 🧪 Testes

- Specs de QA ficam em `OUTPUTS/TEST_SPEC_{ID}.md`
- Implementações reais de testes são feitas apenas após esta fase inicial

## 📅 Versionamento

- Versão inicial: `0.1.0-alpha` (fase de scaffolding/documentação)
- Patch: correções menores de docs/prompts
- Minor: novas histórias concluídas
- Major: MVP pronto para beta público

## 🔒 Segurança

- Nunca commitar credenciais
- Secrets via env vars, com `.env.example` no repo
- Veja `SECURITY.md` (história de AppSec futura)

---

👩‍💻 Este fluxo garante que o **Cursor** possa rodar instâncias de IA de forma autônoma, e que humanos revisem apenas nos marcos certos.
