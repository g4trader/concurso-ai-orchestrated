"""
Configurações do Cebraspe Crawler

Este módulo define todas as configurações da aplicação, incluindo:
- URLs base do Cebraspe
- Parâmetros de download (timeout, retry, concorrência)
- Caminhos de armazenamento
- Configurações de logging
- User agent e headers HTTP

TODO: Implementar carregamento de configurações de arquivo .env
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class CrawlerConfig:
    """
    Configurações principais do crawler.
    
    TODO: Implementar validação de configurações
    TODO: Implementar carregamento de variáveis de ambiente
    """
    # URLs e domínios
    base_url: str = "https://www.cebraspe.org.br"
    allowed_domains: list = None
    
    # Configurações de download
    max_concurrent_downloads: int = 5
    request_timeout: int = 30
    retry_attempts: int = 3
    retry_delay: int = 5
    
    # Armazenamento
    output_dir: str = "./data"
    pdfs_dir: str = "./data/pdfs"
    index_file: str = "./data/index.json"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/crawler.log"
    
    # HTTP
    user_agent: str = "CebraspeCrawler/1.0"
    headers: dict = None
    
    def __post_init__(self):
        """Inicialização pós-criação do dataclass."""
        if self.allowed_domains is None:
            self.allowed_domains = ["cebraspe.org.br", "www.cebraspe.org.br"]
        
        if self.headers is None:
            self.headers = {
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            }


def load_config() -> CrawlerConfig:
    """
    Carrega configurações do ambiente.
    
    TODO: Implementar carregamento de arquivo .env
    TODO: Implementar validação de configurações
    """
    return CrawlerConfig()