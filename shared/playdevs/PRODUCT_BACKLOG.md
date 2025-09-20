# 📋 Product Backlog - Concurso-AI

## Visão Geral
Lista priorizada de todas as histórias necessárias para entregar o MVP da plataforma Concurso-AI.

## Histórias por Sprint

### 🚀 Sprint 1 - Fundamentos da Coleta
**Status**: ✅ COMPLETA
**Objetivo**: Base inicial com PDFs + TXT + metadados

| ID | Título | Status | Prioridade | Estimativa | Valor |
|----|--------|--------|------------|------------|-------|
| CEB-001 | Crawler Cebraspe — listar e baixar PDFs | ✅ Completa | Alta | 8 | Alto |
| CEB-002 | Parser OCR — extrair texto/metadados | ✅ Completa | Alta | 8 | Alto |

### 🤖 Sprint 2 - Camada IA — Infra e Ingestão
**Status**: 🔄 EM PROGRESSO
**Objetivo**: Infra IA e pipeline de ingestão definidos e especificados

| ID | Título | Status | Prioridade | Estimativa | Valor |
|----|--------|--------|------------|------------|-------|
| IA-0 | Infraestrutura IA: Ollama + modelos | 🔴 Não iniciada | Alta | 13 | Alto |
| IA-1 | Pipeline parse→chunk→embed→index + rerank | 🔴 Não iniciada | Alta | 13 | Alto |

### 🎯 Sprint 3 - Camada IA — Geração e Avaliação
**Status**: ⏸️ AGUARDANDO
**Objetivo**: Geração condicionada com validação + avaliação offline especificadas

| ID | Título | Status | Prioridade | Estimativa | Valor |
|----|--------|--------|------------|------------|-------|
| IA-2 | Geração condicionada banca+edital com validação | 🔴 Não iniciada | Alta | 13 | Alto |
| IA-3 | Avaliação offline: topic-hit, style match, answerability | 🔴 Não iniciada | Alta | 13 | Alto |

### 🌐 Sprint 4 - Frontend & Go-to-Market (MVP)
**Status**: ⏸️ AGUARDANDO
**Objetivo**: MVP acessível com experiência ponta-a-ponta

| ID | Título | Status | Prioridade | Estimativa | Valor |
|----|--------|--------|------------|------------|-------|
| WEB-001 | Protótipo Web — shell do app (Next.js) | 🔴 Não iniciada | Alta | 8 | Alto |
| WEB-002 | Autenticação simples (e-mail/senha) | 🔴 Não iniciada | Alta | 5 | Alto |
| WEB-003 | Tela de geração de simulado | 🔴 Não iniciada | Alta | 8 | Alto |
| WEB-004 | Relatório pós-simulado | 🔴 Não iniciada | Alta | 5 | Alto |
| UX-001 | Feedback do usuário | 🔴 Não iniciada | Média | 5 | Médio |
| OPS-001 | Deploy mínimo (Vercel/Cloud Run) | 🔴 Não iniciada | Alta | 8 | Alto |
| OPS-002 | Observabilidade básica (logs + uptime) | 🔴 Não iniciada | Média | 5 | Médio |

## Histórias Futuras (Backlog)

### 📚 Sprint 5 - Expansão de Bancas
**Status**: 📝 PLANEJADA
**Objetivo**: Suporte a múltiplas bancas examinadoras

| ID | Título | Status | Prioridade | Estimativa | Valor |
|----|--------|--------|------------|------------|-------|
| FGV-001 | Crawler FGV — editais e provas | 🔴 Não iniciada | Média | 8 | Alto |
| FGV-002 | Parser FGV — extrair texto/metadados | 🔴 Não iniciada | Média | 8 | Alto |
| VUNESP-001 | Crawler VUNESP — editais e provas | 🔴 Não iniciada | Baixa | 8 | Médio |
| VUNESP-002 | Parser VUNESP — extrair texto/metadados | 🔴 Não iniciada | Baixa | 8 | Médio |

### 🎓 Sprint 6 - Personalização
**Status**: 📝 PLANEJADA
**Objetivo**: Planos de estudo personalizados

| ID | Título | Status | Prioridade | Estimativa | Valor |
|----|--------|--------|------------|------------|-------|
| PLN-001 | Plano de Estudos Inteligente | 🔴 Não iniciada | Média | 13 | Alto |
| SR-001 | Spaced Repetition (revisões automatizadas) | 🔴 Não iniciada | Média | 8 | Médio |

### 📊 Sprint 7 - Analytics e Relatórios
**Status**: 📝 PLANEJADA
**Objetivo**: Analytics avançados e relatórios

| ID | Título | Status | Prioridade | Estimativa | Valor |
|----|--------|--------|------------|------------|-------|
| ANA-001 | Dashboard de performance do usuário | 🔴 Não iniciada | Baixa | 8 | Médio |
| ANA-002 | Relatórios de progresso | 🔴 Não iniciada | Baixa | 5 | Médio |
| ANA-003 | Métricas de engajamento | 🔴 Não iniciada | Baixa | 5 | Baixo |

## Critérios de Priorização

### Fatores de Priorização
1. **Valor de Negócio**: Alto, Médio, Baixo
2. **Dependências**: Histórias que bloqueiam outras
3. **Risco**: Histórias com maior incerteza
4. **Esforço**: Estimativa de complexidade
5. **Urgência**: Prazos e marcos

### Matriz de Priorização
- **Alta Prioridade**: Histórias críticas para o MVP
- **Média Prioridade**: Histórias importantes para funcionalidade
- **Baixa Prioridade**: Histórias de melhoria e expansão

## Métricas do Backlog

### Status Atual
- **Total de Histórias**: 20
- **Completadas**: 2 (10%)
- **Em Progresso**: 0 (0%)
- **Não Iniciadas**: 18 (90%)

### Por Sprint
- **Sprint 1**: 2/2 completas (100%)
- **Sprint 2**: 0/2 completas (0%)
- **Sprint 3**: 0/2 completas (0%)
- **Sprint 4**: 0/7 completas (0%)

### Por Prioridade
- **Alta**: 11 histórias
- **Média**: 6 histórias
- **Baixa**: 3 histórias

## Próximos Passos

### Sprint 2 (Próxima)
1. **IA-0**: Infraestrutura IA
2. **IA-1**: Pipeline de ingestão

### Preparação para Sprint 3
1. Validar outputs da Sprint 2
2. Refinar histórias IA-2 e IA-3
3. Preparar dependências

### Preparação para Sprint 4
1. Definir wireframes do frontend
2. Configurar ambientes de deploy
3. Preparar estratégia de UX

---

**Última Atualização**: [Data]
**Próxima Revisão**: [Data]
**Responsável**: PO
