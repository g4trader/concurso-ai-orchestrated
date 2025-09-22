"""
Sistema de Busca de Editais de Concursos Públicos
Busca editais de fontes oficiais e portais especializados
"""

import requests
import re
from typing import List, Dict, Optional
import logging
from urllib.parse import urljoin, urlparse
import time

# Import opcional do BeautifulSoup
try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False

logger = logging.getLogger(__name__)

class EditalFetcher:
    """Classe para buscar editais de concursos públicos"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Fontes oficiais e portais especializados
        self.fontes_editais = {
            "cespe": {
                "nome": "CESPE/CEBRASPE",
                "url": "https://www.cespe.cebraspe.org.br/concursos",
                "tipo": "banca"
            },
            "fcc": {
                "nome": "FCC - Fundação Carlos Chagas",
                "url": "https://www.concursosfcc.com.br/concursos",
                "tipo": "banca"
            },
            "fgv": {
                "nome": "FGV - Fundação Getúlio Vargas",
                "url": "https://fgvprojetos.fgv.br/concursos",
                "tipo": "banca"
            },
            "vunesp": {
                "nome": "VUNESP",
                "url": "https://www.vunesp.com.br/concursos",
                "tipo": "banca"
            },
            "pci": {
                "nome": "PCI Concursos",
                "url": "https://www.pciconcursos.com.br/concursos",
                "tipo": "portal"
            },
            "estrategia": {
                "nome": "Estratégia Concursos",
                "url": "https://www.estrategiaconcursos.com.br/concursos",
                "tipo": "portal"
            },
            "gran": {
                "nome": "Gran Cursos",
                "url": "https://www.grancursosonline.com.br/concursos",
                "tipo": "portal"
            }
        }
    
    def buscar_concursos_ativos(self, fonte: str = None) -> List[Dict]:
        """Busca concursos ativos de uma fonte específica ou todas"""
        concursos = []
        
        if fonte and fonte in self.fontes_editais:
            fontes = {fonte: self.fontes_editais[fonte]}
        else:
            fontes = self.fontes_editais
        
        for fonte_id, info_fonte in fontes.items():
            try:
                logger.info(f"Buscando concursos em {info_fonte['nome']}")
                concursos_fonte = self._buscar_concursos_fonte(fonte_id, info_fonte)
                concursos.extend(concursos_fonte)
                time.sleep(1)  # Respeitar rate limiting
            except Exception as e:
                logger.error(f"Erro ao buscar concursos em {info_fonte['nome']}: {e}")
                continue
        
        return concursos
    
    def _buscar_concursos_fonte(self, fonte_id: str, info_fonte: Dict) -> List[Dict]:
        """Busca concursos de uma fonte específica"""
        concursos = []
        
        try:
            # Para demonstração, vamos criar dados simulados baseados em concursos reais
            if fonte_id == "cespe":
                concursos = self._simular_concursos_cespe()
            elif fonte_id == "fcc":
                concursos = self._simular_concursos_fcc()
            elif fonte_id == "fgv":
                concursos = self._simular_concursos_fgv()
            elif fonte_id == "vunesp":
                concursos = self._simular_concursos_vunesp()
            else:
                concursos = self._simular_concursos_portais()
            
            # Adicionar informações da fonte
            for concurso in concursos:
                concurso['fonte'] = fonte_id
                concurso['fonte_nome'] = info_fonte['nome']
                concurso['fonte_url'] = info_fonte['url']
            
        except Exception as e:
            logger.error(f"Erro ao processar fonte {fonte_id}: {e}")
        
        return concursos
    
    def _simular_concursos_cespe(self) -> List[Dict]:
        """Simula concursos do CESPE (dados baseados em concursos reais)"""
        return [
            {
                "id": "cespe_001",
                "titulo": "Concurso Público - Tribunal Regional do Trabalho da 1ª Região",
                "orgao": "TRT-1",
                "banca": "CESPE/CEBRASPE",
                "vagas": 50,
                "cargos": ["Analista Judiciário", "Técnico Judiciário"],
                "salario": "R$ 8.500,00",
                "inscricoes": "15/02/2024 a 15/03/2024",
                "prova": "15/04/2024",
                "edital_url": "https://www.trt1.jus.br/concursos/edital-trt1-2024.pdf",
                "status": "inscricoes_abertas",
                "nivel": "superior_medio"
            },
            {
                "id": "cespe_002",
                "titulo": "Concurso Público - Ministério Público da União",
                "orgao": "MPU",
                "banca": "CESPE/CEBRASPE",
                "vagas": 100,
                "cargos": ["Procurador da República", "Analista do MPU"],
                "salario": "R$ 15.000,00",
                "inscricoes": "01/03/2024 a 31/03/2024",
                "prova": "20/05/2024",
                "edital_url": "https://www.mpu.mp.br/concursos/edital-mpu-2024.pdf",
                "status": "inscricoes_abertas",
                "nivel": "superior"
            }
        ]
    
    def _simular_concursos_fcc(self) -> List[Dict]:
        """Simula concursos da FCC"""
        return [
            {
                "id": "fcc_001",
                "titulo": "Concurso Público - Tribunal Regional do Trabalho da 2ª Região",
                "orgao": "TRT-2",
                "banca": "FCC",
                "vagas": 80,
                "cargos": ["Analista Judiciário", "Técnico Judiciário"],
                "salario": "R$ 9.200,00",
                "inscricoes": "20/02/2024 a 20/03/2024",
                "prova": "25/04/2024",
                "edital_url": "https://www.trt2.jus.br/concursos/edital-trt2-2024.pdf",
                "status": "inscricoes_abertas",
                "nivel": "superior_medio"
            },
            {
                "id": "fcc_002",
                "titulo": "Concurso Público - Prefeitura de São Paulo",
                "orgao": "PMSP",
                "banca": "FCC",
                "vagas": 200,
                "cargos": ["Professor", "Agente de Fiscalização"],
                "salario": "R$ 4.500,00",
                "inscricoes": "10/03/2024 a 10/04/2024",
                "prova": "15/05/2024",
                "edital_url": "https://www.prefeitura.sp.gov.br/concursos/edital-pmsp-2024.pdf",
                "status": "inscricoes_abertas",
                "nivel": "superior_medio"
            }
        ]
    
    def _simular_concursos_fgv(self) -> List[Dict]:
        """Simula concursos da FGV"""
        return [
            {
                "id": "fgv_001",
                "titulo": "Concurso Público - Tribunal de Justiça do Estado de São Paulo",
                "orgao": "TJ-SP",
                "banca": "FGV",
                "vagas": 150,
                "cargos": ["Juiz de Direito", "Analista Judiciário"],
                "salario": "R$ 12.000,00",
                "inscricoes": "25/02/2024 a 25/03/2024",
                "prova": "30/04/2024",
                "edital_url": "https://www.tjsp.jus.br/concursos/edital-tjsp-2024.pdf",
                "status": "inscricoes_abertas",
                "nivel": "superior"
            }
        ]
    
    def _simular_concursos_vunesp(self) -> List[Dict]:
        """Simula concursos da VUNESP"""
        return [
            {
                "id": "vunesp_001",
                "titulo": "Concurso Público - Polícia Civil do Estado de São Paulo",
                "orgao": "PC-SP",
                "banca": "VUNESP",
                "vagas": 300,
                "cargos": ["Delegado", "Investigador", "Escrivão"],
                "salario": "R$ 7.500,00",
                "inscricoes": "05/03/2024 a 05/04/2024",
                "prova": "10/05/2024",
                "edital_url": "https://www.policiacivil.sp.gov.br/concursos/edital-pcsp-2024.pdf",
                "status": "inscricoes_abertas",
                "nivel": "superior_medio"
            }
        ]
    
    def _simular_concursos_portais(self) -> List[Dict]:
        """Simula concursos de portais especializados"""
        return [
            {
                "id": "portal_001",
                "titulo": "Concurso Público - Banco do Brasil",
                "orgao": "BB",
                "banca": "CESGRANRIO",
                "vagas": 500,
                "cargos": ["Escriturário", "Analista"],
                "salario": "R$ 6.000,00",
                "inscricoes": "15/03/2024 a 15/04/2024",
                "prova": "20/05/2024",
                "edital_url": "https://www.bb.com.br/concursos/edital-bb-2024.pdf",
                "status": "inscricoes_abertas",
                "nivel": "superior_medio"
            }
        ]
    
    def buscar_edital_por_id(self, concurso_id: str) -> Optional[Dict]:
        """Busca um edital específico por ID"""
        try:
            # Buscar em todas as fontes
            concursos = self.buscar_concursos_ativos()
            
            for concurso in concursos:
                if concurso['id'] == concurso_id:
                    return concurso
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar edital por ID {concurso_id}: {e}")
            return None
    
    def extrair_conteudo_edital(self, url_edital: str) -> Optional[str]:
        """Extrai o conteúdo de um edital a partir da URL"""
        try:
            logger.info(f"Extraindo conteúdo do edital: {url_edital}")
            
            # Para demonstração, vamos retornar um conteúdo simulado
            # Em produção, aqui seria feita a extração real do PDF ou HTML
            
            conteudo_simulado = f"""
            EDITAL Nº 1/2024 - CONCURSO PÚBLICO
            {url_edital}
            
            O órgão responsável torna pública a realização de concurso público para o provimento de vagas.
            
            1. DO CONCURSO
            1.1 O concurso será executado pela banca organizadora.
            1.2 Exige nível superior e/ou médio conforme o cargo.
            1.3 Remuneração inicial conforme tabela salarial.
            
            2. DAS INSCRIÇÕES
            2.1 Período de inscrições conforme cronograma.
            2.2 Taxa de inscrição conforme tabela.
            2.3 Inscrições exclusivamente via internet.
            
            3. DAS PROVAS
            3.1 Prova Objetiva de múltipla escolha.
            3.2 Prova Discursiva (para alguns cargos).
            3.3 Prova de Títulos (para alguns cargos).
            
            4. DO CONTEÚDO PROGRAMÁTICO
            4.1 Língua Portuguesa
            4.2 Matemática
            4.3 Informática
            4.4 Conhecimentos Específicos
            4.5 Legislação Aplicada
            
            5. DA CLASSIFICAÇÃO E APROVAÇÃO
            5.1 Será considerado aprovado o candidato que obtiver nota mínima.
            5.2 Classificação por ordem decrescente de notas.
            
            6. DO CRONOGRAMA
            6.1 Publicação do Edital: {time.strftime('%d/%m/%Y')}
            6.2 Inscrições: Conforme cronograma específico
            6.3 Prova Objetiva: Conforme cronograma específico
            6.4 Resultado: Conforme cronograma específico
            
            Este edital foi extraído automaticamente de: {url_edital}
            """
            
            return conteudo_simulado.strip()
            
        except Exception as e:
            logger.error(f"Erro ao extrair conteúdo do edital {url_edital}: {e}")
            return None
    
    def filtrar_concursos(self, concursos: List[Dict], filtros: Dict) -> List[Dict]:
        """Filtra concursos baseado em critérios"""
        try:
            concursos_filtrados = concursos.copy()
            
            # Filtro por banca
            if filtros.get('banca'):
                concursos_filtrados = [
                    c for c in concursos_filtrados 
                    if filtros['banca'].lower() in c.get('banca', '').lower()
                ]
            
            # Filtro por órgão
            if filtros.get('orgao'):
                concursos_filtrados = [
                    c for c in concursos_filtrados 
                    if filtros['orgao'].lower() in c.get('orgao', '').lower()
                ]
            
            # Filtro por nível
            if filtros.get('nivel'):
                concursos_filtrados = [
                    c for c in concursos_filtrados 
                    if filtros['nivel'] in c.get('nivel', '')
                ]
            
            # Filtro por status
            if filtros.get('status'):
                concursos_filtrados = [
                    c for c in concursos_filtrados 
                    if filtros['status'] in c.get('status', '')
                ]
            
            return concursos_filtrados
            
        except Exception as e:
            logger.error(f"Erro ao filtrar concursos: {e}")
            return concursos
