"""
Index Manager

Este módulo é responsável pelo gerenciamento do índice de metadados.
Responsabilidades:
- Criação e atualização do index.json
- Backup e recuperação do índice
- Consultas ao índice
- Compressão de metadados
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# TODO: Implementar imports necessários
# from src.config.settings import CrawlerConfig
# from src.models.document import DocumentMetadata
# from src.utils.logger import get_logger

class IndexManager:
    """
    Gerenciador do índice de metadados
    
    Responsável por manter o arquivo index.json com todos os
    metadados dos documentos catalogados.
    """
    
    def __init__(self, config):
        """
        Inicializa o gerenciador de índice
        
        Args:
            config: Configurações do crawler
        """
        self.config = config
        # self.logger = get_logger(__name__)
        self.index_path = Path(config.output_dir) / "index.json"
        self.backup_path = Path(config.output_dir) / "index.json.backup"
        self.index_data: Dict = {}
        self._load_index()
    
    def _load_index(self) -> None:
        """
        Carrega índice existente do disco
        
        Carrega o arquivo index.json se existir, caso contrário
        cria uma estrutura vazia.
        """
        if self.index_path.exists():
            try:
                with open(self.index_path, 'r', encoding='utf-8') as f:
                    self.index_data = json.load(f)
                print(f"📚 Índice carregado: {len(self.index_data.get('documents', []))} documentos")
            except Exception as e:
                # self.logger.error(f"Erro ao carregar índice: {e}")
                self.index_data = self._create_empty_index()
        else:
            self.index_data = self._create_empty_index()
            print("📚 Novo índice criado")
    
    def _create_empty_index(self) -> Dict:
        """
        Cria estrutura vazia do índice
        
        Returns:
            Dict: Estrutura vazia do índice
        """
        return {
            "metadata": {
                "created_at": datetime.utcnow().isoformat(),
                "last_updated": datetime.utcnow().isoformat(),
                "version": "1.0.0",
                "total_documents": 0
            },
            "documents": []
        }
    
    def add_documents(self, documents: List[Dict]) -> None:
        """
        Adiciona documentos ao índice
        
        Args:
            documents: Lista de documentos com metadados
        """
        if not documents:
            return
        
        # Adicionar documentos ao índice
        for doc in documents:
            self.index_data["documents"].append(doc)
        
        # Atualizar metadados
        self.index_data["metadata"]["last_updated"] = datetime.utcnow().isoformat()
        self.index_data["metadata"]["total_documents"] = len(self.index_data["documents"])
        
        print(f"📝 {len(documents)} documentos adicionados ao índice")
    
    def save_index(self) -> None:
        """
        Salva índice no disco
        
        Cria backup do índice anterior antes de salvar
        a nova versão.
        """
        try:
            # Criar backup se índice existir
            if self.index_path.exists():
                self._create_backup()
            
            # Salvar novo índice
            with open(self.index_path, 'w', encoding='utf-8') as f:
                json.dump(self.index_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Índice salvo: {self.index_path}")
            
        except Exception as e:
            # self.logger.error(f"Erro ao salvar índice: {e}")
            raise
    
    def _create_backup(self) -> None:
        """
        Cria backup do índice atual
        """
        try:
            import shutil
            shutil.copy2(self.index_path, self.backup_path)
            print(f"💾 Backup criado: {self.backup_path}")
        except Exception as e:
            # self.logger.warning(f"Erro ao criar backup: {e}")
            pass
    
    def get_document_by_hash(self, file_hash: str) -> Optional[Dict]:
        """
        Busca documento por hash
        
        Args:
            file_hash: Hash do arquivo
            
        Returns:
            Dict: Documento encontrado ou None
        """
        for doc in self.index_data["documents"]:
            if doc.get("file_hash") == file_hash:
                return doc
        return None
    
    def get_documents_by_type(self, document_type: str) -> List[Dict]:
        """
        Busca documentos por tipo
        
        Args:
            document_type: Tipo do documento
            
        Returns:
            List[Dict]: Lista de documentos do tipo especificado
        """
        return [
            doc for doc in self.index_data["documents"]
            if doc.get("document_type") == document_type
        ]
    
    def get_documents_by_year(self, year: int) -> List[Dict]:
        """
        Busca documentos por ano
        
        Args:
            year: Ano dos documentos
            
        Returns:
            List[Dict]: Lista de documentos do ano especificado
        """
        return [
            doc for doc in self.index_data["documents"]
            if doc.get("year") == year
        ]
    
    def get_stats(self) -> Dict:
        """
        Retorna estatísticas do índice
        
        Returns:
            Dict: Estatísticas do índice
        """
        documents = self.index_data["documents"]
        
        # Contar por tipo
        type_counts = {}
        for doc in documents:
            doc_type = doc.get("document_type", "unknown")
            type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
        
        # Contar por ano
        year_counts = {}
        for doc in documents:
            year = doc.get("year", "unknown")
            year_counts[year] = year_counts.get(year, 0) + 1
        
        return {
            "total_documents": len(documents),
            "by_type": type_counts,
            "by_year": year_counts,
            "last_updated": self.index_data["metadata"]["last_updated"]
        }


