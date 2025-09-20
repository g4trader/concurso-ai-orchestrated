"""
Logging utilities

Este módulo é responsável pelo sistema de logging estruturado.
Responsabilidades:
- Configuração de logging
- Logs em formato JSON
- Rotação de logs
- Diferentes níveis de log
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class JSONFormatter(logging.Formatter):
    """
    Formatter para logs em JSON
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Formata log record como JSON
        
        Args:
            record: Log record
            
        Returns:
            str: Log formatado em JSON
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Adicionar campos extras se existirem
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)
        
        # Adicionar exception info se existir
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    """
    Configura sistema de logging
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Arquivo de log (opcional)
    """
    # Configurar nível de log
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configurar formato
    if log_file:
        # Log para arquivo em JSON
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(JSONFormatter())
        
        # Log para console em formato legível
        console_handler = logging.StreamHandler(sys.stdout)
        console_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        console_handler.setFormatter(logging.Formatter(console_format))
        
        # Configurar root logger
        logging.basicConfig(
            level=numeric_level,
            handlers=[file_handler, console_handler]
        )
    else:
        # Apenas console
        logging.basicConfig(
            level=numeric_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            stream=sys.stdout
        )

def get_logger(name: str) -> logging.Logger:
    """
    Retorna logger configurado
    
    Args:
        name: Nome do logger
        
    Returns:
        logging.Logger: Logger configurado
    """
    return logging.getLogger(name)

def log_with_context(logger: logging.Logger, level: int, message: str, **kwargs) -> None:
    """
    Log com contexto adicional
    
    Args:
        logger: Logger instance
        level: Nível de log
        message: Mensagem
        **kwargs: Campos adicionais
    """
    extra_fields = kwargs
    logger.log(level, message, extra={'extra_fields': extra_fields})









