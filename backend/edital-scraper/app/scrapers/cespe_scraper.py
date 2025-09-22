import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from typing import List, Dict, Optional
import time
import logging
from datetime import datetime
import hashlib
import json

logger = logging.getLogger(__name__)

class CESPEscraper:
    """
    Scraper para buscar editais do CESPE/CEBRASPE
    """
    
    def __init__(self):
        self.base_url = "https://www.cespe.unb.br"
        self.search_url = "https://www.cespe.unb.br/concursos"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
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
    
    def buscar_concursos_ativos(self) -> List[Dict]:
        """
        Busca todos os concursos ativos do CESPE
        """
        concursos = []
        
        try:
            driver = self.setup_driver()
            driver.get(self.search_url)
            
            # Aguardar carregamento da página
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "concurso-item"))
            )
            
            # Buscar elementos dos concursos
            concurso_elements = driver.find_elements(By.CLASS_NAME, "concurso-item")
            
            for element in concurso_elements:
                try:
                    concurso_data = self._extrair_dados_concurso(element)
                    if concurso_data:
                        concursos.append(concurso_data)
                except Exception as e:
                    logger.error(f"Erro ao extrair dados do concurso: {e}")
                    continue
            
            driver.quit()
            
        except Exception as e:
            logger.error(f"Erro ao buscar concursos do CESPE: {e}")
            if 'driver' in locals():
                driver.quit()
        
        return concursos
    
    def _extrair_dados_concurso(self, element) -> Optional[Dict]:
        """Extrai dados de um elemento de concurso"""
        try:
            # Título do concurso
            titulo_element = element.find_element(By.CSS_SELECTOR, ".concurso-titulo")
            titulo = titulo_element.text.strip()
            
            # Link para o concurso
            link_element = element.find_element(By.CSS_SELECTOR, "a")
            link = link_element.get_attribute("href")
            
            # Status
            status_element = element.find_element(By.CSS_SELECTOR, ".concurso-status")
            status = status_element.text.strip()
            
            # Data de publicação
            data_element = element.find_element(By.CSS_SELECTOR, ".concurso-data")
            data_texto = data_element.text.strip()
            
            # Extrair informações adicionais
            info_elements = element.find_elements(By.CSS_SELECTOR, ".concurso-info span")
            info_dict = {}
            
            for info in info_elements:
                texto = info.text.strip()
                if ":" in texto:
                    chave, valor = texto.split(":", 1)
                    info_dict[chave.strip()] = valor.strip()
            
            return {
                "titulo": titulo,
                "link": link,
                "status": status,
                "data_publicacao": data_texto,
                "informacoes": info_dict,
                "fonte": "CESPE",
                "data_coleta": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados do concurso: {e}")
            return None
    
    def buscar_edital_completo(self, url_concurso: str) -> Optional[Dict]:
        """
        Busca o edital completo de um concurso específico
        """
        try:
            driver = self.setup_driver()
            driver.get(url_concurso)
            
            # Aguardar carregamento
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extrair informações do concurso
            concurso_info = self._extrair_info_concurso(driver)
            
            # Buscar link do edital
            edital_link = self._buscar_link_edital(driver)
            
            if edital_link:
                # Baixar e processar o edital
                edital_data = self._processar_edital_pdf(edital_link)
                concurso_info.update(edital_data)
            
            driver.quit()
            return concurso_info
            
        except Exception as e:
            logger.error(f"Erro ao buscar edital completo: {e}")
            if 'driver' in locals():
                driver.quit()
            return None
    
    def _extrair_info_concurso(self, driver) -> Dict:
        """Extrai informações detalhadas do concurso"""
        info = {}
        
        try:
            # Título
            titulo_element = driver.find_element(By.CSS_SELECTOR, "h1, .titulo-concurso")
            info["titulo"] = titulo_element.text.strip()
            
            # Informações básicas
            info_elements = driver.find_elements(By.CSS_SELECTOR, ".info-concurso, .dados-concurso")
            
            for element in info_elements:
                texto = element.text.strip()
                if ":" in texto:
                    chave, valor = texto.split(":", 1)
                    info[chave.strip().lower().replace(" ", "_")] = valor.strip()
            
            # Status e datas
            status_elements = driver.find_elements(By.CSS_SELECTOR, ".status, .datas")
            for element in status_elements:
                texto = element.text.strip()
                if "inscrições" in texto.lower():
                    info["periodo_inscricoes"] = texto
                elif "prova" in texto.lower():
                    info["data_prova"] = texto
            
        except Exception as e:
            logger.error(f"Erro ao extrair informações do concurso: {e}")
        
        return info
    
    def _buscar_link_edital(self, driver) -> Optional[str]:
        """Busca o link para download do edital"""
        try:
            # Procurar por links de edital
            edital_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='edital'], a[href*='pdf']")
            
            for link in edital_links:
                href = link.get_attribute("href")
                texto = link.text.lower()
                
                if "edital" in texto or "pdf" in href:
                    return href
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar link do edital: {e}")
            return None
    
    def _processar_edital_pdf(self, pdf_url: str) -> Dict:
        """
        Processa o PDF do edital (simplificado - em produção usar PyPDF2 ou similar)
        """
        try:
            # Em uma implementação real, aqui seria feito o download e processamento do PDF
            # Por enquanto, retornamos informações básicas
            
            response = requests.head(pdf_url, headers=self.headers)
            
            return {
                "edital_url": pdf_url,
                "edital_tamanho": response.headers.get("content-length", "0"),
                "edital_tipo": response.headers.get("content-type", "application/pdf"),
                "hash_conteudo": hashlib.md5(pdf_url.encode()).hexdigest()
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar edital PDF: {e}")
            return {}
    
    def verificar_novos_concursos(self, ultima_verificacao: datetime) -> List[Dict]:
        """
        Verifica se há novos concursos desde a última verificação
        """
        concursos = self.buscar_concursos_ativos()
        novos_concursos = []
        
        for concurso in concursos:
            try:
                # Verificar se é mais recente que a última verificação
                data_concurso = datetime.strptime(
                    concurso["data_publicacao"], 
                    "%d/%m/%Y"
                )
                
                if data_concurso > ultima_verificacao:
                    novos_concursos.append(concurso)
                    
            except Exception as e:
                logger.error(f"Erro ao verificar data do concurso: {e}")
                continue
        
        return novos_concursos

# Exemplo de uso
if __name__ == "__main__":
    scraper = CESPEscraper()
    
    # Buscar concursos ativos
    concursos = scraper.buscar_concursos_ativos()
    print(f"Encontrados {len(concursos)} concursos ativos")
    
    for concurso in concursos[:3]:  # Mostrar apenas os 3 primeiros
        print(f"Concurso: {concurso['titulo']}")
        print(f"Status: {concurso['status']}")
        print(f"Link: {concurso['link']}")
        print("---")
