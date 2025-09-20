"""
Document processing data models

Este módulo define os modelos de dados para processamento de documentos.
Responsabilidades:
- Definição de schemas/DTOs
- Validação de dados
- Serialização/deserialização
- Tipos de documento e status
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
import uuid

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
    """
    Análise de um arquivo PDF
    
    Contém informações sobre o tipo de PDF, qualidade do texto,
    número de páginas e imagens, etc.
    """
    file_path: str
    file_size: int
    page_count: int
    pdf_type: PDFType
    has_text: bool
    has_images: bool
    image_count: int
    text_quality_score: float  # 0.0 a 1.0
    analysis_timestamp: datetime
    
    @classmethod
    def create(
        cls,
        file_path: str,
        file_size: int,
        page_count: int,
        pdf_type: PDFType,
        has_text: bool,
        has_images: bool,
        image_count: int,
        text_quality_score: float
    ) -> "PDFAnalysis":
        """
        Cria uma nova instância de PDFAnalysis
        
        Args:
            file_path: Caminho do arquivo PDF
            file_size: Tamanho do arquivo em bytes
            page_count: Número de páginas
            pdf_type: Tipo do PDF
            has_text: Se contém texto nativo
            has_images: Se contém imagens
            image_count: Número de imagens
            text_quality_score: Score de qualidade do texto
            
        Returns:
            PDFAnalysis: Nova instância
        """
        return cls(
            file_path=file_path,
            file_size=file_size,
            page_count=page_count,
            pdf_type=pdf_type,
            has_text=has_text,
            has_images=has_images,
            image_count=image_count,
            text_quality_score=text_quality_score,
            analysis_timestamp=datetime.utcnow()
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte para dicionário
        
        Returns:
            Dict: Representação em dicionário
        """
        return {
            "file_path": self.file_path,
            "file_size": self.file_size,
            "page_count": self.page_count,
            "pdf_type": self.pdf_type.value,
            "has_text": self.has_text,
            "has_images": self.has_images,
            "image_count": self.image_count,
            "text_quality_score": self.text_quality_score,
            "analysis_timestamp": self.analysis_timestamp.isoformat()
        }

@dataclass
class ExtractedText:
    """
    Texto extraído de um documento
    
    Contém o texto extraído, metadados sobre a extração,
    método usado e scores de confiança.
    """
    original_file: str
    extracted_text: str
    page_count: int
    word_count: int
    char_count: int
    extraction_method: str  # "native" ou "ocr"
    confidence_score: float  # 0.0 a 1.0
    processing_time: float   # segundos
    extraction_timestamp: datetime
    
    @classmethod
    def create(
        cls,
        original_file: str,
        extracted_text: str,
        page_count: int,
        extraction_method: str,
        confidence_score: float,
        processing_time: float
    ) -> "ExtractedText":
        """
        Cria uma nova instância de ExtractedText
        
        Args:
            original_file: Arquivo original
            extracted_text: Texto extraído
            page_count: Número de páginas
            extraction_method: Método de extração
            confidence_score: Score de confiança
            processing_time: Tempo de processamento
            
        Returns:
            ExtractedText: Nova instância
        """
        # Calcular contadores
        word_count = len(extracted_text.split())
        char_count = len(extracted_text)
        
        return cls(
            original_file=original_file,
            extracted_text=extracted_text,
            page_count=page_count,
            word_count=word_count,
            char_count=char_count,
            extraction_method=extraction_method,
            confidence_score=confidence_score,
            processing_time=processing_time,
            extraction_timestamp=datetime.utcnow()
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte para dicionário
        
        Returns:
            Dict: Representação em dicionário
        """
        return {
            "original_file": self.original_file,
            "extracted_text": self.extracted_text,
            "page_count": self.page_count,
            "word_count": self.word_count,
            "char_count": self.char_count,
            "extraction_method": self.extraction_method,
            "confidence_score": self.confidence_score,
            "processing_time": self.processing_time,
            "extraction_timestamp": self.extraction_timestamp.isoformat()
        }

@dataclass
class DocumentMetadata:
    """
    Metadados de um documento processado
    
    Contém todas as informações sobre um documento processado,
    incluindo classificação, qualidade e arquivos gerados.
    """
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
    
    @classmethod
    def create(
        cls,
        original_file: str,
        document_class: DocumentClass,
        title: str,
        year: int,
        organization: str,
        extracted_text_file: str,
        metadata_file: str,
        quality_score: float,
        additional_metadata: Optional[Dict[str, Any]] = None
    ) -> "DocumentMetadata":
        """
        Cria uma nova instância de DocumentMetadata
        
        Args:
            original_file: Arquivo original
            document_class: Classe do documento
            title: Título do documento
            year: Ano do documento
            organization: Organização
            extracted_text_file: Arquivo de texto extraído
            metadata_file: Arquivo de metadados
            quality_score: Score de qualidade
            additional_metadata: Metadados adicionais
            
        Returns:
            DocumentMetadata: Nova instância
        """
        return cls(
            document_id=str(uuid.uuid4()),
            original_file=original_file,
            document_class=document_class,
            title=title,
            year=year,
            organization=organization,
            extracted_text_file=extracted_text_file,
            metadata_file=metadata_file,
            processing_status=ProcessingStatus.COMPLETED,
            quality_score=quality_score,
            processing_timestamp=datetime.utcnow(),
            additional_metadata=additional_metadata or {}
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte para dicionário
        
        Returns:
            Dict: Representação em dicionário
        """
        return {
            "document_id": self.document_id,
            "original_file": self.original_file,
            "document_class": self.document_class.value,
            "title": self.title,
            "year": self.year,
            "organization": self.organization,
            "extracted_text_file": self.extracted_text_file,
            "metadata_file": self.metadata_file,
            "processing_status": self.processing_status.value,
            "quality_score": self.quality_score,
            "processing_timestamp": self.processing_timestamp.isoformat(),
            "additional_metadata": self.additional_metadata
        }

@dataclass
class ProcessingStats:
    """
    Estatísticas do processamento
    
    Mantém contadores e métricas de execução do parser.
    """
    total_files: int = 0
    processed_files: int = 0
    failed_files: int = 0
    skipped_files: int = 0
    text_based_pdfs: int = 0
    image_based_pdfs: int = 0
    mixed_pdfs: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    def increment_processed(self) -> None:
        """Incrementa contador de processados"""
        self.processed_files += 1
    
    def increment_failed(self) -> None:
        """Incrementa contador de falhas"""
        self.failed_files += 1
    
    def increment_skipped(self) -> None:
        """Incrementa contador de pulados"""
        self.skipped_files += 1
    
    def increment_pdf_type(self, pdf_type: PDFType) -> None:
        """Incrementa contador por tipo de PDF"""
        if pdf_type == PDFType.TEXT_BASED:
            self.text_based_pdfs += 1
        elif pdf_type == PDFType.IMAGE_BASED:
            self.image_based_pdfs += 1
        elif pdf_type == PDFType.MIXED:
            self.mixed_pdfs += 1
    
    def start_timer(self) -> None:
        """Inicia cronômetro"""
        self.start_time = datetime.utcnow()
    
    def end_timer(self) -> None:
        """Finaliza cronômetro"""
        self.end_time = datetime.utcnow()
    
    @property
    def duration(self) -> Optional[float]:
        """
        Duração da execução em segundos
        
        Returns:
            float: Duração em segundos ou None se não finalizado
        """
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    @property
    def success_rate(self) -> float:
        """
        Taxa de sucesso do processamento
        
        Returns:
            float: Taxa de sucesso (0.0 a 1.0)
        """
        if self.total_files == 0:
            return 0.0
        return self.processed_files / self.total_files









