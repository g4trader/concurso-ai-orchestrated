# Root Guidelines (Detalhado)

## Arquitetura e Organização
- Monorepo orientado a **domínios**. Cada história cria pastas e artefatos sob `playdevs/STORIES/{ID}` até que o código seja iniciado.
- Padrões: 12‑factor, SOLID, Clean Architecture, logs estruturados (JSON) com `request_id`.
- CI/CD (futuro): GitHub Actions com estágios lint → test → build.

## Segurança
- **Jamais** commitar secrets. Use variáveis de ambiente e `.env.example`.
- `SECURITY.md` descreve política, reporte de vulnerabilidades e revisão de PR segura.

## Qualidade
- Meta de cobertura (fase de código): ≥70%, evoluindo para ≥85% em módulos críticos.
- Testes unitários, integração com mocks e timeouts obrigatórios.

## Convenções
- Branch: `feature/{id}-{slug}` · `docs/{id}` · `chore/...`
- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`).
- PR: descrição com contexto, solução, riscos, como testar e prints/artefatos.

## Documentação
- Toda história mantém `STORY.md`, `ORDER.yml`, `PROMPTS/` e gera `OUTPUTS/`.
- `ORDER_SPEC.md` define as chaves aceitas no `ORDER.yml`.
