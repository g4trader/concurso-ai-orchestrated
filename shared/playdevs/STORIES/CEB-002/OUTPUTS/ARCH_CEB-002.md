# ARQUITETURA CEB-002: Parser OCR — Extrair Texto e Metadados

## 1. Diagrama Textual (Entrada → Processamento → Saída)

```
ENTRADA:
┌─────────────────┐
│ PDFs catalogados│
│ (do CEB-001)    │
└─────────────────┘
         │
         ▼
PROCESSAMENTO:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PDF Analysis  │───▶│   Text Extract  │───▶│   OCR Engine    │
│   (tipo/estado) │    │   (PDFs texto)  │    │   (PDFs imagem) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Classification│    │   Normalization │    │   Text Cleanup  │
│   (tipo doc)    │    │   (charset)     │    │   (OCR errors)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Metadata      │    │   File Output   │    │   Quality       │
│   Extraction    │    │   (.txt + JSON) │    │   Validation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘

SAÍDA:
┌─────────────────┐
│ .txt files      │
│ (texto limpo)   │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ JSON metadata   │
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
cebraspe-parser/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Configurações
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── pdf_analyzer.py     # Análise de tipo de PDF
│   │   ├── text_extractor.py   # Extração de texto nativo
│   │   ├── ocr_engine.py       # OCR para PDFs imagem
│   │   └── classifier.py       # Classificação de documentos
│   ├── models/
│   │   ├── __init__.py
│   │   └── document.py         # Schemas/DTOs
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── normalizer.py       # Normalização de texto
│   │   ├── cleaner.py          # Limpeza de texto OCR
│   │   └── validator.py        # Validação de qualidade
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── file_manager.py     # Gerenciamento de arquivos
│   │   └── metadata_store.py   # Armazenamento de metadados
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Logs JSON
│       └── image_utils.py      # Utilitários de imagem
├── tests/
│   ├── __init__.py
│   ├── test_pdf_analyzer.py
│   ├── test_text_extractor.py
│   ├── test_ocr_engine.py
│   ├── test_classifier.py
│   ├── test_normalizer.py
│   └── test_integration.py
├── data/
│   ├── input/                  # PDFs de entrada
│   ├── output/                 # Textos extraídos
│   │   ├── txt/               # Arquivos .txt
│   │   └── metadata/          # Arquivos JSON
│   └── models/                # Modelos de classificação
├── logs/
│   └── parser.log             # Logs JSON
├── requirements.txt
├── .env.example               # Variáveis de ambiente
├── .gitignore
└── README.md
```

## 3. Contratos (Schemas/DTOs)

### Document Processing Models
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

class PDFType(Enum):
    """Tipos de PDF identificados"""
    TEXT_BASED = "text_based"      # PDF com texto nativo
    IMAGE_BASED = "image_based"    # PDF com imagens (requer OCR)
    MIXED = "mixed"                # PDF misto
    UNKNOWN = "unknown"            # Tipo não identificado

class DocumentClass(Enum):
    """Classes de documento"""
    EDITAL = "edital"
    PROVA = "prova"
    GABARITO = "gabarito"
    RETIFICACAO = "retificacao"
    RESULTADO = "resultado"
    OUTRO = "outro"

class ProcessingStatus(Enum):
    """Status do processamento"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class PDFAnalysis:
    """Análise de um arquivo PDF"""
    file_path: str
    file_size: int
    page_count: int
    pdf_type: PDFType
    has_text: bool
    has_images: bool
    image_count: int
    text_quality_score: float  # 0.0 a 1.0
    analysis_timestamp: datetime

@dataclass
class ExtractedText:
    """Texto extraído de um documento"""
    original_file: str
    extracted_text: str
    page_count: int
    word_count: int
    char_count: int
    extraction_method: str  # "native" ou "ocr"
    confidence_score: float  # 0.0 a 1.0
    processing_time: float   # segundos
    extraction_timestamp: datetime

@dataclass
class DocumentMetadata:
    """Metadados de um documento processado"""
    document_id: str
    original_file: str
    document_class: DocumentClass
    title: str
    year: int
    organization: str
    extracted_text_file: str
    metadata_file: str
    processing_status: ProcessingStatus
    quality_score: float
    processing_timestamp: datetime
    additional_metadata: Optional[Dict[str, Any]] = None

@dataclass
class ProcessingConfig:
    """Configurações do processamento"""
    # OCR Settings
    ocr_engine: str = "tesseract"
    ocr_language: str = "por"
    ocr_dpi: int = 300
    
    # Text Processing
    min_confidence: float = 0.7
    max_processing_time: int = 300  # segundos
    
    # Output Settings
    output_encoding: str = "utf-8"
    preserve_formatting: bool = False
    
    # Performance
    max_concurrent_jobs: int = 3
    batch_size: int = 10
    
    # Quality Control
    enable_quality_check: bool = True
    min_text_length: int = 100
    max_file_size_mb: int = 50
```

### API Response Examples
```json
{
  "document_id": "doc_550e8400-e29b-41d4-a716-446655440000",
  "original_file": "./data/input/edital_2024.pdf",
  "document_class": "edital",
  "title": "Edital Concurso Público 2024",
  "year": 2024,
  "organization": "Cebraspe",
  "extracted_text_file": "./data/output/txt/edital_2024.txt",
  "metadata_file": "./data/output/metadata/edital_2024.json",
  "processing_status": "completed",
  "quality_score": 0.95,
  "processing_timestamp": "2024-01-15T10:30:00Z",
  "additional_metadata": {
    "page_count": 45,
    "word_count": 12500,
    "extraction_method": "native",
    "confidence_score": 0.98,
    "processing_time": 2.5
  }
}
```

## 4. Decisões e Trade-offs

### Arquitetura de Processamento
- **Decisão**: Pipeline sequencial com análise prévia de tipo
- **Trade-off**: Simplicidade vs. Performance máxima
- **Justificativa**: Análise prévia evita OCR desnecessário em PDFs com texto nativo

### Engine de OCR
- **Decisão**: Tesseract como engine principal
- **Trade-off**: Precisão vs. Velocidade
- **Justificativa**: Tesseract oferece boa precisão para português e é open-source

### Estratégia de Fallback
- **Decisão**: OCR apenas quando necessário
- **Trade-off**: Complexidade vs. Eficiência
- **Justificativa**: PDFs com texto nativo são mais rápidos e precisos

### Armazenamento de Metadados
- **Decisão**: JSON separado por documento
- **Trade-off**: Fragmentação vs. Flexibilidade
- **Justificativa**: Facilita consultas individuais e evita arquivos grandes

### Controle de Qualidade
- **Decisão**: Validação pós-processamento
- **Trade-off**: Tempo vs. Confiabilidade
- **Justificativa**: Garante qualidade mínima antes de disponibilizar texto

### Configuração
- **Decisão**: Configuração via arquivo + variáveis de ambiente
- **Trade-off**: Flexibilidade vs. Simplicidade
- **Justificativa**: Permite ajustes finos sem recompilação

## 5. Checklist de Implementação

### Fase 1: Core Infrastructure (P)
- [ ] Configurar estrutura de pastas
- [ ] Implementar sistema de logging JSON
- [ ] Criar modelos de dados (PDFAnalysis, ExtractedText, DocumentMetadata)
- [ ] Configurar ambiente de desenvolvimento

### Fase 2: PDF Analysis Engine (M)
- [ ] Implementar análise de tipo de PDF
- [ ] Criar detector de texto nativo vs. imagem
- [ ] Implementar contagem de páginas e imagens
- [ ] Adicionar cálculo de score de qualidade

### Fase 3: Text Extraction (M)
- [ ] Implementar extração de texto nativo
- [ ] Criar parser para diferentes formatos de PDF
- [ ] Implementar extração de metadados do PDF
- [ ] Adicionar tratamento de encoding

### Fase 4: OCR Engine (G)
- [ ] Integrar Tesseract OCR
- [ ] Implementar pré-processamento de imagens
- [ ] Criar sistema de detecção de layout
- [ ] Adicionar pós-processamento de texto OCR

### Fase 5: Text Processing (M)
- [ ] Implementar normalização de texto
- [ ] Criar sistema de limpeza de erros OCR
- [ ] Implementar validação de charset UTF-8
- [ ] Adicionar preservação de formatação

### Fase 6: Document Classification (M)
- [ ] Implementar classificação por padrões
- [ ] Criar sistema de detecção de tipo de documento
- [ ] Implementar extração de metadados específicos
- [ ] Adicionar validação de classificação

### Fase 7: Quality Control (P)
- [ ] Implementar validação de qualidade
- [ ] Criar sistema de scoring de confiança
- [ ] Implementar detecção de erros
- [ ] Adicionar relatórios de qualidade

### Fase 8: File Management (P)
- [ ] Implementar gerenciamento de arquivos
- [ ] Criar sistema de backup
- [ ] Implementar limpeza de arquivos temporários
- [ ] Adicionar verificação de integridade

### Fase 9: Integration & Testing (M)
- [ ] Criar testes unitários para cada módulo
- [ ] Implementar testes de integração
- [ ] Adicionar testes de performance
- [ ] Criar testes com PDFs reais

### Fase 10: Documentation & Deployment (P)
- [ ] Documentar APIs e configurações
- [ ] Criar exemplos de uso
- [ ] Implementar sistema de monitoramento
- [ ] Preparar para deploy em produção

**Legenda de Esforço:**
- P = Pequeno (1-2 dias)
- M = Médio (3-5 dias)  
- G = Grande (1+ semana)

**Total Estimado: 4-5 semanas para implementação completa**

### Dependências Externas
- **Tesseract OCR**: Engine de OCR
- **PyPDF2/pdfplumber**: Extração de texto nativo
- **Pillow**: Processamento de imagens
- **pytesseract**: Interface Python para Tesseract


