# Cebraspe Parser OCR - Documentação Técnica

## 1. Objetivo e Contexto

### Objetivo
O **Cebraspe Parser OCR** é um sistema automatizado para extração de texto e metadados de documentos PDF da banca Cebraspe, com suporte a reconhecimento óptico de caracteres (OCR) para PDFs baseados em imagem. O sistema transforma PDFs em texto pesquisável com fallback para OCR quando necessário.

### Contexto de Negócio
- **Usuário**: Módulo de IA e busca (downstream)
- **Valor**: Texto limpo e metadados para extração de conteúdo programático e indexação
- **Domínio**: Documentos públicos da Cebraspe (editais, provas, gabaritos, resultados)
- **Dependência**: CEB-001 (Crawler Cebraspe) para fornecimento de PDFs

### Funcionalidades Principais
- 🔍 **Análise de PDF**: Detecção automática de tipo (texto/imagem/misto)
- 📄 **Extração de Texto**: Extração nativa para PDFs com texto
- 👁️ **OCR Engine**: Reconhecimento óptico para PDFs baseados em imagem
- 🏷️ **Classificação**: Identificação automática de tipo de documento
- 🧹 **Normalização**: Limpeza e normalização de texto extraído
- 📊 **Metadados**: Extração e catalogação de metadados
- ✅ **Controle de Qualidade**: Validação de qualidade do texto extraído

## 2. Como Rodar (Passo a Passo Conceitual)

### Pré-requisitos
- Python 3.8+
- Tesseract OCR instalado
- Acesso aos PDFs catalogados pelo CEB-001
- Espaço em disco adequado

### Instalação
```bash
# 1. Extrair o scaffold
unzip CODE_SCAFFOLD_CEB-002.zip
cd cebraspe-parser

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar Tesseract OCR
make setup-ocr

# 4. Configurar ambiente
cp .env.example .env
# Editar .env com suas configurações
```

### Execução Básica
```bash
# Execução simples
python src/main.py

# Modo debug
python src/main.py --debug

# Modo dry-run (sem processamento real)
python src/main.py --dry-run

# Processar arquivos específicos
python src/main.py --input ./data/input --output ./data/output
```

### Fluxo de Execução Conceitual

1. **Inicialização**
   - Carregamento de configurações
   - Setup de logging
   - Verificação de dependências (Tesseract)

2. **Análise de PDFs**
   - Escaneamento de arquivos de entrada
   - Análise de tipo de PDF (texto/imagem/misto)
   - Extração de metadados básicos
   - Cálculo de score de qualidade

3. **Extração de Texto**
   - **PDFs com texto nativo**: Extração direta
   - **PDFs baseados em imagem**: Conversão para OCR
   - **PDFs mistos**: Estratégia híbrida

4. **Processamento OCR** (quando necessário)
   - Conversão de PDF para imagens
   - Pré-processamento de imagens
   - Reconhecimento óptico com Tesseract
   - Pós-processamento de texto

5. **Classificação de Documentos**
   - Identificação de tipo (edital/prova/gabarito)
   - Extração de metadados específicos
   - Validação de classificação

6. **Normalização de Texto**
   - Limpeza de erros de OCR
   - Normalização de charset UTF-8
   - Preservação de formatação
   - Validação de qualidade

7. **Geração de Saída**
   - Salvamento de arquivos .txt
   - Geração de metadados JSON
   - Backup de arquivos processados
   - Relatório de processamento

8. **Finalização**
   - Estatísticas de processamento
   - Logs de qualidade
   - Limpeza de arquivos temporários

## 3. APIs (Se Houver) com Exemplos

### Configuração Programática
```python
from src.config.settings import ProcessingConfig
from src.parser.pdf_analyzer import PDFAnalyzer
from src.parser.text_extractor import TextExtractor
from src.parser.ocr_engine import OCREngine

# Configuração customizada
config = ProcessingConfig(
    ocr_engine="tesseract",
    ocr_language="por",
    ocr_dpi=300,
    min_confidence=0.7,
    output_encoding="utf-8"
)

# Uso dos componentes
analyzer = PDFAnalyzer(config)
text_extractor = TextExtractor(config)
ocr_engine = OCREngine(config)

# Análise de PDF
analysis = analyzer.analyze_pdf("documento.pdf")

# Extração baseada no tipo
if analysis.pdf_type == PDFType.TEXT_BASED:
    extracted_text = text_extractor.extract_text("documento.pdf")
else:
    extracted_text = ocr_engine.extract_text_ocr("documento.pdf")
```

### Processamento de Lote
```python
from src.storage.file_manager import FileManager
from src.processing.normalizer import TextNormalizer

# Gerenciamento de arquivos
file_manager = FileManager(config)
normalizer = TextNormalizer(config)

# Processar lote de arquivos
pdf_files = file_manager.get_input_files()

for pdf_file in pdf_files:
    # Análise
    analysis = analyzer.analyze_pdf(pdf_file)
    
    # Extração
    if analysis.pdf_type == PDFType.TEXT_BASED:
        extracted_text = text_extractor.extract_text(pdf_file)
    else:
        extracted_text = ocr_engine.extract_text_ocr(pdf_file)
    
    # Normalização
    normalized_text = normalizer.normalize_text(extracted_text.extracted_text)
    
    # Salvamento
    text_file = file_manager.save_extracted_text(extracted_text, pdf_file)
    metadata_file = file_manager.save_metadata(metadata, pdf_file)
```

### Modelos de Dados
```python
from src.models.document import PDFAnalysis, ExtractedText, DocumentMetadata

# Análise de PDF
analysis = PDFAnalysis.create(
    file_path="documento.pdf",
    file_size=2048576,
    page_count=45,
    pdf_type=PDFType.TEXT_BASED,
    has_text=True,
    has_images=False,
    image_count=0,
    text_quality_score=0.95
)

# Texto extraído
extracted_text = ExtractedText.create(
    original_file="documento.pdf",
    extracted_text="Conteúdo do documento...",
    page_count=45,
    extraction_method="native",
    confidence_score=0.98,
    processing_time=2.5
)

# Metadados do documento
metadata = DocumentMetadata.create(
    original_file="documento.pdf",
    document_class=DocumentClass.EDITAL,
    title="Edital Concurso 2024",
    year=2024,
    organization="Cebraspe",
    extracted_text_file="./output/edital_2024.txt",
    metadata_file="./output/edital_2024.json",
    quality_score=0.95
)
```

## 4. Variáveis de Ambiente e Logs

### Variáveis de Ambiente (.env)
```bash
# OCR Settings
OCR_ENGINE=tesseract
OCR_LANGUAGE=por
OCR_DPI=300
OCR_PSM=6
TESSERACT_CMD=/usr/bin/tesseract

# Text Processing
MIN_CONFIDENCE=0.7
MAX_PROCESSING_TIME=300
PRESERVE_FORMATTING=false

# Output Settings
OUTPUT_ENCODING=utf-8
OUTPUT_DIR=./data/output
INPUT_DIR=./data/input

# Performance
MAX_CONCURRENT_JOBS=3
BATCH_SIZE=10

# Quality Control
ENABLE_QUALITY_CHECK=true
MIN_TEXT_LENGTH=100
MAX_FILE_SIZE_MB=50

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=./logs/parser.log

# Development
DEBUG=false
DRY_RUN=false
VERBOSE=false
```

### Estrutura de Logs
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "logger": "src.parser.pdf_analyzer",
  "message": "PDF analisado com sucesso",
  "module": "pdf_analyzer",
  "function": "analyze_pdf",
  "line": 45,
  "extra_fields": {
    "file_path": "documento.pdf",
    "pdf_type": "text_based",
    "quality_score": 0.95,
    "processing_time": 1.2
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
- `logs/parser.log`: Log principal em formato JSON
- Console: Logs em formato legível para desenvolvimento

## 5. Limitações e Próximos Passos

### Limitações Atuais

#### Funcionais
- **OCR**: Limitado ao Tesseract, precisão dependente da qualidade da imagem
- **Idiomas**: Suporte principal para português
- **Tipos de PDF**: Foco em documentos da Cebraspe
- **Formatação**: Preservação limitada de formatação complexa

#### Técnicas
- **Performance**: OCR pode ser lento para PDFs grandes
- **Memória**: Processamento de imagens consome memória
- **Qualidade**: Dependente da qualidade dos PDFs de entrada
- **Escalabilidade**: Processamento sequencial, não paralelo

#### Operacionais
- **Dependências**: Requer Tesseract instalado
- **Recursos**: Consome CPU e memória durante OCR
- **Armazenamento**: Gera arquivos de texto e metadados
- **Monitoramento**: Logs básicos, sem métricas avançadas

### Próximos Passos

#### Curto Prazo (Sprint 2)
1. **Implementação Completa**
   - Finalizar lógica de análise de PDF
   - Implementar extração de texto nativo
   - Completar engine de OCR
   - Finalizar classificação de documentos

2. **Testes e Qualidade**
   - Implementar testes unitários e integração
   - Configurar CI/CD
   - Adicionar validação de qualidade
   - Testes com PDFs reais

3. **Documentação**
   - Documentar APIs internas
   - Criar guias de troubleshooting
   - Adicionar exemplos de uso

#### Médio Prazo (Sprint 3-4)
1. **Melhorias de Performance**
   - Otimização de algoritmos OCR
   - Processamento paralelo
   - Cache de resultados
   - Compressão de imagens

2. **Robustez**
   - Tratamento de PDFs corrompidos
   - Recuperação de falhas
   - Validação de qualidade
   - Sistema de retry

3. **Monitoramento**
   - Métricas de performance
   - Alertas automáticos
   - Dashboard de status
   - Análise de qualidade

#### Longo Prazo (Futuro)
1. **Escalabilidade**
   - Processamento distribuído
   - Armazenamento em nuvem
   - APIs REST para consulta
   - Processamento em lote

2. **Inteligência**
   - ML para classificação
   - Detecção automática de layout
   - Correção automática de erros
   - Análise de conteúdo

3. **Integração**
   - APIs para sistemas downstream
   - Webhooks para notificações
   - Integração com IA
   - Análise semântica

### Dependências Externas
- **Tesseract OCR**: Engine de OCR (deve estar instalado)
- **PDFs de entrada**: Fornecidos pelo CEB-001
- **Sistema**: Recursos computacionais adequados
- **Rede**: Para download de dependências

### Riscos Identificados
1. **Qualidade dos PDFs**: PDFs de baixa qualidade afetam OCR
2. **Performance**: OCR pode ser lento para grandes volumes
3. **Dependências**: Tesseract deve estar configurado corretamente
4. **Memória**: Processamento de imagens consome recursos

### Critérios de Sucesso
- ✅ Taxa de sucesso OCR ≥95%
- ✅ Tempo razoável por documento
- ✅ Texto extraído com qualidade adequada
- ✅ Metadados extraídos corretamente
- ✅ Encoding UTF-8 válido
- ✅ Logs estruturados e informativos
- ✅ Cobertura de testes >85%
- ✅ Documentação completa e atualizada

### Configuração Recomendada
- **CPU**: 4+ cores para processamento paralelo
- **RAM**: 8GB+ para PDFs grandes
- **Disco**: SSD para melhor performance
- **Tesseract**: Versão 4.0+ com suporte a português









