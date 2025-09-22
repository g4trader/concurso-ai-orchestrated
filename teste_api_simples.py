#!/usr/bin/env python3
"""
Teste simples da API de editais
"""

import requests
import json

def test_api():
    """Testa a API de editais"""
    print("🔍 Testando API de editais...")
    
    try:
        # Testar health
        print("1️⃣ Testando health...")
        response = requests.get("http://localhost:8002/health")
        if response.status_code == 200:
            print("✅ Health OK")
        else:
            print(f"❌ Health falhou: {response.status_code}")
            return False
        
        # Testar concursos
        print("2️⃣ Testando endpoint de concursos...")
        response = requests.get("http://localhost:8002/editais/concursos")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API funcionando! Encontrados {len(data)} concursos")
            
            if data:
                print("\n📋 Primeiro concurso:")
                primeiro = data[0]
                print(f"  Título: {primeiro.get('titulo', 'N/A')}")
                print(f"  Órgão: {primeiro.get('orgao', 'N/A')}")
                print(f"  Banca: {primeiro.get('banca', 'N/A')}")
                print(f"  Fonte: {primeiro.get('fonte', 'N/A')}")
            
            return True
        else:
            print(f"❌ API falhou: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TESTE DA API DE EDITAIS")
    print("=" * 50)
    
    result = test_api()
    
    print("\n" + "=" * 50)
    if result:
        print("✅ API funcionando com editais reais!")
    else:
        print("❌ Problemas na API")
