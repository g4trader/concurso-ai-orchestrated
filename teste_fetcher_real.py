#!/usr/bin/env python3
"""
Teste do fetcher de editais reais
"""

import sys
import os
sys.path.append('/Users/lucianoterres/Documents/GitHub/concurso-ai-orchestrated/backend/edital-analyzer')

from app.api.real_edital_fetcher import RealEditalFetcher

def test_fetcher():
    """Testa o fetcher de editais reais"""
    print("🔍 Testando fetcher de editais reais...")
    
    fetcher = RealEditalFetcher()
    
    try:
        # Testar busca de concursos
        print("1️⃣ Buscando concursos...")
        concursos = fetcher.get_all_concursos()
        print(f"✅ Encontrados {len(concursos)} concursos")
        
        if concursos:
            print("\n📋 Primeiros concursos encontrados:")
            for i, concurso in enumerate(concursos[:3]):
                print(f"  {i+1}. {concurso.get('titulo', 'Sem título')}")
                print(f"     Órgão: {concurso.get('orgao', 'N/A')}")
                print(f"     Banca: {concurso.get('banca', 'N/A')}")
                print(f"     Vagas: {concurso.get('vagas', 'N/A')}")
                print(f"     Fonte: {concurso.get('fonte', 'N/A')}")
                print()
        
        # Testar filtros
        print("2️⃣ Testando filtros...")
        filtros = {'banca': 'CESPE'}
        concursos_filtrados = fetcher.filtrar_concursos(concursos, filtros)
        print(f"✅ Concursos CESPE: {len(concursos_filtrados)}")
        
        # Testar busca por ID
        if concursos:
            print("3️⃣ Testando busca por ID...")
            primeiro_id = concursos[0].get('id')
            concurso_encontrado = fetcher.buscar_edital_por_id(primeiro_id)
            if concurso_encontrado:
                print(f"✅ Concurso encontrado: {concurso_encontrado.get('titulo')}")
            else:
                print("❌ Concurso não encontrado")
        
        # Testar extração de conteúdo
        print("4️⃣ Testando extração de conteúdo...")
        conteudo = fetcher.get_edital_content("teste")
        print(f"✅ Conteúdo extraído: {len(conteudo)} caracteres")
        
        print("\n🎉 Teste concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 TESTE DO FETCHER DE EDITAIS REAIS")
    print("=" * 50)
    
    result = test_fetcher()
    
    print("\n" + "=" * 50)
    if result:
        print("✅ Fetcher funcionando corretamente!")
        print("🔍 Agora os editais são buscados de fontes reais!")
    else:
        print("❌ Problemas no fetcher")
