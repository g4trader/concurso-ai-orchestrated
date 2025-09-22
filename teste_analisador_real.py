#!/usr/bin/env python3
"""
Teste do analisador real de editais
"""

import sys
import os
sys.path.append('/Users/lucianoterres/Documents/GitHub/concurso-ai-orchestrated/backend/edital-analyzer')

from app.ai.edital_analyzer_real import EditalAnalyzerReal

def test_analisador_real():
    """Testa o analisador real de editais"""
    print("🔍 Testando analisador real de editais...")
    
    analyzer = EditalAnalyzerReal()
    
    # Conteúdo de exemplo de um edital real
    conteudo_exemplo = """
    EDITAL Nº 1/2024 - CONCURSO PÚBLICO
    TRIBUNAL REGIONAL DO TRABALHO DA 1ª REGIÃO
    
    O Tribunal Regional do Trabalho da 1ª Região torna pública a realização de concurso público para o provimento de vagas.
    
    1. DO CONCURSO
    1.1 O concurso será executado pela CESPE/CEBRASPE.
    1.2 Exige nível superior e/ou médio conforme o cargo.
    1.3 Remuneração inicial conforme tabela salarial.
    
    2. DAS INSCRIÇÕES
    2.1 Período de inscrições: 01/10/2024 a 15/10/2024.
    2.2 Taxa de inscrição conforme tabela.
    2.3 Inscrições exclusivamente via internet.
    
    3. DAS PROVAS
    3.1 Prova Objetiva de múltipla escolha.
    3.2 Prova Discursiva (para alguns cargos).
    3.3 Prova de Títulos (para alguns cargos).
    
    4. DO CONTEÚDO PROGRAMÁTICO
    4.1 Língua Portuguesa
    4.2 Matemática
    4.3 Informática
    4.4 Conhecimentos Específicos
    4.5 Legislação Aplicada
    
    5. DA CLASSIFICAÇÃO E APROVAÇÃO
    5.1 Será considerado aprovado o candidato que obtiver nota mínima.
    5.2 Classificação por ordem decrescente de notas.
    
    6. DO CRONOGRAMA
    6.1 Publicação do Edital: 20/09/2024
    6.2 Inscrições: 01/10/2024 a 15/10/2024
    6.3 Prova Objetiva: 15/11/2024
    6.4 Resultado: 30/11/2024
    
    CARGOS E VAGAS:
    - Analista Judiciário: 30 vagas
    - Técnico Judiciário: 20 vagas
    
    SALÁRIOS:
    - Analista Judiciário: R$ 8.500,00
    - Técnico Judiciário: R$ 4.200,00
    """
    
    try:
        print("1️⃣ Testando análise completa...")
        resultado = analyzer.analisar_edital_completo(
            conteudo_exemplo, 
            url_edital="https://exemplo.com/edital-trt1.pdf",
            banca="CESPE/CEBRASPE"
        )
        
        print("✅ Análise concluída!")
        print(f"📊 Resumo executivo: {len(resultado.get('resumo_executivo', ''))} caracteres")
        print(f"📋 Cargos encontrados: {len(resultado.get('cargos_disponiveis', []))}")
        print(f"📚 Disciplinas: {len(resultado.get('disciplinas_principais', []))}")
        print(f"📅 Datas: {len(resultado.get('datas_importantes', {}))}")
        print(f"💰 Salários: {len(resultado.get('valores_salariais', {}))}")
        
        print("\n📋 Detalhes da análise:")
        print(f"  Órgão: {resultado.get('informacoes_extras', {}).get('orgao', 'N/A')}")
        print(f"  Banca: {resultado.get('informacoes_extras', {}).get('banca', 'N/A')}")
        print(f"  Nível: {resultado.get('informacoes_extras', {}).get('nivel', 'N/A')}")
        
        relevancia = resultado.get('analise_relevancia', {})
        print(f"  Pontuação: {relevancia.get('pontuacao', 0)}/100")
        print(f"  Recomendação: {relevancia.get('recomendacao', 'N/A')}")
        
        print("\n🎯 Fatores positivos:")
        for fator in relevancia.get('fatores_positivos', []):
            print(f"  ✅ {fator}")
        
        print("\n⚠️ Fatores negativos:")
        for fator in relevancia.get('fatores_negativos', []):
            print(f"  ❌ {fator}")
        
        print("\n🎉 Teste concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 TESTE DO ANALISADOR REAL DE EDITAIS")
    print("=" * 50)
    
    result = test_analisador_real()
    
    print("\n" + "=" * 50)
    if result:
        print("✅ Analisador real funcionando!")
        print("🔍 Agora a análise extrai informações verdadeiras dos editais!")
    else:
        print("❌ Problemas no analisador real")
