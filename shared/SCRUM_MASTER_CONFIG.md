# 🤖 Scrum Master - Configuração e Protocolos

## 📋 Papel e Responsabilidades

O **Scrum Master** é o agente orquestrador que:
- Recebe diretrizes do PO
- Interpreta roadmap e prioridades
- Delega tarefas para agentes especializados
- Monitora progresso e reporta status
- Gerencia dependências entre histórias
- Facilita comunicação entre agentes

## 🎯 Agentes Disponíveis

### **Arquiteta**
- **Função**: Define arquitetura e estrutura técnica
- **Input**: STORY.md + contexto do projeto
- **Output**: ARCH_{STORY_ID}.md
- **Prompt**: `PROMPTS/ARCHITECT.txt`

### **Backend Developer**
- **Função**: Implementa código e APIs
- **Input**: Arquitetura + especificações
- **Output**: CODE_SCAFFOLD_{STORY_ID}.zip
- **Prompt**: `PROMPTS/BACKEND.txt`

### **Data/ML Engineer**
- **Função**: Trabalha com dados e modelos de IA
- **Input**: Especificações de ML/IA
- **Output**: ML_PIPELINE_{STORY_ID}.zip
- **Prompt**: `PROMPTS/DATA_ML.txt`

### **QA Engineer**
- **Função**: Cria especificações de teste
- **Input**: Código + arquitetura
- **Output**: TEST_SPEC_{STORY_ID}.md
- **Prompt**: `PROMPTS/QA.txt`

### **Technical Writer**
- **Função**: Gera documentação técnica
- **Input**: Arquitetura + testes
- **Output**: README_{STORY_ID}.md
- **Prompt**: `PROMPTS/DOCS.txt`

### **Reviewer**
- **Função**: Avalia qualidade e integridade
- **Input**: Todos os outputs da história
- **Output**: REVIEW_{STORY_ID}.md
- **Prompt**: `PROMPTS/REVIEW.txt`

## 🔄 Protocolo de Comunicação

### **PO → Scrum Master**
```
Comando: "Execute Sprint 2"
Scrum Master interpreta: 
- Sprint 2 = IA-0 + IA-1
- Dependências: IA-0 deve ser executado antes de IA-1
- Agentes necessários: Arquiteta, Backend, Data/ML, QA, Docs, Review
```

### **Scrum Master → Agentes**
```
Para Arquiteta:
"Execute história IA-0: Infraestrutura IA
- Input: STORIES/IA-0/STORY.md
- Prompt: STORIES/IA-0/PROMPTS/ARCHITECT.txt
- Output: STORIES/IA-0/OUTPUTS/ARCH_IA-0.md
- Deadline: [data]
- Dependências: nenhuma"
```

### **Agentes → Scrum Master**
```
Status Report:
- História: IA-0
- Agente: Arquiteta
- Status: 80% completo
- Bloqueios: Precisa de decisão sobre modelo LLM
- Próximo passo: Aguardando input do PO
```

## 📊 Status Tracking

### **Estados de História**
- 🔴 **Não iniciada**
- 🟡 **Em progresso**
- 🟢 **Completa**
- ⚠️ **Bloqueada**
- ❌ **Falhou**

### **Estados de Agente**
- 🟢 **Disponível**
- 🟡 **Trabalhando**
- 🔴 **Bloqueado**
- ⏸️ **Aguardando**

## 🎯 Comandos do PO

### **Comandos de Sprint**
- `"Execute Sprint X"` - Inicia execução da sprint
- `"Pause Sprint X"` - Pausa execução
- `"Status Sprint X"` - Relatório de status

### **Comandos de História**
- `"Execute História Y"` - Executa história específica
- `"Priorizar História Y"` - Muda prioridade
- `"Cancelar História Y"` - Cancela execução

### **Comandos de Agente**
- `"Status Agente X"` - Status do agente
- `"Reatribuir História Y para Agente Z"` - Reatribui tarefa

## 📈 Métricas e Relatórios

### **Daily Standup (Virtual)**
- O que foi feito ontem?
- O que será feito hoje?
- Há bloqueios?

### **Sprint Review**
- Histórias completadas
- Histórias não completadas
- Métricas de qualidade
- Lições aprendidas

### **Retrospectiva**
- O que funcionou bem?
- O que pode ser melhorado?
- Ações para próxima sprint

## 🚨 Escalação

### **Níveis de Escalação**
1. **Agente → Scrum Master**: Bloqueios técnicos
2. **Scrum Master → PO**: Decisões de negócio
3. **PO → Stakeholders**: Mudanças de escopo

### **Critérios de Escalação**
- Bloqueio > 24h
- Decisão de arquitetura crítica
- Mudança de escopo
- Risco de deadline

---

**Nota**: Este arquivo serve como guia para o Scrum Master orquestrar o trabalho dos agentes de forma eficiente e organizada.
