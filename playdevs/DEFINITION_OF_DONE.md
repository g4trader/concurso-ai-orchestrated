# ✅ Definition of Done (DoD)

## Critérios para Considerar uma História "Pronta"

### 1. Arquitetura ✅
- [ ] **ARCH_{ID}.md** criado e aprovado
- [ ] Diagramas de arquitetura incluídos
- [ ] Decisões arquiteturais documentadas
- [ ] Estrutura de pastas definida
- [ ] Contratos de API especificados
- [ ] Checklist de implementação completo

### 2. Implementação ✅
- [ ] **CODE_SCAFFOLD_{ID}.zip** gerado
- [ ] Estrutura de pastas implementada
- [ ] Arquivos README/NOTES criados
- [ ] Requirements/dependencies listados
- [ ] Scripts de build/test como placeholders
- [ ] Código segue padrões definidos

### 3. Testes ✅
- [ ] **TEST_SPEC_{ID}.md** criado
- [ ] Casos de teste felizes definidos
- [ ] Casos de erro especificados
- [ ] Mocks e stubs definidos
- [ ] Timeouts e edge cases cobertos
- [ ] Cobertura de testes ≥70%

### 4. Documentação ✅
- [ ] **README_{ID}.md** criado
- [ ] Objetivo da história explicado
- [ ] Instruções de execução claras
- [ ] APIs documentadas
- [ ] Variáveis de ambiente listadas
- [ ] Limitações conhecidas documentadas

### 5. Review de Qualidade ✅
- [ ] **REVIEW_{ID}.md** aprovado
- [ ] Pontos fortes identificados
- [ ] Riscos mapeados
- [ ] Gaps identificados
- [ ] MUST-FIX resolvidos
- [ ] Nota final ≥7/10

### 6. Validação Técnica ✅
- [ ] Postconditions do ORDER.yml validadas
- [ ] Arquivos de output existem
- [ ] Conteúdo obrigatório presente
- [ ] Estrutura de dados correta
- [ ] Integração com dependências testada

### 7. Integração ✅
- [ ] Artefatos integrados ao repositório
- [ ] PR criado e aprovado
- [ ] Merge realizado sem conflitos
- [ ] Histórico de commits limpo
- [ ] Tags e releases atualizadas

### 8. Aceitação do PO ✅
- [ ] Critérios de aceite da STORY.md cumpridos
- [ ] Valor de negócio entregue
- [ ] Demonstração realizada
- [ ] Feedback incorporado
- [ ] Aprovação formal do PO

## Critérios por Tipo de História

### Histórias de Coleta (CEB-*)
- [ ] Crawler funcional
- [ ] Dados coletados e validados
- [ ] Metadados estruturados
- [ ] Logs de execução completos
- [ ] Deduplicação funcionando

### Histórias de IA (IA-*)
- [ ] Modelos configurados
- [ ] Pipeline de processamento funcional
- [ ] Métricas de qualidade definidas
- [ ] Avaliação offline implementada
- [ ] Performance dentro dos limites

### Histórias de Frontend (WEB-*)
- [ ] Interface funcional
- [ ] Responsividade testada
- [ ] Acessibilidade validada
- [ ] Performance otimizada
- [ ] UX aprovada

### Histórias de Operações (OPS-*)
- [ ] Deploy automatizado
- [ ] Monitoramento configurado
- [ ] Logs centralizados
- [ ] Alertas funcionando
- [ ] Backup e recovery testados

## Critérios de Qualidade

### Código
- [ ] Segue padrões de codificação
- [ ] Comentários adequados
- [ ] Tratamento de erros implementado
- [ ] Logs informativos
- [ ] Configuração externalizada

### Documentação
- [ ] Linguagem clara e objetiva
- [ ] Exemplos práticos incluídos
- [ ] Diagramas atualizados
- [ ] Links funcionando
- [ ] Versão controlada

### Testes
- [ ] Cobertura adequada
- [ ] Casos edge cobertos
- [ ] Mocks apropriados
- [ ] Dados de teste realistas
- [ ] Execução automatizada

## Escalação

### Quando NÃO está "Done"
- [ ] Qualquer critério acima não atendido
- [ ] MUST-FIX pendente no review
- [ ] Bloqueio técnico não resolvido
- [ ] Dependência externa não satisfeita
- [ ] Critério de aceite não cumprido

### Processo de Escalação
1. **Agente** identifica critério não atendido
2. **Scrum Master** avalia impacto
3. **PO** decide se aceita ou rejeita
4. **Time** implementa correções
5. **Reviewer** valida novamente

---

**Versão**: 1.0
**Última Atualização**: [Data]
**Aprovado por**: PO
