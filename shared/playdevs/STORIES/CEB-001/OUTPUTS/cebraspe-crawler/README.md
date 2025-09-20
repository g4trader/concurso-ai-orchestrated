# Cebraspe Crawler

Sistema para descoberta, download e catalogação de documentos públicos da banca Cebraspe.

## Estrutura do Projeto

```
cebraspe-crawler/
├── src/                    # Código fonte principal
├── tests/                  # Testes unitários e integração
├── data/                   # Dados baixados e index
├── logs/                   # Logs do sistema
├── requirements.txt        # Dependências Python
├── .env.example           # Exemplo de configuração
├── .gitignore             # Arquivos ignorados pelo Git
└── Makefile               # Comandos de build/test
```

## Instalação

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure as variáveis de ambiente: `cp .env.example .env`
4. Execute: `python src/main.py`

## Funcionalidades

- Descoberta automática de URLs de PDFs
- Download com controle de concorrência
- Deduplicação por hash SHA-256
- Indexação de metadados em JSON
- Logs estruturados
- Configuração flexível

## Próximos Passos

Este é um scaffold inicial. Implementar:
1. Lógica de descoberta de URLs
2. Sistema de download
3. Deduplicação
4. Testes unitários
5. Documentação completa


