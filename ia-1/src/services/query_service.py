"""
Serviço de Query para IA-1
"""

import structlog
from typing import List, Dict, Any, Optional
from src.services.indexing_service import IndexingService
from src.services.embedding_service import EmbeddingService

logger = structlog.get_logger(__name__)

class QueryService:
    """
    Serviço responsável por realizar buscas e queries nos documentos indexados.
    """

    def __init__(self):
        logger.info("QueryService inicializado.")
        self.indexing_service = IndexingService()
        self.embedding_service = EmbeddingService()

    async def search_similarity(
        self, 
        query: str, 
        filters: Optional[Dict[str, Any]] = None, 
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Realiza busca por similaridade usando embeddings.

        Args:
            query (str): A query de busca.
            filters (Optional[Dict[str, Any]]): Filtros adicionais.
            top_k (int): Número de resultados a retornar.

        Returns:
            List[Dict[str, Any]]: Lista de resultados com scores de similaridade.
        """
        logger.info("Realizando busca por similaridade.", query=query, top_k=top_k)
        
        try:
            # 1. Gerar embedding da query
            query_embedding = await self.embedding_service.generate_embeddings([query])
            if not query_embedding:
                logger.warning("Falha ao gerar embedding da query.")
                return []
            
            # 2. Buscar no índice
            search_results = await self.indexing_service.search_index(
                query_embedding[0], 
                k=top_k
            )
            
            # 3. Aplicar filtros se fornecidos
            if filters:
                search_results = self._apply_filters(search_results, filters)
            
            # 4. Formatar resultados
            formatted_results = []
            for result in search_results:
                formatted_results.append({
                    "document_id": result["document_id"],
                    "content": result.get("content", ""),
                    "score": 1.0 - result["distance"],  # Converter distância para score
                    "metadata": result.get("metadata", {})
                })
            
            logger.info("Busca por similaridade concluída.", 
                       num_results=len(formatted_results))
            return formatted_results
            
        except Exception as e:
            logger.error("Erro na busca por similaridade.", error=str(e))
            return []

    async def search_by_keywords(
        self, 
        keywords: List[str], 
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Realiza busca por palavras-chave (busca textual).

        Args:
            keywords (List[str]): Lista de palavras-chave.
            filters (Optional[Dict[str, Any]]): Filtros adicionais.
            top_k (int): Número de resultados a retornar.

        Returns:
            List[Dict[str, Any]]: Lista de resultados.
        """
        logger.info("Realizando busca por palavras-chave.", 
                   keywords=keywords, top_k=top_k)
        
        try:
            # TODO: Implementar busca textual
            # Por enquanto, retorna lista vazia
            logger.warning("Busca por palavras-chave não implementada ainda.")
            return []
            
        except Exception as e:
            logger.error("Erro na busca por palavras-chave.", error=str(e))
            return []

    async def hybrid_search(
        self, 
        query: str, 
        keywords: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10,
        similarity_weight: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Realiza busca híbrida combinando similaridade e palavras-chave.

        Args:
            query (str): Query principal.
            keywords (Optional[List[str]]): Palavras-chave adicionais.
            filters (Optional[Dict[str, Any]]): Filtros adicionais.
            top_k (int): Número de resultados a retornar.
            similarity_weight (float): Peso da busca por similaridade (0-1).

        Returns:
            List[Dict[str, Any]]: Lista de resultados combinados.
        """
        logger.info("Realizando busca híbrida.", 
                   query=query, keywords=keywords, similarity_weight=similarity_weight)
        
        try:
            # 1. Busca por similaridade
            similarity_results = await self.search_similarity(query, filters, top_k)
            
            # 2. Busca por palavras-chave (se fornecidas)
            keyword_results = []
            if keywords:
                keyword_results = await self.search_by_keywords(keywords, filters, top_k)
            
            # 3. Combinar resultados
            combined_results = self._combine_search_results(
                similarity_results, 
                keyword_results, 
                similarity_weight
            )
            
            # 4. Ordenar por score combinado
            combined_results.sort(key=lambda x: x["combined_score"], reverse=True)
            
            # 5. Retornar top_k resultados
            final_results = combined_results[:top_k]
            
            logger.info("Busca híbrida concluída.", num_results=len(final_results))
            return final_results
            
        except Exception as e:
            logger.error("Erro na busca híbrida.", error=str(e))
            return []

    def _apply_filters(
        self, 
        results: List[Dict[str, Any]], 
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Aplica filtros aos resultados da busca.

        Args:
            results (List[Dict[str, Any]]): Resultados da busca.
            filters (Dict[str, Any]): Filtros a aplicar.

        Returns:
            List[Dict[str, Any]]: Resultados filtrados.
        """
        filtered_results = []
        
        for result in results:
            metadata = result.get("metadata", {})
            include_result = True
            
            for filter_key, filter_value in filters.items():
                if filter_key not in metadata:
                    include_result = False
                    break
                
                if isinstance(filter_value, list):
                    if metadata[filter_key] not in filter_value:
                        include_result = False
                        break
                else:
                    if metadata[filter_key] != filter_value:
                        include_result = False
                        break
            
            if include_result:
                filtered_results.append(result)
        
        logger.debug("Filtros aplicados.", 
                    original_count=len(results), 
                    filtered_count=len(filtered_results))
        return filtered_results

    def _combine_search_results(
        self, 
        similarity_results: List[Dict[str, Any]], 
        keyword_results: List[Dict[str, Any]], 
        similarity_weight: float
    ) -> List[Dict[str, Any]]:
        """
        Combina resultados de busca por similaridade e palavras-chave.

        Args:
            similarity_results (List[Dict[str, Any]]): Resultados de similaridade.
            keyword_results (List[Dict[str, Any]]): Resultados de palavras-chave.
            similarity_weight (float): Peso da busca por similaridade.

        Returns:
            List[Dict[str, Any]]: Resultados combinados.
        """
        combined_results = {}
        keyword_weight = 1.0 - similarity_weight
        
        # Adicionar resultados de similaridade
        for result in similarity_results:
            doc_id = result["document_id"]
            combined_results[doc_id] = {
                **result,
                "similarity_score": result["score"],
                "keyword_score": 0.0,
                "combined_score": result["score"] * similarity_weight
            }
        
        # Adicionar resultados de palavras-chave
        for result in keyword_results:
            doc_id = result["document_id"]
            if doc_id in combined_results:
                # Documento já existe, atualizar score
                combined_results[doc_id]["keyword_score"] = result["score"]
                combined_results[doc_id]["combined_score"] = (
                    combined_results[doc_id]["similarity_score"] * similarity_weight +
                    result["score"] * keyword_weight
                )
            else:
                # Novo documento
                combined_results[doc_id] = {
                    **result,
                    "similarity_score": 0.0,
                    "keyword_score": result["score"],
                    "combined_score": result["score"] * keyword_weight
                }
        
        return list(combined_results.values())

    async def get_suggestions(self, partial_query: str, limit: int = 5) -> List[str]:
        """
        Obtém sugestões de autocompletar baseadas na query parcial.

        Args:
            partial_query (str): Query parcial.
            limit (int): Número máximo de sugestões.

        Returns:
            List[str]: Lista de sugestões.
        """
        logger.info("Obtendo sugestões.", partial_query=partial_query, limit=limit)
        
        try:
            # TODO: Implementar sistema de sugestões
            # Por enquanto, retorna lista vazia
            logger.warning("Sistema de sugestões não implementado ainda.")
            return []
            
        except Exception as e:
            logger.error("Erro ao obter sugestões.", error=str(e))
            return []
