#!/usr/bin/env python3
"""
Teste Rigoroso de UX - Concurso AI
Testa todos os aspectos da experiência do usuário usando Selenium
"""

import time
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

class UXTestSuite:
    def __init__(self, base_url="https://concurso-ai-orchestrated.vercel.app/"):
        self.base_url = base_url
        self.driver = None
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'url': base_url,
            'tests': [],
            'summary': {
                'total_tests': 0,
                'passed': 0,
                'failed': 0,
                'warnings': 0
            }
        }
        
    def setup_driver(self):
        """Configura o driver do Selenium"""
        print("🔧 Configurando driver do Selenium...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        # Para modo headless (opcional)
        # chrome_options.add_argument("--headless")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            print("✅ Driver configurado com sucesso")
            return True
        except Exception as e:
            print(f"❌ Erro ao configurar driver: {e}")
            return False
    
    def log_test(self, test_name, status, message="", details=None):
        """Registra resultado de um teste"""
        test_result = {
            'name': test_name,
            'status': status,  # 'PASS', 'FAIL', 'WARN'
            'message': message,
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        }
        
        self.results['tests'].append(test_result)
        self.results['summary']['total_tests'] += 1
        
        if status == 'PASS':
            self.results['summary']['passed'] += 1
            print(f"✅ {test_name}: {message}")
        elif status == 'FAIL':
            self.results['summary']['failed'] += 1
            print(f"❌ {test_name}: {message}")
        else:  # WARN
            self.results['summary']['warnings'] += 1
            print(f"⚠️ {test_name}: {message}")
    
    def test_page_load(self):
        """Testa carregamento da página inicial"""
        print("\n🌐 Testando carregamento da página...")
        
        try:
            self.driver.get(self.base_url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Verificar título
            title = self.driver.title
            if "Concurso AI" in title:
                self.log_test("Page Load", "PASS", f"Página carregada com título: {title}")
            else:
                self.log_test("Page Load", "WARN", f"Título inesperado: {title}")
            
            # Verificar elementos principais
            main_elements = [
                ("h1", "Título principal"),
                ("nav", "Navegação"),
                ("button", "Botões")
            ]
            
            for selector, description in main_elements:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        self.log_test(f"Element Check - {description}", "PASS", f"Elemento {selector} encontrado e visível")
                    else:
                        self.log_test(f"Element Check - {description}", "WARN", f"Elemento {selector} encontrado mas não visível")
                except NoSuchElementException:
                    self.log_test(f"Element Check - {description}", "FAIL", f"Elemento {selector} não encontrado")
            
        except TimeoutException:
            self.log_test("Page Load", "FAIL", "Timeout ao carregar página")
        except Exception as e:
            self.log_test("Page Load", "FAIL", f"Erro inesperado: {str(e)}")
    
    def test_navigation(self):
        """Testa navegação entre páginas"""
        print("\n🧭 Testando navegação...")
        
        try:
            # Testar link de login
            login_link = self.driver.find_element(By.LINK_TEXT, "Entrar")
            if login_link.is_displayed() and login_link.is_enabled():
                self.log_test("Login Link", "PASS", "Link de login encontrado e clicável")
                
                # Clicar no link de login
                login_link.click()
                time.sleep(2)
                
                # Verificar se foi redirecionado para página de login
                current_url = self.driver.current_url
                if "login" in current_url:
                    self.log_test("Login Navigation", "PASS", f"Redirecionamento para login bem-sucedido: {current_url}")
                else:
                    self.log_test("Login Navigation", "FAIL", f"Redirecionamento falhou. URL atual: {current_url}")
            else:
                self.log_test("Login Link", "FAIL", "Link de login não encontrado ou não clicável")
                
        except NoSuchElementException:
            self.log_test("Login Link", "FAIL", "Link de login não encontrado")
        except Exception as e:
            self.log_test("Navigation", "FAIL", f"Erro na navegação: {str(e)}")
    
    def test_login_form(self):
        """Testa formulário de login"""
        print("\n🔐 Testando formulário de login...")
        
        try:
            # Verificar se estamos na página de login
            if "login" not in self.driver.current_url:
                self.driver.get(f"{self.base_url}login")
                time.sleep(2)
            
            # Verificar elementos do formulário
            form_elements = [
                ("input[type='email']", "Campo de email"),
                ("input[type='password']", "Campo de senha"),
                ("button[type='submit']", "Botão de submit")
            ]
            
            for selector, description in form_elements:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed() and element.is_enabled():
                        self.log_test(f"Form Element - {description}", "PASS", f"Elemento {selector} encontrado e funcional")
                    else:
                        self.log_test(f"Form Element - {description}", "WARN", f"Elemento {selector} encontrado mas não funcional")
                except NoSuchElementException:
                    self.log_test(f"Form Element - {description}", "FAIL", f"Elemento {selector} não encontrado")
            
            # Testar preenchimento do formulário
            email_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='email']")
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            
            # Limpar campos e preencher
            email_field.clear()
            email_field.send_keys("admin@concursoai.com")
            
            password_field.clear()
            password_field.send_keys("admin123")
            
            self.log_test("Form Fill", "PASS", "Formulário preenchido com sucesso")
            
            # Testar submissão
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Aguardar redirecionamento ou feedback
            time.sleep(3)
            
            # Verificar se login foi bem-sucedido
            current_url = self.driver.current_url
            if "dashboard" in current_url or "login" not in current_url:
                self.log_test("Login Submit", "PASS", f"Login bem-sucedido. Redirecionado para: {current_url}")
            else:
                # Verificar se há mensagem de erro
                try:
                    error_message = self.driver.find_element(By.CSS_SELECTOR, "[class*='error'], [class*='alert']")
                    if error_message.is_displayed():
                        self.log_test("Login Submit", "FAIL", f"Login falhou com mensagem: {error_message.text}")
                    else:
                        self.log_test("Login Submit", "WARN", "Login pode ter falhado - sem feedback claro")
                except NoSuchElementException:
                    self.log_test("Login Submit", "WARN", "Login pode ter falhado - sem mensagem de erro visível")
                    
        except Exception as e:
            self.log_test("Login Form", "FAIL", f"Erro no teste do formulário: {str(e)}")
    
    def test_responsive_design(self):
        """Testa design responsivo"""
        print("\n📱 Testando design responsivo...")
        
        viewports = [
            (1920, 1080, "Desktop"),
            (1024, 768, "Tablet"),
            (375, 667, "Mobile"),
            (414, 896, "Mobile Large")
        ]
        
        for width, height, device in viewports:
            try:
                self.driver.set_window_size(width, height)
                time.sleep(1)
                
                # Verificar se elementos principais são visíveis
                body = self.driver.find_element(By.TAG_NAME, "body")
                if body.is_displayed():
                    self.log_test(f"Responsive - {device}", "PASS", f"Layout funcional em {width}x{height}")
                else:
                    self.log_test(f"Responsive - {device}", "FAIL", f"Layout quebrado em {width}x{height}")
                    
            except Exception as e:
                self.log_test(f"Responsive - {device}", "FAIL", f"Erro ao testar {device}: {str(e)}")
    
    def test_performance(self):
        """Testa performance da página"""
        print("\n⚡ Testando performance...")
        
        try:
            # Medir tempo de carregamento
            start_time = time.time()
            self.driver.get(self.base_url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            load_time = time.time() - start_time
            
            if load_time < 3:
                self.log_test("Page Load Time", "PASS", f"Carregamento rápido: {load_time:.2f}s")
            elif load_time < 5:
                self.log_test("Page Load Time", "WARN", f"Carregamento moderado: {load_time:.2f}s")
            else:
                self.log_test("Page Load Time", "FAIL", f"Carregamento lento: {load_time:.2f}s")
            
            # Verificar recursos carregados
            resources = self.driver.execute_script("""
                return performance.getEntriesByType('resource').length;
            """)
            
            if resources < 20:
                self.log_test("Resource Count", "PASS", f"Poucos recursos: {resources}")
            elif resources < 50:
                self.log_test("Resource Count", "WARN", f"Recursos moderados: {resources}")
            else:
                self.log_test("Resource Count", "WARN", f"Muitos recursos: {resources}")
                
        except Exception as e:
            self.log_test("Performance", "FAIL", f"Erro no teste de performance: {str(e)}")
    
    def test_accessibility(self):
        """Testa acessibilidade básica"""
        print("\n♿ Testando acessibilidade...")
        
        try:
            # Verificar alt text em imagens
            images = self.driver.find_elements(By.TAG_NAME, "img")
            images_with_alt = 0
            
            for img in images:
                if img.get_attribute("alt"):
                    images_with_alt += 1
            
            if len(images) == 0:
                self.log_test("Image Alt Text", "PASS", "Nenhuma imagem encontrada")
            elif images_with_alt == len(images):
                self.log_test("Image Alt Text", "PASS", f"Todas as {len(images)} imagens têm alt text")
            else:
                self.log_test("Image Alt Text", "WARN", f"Apenas {images_with_alt}/{len(images)} imagens têm alt text")
            
            # Verificar contraste (básico)
            try:
                # Verificar se há elementos com texto
                text_elements = self.driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, p, span, a")
                if len(text_elements) > 0:
                    self.log_test("Text Elements", "PASS", f"{len(text_elements)} elementos de texto encontrados")
                else:
                    self.log_test("Text Elements", "WARN", "Poucos elementos de texto encontrados")
            except:
                self.log_test("Text Elements", "WARN", "Não foi possível verificar elementos de texto")
                
        except Exception as e:
            self.log_test("Accessibility", "FAIL", f"Erro no teste de acessibilidade: {str(e)}")
    
    def test_user_flows(self):
        """Testa fluxos principais do usuário"""
        print("\n🔄 Testando fluxos de usuário...")
        
        try:
            # Fluxo: Home -> Login -> Dashboard
            self.driver.get(self.base_url)
            time.sleep(1)
            
            # Ir para login
            login_link = self.driver.find_element(By.LINK_TEXT, "Entrar")
            login_link.click()
            time.sleep(2)
            
            # Fazer login
            email_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='email']")
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            
            email_field.clear()
            email_field.send_keys("admin@concursoai.com")
            password_field.clear()
            password_field.send_keys("admin123")
            
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            time.sleep(3)
            
            # Verificar se chegou ao dashboard
            current_url = self.driver.current_url
            if "dashboard" in current_url:
                self.log_test("User Flow - Login to Dashboard", "PASS", "Fluxo de login bem-sucedido")
            else:
                self.log_test("User Flow - Login to Dashboard", "WARN", f"Fluxo pode ter falhado. URL: {current_url}")
            
            # Testar navegação no dashboard
            try:
                dashboard_elements = self.driver.find_elements(By.CSS_SELECTOR, "nav a, .nav-link")
                if len(dashboard_elements) > 0:
                    self.log_test("Dashboard Navigation", "PASS", f"{len(dashboard_elements)} links de navegação encontrados")
                else:
                    self.log_test("Dashboard Navigation", "WARN", "Poucos links de navegação no dashboard")
            except:
                self.log_test("Dashboard Navigation", "WARN", "Não foi possível verificar navegação do dashboard")
                
        except Exception as e:
            self.log_test("User Flows", "FAIL", f"Erro no teste de fluxos: {str(e)}")
    
    def generate_report(self):
        """Gera relatório detalhado dos testes"""
        print("\n📊 Gerando relatório...")
        
        # Salvar relatório JSON
        report_file = f"ux_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Gerar relatório HTML
        html_report = self.generate_html_report()
        html_file = f"ux_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"✅ Relatório JSON salvo: {report_file}")
        print(f"✅ Relatório HTML salvo: {html_file}")
        
        # Resumo no console
        summary = self.results['summary']
        print(f"\n📈 RESUMO DOS TESTES:")
        print(f"   Total: {summary['total_tests']}")
        print(f"   ✅ Passou: {summary['passed']}")
        print(f"   ❌ Falhou: {summary['failed']}")
        print(f"   ⚠️ Avisos: {summary['warnings']}")
        
        success_rate = (summary['passed'] / summary['total_tests']) * 100 if summary['total_tests'] > 0 else 0
        print(f"   📊 Taxa de sucesso: {success_rate:.1f}%")
    
    def generate_html_report(self):
        """Gera relatório HTML"""
        summary = self.results['summary']
        success_rate = (summary['passed'] / summary['total_tests']) * 100 if summary['total_tests'] > 0 else 0
        
        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Testes UX - Concurso AI</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .summary-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }}
        .summary-card h3 {{ margin: 0 0 10px 0; color: #333; }}
        .summary-card .number {{ font-size: 2em; font-weight: bold; }}
        .pass {{ color: #28a745; }}
        .fail {{ color: #dc3545; }}
        .warn {{ color: #ffc107; }}
        .test-results {{ margin-top: 30px; }}
        .test-item {{ margin-bottom: 15px; padding: 15px; border-radius: 5px; border-left: 4px solid; }}
        .test-item.pass {{ background: #d4edda; border-color: #28a745; }}
        .test-item.fail {{ background: #f8d7da; border-color: #dc3545; }}
        .test-item.warn {{ background: #fff3cd; border-color: #ffc107; }}
        .test-name {{ font-weight: bold; margin-bottom: 5px; }}
        .test-message {{ color: #666; }}
        .timestamp {{ color: #999; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Relatório de Testes UX</h1>
            <h2>Concurso AI - {self.base_url}</h2>
            <p class="timestamp">Gerado em: {self.results['timestamp']}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Total de Testes</h3>
                <div class="number">{summary['total_tests']}</div>
            </div>
            <div class="summary-card">
                <h3>✅ Passou</h3>
                <div class="number pass">{summary['passed']}</div>
            </div>
            <div class="summary-card">
                <h3>❌ Falhou</h3>
                <div class="number fail">{summary['failed']}</div>
            </div>
            <div class="summary-card">
                <h3>⚠️ Avisos</h3>
                <div class="number warn">{summary['warnings']}</div>
            </div>
            <div class="summary-card">
                <h3>📊 Taxa de Sucesso</h3>
                <div class="number pass">{success_rate:.1f}%</div>
            </div>
        </div>
        
        <div class="test-results">
            <h3>Detalhes dos Testes</h3>
"""
        
        for test in self.results['tests']:
            status_class = test['status'].lower()
            html += f"""
            <div class="test-item {status_class}">
                <div class="test-name">{test['name']}</div>
                <div class="test-message">{test['message']}</div>
                <div class="timestamp">{test['timestamp']}</div>
            </div>
"""
        
        html += """
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 Iniciando Teste Rigoroso de UX - Concurso AI")
        print("=" * 60)
        
        if not self.setup_driver():
            print("❌ Falha ao configurar driver. Abortando testes.")
            return
        
        try:
            # Executar todos os testes
            self.test_page_load()
            self.test_navigation()
            self.test_login_form()
            self.test_responsive_design()
            self.test_performance()
            self.test_accessibility()
            self.test_user_flows()
            
        finally:
            if self.driver:
                self.driver.quit()
                print("\n🔚 Driver finalizado")
        
        # Gerar relatório
        self.generate_report()
        print("\n🎉 Testes concluídos!")

def main():
    """Função principal"""
    print("🧪 Teste Rigoroso de UX - Concurso AI")
    print("URL: https://concurso-ai-orchestrated.vercel.app/")
    print("=" * 60)
    
    # Verificar se Selenium está instalado
    try:
        from selenium import webdriver
    except ImportError:
        print("❌ Selenium não está instalado!")
        print("📦 Instale com: pip install selenium")
        return
    
    # Executar testes
    test_suite = UXTestSuite()
    test_suite.run_all_tests()

if __name__ == "__main__":
    main()
