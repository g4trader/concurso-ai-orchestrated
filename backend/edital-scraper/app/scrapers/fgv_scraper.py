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

class FGVScraper:
    """
    Scraper para buscar editais da FGV (Fundação Getúlio Vargas)
    """
    
    def __init__(self):
        self.base_url = "https://www.fgv.br"
        self.concursos_url = "https://www.fgv.br/concursos"
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
        Busca todos os concursos ativos da FGV
        """
        concursos = []
        
        try:
            # Usar requests primeiro para verificar se a página é estática
            response = requests.get(self.concursos_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar elementos dos concursos
            concurso_elements = soup.find_all('div', class_=['concurso-item', 'card-concurso', 'item-concurso'])
            
            if not concurso_elements:
                # Tentar com seletores alternativos
                concurso_elements = soup.find_all('div', class_=lambda x: x and 'concurso' in x.lower())
            
            for element in concurso_elements:
                try:
                    concurso_data = self._extrair_dados_concurso_bs4(element)
                    if concurso_data:
                        concursos.append(concurso_data)
                except Exception as e:
                    logger.error(f"Erro ao extrair dados do concurso: {e}")
                    continue
            
            # Se não encontrou com BeautifulSoup, tentar com Selenium
            if not concursos:
                concursos = self._buscar_com_selenium()
                
        except Exception as e:
            logger.error(f"Erro ao buscar concursos da FGV: {e}")
            # Fallback para Selenium
            concursos = self._buscar_com_selenium()
        
        return concursos
    
    def _buscar_com_selenium(self) -> List[Dict]:
        """Busca concursos usando Selenium como fallback"""
        concursos = []
        
        try:
            driver = self.setup_driver()
            driver.get(self.concursos_url)
            
            # Aguardar carregamento da página
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Buscar elementos dos concursos
            concurso_elements = driver.find_elements(By.CSS_SELECTOR, 
                ".concurso-item, .card-concurso, .item-concurso, [class*='concurso']")
            
            for element in concurso_elements:
                try:
                    concurso_data = self._extrair_dados_concurso_selenium(element)
                    if concurso_data:
                        concursos.append(concurso_data)
                except Exception as e:
                    logger.error(f"Erro ao extrair dados do concurso: {e}")
                    continue
            
            driver.quit()
            
        except Exception as e:
            logger.error(f"Erro ao buscar concursos com Selenium: {e}")
            if 'driver' in locals():
                driver.quit()
        
        return concursos
    
    def _extrair_dados_concurso_bs4(self, element) -> Optional[Dict]:
        """Extrai dados de um elemento de concurso usando BeautifulSoup"""
        try:
            # Título do concurso
            titulo_element = element.find(['h1', 'h2', 'h3', 'h4'], class_=lambda x: x and 'titulo' in x.lower())
            if not titulo_element:
                titulo_element = element.find(['h1', 'h2', 'h3', 'h4'])
            
            titulo = titulo_element.text.strip() if titulo_element else "Título não encontrado"
            
            # Link para o concurso
            link_element = element.find('a')
            link = link_element.get('href') if link_element else None
            
            if link and not link.startswith('http'):
                link = self.base_url + link
            
            # Status
            status_element = element.find(['span', 'div'], class_=lambda x: x and 'status' in x.lower())
            status = status_element.text.strip() if status_element else "Status não informado"
            
            # Data de publicação
            data_element = element.find(['span', 'div'], class_=lambda x: x and 'data' in x.lower())
            data_texto = data_element.text.strip() if data_element else "Data não informada"
            
            # Extrair informações adicionais
            info_elements = element.find_all(['span', 'div', 'p'])
            info_dict = {}
            
            for info in info_elements:
                texto = info.text.strip()
                if ":" in texto and len(texto) < 100:  # Evitar textos muito longos
                    chave, valor = texto.split(":", 1)
                    info_dict[chave.strip().lower().replace(" ", "_")] = valor.strip()
            
            return {
                "titulo": titulo,
                "link": link,
                "status": status,
                "data_publicacao": data_texto,
                "informacoes": info_dict,
                "fonte": "FGV",
                "data_coleta": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados do concurso: {e}")
            return None
    
    def _extrair_dados_concurso_selenium(self, element) -> Optional[Dict]:
        """Extrai dados de um elemento de concurso usando Selenium"""
        try:
            # Título do concurso
            try:
                titulo_element = element.find_element(By.CSS_SELECTOR, "h1, h2, h3, h4, .titulo")
                titulo = titulo_element.text.strip()
            except:
                titulo = "Título não encontrado"
            
            # Link para o concurso
            try:
                link_element = element.find_element(By.CSS_SELECTOR, "a")
                link = link_element.get_attribute("href")
            except:
                link = None
            
            # Status
            try:
                status_element = element.find_element(By.CSS_SELECTOR, ".status, [class*='status']")
                status = status_element.text.strip()
            except:
                status = "Status não informado"
            
            # Data de publicação
            try:
                data_element = element.find_element(By.CSS_SELECTOR, ".data, [class*='data']")
                data_texto = data_element.text.strip()
            except:
                data_texto = "Data não informada"
            
            return {
                "titulo": titulo,
                "link": link,
                "status": status,
                "data_publicacao": data_texto,
                "informacoes": {},
                "fonte": "FGV",
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
            response = requests.get(url_concurso, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrair informações do concurso
            concurso_info = self._extrair_info_concurso_bs4(soup)
            
            # Buscar link do edital
            edital_link = self._buscar_link_edital_bs4(soup)
            
            if edital_link:
                # Baixar e processar o edital
                edital_data = self._processar_edital_pdf(edital_link)
                concurso_info.update(edital_data)
            
            return concurso_info
            
        except Exception as e:
            logger.error(f"Erro ao buscar edital completo: {e}")
            return None
    
    def _extrair_info_concurso_bs4(self, soup) -> Dict:
        """Extrai informações detalhadas do concurso usando BeautifulSoup"""
        info = {}
        
        try:
            # Título
            titulo_element = soup.find(['h1', 'h2'], class_=lambda x: x and 'titulo' in x.lower())
            if not titulo_element:
                titulo_element = soup.find(['h1', 'h2'])
            
            if titulo_element:
                info["titulo"] = titulo_element.text.strip()
            
            # Informações básicas
            info_elements = soup.find_all(['div', 'span', 'p'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['info', 'dados', 'detalhes']
            ))
            
            for element in info_elements:
                texto = element.text.strip()
                if ":" in texto and len(texto) < 200:
                    chave, valor = texto.split(":", 1)
                    info[chave.strip().lower().replace(" ", "_")] = valor.strip()
            
        except Exception as e:
            logger.error(f"Erro ao extrair informações do concurso: {e}")
        
        return info
    
    def _buscar_link_edital_bs4(self, soup) -> Optional[str]:
        """Busca o link para download do edital usando BeautifulSoup"""
        try:
            # Procurar por links de edital
            edital_links = soup.find_all('a', href=lambda x: x and ('edital' in x.lower() or 'pdf' in x.lower()))
            
            for link in edital_links:
                href = link.get('href')
                texto = link.text.lower()
                
                if "edital" in texto or "pdf" in href:
                    if not href.startswith('http'):
                        href = self.base_url + href
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
    scraper = FGVScraper()
    
    # Buscar concursos ativos
    concursos = scraper.buscar_concursos_ativos()
    print(f"Encontrados {len(concursos)} concursos ativos")
    
    for concurso in concursos[:3]:  # Mostrar apenas os 3 primeiros
        print(f"Concurso: {concurso['titulo']}")
        print(f"Status: {concurso['status']}")
        print(f"Link: {concurso['link']}")
        print("---")
