#!/usr/bin/env python3
"""
Teste Rigoroso com Selenium - Análise de Editais
Testa toda a funcionalidade de análise de editais integrada ao dashboard
"""

import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pytest

class TesteAnaliseEditais:
    def __init__(self):
        self.driver = None
        self.frontend_url = "http://localhost:3001"  # Frontend na porta 3001
        self.backend_url = "http://localhost:8002"   # Backend na porta 8002
        self.wait_timeout = 10
        
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
    
    def test_backend_health(self):
        """Testa se o backend está funcionando"""
        print("\n🧪 Testando saúde do backend...")
        
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            assert data["status"] == "healthy"
            assert data["service"] == "edital-analyzer"
            assert data["ai_available"] == True
            
            print("✅ Backend está saudável!")
            return True
            
        except Exception as e:
            print(f"❌ Backend não está funcionando: {e}")
            return False
    
    def test_frontend_access(self):
        """Testa se o frontend está acessível"""
        print("\n🧪 Testando acesso ao frontend...")
        
        try:
            self.driver.get(self.frontend_url)
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            title = self.driver.title
            print(f"✅ Frontend acessível! Título: {title}")
            return True
            
        except TimeoutException:
            print("❌ Frontend não está respondendo")
            return False
        except Exception as e:
            print(f"❌ Erro ao acessar frontend: {e}")
            return False
    
    def test_dashboard_access(self):
        """Testa acesso ao dashboard"""
        print("\n🧪 Testando acesso ao dashboard...")
        
        try:
            self.driver.get(f"{self.frontend_url}/dashboard")
            
            # Aguardar carregamento
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Verificar se há elementos do dashboard
            dashboard_elements = [
                "Dashboard",
                "Novo Simulado",
                "Análise de Editais",
                "Ver Resultados"
            ]
            
            for element_text in dashboard_elements:
                try:
                    element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{element_text}')]")
                    print(f"✅ Elemento encontrado: {element_text}")
                except NoSuchElementException:
                    print(f"⚠️ Elemento não encontrado: {element_text}")
            
            print("✅ Dashboard acessível!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao acessar dashboard: {e}")
            return False
    
    def test_analise_editais_page(self):
        """Testa a página de análise de editais"""
        print("\n🧪 Testando página de análise de editais...")
        
        try:
            # Acessar página diretamente
            self.driver.get(f"{self.frontend_url}/analise-editais")
            
            # Aguardar carregamento
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Verificar elementos da página
            page_elements = [
                "Análise de Editais com IA",
                "Sistema inteligente de análise",
                "Carregar Exemplo",
                "Limpar",
                "Analisar Edital"
            ]
            
            for element_text in page_elements:
                try:
                    element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{element_text}')]")
                    print(f"✅ Elemento encontrado: {element_text}")
                except NoSuchElementException:
                    print(f"⚠️ Elemento não encontrado: {element_text}")
            
            print("✅ Página de análise de editais acessível!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao acessar página de análise: {e}")
            return False
    
    def test_carregar_exemplo(self):
        """Testa o botão de carregar exemplo"""
        print("\n🧪 Testando carregamento de exemplo...")
        
        try:
            # Acessar página
            self.driver.get(f"{self.frontend_url}/analise-editais")
            
            # Aguardar carregamento
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Encontrar e clicar no botão "Carregar Exemplo"
            try:
                carregar_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Carregar Exemplo')]"))
                )
                carregar_btn.click()
                print("✅ Botão 'Carregar Exemplo' clicado!")
                
                # Aguardar um pouco para o carregamento
                time.sleep(2)
                
                # Verificar se o textarea foi preenchido
                textarea = self.driver.find_element(By.TAG_NAME, "textarea")
                conteudo = textarea.get_attribute("value")
                
                if conteudo and len(conteudo) > 100:
                    print("✅ Exemplo carregado com sucesso!")
                    print(f"   Tamanho do conteúdo: {len(conteudo)} caracteres")
                    return True
                else:
                    print("❌ Exemplo não foi carregado corretamente")
                    return False
                    
            except TimeoutException:
                print("❌ Botão 'Carregar Exemplo' não encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao testar carregamento de exemplo: {e}")
            return False
    
    def test_analise_edital(self):
        """Testa a análise de edital"""
        print("\n🧪 Testando análise de edital...")
        
        try:
            # Acessar página
            self.driver.get(f"{self.frontend_url}/analise-editais")
            
            # Aguardar carregamento
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Carregar exemplo primeiro
            try:
                carregar_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Carregar Exemplo')]"))
                )
                carregar_btn.click()
                time.sleep(2)
            except:
                print("⚠️ Não foi possível carregar exemplo, continuando...")
            
            # Encontrar e clicar no botão "Analisar Edital"
            try:
                analisar_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Analisar Edital')]"))
                )
                analisar_btn.click()
                print("✅ Botão 'Analisar Edital' clicado!")
                
                # Aguardar análise (pode demorar)
                print("⏳ Aguardando análise...")
                time.sleep(10)  # Aguardar 10 segundos para análise
                
                # Verificar se apareceram resultados
                try:
                    resultados = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Resultados da Análise')]"))
                    )
                    print("✅ Resultados da análise apareceram!")
                    
                    # Verificar elementos dos resultados
                    result_elements = [
                        "Informações Básicas",
                        "Estatísticas",
                        "Resumo Executivo"
                    ]
                    
                    for element_text in result_elements:
                        try:
                            element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{element_text}')]")
                            print(f"✅ Resultado encontrado: {element_text}")
                        except NoSuchElementException:
                            print(f"⚠️ Resultado não encontrado: {element_text}")
                    
                    return True
                    
                except TimeoutException:
                    print("❌ Resultados não apareceram após análise")
                    return False
                    
            except TimeoutException:
                print("❌ Botão 'Analisar Edital' não encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao testar análise de edital: {e}")
            return False
    
    def test_navegacao_dashboard(self):
        """Testa navegação do dashboard para análise de editais"""
        print("\n🧪 Testando navegação do dashboard...")
        
        try:
            # Acessar dashboard
            self.driver.get(f"{self.frontend_url}/dashboard")
            
            # Aguardar carregamento
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Tentar encontrar e clicar no botão de análise de editais
            try:
                # Procurar por link ou botão com texto "Análise de Editais"
                analise_link = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Análise de Editais')]"))
                )
                analise_link.click()
                print("✅ Link 'Análise de Editais' clicado!")
                
                # Aguardar navegação
                time.sleep(3)
                
                # Verificar se chegou na página correta
                current_url = self.driver.current_url
                if "analise-editais" in current_url:
                    print("✅ Navegação para análise de editais bem-sucedida!")
                    return True
                else:
                    print(f"❌ Navegação falhou. URL atual: {current_url}")
                    return False
                    
            except TimeoutException:
                print("❌ Link 'Análise de Editais' não encontrado no dashboard")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao testar navegação: {e}")
            return False
    
    def test_api_direct(self):
        """Testa a API diretamente"""
        print("\n🧪 Testando API diretamente...")
        
        try:
            # Teste 1: Health check
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            assert response.status_code == 200
            print("✅ Health check OK")
            
            # Teste 2: Análise de exemplo
            response = requests.get(f"{self.backend_url}/analyze/sample", timeout=10)
            assert response.status_code == 200
            
            data = response.json()
            assert data["status"] == "success"
            assert "resultado" in data
            assert "tempo_processamento" in data
            
            print("✅ Análise de exemplo OK")
            print(f"   Tempo: {data['tempo_processamento']:.2f}s")
            
            # Teste 3: Análise personalizada
            edital_teste = """
            EDITAL Nº 1 – CONCURSO PÚBLICO PARA ANALISTA JUDICIÁRIO
            O TRIBUNAL REGIONAL DO TRABALHO torna pública a realização de concurso público para o provimento de 100 vagas no cargo de Analista Judiciário.
            1.1 O concurso será executado pela FCC.
            1.2 Exige nível superior.
            1.3 Remuneração inicial de R$ 8.500,00.
            2.1 Inscrições de 15/02/2024 a 15/03/2024.
            2.2 Taxa de R$ 120,00.
            3.1 Prova Objetiva em 15/04/2024.
            4.1 Disciplinas: Português, Direito do Trabalho, Direito Constitucional, Informática.
            """
            
            payload = {
                "conteudo": edital_teste,
                "url_edital": "https://exemplo.com/edital-trt",
                "banca": "FCC"
            }
            
            response = requests.post(f"{self.backend_url}/analyze", json=payload, timeout=10)
            assert response.status_code == 200
            
            data = response.json()
            assert data["status"] == "success"
            assert "resultado" in data
            
            print("✅ Análise personalizada OK")
            print(f"   Tempo: {data['tempo_processamento']:.2f}s")
            
            # Verificar dados extraídos
            resultado = data["resultado"]
            analise_basica = resultado.get("analise_basica", {})
            info = resultado.get("informacoes_extraidas", {})
            
            print(f"   Tipo: {analise_basica.get('tipo_documento', 'N/A')}")
            print(f"   Banca: {analise_basica.get('banca_organizadora', 'N/A')}")
            print(f"   Disciplinas: {len(info.get('disciplinas', []))}")
            print(f"   Datas: {len(info.get('datas', []))}")
            print(f"   Valores: {len(info.get('valores', []))}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao testar API: {e}")
            return False
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 INICIANDO TESTE RIGOROSO COM SELENIUM")
        print("=" * 60)
        
        results = {}
        
        try:
            # Configurar driver
            self.setup_driver()
            
            # Executar testes
            tests = [
                ("Backend Health", self.test_backend_health),
                ("Frontend Access", self.test_frontend_access),
                ("Dashboard Access", self.test_dashboard_access),
                ("Analise Editais Page", self.test_analise_editais_page),
                ("Carregar Exemplo", self.test_carregar_exemplo),
                ("Analise Edital", self.test_analise_edital),
                ("Navegacao Dashboard", self.test_navegacao_dashboard),
                ("API Direct", self.test_api_direct)
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
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL DOS TESTES")
        print("="*60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASSOU" if result else "❌ FALHOU"
            print(f"{test_name}: {status}")
        
        print(f"\n🎯 RESULTADO GERAL: {passed}/{total} testes passaram")
        
        if passed == total:
            print("🎉 TODOS OS TESTES PASSARAM! Sistema funcionando perfeitamente!")
        elif passed >= total * 0.8:
            print("⚠️ Maioria dos testes passou. Alguns problemas menores encontrados.")
        else:
            print("❌ Muitos testes falharam. Sistema precisa de correções.")
        
        return results

def main():
    """Função principal"""
    tester = TesteAnaliseEditais()
    results = tester.run_all_tests()
    
    # Salvar resultados em arquivo
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Resultados salvos em: test_results.json")

if __name__ == "__main__":
    main()
