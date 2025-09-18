# ESPECIFICAÇÃO DE TESTES CEB-002: Parser OCR

## Visão Geral

Esta especificação define a estratégia de testes para o sistema de parsing OCR da Cebraspe, cobrindo análise de PDFs, extração de texto, OCR, classificação e normalização.

## Estratégia de Testes

### 1. Testes Unitários
- **Objetivo**: Validar componentes individuais isoladamente
- **Cobertura**: Mínimo 85% de cobertura de código
- **Ferramentas**: pytest, pytest-cov, pytest-mock

### 2. Testes de Integração
- **Objetivo**: Validar interação entre componentes
- **Cobertura**: Fluxos principais e cenários de erro
- **Ferramentas**: pytest, PyMuPDF, Tesseract

### 3. Testes de Performance
- **Objetivo**: Validar requisitos de performance
- **Cobertura**: Tempo de processamento, uso de memória, qualidade OCR
- **Ferramentas**: pytest-benchmark, memory_profiler

### 4. Testes de Qualidade
- **Objetivo**: Validar qualidade do texto extraído
- **Cobertura**: Precisão OCR, normalização, encoding
- **Ferramentas**: Testes com PDFs reais, validação de charset

## Casos de Teste

### PDF Analyzer

#### Casos Felizes
1. **Análise de PDF com texto nativo**
   - **Entrada**: PDF com texto nativo de alta qualidade
   - **Saída Esperada**: PDFType.TEXT_BASED, has_text=True, quality_score>0.8
   - **Critérios**: Tipo identificado corretamente, qualidade alta

2. **Análise de PDF baseado em imagem**
   - **Entrada**: PDF escaneado ou com imagens
   - **Saída Esperada**: PDFType.IMAGE_BASED, has_images=True, image_count>0
   - **Critérios**: Tipo identificado corretamente, imagens detectadas

3. **Análise de PDF misto**
   - **Entrada**: PDF com texto e imagens
   - **Saída Esperada**: PDFType.MIXED, has_text=True, has_images=True
   - **Critérios**: Tipo identificado corretamente, ambos detectados

4. **Extração de metadados**
   - **Entrada**: PDF com metadados completos
   - **Saída Esperada**: Metadados extraídos corretamente
   - **Critérios**: Título, autor, data de criação extraídos

#### Casos de Erro
1. **PDF corrompido**
   - **Entrada**: Arquivo PDF corrompido
   - **Saída Esperada**: Exceção tratada, erro logado
   - **Critérios**: Não deve quebrar o sistema

2. **PDF protegido por senha**
   - **Entrada**: PDF com proteção de senha
   - **Saída Esperada**: Erro tratado, PDF pulado
   - **Critérios**: Mensagem de erro clara

3. **Arquivo não é PDF**
   - **Entrada**: Arquivo com extensão .pdf mas não é PDF
   - **Saída Esperada**: Erro de validação
   - **Critérios**: Validação de header do arquivo

### Text Extractor

#### Casos Felizes
1. **Extração de texto nativo**
   - **Entrada**: PDF com texto nativo bem formatado
   - **Saída Esperada**: Texto extraído com alta confiança
   - **Critérios**: Confiança >0.9, texto legível, formatação preservada

2. **Extração com formatação**
   - **Entrada**: PDF com formatação complexa
   - **Saída Esperada**: Texto com formatação preservada
   - **Critérios**: Estrutura mantida, parágrafos identificados

3. **Extração de texto multilíngue**
   - **Entrada**: PDF com texto em português
   - **Saída Esperada**: Texto extraído corretamente
   - **Critérios**: Caracteres especiais preservados, encoding UTF-8

#### Casos de Erro
1. **PDF sem texto extraível**
   - **Entrada**: PDF com texto em imagem
   - **Saída Esperada**: Texto vazio ou mínimo
   - **Critérios**: Deve detectar necessidade de OCR

2. **Encoding incorreto**
   - **Entrada**: PDF com encoding problemático
   - **Saída Esperada**: Texto com caracteres especiais tratados
   - **Critérios**: Conversão para UTF-8 válido

### OCR Engine

#### Casos Felizes
1. **OCR de texto claro**
   - **Entrada**: PDF com texto escaneado de alta qualidade
   - **Saída Esperada**: Texto reconhecido com alta precisão
   - **Critérios**: Confiança >0.8, erros mínimos

2. **OCR de texto em português**
   - **Entrada**: PDF com texto em português
   - **Saída Esperada**: Texto reconhecido corretamente
   - **Critérios**: Acentos preservados, palavras corretas

3. **OCR de tabelas**
   - **Entrada**: PDF com tabelas escaneadas
   - **Saída Esperada**: Estrutura de tabela preservada
   - **Critérios**: Colunas e linhas identificadas

#### Casos de Erro
1. **Imagem de baixa qualidade**
   - **Entrada**: PDF com imagens borradas ou baixa resolução
   - **Saída Esperada**: Texto com baixa confiança
   - **Critérios**: Confiança <0.5, erros identificados

2. **Texto manuscrito**
   - **Entrada**: PDF com texto manuscrito
   - **Saída Esperada**: Reconhecimento limitado
   - **Critérios**: Deve tentar reconhecer, falhar graciosamente

3. **Timeout de processamento**
   - **Entrada**: PDF muito grande ou complexo
   - **Saída Esperada**: Timeout após tempo configurado
   - **Critérios**: Não deve travar indefinidamente

### Document Classifier

#### Casos Felizes
1. **Classificação de edital**
   - **Entrada**: Texto de edital de concurso
   - **Saída Esperada**: DocumentClass.EDITAL
   - **Critérios**: Padrões identificados corretamente

2. **Classificação de prova**
   - **Entrada**: Texto de prova de concurso
   - **Saída Esperada**: DocumentClass.PROVA
   - **Critérios**: Questões e alternativas identificadas

3. **Classificação de gabarito**
   - **Entrada**: Texto de gabarito
   - **Saída Esperada**: DocumentClass.GABARITO
   - **Critérios**: Respostas identificadas

#### Casos de Erro
1. **Texto ambíguo**
   - **Entrada**: Texto que pode ser de múltiplos tipos
   - **Saída Esperada**: Classificação com baixa confiança
   - **Critérios**: Deve indicar incerteza

2. **Texto muito curto**
   - **Entrada**: Texto com menos de 100 caracteres
   - **Saída Esperada**: DocumentClass.OUTRO
   - **Critérios**: Deve tratar como não classificável

### Text Normalizer

#### Casos Felizes
1. **Normalização de texto limpo**
   - **Entrada**: Texto bem formatado
   - **Saída Esperada**: Texto normalizado mantendo qualidade
   - **Critérios**: UTF-8 válido, espaçamento correto

2. **Limpeza de texto OCR**
   - **Entrada**: Texto com erros de OCR
   - **Saída Esperada**: Texto limpo e corrigido
   - **Critérios**: Erros comuns corrigidos, legibilidade melhorada

3. **Preservação de formatação**
   - **Entrada**: Texto com formatação complexa
   - **Saída Esperada**: Formatação preservada
   - **Critérios**: Estrutura mantida, hierarquia clara

#### Casos de Erro
1. **Texto com encoding inválido**
   - **Entrada**: Texto com caracteres inválidos
   - **Saída Esperada**: Texto com encoding corrigido
   - **Critérios**: UTF-8 válido, caracteres especiais tratados

2. **Texto muito corrompido**
   - **Entrada**: Texto com muitos erros
   - **Saída Esperada**: Texto parcialmente recuperado
   - **Critérios**: Deve tentar recuperar o máximo possível

### File Manager

#### Casos Felizes
1. **Salvamento de texto**
   - **Entrada**: Texto extraído válido
   - **Saída Esperada**: Arquivo .txt salvo corretamente
   - **Critérios**: Encoding UTF-8, arquivo legível

2. **Salvamento de metadados**
   - **Entrada**: Metadados estruturados
   - **Saída Esperada**: Arquivo JSON válido
   - **Critérios**: JSON válido, estrutura correta

3. **Gerenciamento de diretórios**
   - **Entrada**: Operações de criação/limpeza
   - **Saída Esperada**: Diretórios criados/limpos
   - **Critérios**: Permissões corretas, estrutura mantida

#### Casos de Erro
1. **Espaço em disco insuficiente**
   - **Entrada**: Tentativa de salvar arquivo grande
   - **Saída Esperada**: Erro tratado
   - **Critérios**: Verificação prévia de espaço

2. **Permissão de escrita negada**
   - **Entrada**: Tentativa de escrever em diretório protegido
   - **Saída Esperada**: Erro tratado
   - **Critérios**: Mensagem de erro clara

## Estratégias de Mock

### PDF Processing
- **Ferramenta**: PyMuPDF, pytest-mock
- **Estratégia**: Mock de documentos PDF com diferentes características
- **Cenários**: Texto nativo, imagens, PDFs corrompidos, metadados

### OCR Engine
- **Ferramenta**: pytesseract, PIL, pytest-mock
- **Estratégia**: Mock de imagens e resultados de OCR
- **Cenários**: Texto claro, texto borrado, diferentes idiomas

### File System
- **Ferramenta**: pytest-mock, tempfile
- **Estratégia**: Uso de diretórios temporários
- **Cenários**: Permissões, espaço em disco, arquivos corrompidos

### Performance
- **Ferramenta**: time, memory_profiler
- **Estratégia**: Medição de tempo e memória
- **Cenários**: PDFs grandes, processamento em lote

## Configuração de Timeouts

### PDF Analysis
- **Timeout de abertura**: 10 segundos
- **Timeout de análise**: 30 segundos
- **Timeout total**: 60 segundos

### Text Extraction
- **Timeout por página**: 5 segundos
- **Timeout total**: 120 segundos

### OCR Processing
- **Timeout por imagem**: 30 segundos
- **Timeout por página**: 60 segundos
- **Timeout total**: 300 segundos

### File Operations
- **Timeout de leitura**: 5 segundos
- **Timeout de escrita**: 10 segundos

## Critérios de Cobertura

### Cobertura de Código
- **Mínimo**: 85% de linhas cobertas
- **Máximo**: 95% (evitar over-testing)
- **Foco**: Lógica de negócio, tratamento de erros, algoritmos OCR

### Cobertura de Funcionalidades
- **Análise de PDF**: 100% dos tipos de PDF
- **Extração de texto**: 100% dos métodos de extração
- **OCR**: 100% dos cenários de reconhecimento
- **Classificação**: 100% dos tipos de documento
- **Normalização**: 100% dos algoritmos de limpeza

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
- **PyMuPDF**: Manipulação de PDFs
- **pytesseract**: OCR para testes
- **PIL/Pillow**: Processamento de imagens
- **tempfile**: Arquivos temporários

### Testes de Performance
- **pytest-benchmark**: Benchmarking
- **memory_profiler**: Análise de memória
- **psutil**: Monitoramento de sistema
- **time**: Medição de tempo

### Testes de Qualidade
- **chardet**: Detecção de encoding
- **unittest.mock**: Mocking avançado
- **pathlib**: Manipulação de caminhos

### Qualidade de Código
- **black**: Formatação
- **flake8**: Linting
- **mypy**: Type checking
- **bandit**: Segurança

## Estrutura de Testes

```
tests/
├── unit/
│   ├── test_pdf_analyzer.py
│   ├── test_text_extractor.py
│   ├── test_ocr_engine.py
│   ├── test_classifier.py
│   ├── test_normalizer.py
│   └── test_file_manager.py
├── integration/
│   ├── test_pipeline.py
│   ├── test_error_handling.py
│   └── test_performance.py
├── fixtures/
│   ├── sample_pdfs.py
│   ├── sample_images.py
│   └── mock_responses.py
├── data/
│   ├── test_pdfs/
│   ├── test_images/
│   └── expected_outputs/
└── conftest.py
```

## Critérios de Aceite para Testes

### Funcionais
- ✅ Todos os casos felizes passam
- ✅ Todos os casos de erro são tratados
- ✅ Texto extraído com qualidade adequada
- ✅ OCR funciona com precisão ≥95%
- ✅ Classificação de documentos correta
- ✅ Normalização de texto efetiva

### Não Funcionais
- ✅ Taxa de sucesso OCR ≥95%
- ✅ Tempo razoável por documento
- ✅ Uso de memória controlado
- ✅ Logs estruturados em JSON
- ✅ Encoding UTF-8 válido

### Qualidade
- ✅ Cobertura de código ≥85%
- ✅ Todos os linters passam
- ✅ Type hints corretos
- ✅ Documentação atualizada
- ✅ Testes são determinísticos

### Performance
- ✅ Processamento de PDFs em tempo aceitável
- ✅ OCR otimizado para português
- ✅ Uso eficiente de recursos
- ✅ Escalabilidade para lotes grandes


