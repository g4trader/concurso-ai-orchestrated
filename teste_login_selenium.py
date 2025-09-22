#!/usr/bin/env python3
"""
Teste de Login com Selenium - Verificar autenticação
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

def test_login():
    """Teste de login com credenciais"""
    print("🔧 Configurando driver para teste de login...")
    
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
        print("🧪 Testando login...")
        
        # Acessar página de login
        driver.get("http://localhost:3001/login")
        
        # Aguardar carregamento
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
        
        # Verificar se foi redirecionado para dashboard
        current_url = driver.current_url
        if "dashboard" in current_url:
            print("✅ Login bem-sucedido! Redirecionado para dashboard")
            
            # Verificar elementos do dashboard
            try:
                dashboard_title = driver.find_element(By.XPATH, "//h1[contains(text(), 'Dashboard')]")
                print("✅ Dashboard carregado com sucesso")
            except NoSuchElementException:
                print("⚠️ Dashboard carregado, mas título não encontrado")
            
            return True
        else:
            print(f"❌ Login falhou. URL atual: {current_url}")
            
            # Verificar se há mensagem de erro
            try:
                error_message = driver.find_element(By.XPATH, "//*[contains(text(), 'erro') or contains(text(), 'inválid')]")
                print(f"❌ Mensagem de erro: {error_message.text}")
            except NoSuchElementException:
                print("❌ Nenhuma mensagem de erro encontrada")
            
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de login: {e}")
        return False
    
    finally:
        driver.quit()
        print("🔒 Driver fechado")

def test_credentials():
    """Teste com diferentes credenciais"""
    credentials = [
        ("admin@admin.com", "admin123", "Admin"),
        ("teste@local.com", "123456", "Teste Local"),
        ("teste@concursoai.com", "123456", "Teste Original")
    ]
    
    print("🧪 Testando diferentes credenciais...")
    
    for email, password, name in credentials:
        print(f"\n--- Testando {name} ---")
        print(f"Email: {email}")
        print(f"Senha: {password}")
        
        # Teste rápido com curl
        import subprocess
        try:
            result = subprocess.run([
                "curl", "-s", "-X", "POST", "http://localhost:8000/auth/login",
                "-H", "Content-Type: application/x-www-form-urlencoded",
                "-d", f"username={email}&password={password}"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and "access_token" in result.stdout:
                print(f"✅ {name}: Login via API funcionando")
            else:
                print(f"❌ {name}: Login via API falhou")
                print(f"Resposta: {result.stdout}")
        except Exception as e:
            print(f"❌ {name}: Erro no teste API - {e}")

if __name__ == "__main__":
    print("🚀 INICIANDO TESTE DE LOGIN")
    print("=" * 50)
    
    # Teste com Selenium
    selenium_result = test_login()
    
    print("\n" + "=" * 50)
    print("🧪 TESTANDO CREDENCIAIS VIA API")
    print("=" * 50)
    
    # Teste com API
    test_credentials()
    
    print("\n" + "=" * 50)
    print("📊 RESULTADO FINAL")
    print("=" * 50)
    
    if selenium_result:
        print("✅ LOGIN FUNCIONANDO!")
        print("🎯 Você pode usar as credenciais:")
        print("   Email: admin@admin.com")
        print("   Senha: admin123")
    else:
        print("❌ LOGIN COM PROBLEMAS")
        print("🔧 Verifique se o backend está rodando na porta 8000")
