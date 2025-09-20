"""
Sistema de logging para WEB-002
"""

import logging
import structlog
import sys
from typing import Optional

def setup_logging(level: str = "INFO") -> None:
    """Configurar sistema de logging"""
    structlog.configure(
        processors=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )

def get_logger(name: Optional[str] = None) -> structlog.stdlib.BoundLogger:
    """Obter um logger configurado"""
    return structlog.get_logger(name)
