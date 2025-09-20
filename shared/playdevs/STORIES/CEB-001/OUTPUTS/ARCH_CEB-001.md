# ARQUITETURA CEB-001: Crawler Cebraspe

## 1. Diagrama Textual (Entrada → Processamento → Saída)

```
ENTRADA:
┌─────────────────┐
│ Domínio Cebraspe│
│ (URLs públicas) │
└─────────────────┘
         │
         ▼
PROCESSAMENTO:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Discovery     │───▶│   Download      │───▶│   Deduplication │
│   (URLs/PDFs)   │    │   (PDFs)        │    │   (Hash check)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Metadata      │    │   Storage       │    │   Indexing      │
│   Extraction    │    │   (Local/Cloud) │    │   (index.json)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘

SAÍDA:
┌─────────────────┐
│ index.json      │
│ (metadados)     │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Pipeline        │
│ (downstream)    │
└─────────────────┘
```

## 2. Estrutura de Pastas/Arquivos

```
cebraspe-crawler/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Configurações
│   ├── crawler/
│   │   ├── __init__.py
│   │   ├── discovery.py        # Descoberta de URLs
│   │   ├── downloader.py       # Download de PDFs
│   │   └── deduplicator.py     # Verificação de hash
│   ├── models/
│   │   ├── __init__.py
│   │   └── document.py         # Schemas/DTOs
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── local.py           # Armazenamento local
│   │   └── indexer.py         # Gerenciamento do index.json
│   └── utils/
│       ├── __init__.py
│       ├── logger.py          # Logs JSON
│       └── hasher.py          # Cálculo de hash
├── tests/
│   ├── __init__.py
│   ├── test_discovery.py
│   ├── test_downloader.py
│   ├── test_deduplicator.py
│   └── test_integration.py
├── data/
│   ├── pdfs/                  # PDFs baixados
│   └── index.json            # Metadados catalogados
├── logs/
│   └── crawler.log           # Logs JSON
├── requirements.txt
├── .env.example              # Variáveis de ambiente
├── .gitignore
└── README.md
```

## 3. Contratos (Schemas/DTOs)

### Document Model
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

class DocumentType(Enum):
    EDITAL = "edital"
    PROVA = "prova"
    GABARITO = "gabarito"
    RESULTADO = "resultado"

@dataclass
class DocumentMetadata:
    id: str                    # UUID único
    title: str                 # Título do documento
    document_type: DocumentType
    year: int                  # Ano do documento
    url: str                   # URL original
    local_path: str            # Caminho local do PDF
    file_hash: str             # SHA-256 do arquivo
    file_size: int             # Tamanho em bytes
    download_date: datetime    # Data do download
    source_domain: str         # Domínio de origem
    additional_metadata: Optional[dict] = None

@dataclass
class CrawlerConfig:
    base_url: str = "https://www.cebraspe.org.br"
    max_concurrent_downloads: int = 5
    request_timeout: int = 30
    retry_attempts: int = 3
    output_dir: str = "./data"
    log_level: str = "INFO"
    user_agent: str = "CebraspeCrawler/1.0"

@dataclass
class CrawlerStats:
    total_discovered: int = 0
    total_downloaded: int = 0
    total_duplicates: int = 0
    total_errors: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
```

### API Response Examples
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Edital Concurso Público 2024",
  "document_type": "edital",
  "year": 2024,
  "url": "https://www.cebraspe.org.br/concursos/edital_2024.pdf",
  "local_path": "./data/pdfs/edital_2024_550e8400.pdf",
  "file_hash": "a1b2c3d4e5f6...",
  "file_size": 2048576,
  "download_date": "2024-01-15T10:30:00Z",
  "source_domain": "cebraspe.org.br",
  "additional_metadata": {
    "concurso": "Concurso Público 2024",
    "orgao": "Ministério da Educação"
  }
}
```

## 4. Decisões e Trade-offs

### Arquitetura
- **Decisão**: Crawler síncrono com pool de threads limitado
- **Trade-off**: Simplicidade vs. Performance máxima
- **Justificativa**: Para MVP, simplicidade é mais importante que throughput máximo

### Armazenamento
- **Decisão**: Sistema híbrido (local + index JSON)
- **Trade-off**: Complexidade vs. Portabilidade
- **Justificativa**: Facilita desenvolvimento e testes, permite migração futura para cloud

### Deduplicação
- **Decisão**: Hash SHA-256 por arquivo completo
- **Trade-off**: CPU vs. Precisão
- **Justificativa**: SHA-256 é padrão, balanceia performance e confiabilidade

### Logging
- **Decisão**: Logs estruturados em JSON
- **Trade-off**: Legibilidade humana vs. Processamento automático
- **Justificativa**: Facilita monitoramento e debugging em produção

### Configuração
- **Decisão**: Arquivo .env + configuração programática
- **Trade-off**: Flexibilidade vs. Simplicidade
- **Justificativa**: Permite diferentes ambientes sem hardcoding

## 5. Checklist de Implementação

### Fase 1: Core Infrastructure (P)
- [ ] Configurar estrutura de pastas
- [ ] Implementar sistema de logging JSON
- [ ] Criar modelos de dados (DocumentMetadata, CrawlerConfig)
- [ ] Configurar ambiente de desenvolvimento

### Fase 2: Discovery Engine (M)
- [ ] Implementar descoberta de URLs do domínio Cebraspe
- [ ] Criar parser para identificar links de PDFs
- [ ] Implementar filtros por tipo de documento
- [ ] Adicionar validação de URLs

### Fase 3: Download System (M)
- [ ] Implementar downloader com retry logic
- [ ] Adicionar controle de concorrência
- [ ] Implementar verificação de integridade
- [ ] Criar sistema de timeouts e rate limiting

### Fase 4: Deduplication (P)
- [ ] Implementar cálculo de hash SHA-256
- [ ] Criar sistema de verificação de duplicatas
- [ ] Implementar index de hashes existentes
- [ ] Adicionar logs de duplicatas encontradas

### Fase 5: Storage & Indexing (P)
- [ ] Implementar armazenamento local de PDFs
- [ ] Criar sistema de indexação em JSON
- [ ] Implementar backup e recuperação do index
- [ ] Adicionar compressão de metadados

### Fase 6: Integration & Testing (M)
- [ ] Criar testes unitários para cada módulo
- [ ] Implementar testes de integração
- [ ] Adicionar testes de performance
- [ ] Criar testes de cenários de erro

### Fase 7: Documentation & Deployment (P)
- [ ] Documentar APIs e configurações
- [ ] Criar exemplos de uso
- [ ] Implementar sistema de monitoramento
- [ ] Preparar para deploy em produção

**Legenda de Esforço:**
- P = Pequeno (1-2 dias)
- M = Médio (3-5 dias)  
- G = Grande (1+ semana)

**Total Estimado: 3-4 semanas para implementação completa**


