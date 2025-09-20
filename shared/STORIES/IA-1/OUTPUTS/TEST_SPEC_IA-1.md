# TEST_SPEC_IA-1: Especificações de Teste - Pipeline de Ingestão

## 1. Casos Felizes e de Erro

### **Parser Service Tests**

#### Casos Felizes
- **PDF válido com texto nativo**
  - Input: PDF com texto extraível
  - Expected: Texto extraído com metadados
  - Assertions: Texto não vazio, metadados presentes

- **PDF escaneado (OCR)**
  - Input: PDF com imagens de texto
  - Expected: Texto extraído via Tesseract
  - Assertions: Texto extraído, método = "tesseract"

- **Imagem PNG/JPG**
  - Input: Imagem com texto
  - Expected: Texto extraído via OCR
  - Assertions: Texto extraído, formato correto

- **Arquivo TXT**
  - Input: Arquivo de texto simples
  - Expected: Texto lido diretamente
  - Assertions: Texto idêntico ao arquivo

#### Casos de Erro
- **Arquivo não encontrado**
  - Input: Caminho inexistente
  - Expected: FileNotFoundError
  - Assertions: Erro específico, mensagem clara

- **Arquivo corrompido**
  - Input: PDF corrompido
  - Expected: ParsingError com fallback para OCR
  - Assertions: Fallback executado, erro tratado

- **Arquivo muito grande**
  - Input: Arquivo > 10MB
  - Expected: ValueError
  - Assertions: Erro de tamanho, limite respeitado

- **Formato não suportado**
  - Input: Arquivo .xyz
  - Expected: ValueError
  - Assertions: Erro de formato, lista de suportados

- **Timeout de parsing**
  - Input: PDF muito complexo
  - Expected: TimeoutError
  - Assertions: Timeout respeitado, erro tratado

### **Chunking Service Tests**

#### Casos Felizes
- **Texto normal**
  - Input: Texto de 2000 caracteres
  - Expected: 4 chunks de 512 caracteres com overlap
  - Assertions: Tamanho correto, overlap respeitado

- **Texto com quebras de linha**
  - Input: Texto com parágrafos
  - Expected: Chunks respeitando quebras
  - Assertions: Quebras preservadas, contexto mantido

- **Metadados preservados**
  - Input: Texto com metadados
  - Expected: Metadados em cada chunk
  - Assertions: Metadados idênticos, posições corretas

#### Casos de Erro
- **Texto vazio**
  - Input: String vazia
  - Expected: ValueError
  - Assertions: Erro de texto vazio

- **Chunk muito pequeno**
  - Input: Texto < 50 caracteres
  - Expected: Warning ou chunk único
  - Assertions: Tratamento adequado

- **Overlap maior que chunk**
  - Input: Overlap > chunk_size
  - Expected: ValueError
  - Assertions: Validação de parâmetros

### **Embedding Service Tests**

#### Casos Felizes
- **Texto normal**
  - Input: Lista de chunks
  - Expected: Embeddings de dimensão 1024
  - Assertions: Dimensão correta, não nulos

- **Batch processing**
  - Input: 100 chunks
  - Expected: 100 embeddings
  - Assertions: Todos processados, performance adequada

- **Cache funcionando**
  - Input: Texto já processado
  - Expected: Embedding do cache
  - Assertions: Cache hit, tempo reduzido

#### Casos de Erro
- **Modelo não encontrado**
  - Input: Modelo inexistente
  - Expected: ModelNotFoundError
  - Assertions: Erro específico, fallback

- **Memória insuficiente**
  - Input: Batch muito grande
  - Expected: MemoryError ou batch menor
  - Assertions: Tratamento de memória

- **Timeout de embedding**
  - Input: Texto muito longo
  - Expected: TimeoutError
  - Assertions: Timeout respeitado

### **Indexing Service Tests**

#### Casos Felizes
- **Indexação normal**
  - Input: Embeddings + metadados
  - Expected: Índice FAISS criado
  - Assertions: Índice válido, metadados salvos

- **Busca por similaridade**
  - Input: Query embedding
  - Expected: Resultados ordenados por score
  - Assertions: Scores decrescentes, resultados relevantes

- **Filtros por metadados**
  - Input: Query + filtros
  - Expected: Resultados filtrados
  - Assertions: Filtros aplicados, resultados corretos

#### Casos de Erro
- **Índice corrompido**
  - Input: Índice FAISS inválido
  - Expected: IndexCorruptedError
  - Assertions: Erro detectado, rebuild sugerido

- **Disco cheio**
  - Input: Índice muito grande
  - Expected: DiskFullError
  - Assertions: Erro de espaço, cleanup sugerido

- **Busca sem resultados**
  - Input: Query irrelevante
  - Expected: Lista vazia
  - Assertions: Resultado vazio, não erro

### **Reranker Service Tests**

#### Casos Felizes
- **Reranking normal**
  - Input: Query + resultados
  - Expected: Resultados rerankeados
  - Assertions: Ordem alterada, scores atualizados

- **Threshold aplicado**
  - Input: Resultados com scores baixos
  - Expected: Filtro por threshold
  - Assertions: Threshold respeitado, resultados filtrados

#### Casos de Erro
- **Modelo não carregado**
  - Input: Reranker não inicializado
  - Expected: ModelNotLoadedError
  - Assertions: Erro específico, inicialização

- **Timeout de reranking**
  - Input: Muitos resultados
  - Expected: TimeoutError
  - Assertions: Timeout respeitado

### **Query Service Tests**

#### Casos Felizes
- **Query simples**
  - Input: "princípios constitucionais"
  - Expected: Resultados relevantes
  - Assertions: Resultados não vazios, relevância

- **Query com filtros**
  - Input: Query + filtros específicos
  - Expected: Resultados filtrados
  - Assertions: Filtros aplicados, resultados corretos

- **Query com reranking**
  - Input: Query + rerank=True
  - Expected: Resultados rerankeados
  - Assertions: Reranking aplicado, ordem alterada

#### Casos de Erro
- **Query vazia**
  - Input: String vazia
  - Expected: ValueError
  - Assertions: Validação de input

- **Query muito longa**
  - Input: Texto > 1000 caracteres
  - Expected: ValueError ou truncamento
  - Assertions: Tratamento adequado

- **Filtros inválidos**
  - Input: Filtros malformados
  - Expected: ValidationError
  - Assertions: Validação de filtros

## 2. Estratégias de Mocks

### **Rede/IO Mocks**

#### Parser Service
```python
@pytest.fixture
def mock_pymupdf():
    with patch('fitz.open') as mock_open:
        mock_doc = MagicMock()
        mock_doc.page_count = 2
        mock_doc.metadata = {"title": "Test PDF"}
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Sample text"
        mock_doc.load_page.return_value = mock_page
        mock_open.return_value = mock_doc
        yield mock_open

@pytest.fixture
def mock_tesseract():
    with patch('pytesseract.image_to_string') as mock_ocr:
        mock_ocr.return_value = "OCR extracted text"
        yield mock_ocr
```

#### Embedding Service
```python
@pytest.fixture
def mock_sentence_transformer():
    with patch('sentence_transformers.SentenceTransformer') as mock_model:
        mock_encoder = MagicMock()
        mock_encoder.encode.return_value = np.random.rand(5, 1024)
        mock_model.return_value = mock_encoder
        yield mock_model
```

#### Indexing Service
```python
@pytest.fixture
def mock_faiss():
    with patch('faiss.IndexFlatIP') as mock_index:
        mock_faiss_index = MagicMock()
        mock_faiss_index.add.return_value = None
        mock_faiss_index.search.return_value = (
            np.array([[0.9, 0.8, 0.7]]),
            np.array([[0, 1, 2]])
        )
        mock_index.return_value = mock_faiss_index
        yield mock_index
```

### **File System Mocks**

```python
@pytest.fixture
def mock_file_system():
    with patch('os.path.exists') as mock_exists, \
         patch('os.path.getsize') as mock_size, \
         patch('builtins.open', mock_open(read_data="test content")):
        mock_exists.return_value = True
        mock_size.return_value = 1024
        yield
```

### **Model Mocks**

```python
@pytest.fixture
def mock_reranker():
    with patch('sentence_transformers.CrossEncoder') as mock_reranker:
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([0.9, 0.8, 0.7])
        mock_reranker.return_value = mock_model
        yield mock_reranker
```

## 3. Timeouts e Re-tentativas

### **Parser Service**
- **PyMuPDF timeout**: 30 segundos
- **Tesseract timeout**: 60 segundos
- **Retry strategy**: 3 tentativas com backoff exponencial
- **Fallback**: PyMuPDF → Tesseract → Error

### **Embedding Service**
- **Model loading timeout**: 120 segundos
- **Inference timeout**: 30 segundos por batch
- **Retry strategy**: 2 tentativas com fallback para modelo menor
- **Fallback**: BGE-M3 → BGE-M3-base → Error

### **Indexing Service**
- **Index creation timeout**: 60 segundos
- **Search timeout**: 5 segundos
- **Retry strategy**: 2 tentativas com rebuild se necessário
- **Fallback**: In-memory index → Error

### **Reranker Service**
- **Reranking timeout**: 10 segundos
- **Retry strategy**: 1 tentativa
- **Fallback**: Sem reranking → Resultados originais

### **Query Service**
- **Total query timeout**: 30 segundos
- **Retry strategy**: 2 tentativas
- **Fallback**: Resultados sem reranking

## 4. Critérios de Cobertura por Arquivo

### **src/main.py**
- **Cobertura mínima**: 80%
- **Casos críticos**: Inicialização da app, configuração CORS
- **Testes**: Health check, configuração de rotas

### **src/config/settings.py**
- **Cobertura mínima**: 90%
- **Casos críticos**: Todas as configurações, validações
- **Testes**: Valores padrão, variáveis de ambiente

### **src/services/parser_service.py**
- **Cobertura mínima**: 85%
- **Casos críticos**: Todos os formatos, timeouts, fallbacks
- **Testes**: PDF, imagem, texto, erros, validações

### **src/services/chunking_service.py**
- **Cobertura mínima**: 80%
- **Casos críticos**: Chunking, overlap, metadados
- **Testes**: Tamanhos variados, edge cases

### **src/services/embedding_service.py**
- **Cobertura mínima**: 80%
- **Casos críticos**: Model loading, batch processing, cache
- **Testes**: Embeddings, cache, erros de modelo

### **src/services/indexing_service.py**
- **Cobertura mínima**: 85%
- **Casos críticos**: Indexação, busca, filtros, persistência
- **Testes**: CRUD operations, busca, filtros

### **src/services/reranker_service.py**
- **Cobertura mínima**: 75%
- **Casos críticos**: Reranking, threshold, fallback
- **Testes**: Reranking, threshold, erros

### **src/services/query_service.py**
- **Cobertura mínima**: 85%
- **Casos críticos**: Busca, filtros, pipeline completo
- **Testes**: Queries variadas, filtros, pipeline

### **src/api/routes.py**
- **Cobertura mínima**: 80%
- **Casos críticos**: Todos os endpoints, validações, erros
- **Testes**: Upload, query, health, métricas

### **src/models/request.py**
- **Cobertura mínima**: 90%
- **Casos críticos**: Validações Pydantic, enums
- **Testes**: Validações, tipos, campos obrigatórios

### **src/models/response.py**
- **Cobertura mínima**: 90%
- **Casos críticos**: Serialização, tipos de dados
- **Testes**: Serialização, validações

## 5. Testes de Integração

### **Pipeline Completo**
- **Upload → Parse → Chunk → Embed → Index**
- **Query → Search → Rerank → Response**
- **Health Check → All Services**
- **Metrics → Performance Data**

### **Testes de Performance**
- **Upload de 100 documentos**
- **Query com 1000 resultados**
- **Concurrent requests (10 users)**
- **Memory usage under load**

### **Testes de Resilência**
- **Service failures**
- **Network timeouts**
- **Disk space issues**
- **Memory pressure**

## 6. Testes de Segurança

### **Input Validation**
- **File upload security**
- **SQL injection prevention**
- **Path traversal prevention**
- **XSS prevention**

### **Authentication/Authorization**
- **API key validation**
- **Rate limiting**
- **CORS validation**
- **Input sanitization**

## 7. Testes de Monitoramento

### **Logging**
- **Structured logging**
- **Error tracking**
- **Performance metrics**
- **Audit trail**

### **Health Checks**
- **Service availability**
- **Resource usage**
- **Dependency health**
- **Performance degradation**

---

**Este documento define especificações completas de teste para o pipeline IA-1, incluindo casos felizes, erros, mocks, timeouts e critérios de cobertura.**
