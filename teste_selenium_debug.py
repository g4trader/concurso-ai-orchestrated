#!/usr/bin/env python3
"""
Teste de Debug com Selenium - Verificar problemas específicos
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def test_debug():
    """Teste de debug para identificar problemas"""
    print("🔧 Configurando driver para debug...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)
    
    try:
        print("🧪 Testando página de seleção de concursos...")
        
        # Acessar página
        driver.get("http://localhost:3001/selecionar-concurso")
        
        # Aguardar carregamento
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print("✅ Página carregada")
        
        # Aguardar mais tempo para carregamento dos dados
        time.sleep(10)
        
        # Verificar se há elementos
        try:
            title = driver.find_element(By.XPATH, "//h1[contains(text(), 'Selecionar Concurso')]")
            print("✅ Título encontrado")
        except NoSuchElementException:
            print("❌ Título não encontrado")
        
        # Verificar se há concursos
        try:
            concursos = driver.find_elements(By.XPATH, "//div[contains(@class, 'p-6')]")
            print(f"✅ Concursos encontrados: {len(concursos)}")
        except:
            print("❌ Nenhum concurso encontrado")
        
        # Verificar se há botões
        try:
            buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Analisar Edital')]")
            print(f"✅ Botões encontrados: {len(buttons)}")
        except:
            print("❌ Nenhum botão encontrado")
        
        # Verificar console do navegador
        logs = driver.get_log('browser')
        if logs:
            print("📋 Logs do navegador:")
            for log in logs:
                print(f"   {log['level']}: {log['message']}")
        else:
            print("📋 Nenhum log encontrado")
        
        # Verificar se há erros de rede
        try:
            # Tentar fazer requisição direta
            driver.execute_script("""
                fetch('http://localhost:8002/editais/concursos')
                    .then(response => response.json())
                    .then(data => console.log('API Response:', data))
                    .catch(error => console.error('API Error:', error));
            """)
            time.sleep(3)
            
            logs = driver.get_log('browser')
            for log in logs:
                if 'API' in log['message']:
                    print(f"📡 API Log: {log['message']}")
        except Exception as e:
            print(f"❌ Erro ao testar API: {e}")
        
        # Capturar screenshot para debug
        driver.save_screenshot("debug_screenshot.png")
        print("📸 Screenshot salvo como debug_screenshot.png")
        
        # Verificar HTML atual
        html = driver.page_source
        if "Selecionar Concurso" in html:
            print("✅ HTML contém 'Selecionar Concurso'")
        else:
            print("❌ HTML não contém 'Selecionar Concurso'")
        
        if "Analisar Edital" in html:
            print("✅ HTML contém 'Analisar Edital'")
        else:
            print("❌ HTML não contém 'Analisar Edital'")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    finally:
        driver.quit()
        print("🔒 Driver fechado")

if __name__ == "__main__":
    test_debug()
