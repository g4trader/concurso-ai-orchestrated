"""
Configuration settings for Cebraspe Parser

Este módulo define todas as configurações do sistema de parsing.
Responsabilidades:
- Carregamento de variáveis de ambiente
- Validação de configurações
- Valores padrão
- Configurações específicas por ambiente
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

@dataclass
class ProcessingConfig:
    """Configurações do processamento"""
    
    # OCR Settings
    ocr_engine: str = "tesseract"
    ocr_language: str = "por"
    ocr_dpi: int = 300
    ocr_psm: int = 6
    tesseract_cmd: str = "/usr/bin/tesseract"
    
    # Text Processing
    min_confidence: float = 0.7
    max_processing_time: int = 300  # segundos
    preserve_formatting: bool = False
    
    # Output Settings
    output_encoding: str = "utf-8"
    output_dir: str = "./data/output"
    input_dir: str = "./data/input"
    
    # Performance
    max_concurrent_jobs: int = 3
    batch_size: int = 10
    
    # Quality Control
    enable_quality_check: bool = True
    min_text_length: int = 100
    max_file_size_mb: int = 50
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    log_file: str = "./logs/parser.log"
    
    # Development
    debug: bool = False
    dry_run: bool = False
    verbose: bool = False
    
    @classmethod
    def load(cls) -> "ProcessingConfig":
        """
        Carrega configurações das variáveis de ambiente
        
        Returns:
            ProcessingConfig: Instância configurada
        """
        return cls(
            ocr_engine=os.getenv("OCR_ENGINE", cls.ocr_engine),
            ocr_language=os.getenv("OCR_LANGUAGE", cls.ocr_language),
            ocr_dpi=int(os.getenv("OCR_DPI", cls.ocr_dpi)),
            ocr_psm=int(os.getenv("OCR_PSM", cls.ocr_psm)),
            tesseract_cmd=os.getenv("TESSERACT_CMD", cls.tesseract_cmd),
            min_confidence=float(os.getenv("MIN_CONFIDENCE", cls.min_confidence)),
            max_processing_time=int(os.getenv("MAX_PROCESSING_TIME", cls.max_processing_time)),
            preserve_formatting=os.getenv("PRESERVE_FORMATTING", "false").lower() == "true",
            output_encoding=os.getenv("OUTPUT_ENCODING", cls.output_encoding),
            output_dir=os.getenv("OUTPUT_DIR", cls.output_dir),
            input_dir=os.getenv("INPUT_DIR", cls.input_dir),
            max_concurrent_jobs=int(os.getenv("MAX_CONCURRENT_JOBS", cls.max_concurrent_jobs)),
            batch_size=int(os.getenv("BATCH_SIZE", cls.batch_size)),
            enable_quality_check=os.getenv("ENABLE_QUALITY_CHECK", "true").lower() == "true",
            min_text_length=int(os.getenv("MIN_TEXT_LENGTH", cls.min_text_length)),
            max_file_size_mb=int(os.getenv("MAX_FILE_SIZE_MB", cls.max_file_size_mb)),
            log_level=os.getenv("LOG_LEVEL", cls.log_level),
            log_format=os.getenv("LOG_FORMAT", cls.log_format),
            log_file=os.getenv("LOG_FILE", cls.log_file),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            dry_run=os.getenv("DRY_RUN", "false").lower() == "true",
            verbose=os.getenv("VERBOSE", "false").lower() == "true",
        )
    
    def validate(self) -> None:
        """
        Valida configurações carregadas
        
        Raises:
            ValueError: Se configurações são inválidas
        """
        if self.max_concurrent_jobs <= 0:
            raise ValueError("max_concurrent_jobs deve ser > 0")
        
        if self.max_processing_time <= 0:
            raise ValueError("max_processing_time deve ser > 0")
        
        if self.min_confidence < 0 or self.min_confidence > 1:
            raise ValueError("min_confidence deve estar entre 0 e 1")
        
        if self.min_text_length <= 0:
            raise ValueError("min_text_length deve ser > 0")
        
        if self.max_file_size_mb <= 0:
            raise ValueError("max_file_size_mb deve ser > 0")
        
        # Criar diretórios se não existirem
        for directory in [self.output_dir, self.input_dir, os.path.dirname(self.log_file)]:
            os.makedirs(directory, exist_ok=True)
    
    def get_tesseract_config(self) -> dict:
        """
        Retorna configuração do Tesseract
        
        Returns:
            dict: Configuração do Tesseract
        """
        return {
            "cmd": self.tesseract_cmd,
            "lang": self.ocr_language,
            "config": f"--psm {self.ocr_psm}",
            "dpi": self.ocr_dpi
        }









