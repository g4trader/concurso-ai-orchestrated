"""
Local Storage Manager

Este módulo é responsável pelo armazenamento local de arquivos.
Responsabilidades:
- Criação de diretórios
- Organização de arquivos
- Limpeza de arquivos temporários
- Verificação de espaço em disco
"""

import os
import shutil
from pathlib import Path
from typing import Optional

# TODO: Implementar imports necessários
# from src.config.settings import CrawlerConfig
# from src.utils.logger import get_logger

class LocalStorageManager:
    """
    Gerenciador de armazenamento local
    
    Responsável por gerenciar o armazenamento local de arquivos PDF
    e metadados do sistema.
    """
    
    def __init__(self, config):
        """
        Inicializa o gerenciador de armazenamento
        
        Args:
            config: Configurações do crawler
        """
        self.config = config
        # self.logger = get_logger(__name__)
        self.pdfs_dir = Path(config.pdfs_dir)
        self.output_dir = Path(config.output_dir)
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """
        Garante que todos os diretórios necessários existam
        """
        directories = [
            self.output_dir,
            self.pdfs_dir,
            Path(self.config.logs_dir)
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"📁 Diretório verificado: {directory}")
    
    def get_available_space(self) -> int:
        """
        Retorna espaço disponível em bytes
        
        Returns:
            int: Espaço disponível em bytes
        """
        try:
            stat = shutil.disk_usage(self.output_dir)
            return stat.free
        except Exception as e:
            # self.logger.error(f"Erro ao verificar espaço: {e}")
            return 0
    
    def get_used_space(self) -> int:
        """
        Retorna espaço usado em bytes
        
        Returns:
            int: Espaço usado em bytes
        """
        total_size = 0
        
        try:
            for file_path in self.pdfs_dir.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception as e:
            # self.logger.error(f"Erro ao calcular espaço usado: {e}")
            pass
        
        return total_size
    
    def cleanup_temp_files(self) -> None:
        """
        Remove arquivos temporários
        """
        temp_patterns = ["*.tmp", "*.temp", "*.part"]
        cleaned_count = 0
        
        for pattern in temp_patterns:
            for temp_file in self.pdfs_dir.glob(pattern):
                try:
                    temp_file.unlink()
                    cleaned_count += 1
                except Exception as e:
                    # self.logger.warning(f"Erro ao remover {temp_file}: {e}")
                    pass
        
        if cleaned_count > 0:
            print(f"🧹 {cleaned_count} arquivos temporários removidos")
    
    def organize_files_by_type(self) -> None:
        """
        Organiza arquivos em subdiretórios por tipo
        """
        # TODO: Implementar organização por tipo
        # 1. Ler metadados do índice
        # 2. Mover arquivos para subdiretórios por tipo
        # 3. Atualizar caminhos no índice
        
        print("📂 Organização de arquivos por tipo (placeholder)")
    
    def get_file_info(self, file_path: str) -> Optional[dict]:
        """
        Retorna informações de um arquivo
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            dict: Informações do arquivo ou None
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return None
            
            stat = path.stat()
            return {
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "exists": True
            }
        except Exception as e:
            # self.logger.error(f"Erro ao obter info do arquivo {file_path}: {e}")
            return None


