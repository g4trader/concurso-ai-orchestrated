"""
Document data models

Este módulo define os modelos de dados para documentos e metadados.
Responsabilidades:
- Definição de schemas/DTOs
- Validação de dados
- Serialização/deserialização
- Tipos de documento suportados
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
import uuid

class DocumentType(Enum):
    """Tipos de documento suportados"""
    EDITAL = "edital"
    PROVA = "prova"
    GABARITO = "gabarito"
    RESULTADO = "resultado"
    OUTRO = "outro"

@dataclass
class DocumentMetadata:
    """
    Metadados de um documento
    
    Representa todas as informações sobre um documento baixado,
    incluindo localização, hash, tipo e metadados adicionais.
    """
    id: str                    # UUID único
    title: str                 # Título do documento
    document_type: DocumentType
    year: int                  # Ano do documento
    url: str                   # URL original
    local_path: str            # Caminho local do PDF
    file_hash: str             # SHA-256 do arquivo
    file_size: int             # Tamanho em bytes
    download_date: datetime    # Data do download
    source_domain: str         # Domínio de origem
    additional_metadata: Optional[Dict[str, Any]] = None
    
    @classmethod
    def create(
        cls,
        title: str,
        document_type: DocumentType,
        year: int,
        url: str,
        local_path: str,
        file_hash: str,
        file_size: int,
        source_domain: str,
        additional_metadata: Optional[Dict[str, Any]] = None
    ) -> "DocumentMetadata":
        """
        Cria uma nova instância de DocumentMetadata
        
        Args:
            title: Título do documento
            document_type: Tipo do documento
            year: Ano do documento
            url: URL original
            local_path: Caminho local do arquivo
            file_hash: Hash SHA-256 do arquivo
            file_size: Tamanho do arquivo em bytes
            source_domain: Domínio de origem
            additional_metadata: Metadados adicionais
            
        Returns:
            DocumentMetadata: Nova instância
        """
        return cls(
            id=str(uuid.uuid4()),
            title=title,
            document_type=document_type,
            year=year,
            url=url,
            local_path=local_path,
            file_hash=file_hash,
            file_size=file_size,
            download_date=datetime.utcnow(),
            source_domain=source_domain,
            additional_metadata=additional_metadata or {}
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte para dicionário
        
        Returns:
            Dict: Representação em dicionário
        """
        return {
            "id": self.id,
            "title": self.title,
            "document_type": self.document_type.value,
            "year": self.year,
            "url": self.url,
            "local_path": self.local_path,
            "file_hash": self.file_hash,
            "file_size": self.file_size,
            "download_date": self.download_date.isoformat(),
            "source_domain": self.source_domain,
            "additional_metadata": self.additional_metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentMetadata":
        """
        Cria instância a partir de dicionário
        
        Args:
            data: Dados do dicionário
            
        Returns:
            DocumentMetadata: Nova instância
        """
        return cls(
            id=data["id"],
            title=data["title"],
            document_type=DocumentType(data["document_type"]),
            year=data["year"],
            url=data["url"],
            local_path=data["local_path"],
            file_hash=data["file_hash"],
            file_size=data["file_size"],
            download_date=datetime.fromisoformat(data["download_date"]),
            source_domain=data["source_domain"],
            additional_metadata=data.get("additional_metadata")
        )

@dataclass
class CrawlerStats:
    """
    Estatísticas do crawler
    
    Mantém contadores e métricas de execução do crawler.
    """
    total_discovered: int = 0
    total_downloaded: int = 0
    total_duplicates: int = 0
    total_errors: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    def increment_discovered(self) -> None:
        """Incrementa contador de descobertos"""
        self.total_discovered += 1
    
    def increment_downloaded(self) -> None:
        """Incrementa contador de baixados"""
        self.total_downloaded += 1
    
    def increment_duplicates(self) -> None:
        """Incrementa contador de duplicatas"""
        self.total_duplicates += 1
    
    def increment_errors(self) -> None:
        """Incrementa contador de erros"""
        self.total_errors += 1
    
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


