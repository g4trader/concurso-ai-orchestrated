from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import logging
from app.ai.edital_analyzer_simples import EditalAnalyzerSimples
from app.ai.edital_analyzer_real import EditalAnalyzerReal
from .routes_editais import router as editais_router

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="Analisador de Editais - IA",
    description="Sistema de análise inteligente de editais de concursos públicos",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas de editais
app.include_router(editais_router)

# Instanciar analisador real
analyzer = EditalAnalyzerReal()

class EditalRequest(BaseModel):
    conteudo: str
    url_edital: str = None
    banca: str = None

class EditalResponse(BaseModel):
    status: str
    resultado: Dict[str, Any]
    tempo_processamento: float

@app.get("/health")
async def health_check():
    """Verificação de saúde do serviço"""
    return {
        "status": "healthy",
        "service": "edital-analyzer",
        "version": "2.0.0",
        "ai_available": True
    }

@app.post("/analyze", response_model=EditalResponse)
async def analisar_edital(request: EditalRequest):
    """
    Analisa um edital de concurso público
    """
    try:
        import time
        start_time = time.time()
        
        logger.info(f"Iniciando análise de edital - URL: {request.url_edital}")
        
        # Validar entrada
        if not request.conteudo or len(request.conteudo.strip()) < 100:
            raise HTTPException(
                status_code=400, 
                detail="Conteúdo do edital muito curto. Mínimo 100 caracteres."
            )
        
        # Executar análise
        resultado = analyzer.analisar_edital_completo(request.conteudo)
        
        # Calcular tempo de processamento
        tempo_processamento = time.time() - start_time
        
        logger.info(f"Análise concluída em {tempo_processamento:.2f} segundos")
        
        return EditalResponse(
            status="success",
            resultado=resultado,
            tempo_processamento=tempo_processamento
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na análise do edital: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno na análise: {str(e)}"
        )

@app.get("/analyze/sample")
async def analisar_edital_exemplo():
    """
    Analisa um edital de exemplo para demonstração
    """
    try:
        # Edital de exemplo
        edital_exemplo = """
        EDITAL Nº 1 – DGP/DPF, DE 15 DE JUNHO DE 2023
        CONCURSO PÚBLICO PARA O PROVIMENTO DE VAGAS NO CARGO DE AGENTE DE POLÍCIA FEDERAL

        O DIRETOR-GERAL DA POLÍCIA FEDERAL, no uso de suas atribuições, torna pública a realização de concurso público para o provimento de 1.500 vagas no cargo de Agente de Polícia Federal.

        1 DAS DISPOSIÇÕES PRELIMINARES
        1.1 O concurso público será regido por este edital e executado pelo Centro Brasileiro de Pesquisa em Avaliação e Seleção e de Promoção de Eventos (Cebraspe).
        1.2 O cargo de Agente de Polícia Federal exige nível superior em qualquer área de formação.
        1.3 A remuneração inicial é de R$ 12.522,50.

        2 DAS INSCRIÇÕES
        2.1 As inscrições poderão ser realizadas no período de 20/07/2023 a 02/08/2023.
        2.2 A taxa de inscrição é de R$ 180,00.

        3 DAS ETAPAS DO CONCURSO
        3.1 Prova Objetiva e Discursiva: 19/09/2023.
        3.2 Exame de Aptidão Física.
        3.3 Avaliação Médica.
        3.4 Avaliação Psicológica.

        4 DAS DISCIPLINAS
        Serão cobradas as seguintes disciplinas: Língua Portuguesa, Noções de Direito Administrativo, Noções de Direito Constitucional, Raciocínio Lógico, Informática, Contabilidade Geral.
        """
        
        import time
        start_time = time.time()
        
        # Executar análise
        resultado = analyzer.analisar_edital_completo(edital_exemplo)
        
        tempo_processamento = time.time() - start_time
        
        return EditalResponse(
            status="success",
            resultado=resultado,
            tempo_processamento=tempo_processamento
        )
        
    except Exception as e:
        logger.error(f"Erro na análise do edital de exemplo: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno na análise: {str(e)}"
        )

@app.get("/stats")
async def obter_estatisticas():
    """
    Obtém estatísticas do analisador
    """
    return {
        "status": "success",
        "estatisticas": {
            "versao": "2.0.0",
            "modelo_ia": "Regex + Lógica Inteligente",
            "disciplinas_conhecidas": len(analyzer.disciplinas_conhecidas),
            "bancas_conhecidas": len(analyzer.bancas_conhecidas),
            "cargos_conhecidos": len(analyzer.cargos_comuns),
            "funcionalidades": [
                "Análise de estrutura",
                "Extração de informações",
                "Identificação de datas",
                "Extração de valores",
                "Análise de disciplinas",
                "Geração de resumo",
                "Análise de relevância"
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
