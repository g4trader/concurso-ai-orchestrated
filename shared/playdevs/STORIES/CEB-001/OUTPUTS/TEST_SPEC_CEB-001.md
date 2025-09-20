# ESPECIFICAÇÃO DE TESTES CEB-001: Crawler Cebraspe

## Visão Geral

Esta especificação define a estratégia de testes para o sistema de crawling da Cebraspe, cobrindo descoberta de URLs, download de PDFs, deduplicação e indexação de metadados.

## Estratégia de Testes

### 1. Testes Unitários
- **Objetivo**: Validar componentes individuais isoladamente
- **Cobertura**: Mínimo 80% de cobertura de código
- **Ferramentas**: pytest, pytest-cov, pytest-mock

### 2. Testes de Integração
- **Objetivo**: Validar interação entre componentes
- **Cobertura**: Fluxos principais e cenários de erro
- **Ferramentas**: pytest, httpx (para mocking HTTP)

### 3. Testes de Performance
- **Objetivo**: Validar requisitos de performance
- **Cobertura**: Tempo de resposta, uso de memória, concorrência
- **Ferramentas**: pytest-benchmark, memory_profiler

## Casos de Teste

### Discovery Engine

#### Casos Felizes
1. **Descoberta de URLs válidas**
   - **Entrada**: Página HTML com links para PDFs
   - **Saída Esperada**: Lista de URLs com metadados extraídos
   - **Critérios**: URLs válidas, tipos de documento identificados, anos extraídos

2. **Filtragem por tipo de documento**
   - **Entrada**: URLs mistas (editais, provas, gabaritos)
   - **Saída Esperada**: Apenas URLs do tipo especificado
   - **Critérios**: Filtragem correta por padrões de URL

3. **Extração de metadados**
   - **Entrada**: URLs com títulos e anos
   - **Saída Esperada**: Metadados estruturados
   - **Critérios**: Título, tipo, ano extraídos corretamente

#### Casos de Erro
1. **Página inacessível**
   - **Entrada**: URL inválida ou servidor offline
   - **Saída Esperada**: Lista vazia ou erro tratado
   - **Critérios**: Não deve quebrar o sistema

2. **HTML malformado**
   - **Entrada**: HTML inválido ou sem links
   - **Saída Esperada**: Lista vazia
   - **Critérios**: Parser deve ser robusto

3. **Timeout de requisição**
   - **Entrada**: Servidor lento
   - **Saída Esperada**: Timeout após tempo configurado
   - **Critérios**: Não deve travar indefinidamente

### Download Engine

#### Casos Felizes
1. **Download de PDF único**
   - **Entrada**: URL válida de PDF
   - **Saída Esperada**: Arquivo baixado com metadados
   - **Critérios**: Arquivo salvo, hash calculado, tamanho correto

2. **Download concorrente**
   - **Entrada**: Múltiplas URLs
   - **Saída Esperada**: Todos os arquivos baixados
   - **Critérios**: Respeitar limite de concorrência, sem race conditions

3. **Retry em falhas temporárias**
   - **Entrada**: URL com falha intermitente
   - **Saída Esperada**: Sucesso após retry
   - **Critérios**: Backoff exponencial, limite de tentativas

#### Casos de Erro
1. **Arquivo não encontrado (404)**
   - **Entrada**: URL inexistente
   - **Saída Esperada**: Erro tratado, não quebra pipeline
   - **Critérios**: Log de erro, continua processamento

2. **Arquivo corrompido**
   - **Entrada**: PDF inválido
   - **Saída Esperada**: Erro detectado
   - **Critérios**: Validação de integridade

3. **Espaço em disco insuficiente**
   - **Entrada**: Disco cheio
   - **Saída Esperada**: Erro tratado
   - **Critérios**: Verificação prévia de espaço

### Deduplication Engine

#### Casos Felizes
1. **Detecção de duplicatas**
   - **Entrada**: Arquivos com mesmo conteúdo
   - **Saída Esperada**: Duplicatas identificadas
   - **Critérios**: Hash SHA-256 correto, performance adequada

2. **Arquivos únicos**
   - **Entrada**: Arquivos diferentes
   - **Saída Esperada**: Todos considerados únicos
   - **Critérios**: Nenhuma duplicata falsa

3. **Atualização de índice**
   - **Entrada**: Novos arquivos
   - **Saída Esperada**: Índice atualizado
   - **Critérios**: Persistência correta

#### Casos de Erro
1. **Arquivo inacessível**
   - **Entrada**: Arquivo com permissão negada
   - **Saída Esperada**: Erro tratado
   - **Critérios**: Não quebra processamento

2. **Hash inválido**
   - **Entrada**: Arquivo corrompido durante cálculo
   - **Saída Esperada**: Erro detectado
   - **Critérios**: Validação de integridade

### Index Manager

#### Casos Felizes
1. **Criação de índice**
   - **Entrada**: Primeira execução
   - **Saída Esperada**: index.json criado
   - **Critérios**: Estrutura válida, metadados corretos

2. **Atualização incremental**
   - **Entrada**: Novos documentos
   - **Saída Esperada**: Índice atualizado
   - **Critérios**: Backup criado, dados preservados

3. **Consultas ao índice**
   - **Entrada**: Busca por tipo/ano
   - **Saída Esperada**: Resultados corretos
   - **Critérios**: Performance adequada

#### Casos de Erro
1. **Corrupção do índice**
   - **Entrada**: JSON inválido
   - **Saída Esperada**: Recuperação do backup
   - **Critérios**: Robustez contra corrupção

2. **Permissão de escrita negada**
   - **Entrada**: Diretório sem permissão
   - **Saída Esperada**: Erro tratado
   - **Critérios**: Mensagem clara de erro

## Estratégias de Mock

### HTTP Requests
- **Ferramenta**: httpx, aioresponses
- **Estratégia**: Mock de respostas HTTP com diferentes cenários
- **Cenários**: Sucesso, erro 404, timeout, conteúdo inválido

### Sistema de Arquivos
- **Ferramenta**: pytest-mock, tempfile
- **Estratégia**: Uso de diretórios temporários
- **Cenários**: Permissões, espaço em disco, arquivos corrompidos

### Tempo e Data
- **Ferramenta**: freezegun
- **Estratégia**: Mock de datetime para testes determinísticos
- **Cenários**: Timestamps consistentes, timeouts

### Concorrência
- **Ferramenta**: asyncio, pytest-asyncio
- **Estratégia**: Testes com diferentes níveis de concorrência
- **Cenários**: Race conditions, deadlocks

## Configuração de Timeouts

### Discovery Engine
- **Timeout de requisição**: 30 segundos
- **Timeout de parsing**: 5 segundos
- **Timeout total**: 60 segundos

### Download Engine
- **Timeout por arquivo**: 60 segundos
- **Timeout de conexão**: 10 segundos
- **Timeout de leitura**: 30 segundos

### Deduplication Engine
- **Timeout por arquivo**: 10 segundos
- **Timeout de hash**: 5 segundos

### Index Manager
- **Timeout de escrita**: 5 segundos
- **Timeout de backup**: 10 segundos

## Critérios de Cobertura

### Cobertura de Código
- **Mínimo**: 80% de linhas cobertas
- **Máximo**: 95% (evitar over-testing)
- **Foco**: Lógica de negócio, tratamento de erros

### Cobertura de Funcionalidades
- **Descoberta**: 100% dos tipos de documento
- **Download**: 100% dos cenários de erro
- **Deduplicação**: 100% dos algoritmos de hash
- **Indexação**: 100% das operações CRUD

### Cobertura de Integração
- **Pipeline completo**: 100% dos fluxos principais
- **Cenários de erro**: 100% dos tipos de falha
- **Performance**: 100% dos requisitos não funcionais

## Ferramentas Propostas

### Testes Unitários
- **pytest**: Framework principal
- **pytest-cov**: Cobertura de código
- **pytest-mock**: Mocking
- **pytest-asyncio**: Testes assíncronos

### Testes de Integração
- **httpx**: Cliente HTTP para testes
- **aioresponses**: Mock de requisições assíncronas
- **tempfile**: Arquivos temporários

### Testes de Performance
- **pytest-benchmark**: Benchmarking
- **memory_profiler**: Análise de memória
- **psutil**: Monitoramento de sistema

### Qualidade de Código
- **black**: Formatação
- **flake8**: Linting
- **mypy**: Type checking
- **bandit**: Segurança

## Estrutura de Testes

```
tests/
├── unit/
│   ├── test_discovery.py
│   ├── test_downloader.py
│   ├── test_deduplicator.py
│   └── test_indexer.py
├── integration/
│   ├── test_pipeline.py
│   ├── test_error_handling.py
│   └── test_performance.py
├── fixtures/
│   ├── sample_html.py
│   ├── sample_pdfs.py
│   └── mock_responses.py
└── conftest.py
```

## Critérios de Aceite para Testes

### Funcionais
- ✅ Todos os casos felizes passam
- ✅ Todos os casos de erro são tratados
- ✅ Metadados são extraídos corretamente
- ✅ Deduplicação funciona 100%
- ✅ Índice é persistido corretamente

### Não Funcionais
- ✅ Taxa de erro < 3%
- ✅ 0 duplicatas por execução incremental
- ✅ Performance dentro dos limites
- ✅ Uso de memória controlado
- ✅ Logs estruturados em JSON

### Qualidade
- ✅ Cobertura de código ≥ 80%
- ✅ Todos os linters passam
- ✅ Type hints corretos
- ✅ Documentação atualizada
- ✅ Testes são determinísticos


