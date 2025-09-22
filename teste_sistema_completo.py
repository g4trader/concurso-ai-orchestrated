#!/usr/bin/env python3
"""
Teste Completo do Sistema de Seleção e Análise de Editais
"""

import requests
import time

def test_backend_editais():
    """Testa as novas rotas de editais"""
    print("🧪 Testando Backend - Rotas de Editais...")
    
    try:
        # Teste 1: Listar concursos
        response = requests.get("http://localhost:8002/editais/concursos", timeout=5)
        if response.status_code == 200:
            concursos = response.json()
            print(f"✅ Lista de concursos OK - {len(concursos)} concursos encontrados")
            
            # Teste 2: Obter concurso específico
            if concursos:
                primeiro_concurso = concursos[0]
                concurso_id = primeiro_concurso['id']
                
                response = requests.get(f"http://localhost:8002/editais/concursos/{concurso_id}", timeout=5)
                if response.status_code == 200:
                    print(f"✅ Concurso específico OK - {primeiro_concurso['titulo']}")
                    
                    # Teste 3: Obter conteúdo do edital
                    response = requests.get(f"http://localhost:8002/editais/concursos/{concurso_id}/edital", timeout=5)
                    if response.status_code == 200:
                        edital_data = response.json()
                        print(f"✅ Conteúdo do edital OK - {len(edital_data['conteudo'])} caracteres")
                        return True
                    else:
                        print(f"❌ Erro ao obter conteúdo do edital - {response.status_code}")
                        return False
                else:
                    print(f"❌ Erro ao obter concurso específico - {response.status_code}")
                    return False
            else:
                print("❌ Nenhum concurso encontrado")
                return False
        else:
            print(f"❌ Erro ao listar concursos - {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de editais: {e}")
        return False

def test_frontend_pages():
    """Testa as páginas do frontend"""
    print("🧪 Testando Frontend - Páginas...")
    
    try:
        # Teste 1: Página principal
        response = requests.get("http://localhost:3001", timeout=5)
        if response.status_code == 200:
            print("✅ Página principal OK")
        else:
            print(f"❌ Página principal erro - {response.status_code}")
            return False
        
        # Teste 2: Página de análise de editais
        response = requests.get("http://localhost:3001/analise-editais", timeout=5)
        if response.status_code == 200:
            print("✅ Página de análise OK")
        else:
            print(f"❌ Página de análise erro - {response.status_code}")
            return False
        
        # Teste 3: Página de seleção de concursos
        response = requests.get("http://localhost:3001/selecionar-concurso", timeout=5)
        if response.status_code == 200:
            print("✅ Página de seleção OK")
        else:
            print(f"❌ Página de seleção erro - {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do frontend: {e}")
        return False

def test_analise_completa():
    """Testa análise completa com concurso selecionado"""
    print("🧪 Testando Análise Completa...")
    
    try:
        # 1. Buscar concursos
        response = requests.get("http://localhost:8002/editais/concursos", timeout=5)
        if response.status_code != 200:
            print("❌ Erro ao buscar concursos")
            return False
        
        concursos = response.json()
        if not concursos:
            print("❌ Nenhum concurso disponível")
            return False
        
        # 2. Selecionar primeiro concurso
        concurso = concursos[0]
        print(f"   Selecionando: {concurso['titulo']}")
        
        # 3. Obter conteúdo do edital
        response = requests.get(f"http://localhost:8002/editais/concursos/{concurso['id']}/edital", timeout=5)
        if response.status_code != 200:
            print("❌ Erro ao obter conteúdo do edital")
            return False
        
        edital_data = response.json()
        print(f"   Conteúdo obtido: {len(edital_data['conteudo'])} caracteres")
        
        # 4. Analisar o edital
        payload = {
            "conteudo": edital_data['conteudo'],
            "url_edital": edital_data['url_edital'],
            "banca": concurso['banca']
        }
        
        response = requests.post("http://localhost:8002/analyze", json=payload, timeout=10)
        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ Análise completa OK - Tempo: {resultado['tempo_processamento']:.2f}s")
            
            # Verificar dados extraídos
            analise = resultado['resultado']
            info = analise.get('informacoes_extraidas', {})
            
            print(f"   Disciplinas: {len(info.get('disciplinas', []))}")
            print(f"   Datas: {len(info.get('datas', []))}")
            print(f"   Valores: {len(info.get('valores', []))}")
            
            return True
        else:
            print(f"❌ Erro na análise - {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de análise completa: {e}")
        return False

def test_filtros():
    """Testa filtros de concursos"""
    print("🧪 Testando Filtros...")
    
    try:
        # Teste filtro por banca
        response = requests.get("http://localhost:8002/editais/concursos?banca=CESPE", timeout=5)
        if response.status_code == 200:
            concursos_cespe = response.json()
            print(f"✅ Filtro por banca OK - {len(concursos_cespe)} concursos CESPE")
        else:
            print(f"❌ Erro no filtro por banca - {response.status_code}")
            return False
        
        # Teste filtro por órgão
        response = requests.get("http://localhost:8002/editais/concursos?orgao=TRT", timeout=5)
        if response.status_code == 200:
            concursos_trt = response.json()
            print(f"✅ Filtro por órgão OK - {len(concursos_trt)} concursos TRT")
        else:
            print(f"❌ Erro no filtro por órgão - {response.status_code}")
            return False
        
        # Teste filtro por nível
        response = requests.get("http://localhost:8002/editais/concursos?nivel=superior", timeout=5)
        if response.status_code == 200:
            concursos_superior = response.json()
            print(f"✅ Filtro por nível OK - {len(concursos_superior)} concursos nível superior")
        else:
            print(f"❌ Erro no filtro por nível - {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de filtros: {e}")
        return False

def test_estatisticas():
    """Testa estatísticas"""
    print("🧪 Testando Estatísticas...")
    
    try:
        response = requests.get("http://localhost:8002/editais/estatisticas", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Estatísticas OK")
            print(f"   Total de concursos: {stats['total_concursos']}")
            print(f"   Total de vagas: {stats['total_vagas']}")
            print(f"   Fontes ativas: {stats['fontes_ativas']}")
            return True
        else:
            print(f"❌ Erro nas estatísticas - {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de estatísticas: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 TESTE COMPLETO DO SISTEMA DE SELEÇÃO E ANÁLISE DE EDITAIS")
    print("=" * 70)
    
    tests = [
        ("Backend Editais", test_backend_editais),
        ("Frontend Pages", test_frontend_pages),
        ("Análise Completa", test_analise_completa),
        ("Filtros", test_filtros),
        ("Estatísticas", test_estatisticas)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"💥 {test_name}: ERRO - {e}")
            results[test_name] = False
    
    # Relatório final
    print("\n" + "="*70)
    print("📊 RELATÓRIO FINAL")
    print("="*70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 RESULTADO GERAL: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema de seleção e análise de editais funcionando perfeitamente!")
    elif passed >= total * 0.8:
        print("⚠️ Maioria dos testes passou.")
        print("✅ Sistema funcional com pequenos problemas.")
    else:
        print("❌ Muitos testes falharam.")
        print("❌ Sistema precisa de correções.")
    
    print(f"\n🌐 URLs para testar:")
    print(f"   Frontend: http://localhost:3001")
    print(f"   Selecionar Concurso: http://localhost:3001/selecionar-concurso")
    print(f"   Análise de Editais: http://localhost:3001/analise-editais")
    print(f"   Backend API: http://localhost:8002")
    print(f"   API Concursos: http://localhost:8002/editais/concursos")
    print(f"   Backend Docs: http://localhost:8002/docs")

if __name__ == "__main__":
    main()
