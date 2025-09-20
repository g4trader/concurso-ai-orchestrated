"""
Serviço de integração com Ollama
"""

import httpx
import json
import time
from typing import List, Dict, Any
from datetime import datetime
from fastapi import HTTPException
from src.models.request import QuestionRequest
from src.models.response import QuestionResponse, ModelInfo
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class OllamaService:
    """Serviço para integração com Ollama"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=settings.OLLAMA_TIMEOUT)
        self.host = settings.OLLAMA_HOST
    
    async def list_models(self) -> List[ModelInfo]:
        """Listar modelos disponíveis"""
        try:
            response = await self.client.get(f"{self.host}/api/tags")
            if response.status_code == 200:
                models_data = response.json()
                return [
                    ModelInfo(
                        name=model["name"],
                        size=model.get("size", "unknown"),
                        modified_at=model.get("modified_at", "unknown"),
                        digest=model.get("digest", "unknown")
                    )
                    for model in models_data.get("models", [])
                ]
            else:
                raise HTTPException(status_code=500, detail="Erro ao listar modelos")
        except Exception as e:
            logger.error(f"Erro ao listar modelos: {e}")
            raise HTTPException(status_code=500, detail=f"Erro ao conectar com Ollama: {e}")
    
    async def generate_question(self, request: QuestionRequest) -> QuestionResponse:
        """Gerar questão de concurso"""
        start_time = time.time()
        
        try:
            # Preparar prompt otimizado
            optimized_prompt = self._prepare_prompt(request)
            
            # Fazer requisição para Ollama
            ollama_request = {
                "model": request.model or settings.DEFAULT_MODEL,
                "prompt": optimized_prompt,
                "stream": False,
                "options": {
                    "temperature": request.temperature,
                    "num_predict": request.max_tokens
                }
            }
            
            response = await self.client.post(
                f"{self.host}/api/generate",
                json=ollama_request
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Erro na geração com Ollama")
            
            # Processar resposta
            ollama_response = response.json()
            generated_text = ollama_response.get("response", "")
            
            # Extrair dados estruturados
            question_data = self._extract_question_data(generated_text)
            
            processing_time = time.time() - start_time
            
            return QuestionResponse(
                question=question_data["question"],
                alternatives=question_data["alternatives"],
                correct_answer=question_data["correct_answer"],
                explanation=question_data["explanation"],
                model_used=request.model or settings.DEFAULT_MODEL,
                processing_time=processing_time,
                timestamp=datetime.now()
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erro na geração de questão: {e}")
            raise HTTPException(status_code=500, detail=f"Erro interno: {e}")
    
    def _prepare_prompt(self, request: QuestionRequest) -> str:
        """Preparar prompt otimizado para questões de concurso"""
        return f"""
Você é um especialista em concursos públicos. Gere uma questão de múltipla escolha seguindo este formato:

PROMPT: {request.prompt}

FORMATO DE RESPOSTA (JSON):
{{
    "question": "Enunciado da questão",
    "alternatives": ["A) Alternativa 1", "B) Alternativa 2", "C) Alternativa 3", "D) Alternativa 4"],
    "correct_answer": "A",
    "explanation": "Explicação detalhada da resposta correta"
}}

CONTEXTO: {request.context or "Concurso público geral"}

Gere uma questão clara, objetiva e com alternativas bem diferenciadas.
"""
    
    def _extract_question_data(self, generated_text: str) -> Dict[str, Any]:
        """Extrair dados estruturados da resposta gerada"""
        try:
            # Procurar por JSON na resposta
            json_start = generated_text.find('{')
            json_end = generated_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_text = generated_text[json_start:json_end]
                return json.loads(json_text)
            else:
                # Fallback: criar estrutura básica
                return {
                    "question": generated_text[:200] + "...",
                    "alternatives": ["A) Alternativa A", "B) Alternativa B", "C) Alternativa C", "D) Alternativa D"],
                    "correct_answer": "A",
                    "explanation": "Explicação baseada na resposta gerada."
                }
        except json.JSONDecodeError:
            # Fallback em caso de erro no JSON
            return {
                "question": generated_text[:200] + "...",
                "alternatives": ["A) Alternativa A", "B) Alternativa B", "C) Alternativa C", "D) Alternativa D"],
                "correct_answer": "A",
                "explanation": "Explicação baseada na resposta gerada."
            }
    
    async def generate_questions_batch(self, requests: List[QuestionRequest]) -> Dict[str, Any]:
        """Gerar múltiplas questões em lote"""
        results = []
        
        for i, request in enumerate(requests):
            try:
                result = await self.generate_question(request)
                results.append({
                    "index": i,
                    "success": True,
                    "data": result
                })
            except Exception as e:
                results.append({
                    "index": i,
                    "success": False,
                    "error": str(e)
                })
        
        return {"results": results}
