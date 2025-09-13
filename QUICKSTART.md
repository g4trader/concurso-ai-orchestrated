# 🚀 QUICKSTART — Concurso-AI

Guia rápido para começar a usar este repositório com o **Cursor** e instâncias de IA.

---

## 1. Pré-requisitos

- Conta no [GitHub](https://github.com) para hospedar o repositório.  
- [Cursor](https://cursor.sh) instalado e configurado no seu ambiente.  
- Ambiente com Python 3.11+ (para rodar scripts auxiliares).  

---

## 2. Clonar o projeto

```bash
git clone https://github.com/<sua-org>/concurso-ai-orchestrated.git
cd concurso-ai-orchestrated/playdevs
```

---

## 3. Estrutura principal

- `INDEX.md` → homepage do projeto  
- `ROADMAP.md` → visão macro até o MVP  
- `SPRINT_PLAN_SX.yml` → plano da sprint (ordem de histórias)  
- `SPRINT_X_BACKLOG.md` → backlog detalhado (critérios, links)  
- `STORIES/` → cada história com prompts, ordem e outputs  
- `TOOLS/` → guias e validadores de ordem  

---

## 4. Executando uma Sprint no Cursor

1. Abra o Cursor.  
2. Vá até a pasta da sprint desejada (exemplo Sprint 2):  
   - Abra `SPRINT_PLAN_S2.yml`.  
3. Para cada história listada:  
   - Abra a pasta `STORIES/<ID>/`.  
   - Leia `STORY.md` (contexto, valor, critérios).  
   - Siga o `ORDER.yml` passo a passo.  
   - Cada passo ativa uma instância da IA (Arquiteta, Backend, QA, etc).  
   - Salve os resultados em `OUTPUTS/`.  

---

## 5. Pós-execução

- Valide se todos os `postconditions` foram atendidos (arquivos criados, seções obrigatórias).  
- Rode `TOOLS/verify_order_pseudo.py` para conferir consistência dos ORDER.yml.  
- Faça commit e abra PR no GitHub.  

```bash
git add .
git commit -m "Sprint 2 — histórias concluídas"
git push origin main
```

---

## 6. Dicas

- Sempre leia os **Critérios** em `STORY.md` antes de rodar.  
- Use os **prompts de cada papel** em `PROMPTS/`.  
- Se algo falhar, verifique se os **OUTPUTS** estão completos.  
- Consulte `SPRINT_X_BACKLOG.md` para ver critérios de aceite.  
- Use o `INDEX.md` como hub central.  

---

🎯 Com isso, você consegue rodar qualquer sprint, história ou ordem de execução de forma autônoma e consistente no Cursor.
