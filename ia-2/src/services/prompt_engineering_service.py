"""
Serviço de Engenharia de Prompt para IA-2
"""

import structlog
from typing import Dict, Any, List

logger = structlog.get_logger(__name__)

class PromptEngineeringService:
    """
    Serviço responsável por criar prompts otimizados para geração de questões.
    """

    def __init__(self):
        logger.info("PromptEngineeringService inicializado.")

    async def create_prompt(self, contexts: List[Dict[str, Any]], edital_summary: Dict[str, Any], topic: str) -> str:
        """
        Cria um prompt otimizado para geração de questões.
        """
        logger.info("Criando prompt para geração de questão.", topic=topic)
        
        # Prompt básico para geração de questões
        prompt = f"""
        Com base no contexto fornecido e no resumo do edital, gere uma questão de múltipla escolha sobre o tópico: {topic}
        
        Resumo do Edital:
        - Banca: {edital_summary.get('banca', 'N/A')}
        - Ano: {edital_summary.get('ano', 'N/A')}
        - Dificuldade: {edital_summary.get('dificuldade', 'intermediária')}
        - Estilo: {edital_summary.get('estilo', 'conceitual')}
        
        Contexto: {contexts}
        
        Gere uma questão seguindo o formato:
        - Enunciado claro e objetivo
        - 5 alternativas (A, B, C, D, E)
        - Uma resposta correta
        - Justificativa da resposta
        - Referência aos trechos do contexto utilizados
        """
        
        logger.info("Prompt criado com sucesso.")
        return prompt
