"""
Hash utilities

Este módulo é responsável por cálculos de hash e verificação de integridade.
Responsabilidades:
- Cálculo de hash SHA-256
- Verificação de integridade de arquivos
- Comparação de hashes
- Otimização para arquivos grandes
"""

import hashlib
from pathlib import Path
from typing import Optional

def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """
    Calcula hash de um arquivo
    
    Args:
        file_path: Caminho do arquivo
        algorithm: Algoritmo de hash (sha256, md5, sha1)
        
    Returns:
        str: Hash em hexadecimal
        
    Raises:
        FileNotFoundError: Se arquivo não existir
        ValueError: Se algoritmo não for suportado
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    # Selecionar algoritmo
    if algorithm == "sha256":
        hash_obj = hashlib.sha256()
    elif algorithm == "md5":
        hash_obj = hashlib.md5()
    elif algorithm == "sha1":
        hash_obj = hashlib.sha1()
    else:
        raise ValueError(f"Algoritmo não suportado: {algorithm}")
    
    # Calcular hash em chunks para economizar memória
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()

def calculate_string_hash(text: str, algorithm: str = "sha256") -> str:
    """
    Calcula hash de uma string
    
    Args:
        text: Texto para calcular hash
        algorithm: Algoritmo de hash
        
    Returns:
        str: Hash em hexadecimal
    """
    if algorithm == "sha256":
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    elif algorithm == "md5":
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(text.encode('utf-8')).hexdigest()
    else:
        raise ValueError(f"Algoritmo não suportado: {algorithm}")

def verify_file_integrity(file_path: str, expected_hash: str, algorithm: str = "sha256") -> bool:
    """
    Verifica integridade de um arquivo
    
    Args:
        file_path: Caminho do arquivo
        expected_hash: Hash esperado
        algorithm: Algoritmo de hash
        
    Returns:
        bool: True se integridade estiver OK
    """
    try:
        actual_hash = calculate_file_hash(file_path, algorithm)
        return actual_hash.lower() == expected_hash.lower()
    except Exception:
        return False

def get_file_size(file_path: str) -> int:
    """
    Retorna tamanho do arquivo em bytes
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        int: Tamanho em bytes
    """
    return Path(file_path).stat().st_size


