"""
Módulo Crawler

Responsável por toda a lógica de crawling, incluindo:
- Descoberta de URLs e PDFs
- Download de arquivos
- Deduplicação de conteúdo
"""

from .discovery import DiscoveryEngine
from .downloader import DownloadEngine
from .deduplicator import DeduplicationEngine

__all__ = ['DiscoveryEngine', 'DownloadEngine', 'DeduplicationEngine']