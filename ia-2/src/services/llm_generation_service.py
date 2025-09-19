"""
Serviço de Geração LLM para IA-2
"""

import structlog
from typing import Dict, Any

logger = structlog.get_logger(__name__)

class LLMGenerationService:
    """
    Serviço responsável por gerar questões usando LLMs.
    """

    def __init__(self):
        logger.info("LLMGenerationService inicializado.")

    async def generate_question(self, prompt: str) -> Dict[str, Any]:
        """
        Gera uma questão usando LLM baseado no prompt fornecido.
        """
        logger.info("Gerando questão com LLM.")
        
        # Mock response - em produção seria integração com LLM real
        mock_question = {
            "question": "Qual é a principal função do sistema de gestão de documentos?",
            "alternatives": [
                "A) Armazenar informações de forma desorganizada",
                "B) Organizar, armazenar e facilitar o acesso a documentos digitais",
                "C) Apenas imprimir documentos",
                "D) Excluir documentos antigos automaticamente",
                "E) Criar documentos automaticamente"
            ],
            "correct_answer": "B",
            "justification": "O sistema de gestão de documentos tem como principal função organizar, armazenar e facilitar o acesso a documentos digitais, permitindo controle de versões, busca eficiente e segurança da informação.",
            "source_chunks": ["chunk_1", "chunk_2"]
        }
        
        logger.info("Questão gerada com sucesso.")
        return mock_question
