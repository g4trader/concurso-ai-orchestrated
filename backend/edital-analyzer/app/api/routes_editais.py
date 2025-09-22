"""
Rotas para busca e seleção de editais de concursos
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional
from pydantic import BaseModel
import logging

from .edital_fetcher import EditalFetcher
from .real_edital_fetcher import RealEditalFetcher

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/editais", tags=["editais"])

# Instância global do fetcher (usando fetcher real)
edital_fetcher = RealEditalFetcher()

class FiltroConcursos(BaseModel):
    """Modelo para filtros de concursos"""
    banca: Optional[str] = None
    orgao: Optional[str] = None
    nivel: Optional[str] = None
    status: Optional[str] = None

class ConcursoResponse(BaseModel):
    """Modelo de resposta para concurso"""
    id: str
    titulo: str
    orgao: str
    banca: str
    vagas: int
    cargos: List[str]
    salario: str
    inscricoes: str
    prova: str
    edital_url: str
    status: str
    nivel: str
    fonte: str
    fonte_nome: str
    fonte_url: str

class EditalContentResponse(BaseModel):
    """Modelo de resposta para conteúdo do edital"""
    concurso_id: str
    titulo: str
    conteudo: str
    url_edital: str
    fonte: str

@router.get("/concursos", response_model=List[ConcursoResponse])
async def listar_concursos(
    fonte: Optional[str] = Query(None, description="Fonte específica (cespe, fcc, fgv, vunesp, pci, estrategia, gran)"),
    banca: Optional[str] = Query(None, description="Filtrar por banca organizadora"),
    orgao: Optional[str] = Query(None, description="Filtrar por órgão"),
    nivel: Optional[str] = Query(None, description="Filtrar por nível (superior, medio, superior_medio)"),
    status: Optional[str] = Query(None, description="Filtrar por status (inscricoes_abertas, em_andamento, finalizado)")
):
    """
    Lista concursos públicos disponíveis para análise
    
    - **fonte**: Fonte específica para buscar (opcional)
    - **banca**: Filtrar por banca organizadora
    - **orgao**: Filtrar por órgão
    - **nivel**: Filtrar por nível de escolaridade
    - **status**: Filtrar por status do concurso
    """
    try:
        logger.info(f"Listando concursos - fonte: {fonte}, filtros: banca={banca}, orgao={orgao}, nivel={nivel}, status={status}")
        
        # Buscar concursos
        concursos = edital_fetcher.buscar_concursos_ativos(fonte)
        
        # Aplicar filtros
        filtros = {
            'banca': banca,
            'orgao': orgao,
            'nivel': nivel,
            'status': status
        }
        
        concursos_filtrados = edital_fetcher.filtrar_concursos(concursos, filtros)
        
        logger.info(f"Encontrados {len(concursos_filtrados)} concursos")
        
        return concursos_filtrados
        
    except Exception as e:
        logger.error(f"Erro ao listar concursos: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/concursos/{concurso_id}", response_model=ConcursoResponse)
async def obter_concurso(concurso_id: str):
    """
    Obtém informações detalhadas de um concurso específico
    """
    try:
        logger.info(f"Buscando concurso: {concurso_id}")
        
        concurso = edital_fetcher.buscar_edital_por_id(concurso_id)
        
        if not concurso:
            raise HTTPException(status_code=404, detail="Concurso não encontrado")
        
        logger.info(f"Concurso encontrado: {concurso['titulo']}")
        
        return concurso
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter concurso {concurso_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/concursos/{concurso_id}/edital", response_model=EditalContentResponse)
async def obter_conteudo_edital(concurso_id: str):
    """
    Obtém o conteúdo completo do edital de um concurso
    """
    try:
        logger.info(f"Buscando conteúdo do edital: {concurso_id}")
        
        # Buscar informações do concurso
        concurso = edital_fetcher.buscar_edital_por_id(concurso_id)
        
        if not concurso:
            raise HTTPException(status_code=404, detail="Concurso não encontrado")
        
        # Extrair conteúdo do edital
        conteudo = edital_fetcher.extrair_conteudo_edital(concurso['edital_url'])
        
        if not conteudo:
            raise HTTPException(status_code=500, detail="Erro ao extrair conteúdo do edital")
        
        response = EditalContentResponse(
            concurso_id=concurso_id,
            titulo=concurso['titulo'],
            conteudo=conteudo,
            url_edital=concurso['edital_url'],
            fonte=concurso['fonte_nome']
        )
        
        logger.info(f"Conteúdo do edital extraído com sucesso: {len(conteudo)} caracteres")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter conteúdo do edital {concurso_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/fontes")
async def listar_fontes():
    """
    Lista as fontes disponíveis para busca de editais
    """
    try:
        logger.info("Listando fontes de editais")
        
        fontes = []
        for fonte_id, info in edital_fetcher.fontes_editais.items():
            fontes.append({
                "id": fonte_id,
                "nome": info["nome"],
                "url": info["url"],
                "tipo": info["tipo"]
            })
        
        return {
            "fontes": fontes,
            "total": len(fontes)
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar fontes: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/concursos/{concurso_id}/analisar")
async def analisar_edital_concurso(concurso_id: str):
    """
    Analisa automaticamente o edital de um concurso específico
    """
    try:
        logger.info(f"Iniciando análise automática do concurso: {concurso_id}")
        
        # Buscar informações do concurso
        concurso = edital_fetcher.buscar_edital_por_id(concurso_id)
        
        if not concurso:
            raise HTTPException(status_code=404, detail="Concurso não encontrado")
        
        # Extrair conteúdo do edital
        conteudo = edital_fetcher.extrair_conteudo_edital(concurso['edital_url'])
        
        if not conteudo:
            raise HTTPException(status_code=500, detail="Erro ao extrair conteúdo do edital")
        
        # Preparar dados para análise
        dados_analise = {
            "conteudo": conteudo,
            "url_edital": concurso['edital_url'],
            "banca": concurso['banca'],
            "orgao": concurso['orgao'],
            "titulo": concurso['titulo']
        }
        
        # Aqui seria feita a análise usando o sistema existente
        # Por enquanto, retornamos os dados preparados
        return {
            "concurso_id": concurso_id,
            "titulo": concurso['titulo'],
            "dados_analise": dados_analise,
            "status": "dados_preparados",
            "mensagem": "Dados do edital extraídos e preparados para análise"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao analisar edital do concurso {concurso_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/estatisticas")
async def obter_estatisticas():
    """
    Obtém estatísticas dos concursos disponíveis
    """
    try:
        logger.info("Gerando estatísticas dos concursos")
        
        concursos = edital_fetcher.buscar_concursos_ativos()
        
        # Estatísticas por banca
        bancas = {}
        for concurso in concursos:
            banca = concurso.get('banca', 'Não informado')
            bancas[banca] = bancas.get(banca, 0) + 1
        
        # Estatísticas por órgão
        orgaos = {}
        for concurso in concursos:
            orgao = concurso.get('orgao', 'Não informado')
            orgaos[orgao] = orgaos.get(orgao, 0) + 1
        
        # Estatísticas por nível
        niveis = {}
        for concurso in concursos:
            nivel = concurso.get('nivel', 'Não informado')
            niveis[nivel] = niveis.get(nivel, 0) + 1
        
        # Total de vagas
        total_vagas = sum(concurso.get('vagas', 0) for concurso in concursos)
        
        return {
            "total_concursos": len(concursos),
            "total_vagas": total_vagas,
            "bancas": bancas,
            "orgaos": orgaos,
            "niveis": niveis,
            "fontes_ativas": len(edital_fetcher.fontes_editais)
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar estatísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
