# 📝 RELATORES — Documentação de Marcos por Sprint

Este guia define como relatar os resultados de cada sprint e registrar a evolução do projeto até o MVP.

---

## Estrutura de Relatório por Sprint

Cada relatório deve estar em `RELATORES/SPRINT_{N}_REPORT.md` e conter:

### 1. Objetivo da Sprint
- Reescreva o objetivo conforme definido no plano (SPRINT_PLAN).

### 2. Histórias Concluídas
- Liste cada história com links para:
  - STORY.md
  - ORDER.yml
  - OUTPUTS principais (ARCH, README, REVIEW)

### 3. Critérios de Aceite
- Explique se todos foram cumpridos.
- Se algum critério ficou pendente, descreva o motivo.

### 4. Artefatos Gerados
- Capture prints ou resumos dos principais arquivos em OUTPUTS/.
- Indique se foram validados pelas postconditions.

### 5. Riscos e Gaps Encontrados
- Liste problemas descobertos durante a sprint.
- Indique se foram resolvidos ou transferidos para a próxima.

### 6. Métricas
- Quantidade de histórias concluídas vs planejadas.
- Taxa de cumprimento dos critérios.
- Observações de qualidade ou velocidade.

### 7. Decisão de Marco
- Declare se o marco foi **ATINIGIDO** ou **NÃO ATINGIDO**.
- Justifique com base nas evidências.

### 8. Próximos Passos
- Liste as prioridades da próxima sprint.
- Referencie o backlog seguinte.

---

## Checklist do Relator

- [ ] Todos os links para STORY.md e ORDER.yml funcionam.  
- [ ] Os arquivos OUTPUTS/ obrigatórios estão anexados.  
- [ ] Critérios de aceite foram revistos.  
- [ ] Postconditions foram verificadas.  
- [ ] O status do marco foi declarado de forma clara.  

---

## Estrutura de Pastas

```
RELATORES/
 ├── SPRINT_1_REPORT.md
 ├── SPRINT_2_REPORT.md
 ├── SPRINT_3_REPORT.md
 └── SPRINT_4_REPORT.md
```

Cada arquivo começa vazio, preenchido ao final da sprint pelo time (humano ou IA Documentadora).

---

📌 **Nota:** Esses relatórios funcionam como histórico de evolução e são úteis para onboarding de novos membros e para investidores acompanharem a entrega de valor.
