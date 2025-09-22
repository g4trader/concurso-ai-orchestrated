#!/usr/bin/env python3
"""
Teste Completo com Selenium - Sistema de Seleção e Análise de Editais
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

class TesteSistemaCompleto:
    def __init__(self):
        self.driver = None
        self.frontend_url = "http://localhost:3001"
        self.backend_url = "http://localhost:8002"
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
    
    def test_api_concursos(self):
        """Testa a API de concursos"""
        print("\n🧪 Testando API de concursos...")
        
        try:
            # Teste 1: Listar concursos
            response = requests.get(f"{self.backend_url}/editais/concursos", timeout=10)
            assert response.status_code == 200
            
            concursos = response.json()
            assert len(concursos) > 0
            print(f"✅ API concursos OK - {len(concursos)} concursos encontrados")
            
            # Teste 2: Filtro por banca
            response = requests.get(f"{self.backend_url}/editais/concursos?banca=CESPE", timeout=10)
            assert response.status_code == 200
            
            concursos_cespe = response.json()
            print(f"✅ Filtro por banca OK - {len(concursos_cespe)} concursos CESPE")
            
            # Teste 3: Conteúdo do edital
            if concursos:
                primeiro_concurso = concursos[0]
                response = requests.get(f"{self.backend_url}/editais/concursos/{primeiro_concurso['id']}/edital", timeout=10)
                assert response.status_code == 200
                
                edital_data = response.json()
                assert len(edital_data['conteudo']) > 100
                print(f"✅ Conteúdo do edital OK - {len(edital_data['conteudo'])} caracteres")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na API de concursos: {e}")
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
    
    def test_pagina_selecionar_concurso(self):
        """Testa a página de seleção de concursos"""
        print("\n🧪 Testando página de seleção de concursos...")
        
        try:
            self.driver.get(f"{self.frontend_url}/selecionar-concurso")
            
            # Aguardar carregamento
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Verificar elementos da página
            page_elements = [
                "Selecionar Concurso",
                "Escolha um concurso público",
                "Filtros",
                "Buscar"
            ]
            
            for element_text in page_elements:
                try:
                    element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{element_text}')]")
                    print(f"✅ Elemento encontrado: {element_text}")
                except NoSuchElementException:
                    print(f"⚠️ Elemento não encontrado: {element_text}")
            
            # Aguardar carregamento dos concursos
            time.sleep(3)
            
            # Verificar se há concursos carregados
            try:
                concursos = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'space-y-6')]//div[contains(@class, 'p-6')]")
                if len(concursos) > 0:
                    print(f"✅ Concursos carregados: {len(concursos)} encontrados")
                else:
                    print("⚠️ Nenhum concurso carregado na interface")
            except:
                print("⚠️ Não foi possível verificar concursos carregados")
            
            print("✅ Página de seleção de concursos acessível!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao acessar página de seleção: {e}")
            return False
    
    def test_filtros_concursos(self):
        """Testa os filtros de concursos"""
        print("\n🧪 Testando filtros de concursos...")
        
        try:
            self.driver.get(f"{self.frontend_url}/selecionar-concurso")
            
            # Aguardar carregamento
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            time.sleep(3)  # Aguardar carregamento dos concursos
            
            # Teste filtro por banca
            try:
                banca_input = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "banca"))
                )
                banca_input.clear()
                banca_input.send_keys("CESPE")
                time.sleep(2)
                print("✅ Filtro por banca aplicado")
            except TimeoutException:
                print("⚠️ Campo de filtro por banca não encontrado")
            
            # Teste filtro por órgão
            try:
                orgao_input = self.driver.find_element(By.ID, "orgao")
                orgao_input.clear()
                orgao_input.send_keys("TRT")
                time.sleep(2)
                print("✅ Filtro por órgão aplicado")
            except NoSuchElementException:
                print("⚠️ Campo de filtro por órgão não encontrado")
            
            # Teste filtro por nível
            try:
                nivel_select = self.driver.find_element(By.ID, "nivel")
                from selenium.webdriver.support.ui import Select
                select = Select(nivel_select)
                select.select_by_value("superior")
                time.sleep(2)
                print("✅ Filtro por nível aplicado")
            except NoSuchElementException:
                print("⚠️ Campo de filtro por nível não encontrado")
            
            print("✅ Filtros de concursos testados!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao testar filtros: {e}")
            return False
    
    def test_selecao_concurso(self):
        """Testa a seleção de um concurso"""
        print("\n🧪 Testando seleção de concurso...")
        
        try:
            self.driver.get(f"{self.frontend_url}/selecionar-concurso")
            
            # Aguardar carregamento
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            time.sleep(5)  # Aguardar carregamento dos concursos
            
            # Procurar por botão "Analisar Edital"
            try:
                analisar_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Analisar Edital')]")
                if len(analisar_buttons) > 0:
                    print(f"✅ Botões 'Analisar Edital' encontrados: {len(analisar_buttons)}")
                    
                    # Clicar no primeiro botão
                    analisar_buttons[0].click()
                    print("✅ Botão 'Analisar Edital' clicado!")
                    
                    # Aguardar redirecionamento
                    time.sleep(3)
                    
                    # Verificar se foi redirecionado para página de análise
                    current_url = self.driver.current_url
                    if "analise-editais" in current_url:
                        print("✅ Redirecionamento para análise bem-sucedido!")
                        
                        # Verificar se há indicador de concurso selecionado
                        try:
                            concurso_selecionado = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Concurso Selecionado')]")
                            print("✅ Indicador de concurso selecionado encontrado!")
                        except NoSuchElementException:
                            print("⚠️ Indicador de concurso selecionado não encontrado")
                        
                        return True
                    else:
                        print(f"❌ Redirecionamento falhou. URL atual: {current_url}")
                        return False
                else:
                    print("❌ Nenhum botão 'Analisar Edital' encontrado")
                    return False
                    
            except Exception as e:
                print(f"❌ Erro ao clicar no botão: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao testar seleção de concurso: {e}")
            return False
    
    def test_analise_automatica(self):
        """Testa a análise automática após seleção"""
        print("\n🧪 Testando análise automática...")
        
        try:
            # Primeiro, selecionar um concurso
            self.driver.get(f"{self.frontend_url}/selecionar-concurso")
            
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            time.sleep(5)  # Aguardar carregamento
            
            # Clicar em "Analisar Edital"
            try:
                analisar_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Analisar Edital')]")
                if len(analisar_buttons) > 0:
                    analisar_buttons[0].click()
                    time.sleep(3)
                    
                    # Verificar se chegou na página de análise
                    if "analise-editais" in self.driver.current_url:
                        print("✅ Chegou na página de análise")
                        
                        # Verificar se o formulário foi preenchido automaticamente
                        try:
                            textarea = self.driver.find_element(By.ID, "conteudoEdital")
                            conteudo = textarea.get_attribute("value")
                            
                            if conteudo and len(conteudo) > 100:
                                print(f"✅ Formulário preenchido automaticamente - {len(conteudo)} caracteres")
                                
                                # Clicar em "Analisar Edital"
                                try:
                                    analisar_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Analisar Edital')]")
                                    analisar_btn.click()
                                    print("✅ Botão 'Analisar Edital' clicado!")
                                    
                                    # Aguardar análise
                                    print("⏳ Aguardando análise...")
                                    time.sleep(10)
                                    
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
                                        
                                except NoSuchElementException:
                                    print("❌ Botão 'Analisar Edital' não encontrado na página de análise")
                                    return False
                            else:
                                print("❌ Formulário não foi preenchido automaticamente")
                                return False
                                
                        except NoSuchElementException:
                            print("❌ Campo de conteúdo do edital não encontrado")
                            return False
                    else:
                        print("❌ Não chegou na página de análise")
                        return False
                else:
                    print("❌ Nenhum botão 'Analisar Edital' encontrado")
                    return False
                    
            except Exception as e:
                print(f"❌ Erro na análise automática: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao testar análise automática: {e}")
            return False
    
    def test_navegacao_completa(self):
        """Testa navegação completa entre páginas"""
        print("\n🧪 Testando navegação completa...")
        
        try:
            # 1. Acessar página principal
            self.driver.get(self.frontend_url)
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("✅ Página principal acessada")
            
            # 2. Ir para seleção de concursos
            self.driver.get(f"{self.frontend_url}/selecionar-concurso")
            time.sleep(3)
            print("✅ Página de seleção acessada")
            
            # 3. Ir para análise de editais
            self.driver.get(f"{self.frontend_url}/analise-editais")
            time.sleep(3)
            print("✅ Página de análise acessada")
            
            # 4. Voltar para seleção de concursos
            try:
                selecionar_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Selecionar Concurso')]")
                selecionar_btn.click()
                time.sleep(3)
                
                if "selecionar-concurso" in self.driver.current_url:
                    print("✅ Navegação de volta para seleção bem-sucedida!")
                    return True
                else:
                    print("❌ Navegação de volta falhou")
                    return False
                    
            except NoSuchElementException:
                print("⚠️ Botão 'Selecionar Concurso' não encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro na navegação completa: {e}")
            return False
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 INICIANDO TESTE COMPLETO COM SELENIUM")
        print("=" * 70)
        
        results = {}
        
        try:
            # Configurar driver
            self.setup_driver()
            
            # Executar testes
            tests = [
                ("Backend Health", self.test_backend_health),
                ("API Concursos", self.test_api_concursos),
                ("Frontend Access", self.test_frontend_access),
                ("Página Seleção", self.test_pagina_selecionar_concurso),
                ("Filtros Concursos", self.test_filtros_concursos),
                ("Seleção Concurso", self.test_selecao_concurso),
                ("Análise Automática", self.test_analise_automatica),
                ("Navegação Completa", self.test_navegacao_completa)
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
        print("📊 RELATÓRIO FINAL DOS TESTES SELENIUM")
        print("="*70)
        
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
    tester = TesteSistemaCompleto()
    results = tester.run_all_tests()
    
    # Salvar resultados em arquivo
    with open("test_results_selenium.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Resultados salvos em: test_results_selenium.json")

if __name__ == "__main__":
    main()
