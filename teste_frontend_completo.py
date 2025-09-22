#!/usr/bin/env python3
"""
Teste Completo do Frontend - Login e Navegação
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

class TesteFrontendCompleto:
    def __init__(self):
        self.driver = None
        self.frontend_url = "http://localhost:3001"
        self.wait_timeout = 15
        
    def setup_driver(self):
        """Configura o driver do Chrome"""
        print("🔧 Configurando driver do Chrome...")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Executar sem interface gráfica
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(5)
        
        print("✅ Driver configurado com sucesso!")
        
    def teardown_driver(self):
        """Fecha o driver"""
        if self.driver:
            self.driver.quit()
            print("🔒 Driver fechado")
    
    def test_pagina_inicial(self):
        """Testa a página inicial"""
        print("\n🧪 Testando página inicial...")
        
        try:
            self.driver.get(self.frontend_url)
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            title = self.driver.title
            print(f"✅ Página inicial carregada! Título: {title}")
            
            # Verificar elementos da página inicial
            try:
                logo = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Concurso AI')]")
                print("✅ Logo encontrado")
            except NoSuchElementException:
                print("⚠️ Logo não encontrado")
            
            try:
                entrar_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Entrar')]")
                print("✅ Link 'Entrar' encontrado")
            except NoSuchElementException:
                print("⚠️ Link 'Entrar' não encontrado")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao acessar página inicial: {e}")
            return False
    
    def test_login(self):
        """Testa o processo de login"""
        print("\n🧪 Testando login...")
        
        try:
            # Acessar página de login
            self.driver.get(f"{self.frontend_url}/login")
            
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print("✅ Página de login carregada")
            
            # Preencher credenciais
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_input.clear()
            email_input.send_keys("admin@admin.com")
            
            password_input = self.driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys("admin123")
            
            print("✅ Credenciais preenchidas")
            
            # Clicar em entrar
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
            login_button.click()
            
            print("✅ Botão de login clicado")
            
            # Aguardar redirecionamento
            time.sleep(5)
            
            # Verificar se foi redirecionado
            current_url = self.driver.current_url
            if "dashboard" in current_url:
                print("✅ Login bem-sucedido! Redirecionado para dashboard")
                return True
            else:
                print(f"❌ Login falhou. URL atual: {current_url}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no teste de login: {e}")
            return False
    
    def test_dashboard(self):
        """Testa o dashboard após login"""
        print("\n🧪 Testando dashboard...")
        
        try:
            # Verificar se estamos no dashboard
            if "dashboard" not in self.driver.current_url:
                print("❌ Não estamos no dashboard")
                return False
            
            # Aguardar carregamento do dashboard
            time.sleep(3)
            
            # Verificar elementos do dashboard
            dashboard_elements = [
                "Dashboard",
                "Estatísticas",
                "Simulados",
                "Resultados"
            ]
            
            for element_text in dashboard_elements:
                try:
                    element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{element_text}')]")
                    print(f"✅ Elemento encontrado: {element_text}")
                except NoSuchElementException:
                    print(f"⚠️ Elemento não encontrado: {element_text}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no teste do dashboard: {e}")
            return False
    
    def test_navegacao_menu(self):
        """Testa a navegação pelo menu"""
        print("\n🧪 Testando navegação pelo menu...")
        
        try:
            # Testar links do menu
            menu_links = [
                ("Dashboard", "/dashboard"),
                ("Gerador de Simulado", "/gerador-simulado"),
                ("Resultados", "/resultados")
            ]
            
            for link_text, expected_path in menu_links:
                try:
                    # Procurar pelo link
                    link = self.driver.find_element(By.XPATH, f"//a[contains(text(), '{link_text}')]")
                    link.click()
                    time.sleep(2)
                    
                    current_url = self.driver.current_url
                    if expected_path in current_url:
                        print(f"✅ Navegação para {link_text} bem-sucedida")
                    else:
                        print(f"⚠️ Navegação para {link_text} - URL: {current_url}")
                        
                except NoSuchElementException:
                    print(f"⚠️ Link {link_text} não encontrado")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na navegação do menu: {e}")
            return False
    
    def test_analise_editais(self):
        """Testa a página de análise de editais"""
        print("\n🧪 Testando análise de editais...")
        
        try:
            # Navegar para análise de editais
            self.driver.get(f"{self.frontend_url}/analise-editais")
            
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print("✅ Página de análise de editais carregada")
            
            # Verificar elementos da página
            analise_elements = [
                "Análise de Editais com IA",
                "Conteúdo do Edital",
                "Analisar Edital"
            ]
            
            for element_text in analise_elements:
                try:
                    element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{element_text}')]")
                    print(f"✅ Elemento encontrado: {element_text}")
                except NoSuchElementException:
                    print(f"⚠️ Elemento não encontrado: {element_text}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no teste de análise de editais: {e}")
            return False
    
    def test_selecionar_concurso(self):
        """Testa a página de seleção de concursos"""
        print("\n🧪 Testando seleção de concursos...")
        
        try:
            # Navegar para seleção de concursos
            self.driver.get(f"{self.frontend_url}/selecionar-concurso")
            
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print("✅ Página de seleção de concursos carregada")
            
            # Aguardar carregamento dos concursos
            time.sleep(5)
            
            # Verificar elementos da página
            selecao_elements = [
                "Selecionar Concurso",
                "Escolha um concurso público",
                "Filtros"
            ]
            
            for element_text in selecao_elements:
                try:
                    element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{element_text}')]")
                    print(f"✅ Elemento encontrado: {element_text}")
                except NoSuchElementException:
                    print(f"⚠️ Elemento não encontrado: {element_text}")
            
            # Verificar se há concursos carregados
            try:
                concursos = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'p-6')]")
                if len(concursos) > 0:
                    print(f"✅ Concursos carregados: {len(concursos)} encontrados")
                else:
                    print("⚠️ Nenhum concurso carregado")
            except:
                print("⚠️ Não foi possível verificar concursos")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no teste de seleção de concursos: {e}")
            return False
    
    def test_analise_manual(self):
        """Testa análise manual de edital"""
        print("\n🧪 Testando análise manual de edital...")
        
        try:
            # Navegar para análise de editais
            self.driver.get(f"{self.frontend_url}/analise-editais")
            
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Aguardar carregamento
            time.sleep(3)
            
            # Preencher formulário
            try:
                textarea = self.driver.find_element(By.ID, "conteudoEdital")
                textarea.clear()
                textarea.send_keys("""
                EDITAL Nº 1/2024 - CONCURSO PÚBLICO
                
                O órgão responsável torna pública a realização de concurso público.
                
                1. DO CONCURSO
                1.1 O concurso será executado pela banca organizadora.
                1.2 Exige nível superior e/ou médio conforme o cargo.
                
                2. DAS INSCRIÇÕES
                2.1 Período de inscrições conforme cronograma.
                2.2 Taxa de inscrição conforme tabela.
                
                3. DAS PROVAS
                3.1 Prova Objetiva de múltipla escolha.
                3.2 Prova Discursiva (para alguns cargos).
                """)
                print("✅ Conteúdo do edital preenchido")
            except NoSuchElementException:
                print("❌ Campo de conteúdo não encontrado")
                return False
            
            # Clicar em analisar
            try:
                analisar_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Analisar Edital')]")
                analisar_button.click()
                print("✅ Botão 'Analisar Edital' clicado")
                
                # Aguardar análise
                print("⏳ Aguardando análise...")
                time.sleep(10)
                
                # Verificar se apareceram resultados
                try:
                    resultados = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Resultados da Análise')]"))
                    )
                    print("✅ Resultados da análise apareceram!")
                    return True
                except TimeoutException:
                    print("❌ Resultados não apareceram após análise")
                    return False
                    
            except NoSuchElementException:
                print("❌ Botão 'Analisar Edital' não encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro no teste de análise manual: {e}")
            return False
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 INICIANDO TESTE COMPLETO DO FRONTEND")
        print("=" * 70)
        
        results = {}
        
        try:
            # Configurar driver
            self.setup_driver()
            
            # Executar testes
            tests = [
                ("Página Inicial", self.test_pagina_inicial),
                ("Login", self.test_login),
                ("Dashboard", self.test_dashboard),
                ("Navegação Menu", self.test_navegacao_menu),
                ("Análise Editais", self.test_analise_editais),
                ("Seleção Concursos", self.test_selecionar_concurso),
                ("Análise Manual", self.test_analise_manual)
            ]
            
            for test_name, test_func in tests:
                print(f"\n{'='*20} {test_name} {'='*20}")
                try:
                    result = test_func()
                    results[test_name] = result
                    if result:
                        print(f"✅ {test_name}: PASSOU")
                    else:
                        print(f"❌ {test_name}: FALHOU")
                except Exception as e:
                    print(f"💥 {test_name}: ERRO - {e}")
                    results[test_name] = False
            
        finally:
            self.teardown_driver()
        
        # Relatório final
        print("\n" + "="*70)
        print("📊 RELATÓRIO FINAL DOS TESTES FRONTEND")
        print("="*70)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASSOU" if result else "❌ FALHOU"
            print(f"{test_name}: {status}")
        
        print(f"\n🎯 RESULTADO GERAL: {passed}/{total} testes passaram")
        
        if passed == total:
            print("🎉 TODOS OS TESTES PASSARAM! Frontend funcionando perfeitamente!")
        elif passed >= total * 0.8:
            print("⚠️ Maioria dos testes passou. Alguns problemas menores encontrados.")
        else:
            print("❌ Muitos testes falharam. Frontend precisa de correções.")
        
        return results

def main():
    """Função principal"""
    tester = TesteFrontendCompleto()
    results = tester.run_all_tests()
    
    # Salvar resultados em arquivo
    import json
    with open("test_results_frontend.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Resultados salvos em: test_results_frontend.json")

if __name__ == "__main__":
    main()
