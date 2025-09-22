#!/usr/bin/env python3
"""
Teste para verificar se o CORS foi corrigido
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

def test_cors_fix():
    """Teste para verificar se o CORS foi corrigido"""
    print("🔧 Configurando driver para teste de CORS...")
    
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
        print("🧪 Testando login após correção do CORS...")
        
        # Acessar página de login
        driver.get("http://localhost:3001/login")
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print("✅ Página de login carregada")
        
        # Preencher credenciais
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.clear()
        email_input.send_keys("admin@admin.com")
        
        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys("admin123")
        
        print("✅ Credenciais preenchidas")
        
        # Clicar em entrar
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        login_button.click()
        
        print("✅ Botão de login clicado")
        
        # Aguardar redirecionamento
        time.sleep(5)
        
        # Verificar se foi redirecionado
        current_url = driver.current_url
        if "dashboard" in current_url:
            print("✅ Login bem-sucedido! Redirecionado para dashboard")
            return True
        else:
            print(f"❌ Login falhou. URL atual: {current_url}")
            
            # Verificar logs do navegador
            logs = driver.get_log('browser')
            if logs:
                print("📋 Logs do navegador:")
                for log in logs:
                    if 'CORS' in log['message'] or 'error' in log['message'].lower():
                        print(f"   {log['level']}: {log['message']}")
            
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
    
    finally:
        driver.quit()
        print("🔒 Driver fechado")

if __name__ == "__main__":
    print("🚀 TESTANDO CORREÇÃO DO CORS")
    print("=" * 50)
    
    result = test_cors_fix()
    
    print("\n" + "=" * 50)
    if result:
        print("🎉 CORS CORRIGIDO! Login funcionando!")
        print("✅ Você pode testar no frontend agora:")
        print("   http://localhost:3001")
        print("   Email: admin@admin.com")
        print("   Senha: admin123")
    else:
        print("❌ CORS ainda com problemas")
        print("🔧 Verifique se o backend foi reiniciado")
