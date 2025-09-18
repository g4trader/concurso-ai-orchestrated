# Cebraspe Parser OCR

Sistema para extração de texto e metadados de documentos PDF da banca Cebraspe, com suporte a OCR para PDFs baseados em imagem.

## Estrutura do Projeto

```
cebraspe-parser/
├── src/                    # Código fonte principal
├── tests/                  # Testes unitários e integração
├── data/                   # Dados de entrada e saída
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

- 🔍 **Análise de PDF**: Detecção automática de tipo (texto/imagem/misto)
- 📄 **Extração de Texto**: Extração nativa para PDFs com texto
- 👁️ **OCR Engine**: Reconhecimento óptico para PDFs baseados em imagem
- 🏷️ **Classificação**: Identificação automática de tipo de documento
- 🧹 **Normalização**: Limpeza e normalização de texto extraído
- 📊 **Metadados**: Extração e catalogação de metadados
- ✅ **Controle de Qualidade**: Validação de qualidade do texto extraído

## Próximos Passos

Este é um scaffold inicial. Implementar:
1. Análise de tipo de PDF
2. Extração de texto nativo
3. Engine de OCR com Tesseract
4. Sistema de classificação
5. Normalização e limpeza de texto
6. Testes unitários e integração
7. Documentação completa


