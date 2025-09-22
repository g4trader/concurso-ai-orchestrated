#!/usr/bin/env python3
"""
Teste da API do Analisador de Editais
"""

import requests
import json
import time

def test_api():
    """Testa a API do analisador de editais"""
    
    # URL base da API
    base_url = "http://localhost:8002"
    
    print("🧪 TESTANDO API DO ANALISADOR DE EDITAIS")
    print("=" * 50)
    
    # Teste 1: Health Check
    print("\n1️⃣ Testando Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health Check: OK")
            print(f"   Resposta: {response.json()}")
        else:
            print(f"❌ Health Check: Erro {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Health Check: Erro de conexão - {e}")
        return False
    
    # Teste 2: Análise de Edital de Exemplo
    print("\n2️⃣ Testando Análise de Edital de Exemplo...")
    try:
        response = requests.get(f"{base_url}/analyze/sample", timeout=10)
        if response.status_code == 200:
            print("✅ Análise de Exemplo: OK")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Tempo: {data.get('tempo_processamento', 0):.2f}s")
            
            # Mostrar resultados principais
            resultado = data.get('resultado', {})
            analise_basica = resultado.get('analise_basica', {})
            print(f"   Tipo: {analise_basica.get('tipo_documento', 'N/A')}")
            print(f"   Banca: {analise_basica.get('banca_organizadora', 'N/A')}")
            
            info = resultado.get('informacoes_extraidas', {})
            print(f"   Disciplinas: {len(info.get('disciplinas', []))}")
            print(f"   Datas: {len(info.get('datas', []))}")
            print(f"   Valores: {len(info.get('valores', []))}")
            
        else:
            print(f"❌ Análise de Exemplo: Erro {response.status_code}")
            print(f"   Resposta: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Análise de Exemplo: Erro de conexão - {e}")
    
    # Teste 3: Análise de Edital Personalizado
    print("\n3️⃣ Testando Análise de Edital Personalizado...")
    try:
        edital_teste = """
        EDITAL Nº 2 – TRT/SP, DE 10 DE JANEIRO DE 2024
        CONCURSO PÚBLICO PARA O PROVIMENTO DE VAGAS NO CARGO DE ANALISTA JUDICIÁRIO

        O PRESIDENTE DO TRIBUNAL REGIONAL DO TRABALHO DA 2ª REGIÃO, no uso de suas atribuições, torna pública a realização de concurso público para o provimento de 200 vagas no cargo de Analista Judiciário.

        1 DAS DISPOSIÇÕES PRELIMINARES
        1.1 O concurso público será regido por este edital e executado pela Fundação Carlos Chagas (FCC).
        1.2 O cargo de Analista Judiciário exige nível superior em qualquer área de formação.
        1.3 A remuneração inicial é de R$ 8.500,00.

        2 DAS INSCRIÇÕES
        2.1 As inscrições poderão ser realizadas no período de 15/02/2024 a 15/03/2024.
        2.2 A taxa de inscrição é de R$ 120,00.

        3 DAS ETAPAS DO CONCURSO
        3.1 Prova Objetiva: 15/04/2024.
        3.2 Prova Discursiva: 22/04/2024.
        3.3 Avaliação de Títulos.

        4 DAS DISCIPLINAS
        Serão cobradas as seguintes disciplinas: Português, Direito do Trabalho, Direito Processual do Trabalho, Direito Constitucional, Direito Administrativo, Informática, Raciocínio Lógico.
        """
        
        payload = {
            "conteudo": edital_teste,
            "url_edital": "https://exemplo.com/edital-trt",
            "banca": "FCC"
        }
        
        response = requests.post(f"{base_url}/analyze", json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Análise Personalizada: OK")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Tempo: {data.get('tempo_processamento', 0):.2f}s")
            
            # Mostrar resultados principais
            resultado = data.get('resultado', {})
            analise_basica = resultado.get('analise_basica', {})
            print(f"   Tipo: {analise_basica.get('tipo_documento', 'N/A')}")
            print(f"   Banca: {analise_basica.get('banca_organizadora', 'N/A')}")
            
            info = resultado.get('informacoes_extraidas', {})
            print(f"   Disciplinas: {len(info.get('disciplinas', []))}")
            print(f"   Datas: {len(info.get('datas', []))}")
            print(f"   Valores: {len(info.get('valores', []))}")
            
        else:
            print(f"❌ Análise Personalizada: Erro {response.status_code}")
            print(f"   Resposta: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Análise Personalizada: Erro de conexão - {e}")
    
    # Teste 4: Estatísticas
    print("\n4️⃣ Testando Estatísticas...")
    try:
        response = requests.get(f"{base_url}/stats", timeout=5)
        if response.status_code == 200:
            print("✅ Estatísticas: OK")
            data = response.json()
            stats = data.get('estatisticas', {})
            print(f"   Versão: {stats.get('versao', 'N/A')}")
            print(f"   Modelo: {stats.get('modelo_ia', 'N/A')}")
            print(f"   Disciplinas: {stats.get('disciplinas_conhecidas', 0)}")
            print(f"   Bancas: {stats.get('bancas_conhecidas', 0)}")
        else:
            print(f"❌ Estatísticas: Erro {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Estatísticas: Erro de conexão - {e}")
    
    print("\n" + "=" * 50)
    print("🎉 TESTE DA API CONCLUÍDO!")
    return True

if __name__ == "__main__":
    test_api()
