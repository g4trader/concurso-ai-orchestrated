#!/usr/bin/env python3
"""
Teste Final Simples - Verificar se tudo está funcionando
"""

import requests
import time

def test_backend():
    """Testa o backend"""
    print("🧪 Testando Backend...")
    try:
        response = requests.get("http://localhost:8002/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend OK - {data['status']}")
            return True
        else:
            print(f"❌ Backend erro - {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend erro - {e}")
        return False

def test_frontend():
    """Testa o frontend"""
    print("🧪 Testando Frontend...")
    try:
        response = requests.get("http://localhost:3001", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend OK")
            return True
        else:
            print(f"❌ Frontend erro - {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend erro - {e}")
        return False

def test_analise_editais_page():
    """Testa a página de análise de editais"""
    print("🧪 Testando Página de Análise de Editais...")
    try:
        response = requests.get("http://localhost:3001/analise-editais", timeout=5)
        if response.status_code == 200:
            content = response.text
            if "Análise de Editais com IA" in content:
                print("✅ Página de Análise OK")
                return True
            else:
                print("❌ Página não contém conteúdo esperado")
                return False
        else:
            print(f"❌ Página erro - {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Página erro - {e}")
        return False

def test_api_analise():
    """Testa a API de análise"""
    print("🧪 Testando API de Análise...")
    try:
        # Teste com exemplo
        response = requests.get("http://localhost:8002/analyze/sample", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Análise OK - Tempo: {data['tempo_processamento']:.2f}s")
            return True
        else:
            print(f"❌ API Análise erro - {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Análise erro - {e}")
        return False

def test_analise_personalizada():
    """Testa análise personalizada"""
    print("🧪 Testando Análise Personalizada...")
    try:
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
        
        response = requests.post("http://localhost:8002/analyze", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            resultado = data["resultado"]
            analise_basica = resultado.get("analise_basica", {})
            info = resultado.get("informacoes_extraidas", {})
            
            print(f"✅ Análise Personalizada OK")
            print(f"   Tipo: {analise_basica.get('tipo_documento', 'N/A')}")
            print(f"   Banca: {analise_basica.get('banca_organizadora', 'N/A')}")
            print(f"   Disciplinas: {len(info.get('disciplinas', []))}")
            print(f"   Datas: {len(info.get('datas', []))}")
            print(f"   Valores: {len(info.get('valores', []))}")
            return True
        else:
            print(f"❌ Análise Personalizada erro - {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Análise Personalizada erro - {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 TESTE FINAL SIMPLES - ANÁLISE DE EDITAIS")
    print("=" * 50)
    
    tests = [
        ("Backend", test_backend),
        ("Frontend", test_frontend),
        ("Página Análise", test_analise_editais_page),
        ("API Análise", test_api_analise),
        ("Análise Personalizada", test_analise_personalizada)
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
    print("\n" + "="*50)
    print("📊 RELATÓRIO FINAL")
    print("="*50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 RESULTADO GERAL: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema funcionando perfeitamente!")
    elif passed >= total * 0.8:
        print("⚠️ Maioria dos testes passou.")
        print("✅ Sistema funcional com pequenos problemas.")
    else:
        print("❌ Muitos testes falharam.")
        print("❌ Sistema precisa de correções.")
    
    print(f"\n🌐 URLs para testar:")
    print(f"   Frontend: http://localhost:3001")
    print(f"   Análise de Editais: http://localhost:3001/analise-editais")
    print(f"   Backend API: http://localhost:8002")
    print(f"   Backend Docs: http://localhost:8002/docs")

if __name__ == "__main__":
    main()
