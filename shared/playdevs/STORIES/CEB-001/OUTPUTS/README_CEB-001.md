# Cebraspe Crawler - Documentação Técnica

## 1. Objetivo e Contexto

### Objetivo
O **Cebraspe Crawler** é um sistema automatizado para descoberta, download e catalogação de documentos públicos da banca Cebraspe (Centro Brasileiro de Pesquisa em Avaliação e Seleção e de Promoção de Eventos). O sistema serve como base inicial para análise de editais e geração de simulados.

### Contexto de Negócio
- **Usuário**: Pipeline de ingestão (downstream: parser/IA)
- **Valor**: Base inicial para análise de editais e geração de simulados
- **Domínio**: Documentos públicos (editais, provas, gabaritos, resultados)
- **Fonte**: Site oficial da Cebraspe (https://www.cebraspe.org.br)

### Funcionalidades Principais
- 🔍 **Descoberta Automática**: Navegação e identificação de URLs de PDFs
- 📥 **Download Inteligente**: Download com controle de concorrência e retry logic
- 🔄 **Deduplicação**: Verificação de duplicatas por hash SHA-256
- 📚 **Indexação**: Catalogação de metadados em formato JSON
- 📊 **Logs Estruturados**: Logs em formato JSON para monitoramento

## 2. Como Rodar (Passo a Passo Conceitual)

### Pré-requisitos
- Python 3.8+
- Acesso à internet
- Espaço em disco adequado (configurável)

### Instalação
```bash
# 1. Extrair o scaffold
unzip CODE_SCAFFOLD_CEB-001.zip
cd cebraspe-crawler

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar ambiente
cp .env.example .env
# Editar .env com suas configurações
```

### Execução Básica
```bash
# Execução simples
python src/main.py

# Modo debug
python src/main.py --debug

# Modo dry-run (sem downloads reais)
python src/main.py --dry-run
```

### Fluxo de Execução Conceitual

1. **Inicialização**
   - Carregamento de configurações
   - Setup de logging
   - Verificação de diretórios

2. **Descoberta de URLs**
   - Navegação no site da Cebraspe
   - Identificação de links para PDFs
   - Extração de metadados (título, tipo, ano)

3. **Download de Arquivos**
   - Download assíncrono com controle de concorrência
   - Verificação de integridade
   - Retry em caso de falhas

4. **Deduplicação**
   - Cálculo de hash SHA-256
   - Verificação contra índice existente
   - Filtragem de duplicatas

5. **Indexação**
   - Atualização do index.json
   - Backup do índice anterior
   - Geração de estatísticas

6. **Finalização**
   - Relatório de execução
   - Logs de performance
   - Limpeza de arquivos temporários

## 3. APIs (Se Houver) com Exemplos

### Configuração Programática
```python
from src.config.settings import CrawlerConfig
from src.crawler.discovery import DiscoveryEngine
from src.crawler.downloader import DownloadEngine

# Configuração customizada
config = CrawlerConfig(
    base_url="https://www.cebraspe.org.br",
    max_concurrent_downloads=3,
    request_timeout=30,
    output_dir="./custom_data"
)

# Uso dos componentes
discovery = DiscoveryEngine(config)
downloader = DownloadEngine(config)

# Descoberta de URLs
urls = await discovery.discover_urls()

# Download de arquivos
files = await downloader.download_pdfs(urls)
```

### Consulta ao Índice
```python
from src.storage.indexer import IndexManager

# Carregar índice
indexer = IndexManager(config)

# Buscar por tipo
editais = indexer.get_documents_by_type("edital")

# Buscar por ano
docs_2024 = indexer.get_documents_by_year(2024)

# Buscar por hash
doc = indexer.get_document_by_hash("abc123...")

# Estatísticas
stats = indexer.get_stats()
```

### Modelos de Dados
```python
from src.models.document import DocumentMetadata, DocumentType

# Criar metadados
metadata = DocumentMetadata.create(
    title="Edital Concurso 2024",
    document_type=DocumentType.EDITAL,
    year=2024,
    url="https://www.cebraspe.org.br/edital.pdf",
    local_path="./data/pdfs/edital.pdf",
    file_hash="sha256_hash_here",
    file_size=2048576,
    source_domain="cebraspe.org.br"
)

# Converter para dicionário
data = metadata.to_dict()
```

## 4. Variáveis de Ambiente e Logs

### Variáveis de Ambiente (.env)
```bash
# URLs e domínios
CEBRASPE_BASE_URL=https://www.cebraspe.org.br
USER_AGENT=CebraspeCrawler/1.0

# Configurações de download
MAX_CONCURRENT_DOWNLOADS=5
REQUEST_TIMEOUT=30
RETRY_ATTEMPTS=3
RATE_LIMIT_DELAY=1.0

# Diretórios
OUTPUT_DIR=./data
PDFS_DIR=./data/pdfs
LOGS_DIR=./logs

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Modo de operação
DEBUG=false
DRY_RUN=false
```

### Estrutura de Logs
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "logger": "src.crawler.discovery",
  "message": "Descobertas 15 URLs",
  "module": "discovery",
  "function": "discover_urls",
  "line": 45,
  "extra_fields": {
    "urls_found": 15,
    "processing_time": 2.5
  }
}
```

### Níveis de Log
- **DEBUG**: Informações detalhadas para desenvolvimento
- **INFO**: Informações gerais sobre o progresso
- **WARNING**: Situações que podem causar problemas
- **ERROR**: Erros que não impedem a execução
- **CRITICAL**: Erros que impedem a execução

### Arquivos de Log
- `logs/crawler.log`: Log principal em formato JSON
- Console: Logs em formato legível para desenvolvimento

## 5. Limitações e Próximos Passos

### Limitações Atuais

#### Funcionais
- **Descoberta**: Limitada a padrões conhecidos de URLs
- **Tipos de Documento**: Suporte apenas para editais, provas, gabaritos e resultados
- **Formato**: Apenas arquivos PDF são processados
- **Domínio**: Limitado ao site oficial da Cebraspe

#### Técnicas
- **Concorrência**: Máximo de 5 downloads simultâneos (configurável)
- **Timeout**: 30 segundos por requisição (configurável)
- **Armazenamento**: Apenas armazenamento local
- **Deduplicação**: Baseada apenas em hash de arquivo

#### Operacionais
- **Monitoramento**: Logs básicos, sem métricas avançadas
- **Recuperação**: Backup manual do índice
- **Escalabilidade**: Não testado com grandes volumes

### Próximos Passos

#### Curto Prazo (Sprint 2)
1. **Implementação Completa**
   - Finalizar lógica de descoberta de URLs
   - Implementar sistema de download real
   - Completar deduplicação e indexação

2. **Testes e Qualidade**
   - Implementar testes unitários e integração
   - Configurar CI/CD
   - Adicionar linting e type checking

3. **Documentação**
   - Documentar APIs internas
   - Criar guias de troubleshooting
   - Adicionar exemplos de uso

#### Médio Prazo (Sprint 3-4)
1. **Melhorias de Performance**
   - Otimização de algoritmos de descoberta
   - Implementação de cache
   - Paralelização de processamento

2. **Robustez**
   - Sistema de retry mais sofisticado
   - Detecção de mudanças no site
   - Recuperação automática de falhas

3. **Monitoramento**
   - Métricas de performance
   - Alertas automáticos
   - Dashboard de status

#### Longo Prazo (Futuro)
1. **Escalabilidade**
   - Suporte a múltiplas fontes
   - Armazenamento em nuvem
   - Processamento distribuído

2. **Inteligência**
   - ML para classificação de documentos
   - Detecção automática de novos tipos
   - Análise de conteúdo

3. **Integração**
   - APIs REST para consulta
   - Webhooks para notificações
   - Integração com sistemas downstream

### Dependências Externas
- **Site da Cebraspe**: Disponibilidade e estrutura das páginas
- **Rede**: Conectividade e velocidade de internet
- **Sistema**: Espaço em disco e recursos computacionais

### Riscos Identificados
1. **Mudanças no Site**: Alterações na estrutura podem quebrar a descoberta
2. **Rate Limiting**: Limitações do servidor podem afetar performance
3. **Volume de Dados**: Crescimento pode impactar performance
4. **Manutenção**: Necessidade de atualizações regulares

### Critérios de Sucesso
- ✅ Taxa de erro < 3%
- ✅ 0 duplicatas por execução incremental
- ✅ Performance razoável (< 1 min por 100 documentos)
- ✅ Logs estruturados e informativos
- ✅ Cobertura de testes > 80%
- ✅ Documentação completa e atualizada


