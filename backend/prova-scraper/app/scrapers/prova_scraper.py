import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from typing import List, Dict, Optional, Tuple
import time
import logging
from datetime import datetime
import hashlib
import json
import re
from urllib.parse import urljoin, urlparse
import os

logger = logging.getLogger(__name__)

class ProvaScraper:
    """
    Scraper base para buscar provas de concursos
    """
    
    def __init__(self, banca: str, base_url: str):
        self.banca = banca
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def setup_driver(self) -> webdriver.Chrome:
        """Configura o driver do Selenium"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            logger.error(f"Erro ao configurar driver: {e}")
            raise
    
    def buscar_provas(self, limite: int = 50) -> List[Dict]:
        """
        Busca provas da banca (método abstrato - deve ser implementado pelas subclasses)
        """
        raise NotImplementedError("Método deve ser implementado pelas subclasses")
    
    def extrair_questoes_prova(self, url_prova: str) -> List[Dict]:
        """
        Extrai questões de uma prova específica (método abstrato)
        """
        raise NotImplementedError("Método deve ser implementado pelas subclasses")
    
    def _download_arquivo(self, url: str, destino: str) -> bool:
        """
        Baixa um arquivo da URL para o destino
        """
        try:
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            
            with open(destino, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Arquivo baixado: {destino}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao baixar arquivo {url}: {e}")
            return False
    
    def _extrair_metadados_prova(self, conteudo: str) -> Dict:
        """
        Extrai metadados básicos de uma prova
        """
        metadados = {
            'tamanho_conteudo': len(conteudo),
            'data_extracao': datetime.now().isoformat(),
            'hash_conteudo': hashlib.md5(conteudo.encode()).hexdigest()
        }
        
        # Extrair ano
        anos = re.findall(r'\b(19|20)\d{2}\b', conteudo)
        if anos:
            metadados['anos_identificados'] = list(set(anos))
        
        # Extrair disciplinas
        disciplinas = re.findall(r'(português|matemática|direito|administração|informática|história|geografia)', 
                               conteudo, re.IGNORECASE)
        if disciplinas:
            metadados['disciplinas_identificadas'] = list(set(disciplinas))
        
        return metadados
    
    def _classificar_dificuldade_questao(self, enunciado: str, opcoes: List[str]) -> str:
        """
        Classifica a dificuldade de uma questão baseada em heurísticas
        """
        # Análise básica de dificuldade
        palavras_dificeis = ['análise', 'interpretação', 'aplicação', 'síntese', 'avaliação']
        palavras_faceis = ['definição', 'conceito', 'básico', 'elementar', 'simples']
        
        texto_completo = enunciado + ' ' + ' '.join(opcoes)
        texto_lower = texto_completo.lower()
        
        score_dificuldade = 0
        
        # Contar palavras difíceis
        for palavra in palavras_dificeis:
            score_dificuldade += texto_lower.count(palavra)
        
        # Contar palavras fáceis
        for palavra in palavras_faceis:
            score_dificuldade -= texto_lower.count(palavra)
        
        # Considerar tamanho do enunciado
        if len(enunciado) > 500:
            score_dificuldade += 1
        elif len(enunciado) < 100:
            score_dificuldade -= 1
        
        # Classificar
        if score_dificuldade >= 2:
            return 'dificil'
        elif score_dificuldade <= -1:
            return 'facil'
        else:
            return 'medio'
    
    def _extrair_disciplina_questao(self, enunciado: str, contexto: str = "") -> str:
        """
        Extrai a disciplina de uma questão baseada no conteúdo
        """
        texto_analise = (enunciado + ' ' + contexto).lower()
        
        # Mapeamento de palavras-chave para disciplinas
        disciplinas_map = {
            'português': ['português', 'gramática', 'sintaxe', 'morfologia', 'semântica', 'literatura'],
            'matemática': ['matemática', 'álgebra', 'geometria', 'trigonometria', 'cálculo', 'estatística'],
            'direito constitucional': ['constituição', 'constitucional', 'direitos fundamentais', 'poderes'],
            'direito administrativo': ['administrativo', 'servidor público', 'licitação', 'contrato administrativo'],
            'direito penal': ['penal', 'crime', 'pena', 'processo penal', 'código penal'],
            'direito civil': ['civil', 'código civil', 'contrato', 'responsabilidade civil'],
            'informática': ['informática', 'computador', 'software', 'hardware', 'sistema operacional'],
            'administração': ['administração', 'gestão', 'planejamento', 'organização', 'controle'],
            'contabilidade': ['contabilidade', 'balanço', 'demonstração', 'ativo', 'passivo'],
            'história': ['história', 'histórico', 'passado', 'época', 'período'],
            'geografia': ['geografia', 'geográfico', 'país', 'estado', 'cidade', 'região'],
            'atualidades': ['atual', 'recente', 'notícia', 'acontecimento', 'evento']
        }
        
        # Encontrar disciplina com mais correspondências
        disciplina_scores = {}
        for disciplina, palavras in disciplinas_map.items():
            score = sum(texto_analise.count(palavra) for palavra in palavras)
            if score > 0:
                disciplina_scores[disciplina] = score
        
        if disciplina_scores:
            return max(disciplina_scores, key=disciplina_scores.get)
        
        return 'geral'
    
    def _validar_questao(self, questao: Dict) -> Tuple[bool, List[str]]:
        """
        Valida se uma questão está completa e correta
        """
        problemas = []
        
        # Verificar se tem enunciado
        if not questao.get('enunciado') or len(questao['enunciado'].strip()) < 10:
            problemas.append("Enunciado muito curto ou ausente")
        
        # Verificar se tem opções
        opcoes = questao.get('opcoes', [])
        if len(opcoes) < 2:
            problemas.append("Número insuficiente de opções")
        
        # Verificar se tem gabarito
        if not questao.get('gabarito'):
            problemas.append("Gabarito ausente")
        
        # Verificar se o gabarito é válido
        gabarito = questao.get('gabarito', '').upper()
        if gabarito not in ['A', 'B', 'C', 'D', 'E']:
            problemas.append("Gabarito inválido")
        
        # Verificar se o gabarito corresponde às opções
        if gabarito and opcoes:
            indice_gabarito = ord(gabarito) - ord('A')
            if indice_gabarito >= len(opcoes):
                problemas.append("Gabarito não corresponde às opções disponíveis")
        
        return len(problemas) == 0, problemas
    
    def _processar_questao(self, questao_raw: Dict) -> Optional[Dict]:
        """
        Processa e valida uma questão extraída
        """
        try:
            # Limpar e normalizar dados
            questao = {
                'numero': questao_raw.get('numero', 0),
                'enunciado': questao_raw.get('enunciado', '').strip(),
                'opcoes': questao_raw.get('opcoes', []),
                'gabarito': questao_raw.get('gabarito', '').upper(),
                'disciplina': questao_raw.get('disciplina', ''),
                'nivel_dificuldade': questao_raw.get('nivel_dificuldade', 'medio'),
                'explicacao': questao_raw.get('explicacao', ''),
                'fonte': self.banca,
                'ano_original': questao_raw.get('ano', None),
                'tags': questao_raw.get('tags', [])
            }
            
            # Classificar dificuldade se não especificada
            if not questao['nivel_dificuldade'] or questao['nivel_dificuldade'] == 'medio':
                questao['nivel_dificuldade'] = self._classificar_dificuldade_questao(
                    questao['enunciado'], questao['opcoes']
                )
            
            # Extrair disciplina se não especificada
            if not questao['disciplina']:
                questao['disciplina'] = self._extrair_disciplina_questao(questao['enunciado'])
            
            # Validar questão
            valida, problemas = self._validar_questao(questao)
            
            if not valida:
                logger.warning(f"Questão {questao['numero']} rejeitada: {problemas}")
                return None
            
            return questao
            
        except Exception as e:
            logger.error(f"Erro ao processar questão: {e}")
            return None

class CESPEProvaScraper(ProvaScraper):
    """
    Scraper específico para provas do CESPE/CEBRASPE
    """
    
    def __init__(self):
        super().__init__("CESPE", "https://www.cespe.unb.br")
        self.provas_url = "https://www.cespe.unb.br/concursos"
    
    def buscar_provas(self, limite: int = 50) -> List[Dict]:
        """
        Busca provas do CESPE
        """
        provas = []
        
        try:
            driver = self.setup_driver()
            driver.get(self.provas_url)
            
            # Aguardar carregamento
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Buscar links de provas
            prova_links = driver.find_elements(By.CSS_SELECTOR, 
                "a[href*='prova'], a[href*='gabarito'], a[href*='pdf']")
            
            for link in prova_links[:limite]:
                try:
                    url = link.get_attribute("href")
                    texto = link.text.strip()
                    
                    if self._eh_prova_valida(texto, url):
                        prova_data = {
                            'titulo': texto,
                            'url': url,
                            'banca': self.banca,
                            'data_coleta': datetime.now().isoformat()
                        }
                        provas.append(prova_data)
                        
                except Exception as e:
                    logger.error(f"Erro ao processar link de prova: {e}")
                    continue
            
            driver.quit()
            
        except Exception as e:
            logger.error(f"Erro ao buscar provas do CESPE: {e}")
            if 'driver' in locals():
                driver.quit()
        
        return provas
    
    def extrair_questoes_prova(self, url_prova: str) -> List[Dict]:
        """
        Extrai questões de uma prova do CESPE
        """
        questoes = []
        
        try:
            # Tentar com requests primeiro
            response = self.session.get(url_prova)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Procurar por questões
            questoes_elements = soup.find_all(['div', 'p'], class_=lambda x: x and 'questao' in x.lower())
            
            if not questoes_elements:
                # Tentar com seletores alternativos
                questoes_elements = soup.find_all('div', string=re.compile(r'^\d+\.'))
            
            for i, element in enumerate(questoes_elements):
                try:
                    questao_data = self._extrair_questao_cespe(element, i + 1)
                    if questao_data:
                        questao_processada = self._processar_questao(questao_data)
                        if questao_processada:
                            questoes.append(questao_processada)
                            
                except Exception as e:
                    logger.error(f"Erro ao extrair questão {i + 1}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Erro ao extrair questões da prova: {e}")
        
        return questoes
    
    def _eh_prova_valida(self, texto: str, url: str) -> bool:
        """
        Verifica se o link é de uma prova válida
        """
        texto_lower = texto.lower()
        url_lower = url.lower()
        
        # Palavras que indicam que é uma prova
        indicadores_prova = ['prova', 'gabarito', 'questões', 'concurso']
        
        # Palavras que indicam que NÃO é uma prova
        excluidos = ['edital', 'inscrição', 'resultado', 'homologação']
        
        # Verificar indicadores positivos
        tem_indicador = any(ind in texto_lower for ind in indicadores_prova)
        
        # Verificar exclusões
        tem_exclusao = any(exc in texto_lower for exc in excluidos)
        
        # Verificar se é PDF ou documento
        eh_documento = any(ext in url_lower for ext in ['.pdf', '.doc', '.docx'])
        
        return (tem_indicador or eh_documento) and not tem_exclusao
    
    def _extrair_questao_cespe(self, element, numero: int) -> Dict:
        """
        Extrai dados de uma questão específica do CESPE
        """
        try:
            texto_completo = element.get_text()
            
            # Extrair enunciado (primeira parte até as opções)
            linhas = texto_completo.split('\n')
            enunciado = ""
            opcoes = []
            gabarito = ""
            
            # Procurar por padrão de opções (A), (B), (C), etc.
            for i, linha in enumerate(linhas):
                linha = linha.strip()
                if re.match(r'^[A-E]\)', linha):
                    opcoes.append(linha[2:].strip())
                elif not opcoes and linha:
                    enunciado += linha + " "
                elif 'gabarito' in linha.lower() or 'resposta' in linha.lower():
                    # Extrair gabarito
                    gabarito_match = re.search(r'[A-E]', linha)
                    if gabarito_match:
                        gabarito = gabarito_match.group()
            
            return {
                'numero': numero,
                'enunciado': enunciado.strip(),
                'opcoes': opcoes,
                'gabarito': gabarito,
                'ano': self._extrair_ano_do_contexto(texto_completo)
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair questão CESPE: {e}")
            return None
    
    def _extrair_ano_do_contexto(self, texto: str) -> Optional[int]:
        """
        Extrai o ano do contexto da questão
        """
        anos = re.findall(r'\b(19|20)\d{2}\b', texto)
        if anos:
            return int(anos[0])
        return None

class FGVProvaScraper(ProvaScraper):
    """
    Scraper específico para provas da FGV
    """
    
    def __init__(self):
        super().__init__("FGV", "https://www.fgv.br")
        self.provas_url = "https://www.fgv.br/concursos"
    
    def buscar_provas(self, limite: int = 50) -> List[Dict]:
        """
        Busca provas da FGV
        """
        provas = []
        
        try:
            response = self.session.get(self.provas_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar links de provas
            prova_links = soup.find_all('a', href=lambda x: x and any(
                palavra in x.lower() for palavra in ['prova', 'gabarito', 'pdf']
            ))
            
            for link in prova_links[:limite]:
                try:
                    url = link.get('href')
                    texto = link.get_text().strip()
                    
                    if not url.startswith('http'):
                        url = urljoin(self.base_url, url)
                    
                    if self._eh_prova_valida(texto, url):
                        prova_data = {
                            'titulo': texto,
                            'url': url,
                            'banca': self.banca,
                            'data_coleta': datetime.now().isoformat()
                        }
                        provas.append(prova_data)
                        
                except Exception as e:
                    logger.error(f"Erro ao processar link de prova: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Erro ao buscar provas da FGV: {e}")
        
        return provas
    
    def extrair_questoes_prova(self, url_prova: str) -> List[Dict]:
        """
        Extrai questões de uma prova da FGV
        """
        questoes = []
        
        try:
            response = self.session.get(url_prova)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Procurar por questões
            questoes_elements = soup.find_all(['div', 'p'], string=re.compile(r'^\d+\.'))
            
            for i, element in enumerate(questoes_elements):
                try:
                    questao_data = self._extrair_questao_fgv(element, i + 1)
                    if questao_data:
                        questao_processada = self._processar_questao(questao_data)
                        if questao_processada:
                            questoes.append(questao_processada)
                            
                except Exception as e:
                    logger.error(f"Erro ao extrair questão {i + 1}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Erro ao extrair questões da prova: {e}")
        
        return questoes
    
    def _eh_prova_valida(self, texto: str, url: str) -> bool:
        """
        Verifica se o link é de uma prova válida
        """
        return super()._eh_prova_valida(texto, url)
    
    def _extrair_questao_fgv(self, element, numero: int) -> Dict:
        """
        Extrai dados de uma questão específica da FGV
        """
        try:
            texto_completo = element.get_text()
            
            # Lógica similar ao CESPE, mas adaptada para FGV
            linhas = texto_completo.split('\n')
            enunciado = ""
            opcoes = []
            gabarito = ""
            
            for i, linha in enumerate(linhas):
                linha = linha.strip()
                if re.match(r'^[A-E]\)', linha):
                    opcoes.append(linha[2:].strip())
                elif not opcoes and linha:
                    enunciado += linha + " "
                elif 'gabarito' in linha.lower() or 'resposta' in linha.lower():
                    gabarito_match = re.search(r'[A-E]', linha)
                    if gabarito_match:
                        gabarito = gabarito_match.group()
            
            return {
                'numero': numero,
                'enunciado': enunciado.strip(),
                'opcoes': opcoes,
                'gabarito': gabarito,
                'ano': self._extrair_ano_do_contexto(texto_completo)
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair questão FGV: {e}")
            return None
    
    def _extrair_ano_do_contexto(self, texto: str) -> Optional[int]:
        """
        Extrai o ano do contexto da questão
        """
        return super()._extrair_ano_do_contexto(texto)

# Exemplo de uso
if __name__ == "__main__":
    # Testar scraper do CESPE
    cespe_scraper = CESPEProvaScraper()
    provas = cespe_scraper.buscar_provas(limite=5)
    print(f"Encontradas {len(provas)} provas do CESPE")
    
    # Testar scraper da FGV
    fgv_scraper = FGVProvaScraper()
    provas_fgv = fgv_scraper.buscar_provas(limite=5)
    print(f"Encontradas {len(provas_fgv)} provas da FGV")
