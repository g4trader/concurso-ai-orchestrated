# Concurso AI Orchestrated

Sistema de orquestração de IA para concursos, organizado em uma arquitetura modular com separação clara entre frontend, backend e recursos compartilhados.

## 📁 Estrutura do Projeto

```
concurso-ai-orchestrated/
├── backend/                    # Serviços backend (Python/FastAPI)
│   ├── ia-0/                  # Serviço de IA 0
│   ├── ia-1/                  # Serviço de IA 1
│   ├── ia-2/                  # Serviço de IA 2
│   ├── ia-3/                  # Serviço de IA 3
│   ├── ops-002/               # Serviço de operações
│   ├── ux-001/                # Serviço de UX
│   ├── web-002/               # Serviço web 2
│   ├── web-003/               # Serviço web 3
│   └── web-004/               # Serviço web 4
├── frontend/                   # Aplicação frontend (Next.js/React)
│   └── web-001/               # Interface web principal
└── shared/                     # Recursos compartilhados
    ├── STORIES/               # Histórias de usuário e especificações
    ├── SCHEMAS/               # Esquemas JSON
    ├── TEMPLATES/             # Templates de documentação
    ├── TOOLS/                 # Ferramentas de desenvolvimento
    ├── RELATORES/             # Relatórios de sprints
    └── playdevs/              # Documentação e configurações
```

## 🚀 Início Rápido

### Backend
Cada serviço backend é independente e pode ser executado separadamente:

```bash
# Navegar para um serviço específico
cd backend/ia-0

# Instalar dependências
pip install -r requirements.txt

# Executar o serviço
python src/main.py
```

### Frontend
A aplicação frontend principal:

```bash
# Navegar para o frontend
cd frontend/web-001

# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run dev
```

## 🏗️ Arquitetura

### Backend
- **Framework**: FastAPI
- **Linguagem**: Python 3.8+
- **Estrutura**: Cada serviço segue o padrão de pastas:
  - `src/api/` - Endpoints da API
  - `src/models/` - Modelos de dados
  - `src/services/` - Lógica de negócio
  - `src/config/` - Configurações
  - `src/utils/` - Utilitários

### Frontend
- **Framework**: Next.js 14
- **Linguagem**: TypeScript
- **Styling**: Tailwind CSS
- **Estrutura**:
  - `src/app/` - Páginas da aplicação
  - `src/components/` - Componentes reutilizáveis
  - `src/hooks/` - Hooks customizados
  - `src/types/` - Definições de tipos

## 📚 Documentação

Toda a documentação do projeto está organizada na pasta `shared/`:

- **Stories**: Histórias de usuário e especificações técnicas
- **Schemas**: Esquemas JSON para validação de dados
- **Templates**: Templates para documentação
- **Relatórios**: Relatórios de sprints e progresso

## 🔧 Desenvolvimento

### Pré-requisitos
- Python 3.8+
- Node.js 18+
- Docker (opcional)

### Scripts Úteis
```bash
# Executar todos os testes do backend
find backend -name "requirements.txt" -execdir pip install -r {} \;

# Executar testes do frontend
cd frontend/web-001 && npm test

# Build de produção do frontend
cd frontend/web-001 && npm run build
```

## 📋 Status do Projeto

Este projeto está em desenvolvimento ativo. Consulte a pasta `shared/RELATORES/` para relatórios de progresso e `shared/ROADMAP.md` para o roadmap do projeto.

## 🤝 Contribuição

Consulte `shared/CONTRIBUTING.md` para diretrizes de contribuição.

## 📄 Licença

Este projeto está licenciado sob a licença especificada no arquivo `LICENSE`.
