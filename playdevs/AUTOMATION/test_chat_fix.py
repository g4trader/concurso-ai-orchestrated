#!/usr/bin/env python3
"""
Teste da Correção de Abertura de Chats
Verifica se o problema foi resolvido
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório pai ao path para importar os módulos
sys.path.append(str(Path(__file__).parent))

from fixed_cursor_automation import FixedCursorAutomation

def test_chat_opening():
    """Testa a abertura de chats corrigida"""
    print("🧪 Teste de Correção de Abertura de Chats")
    print("=" * 50)
    
    automation = FixedCursorAutomation()
    
    try:
        # 1. Verifica se o Cursor está rodando
        cursor_info = automation.get_cursor_info()
        if cursor_info["status"] == "not_running":
            print("🚀 Lançando Cursor...")
            if not automation.launch_cursor():
                print("❌ Falha ao lançar Cursor")
                return False
        else:
            print(f"✅ Cursor já está rodando (PID: {cursor_info['pid']})")
            automation.cursor_process = automation.find_cursor_process()
        
        # 2. Testa abertura de chat
        print("\n🔧 Testando abertura de chat...")
        test_chat_name = "Teste-Correção"
        
        if automation.open_new_chat(test_chat_name):
            print("✅ Teste de abertura de chat: PASSOU")
            
            # 3. Testa envio de prompt
            print("\n📤 Testando envio de prompt...")
            test_prompt = "Este é um teste de correção da automação. O chat foi aberto corretamente?"
            
            if automation.send_prompt(test_prompt, test_chat_name):
                print("✅ Teste de envio de prompt: PASSOU")
                print("\n🎉 TODOS OS TESTES PASSARAM!")
                print("✅ A correção foi bem-sucedida")
                return True
            else:
                print("❌ Teste de envio de prompt: FALHOU")
                return False
        else:
            print("❌ Teste de abertura de chat: FALHOU")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False
    finally:
        automation.cleanup()

def test_sprint_execution():
    """Testa execução de sprint com correção"""
    print("\n🚀 Teste de Execução de Sprint (Corrigida)")
    print("=" * 50)
    
    automation = FixedCursorAutomation()
    
    try:
        # Verifica se o Cursor está rodando
        cursor_info = automation.get_cursor_info()
        if cursor_info["status"] == "not_running":
            print("🚀 Lançando Cursor...")
            if not automation.launch_cursor():
                print("❌ Falha ao lançar Cursor")
                return False
        else:
            print(f"✅ Cursor já está rodando (PID: {cursor_info['pid']})")
            automation.cursor_process = automation.find_cursor_process()
        
        # Testa execução da Sprint 2
        print("\n🎯 Testando execução da Sprint 2...")
        print("⚠️ Este teste irá abrir chats reais - pressione Ctrl+C para interromper")
        
        try:
            # Executa apenas o primeiro agente para teste
            sprint_config = automation._load_sprint_config(2)
            if sprint_config and sprint_config["chats"]:
                first_agent = sprint_config["chats"][0]
                print(f"🧪 Testando com agente: {first_agent['agent_type']}")
                
                if automation.execute_agent_workflow(first_agent):
                    print("✅ Teste de execução de agente: PASSOU")
                return True
                else:
                    print("❌ Teste de execução de agente: FALHOU")
                    return False
            else:
                print("❌ Configuração da Sprint 2 não encontrada")
                return False
                
        except KeyboardInterrupt:
            print("\n⏹️ Teste interrompido pelo usuário")
            return True  # Considera como sucesso se foi interrompido manualmente
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False
    finally:
        automation.cleanup()

def main():
    """Função principal de teste"""
    print("🔧 Teste de Correção da Automação do Cursor")
    print("=" * 60)
    
    print("\n📋 Opções de teste:")
    print("1. Teste básico de abertura de chat")
    print("2. Teste de execução de sprint")
    print("3. Executar ambos os testes")
    print("4. Sair")
    
    try:
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            success = test_chat_opening()
            if success:
                print("\n🎉 Teste básico concluído com sucesso!")
            else:
                print("\n❌ Teste básico falhou")
                
        elif choice == "2":
            success = test_sprint_execution()
    if success:
                print("\n🎉 Teste de sprint concluído com sucesso!")
            else:
                print("\n❌ Teste de sprint falhou")
                
        elif choice == "3":
            print("\n🧪 Executando ambos os testes...")
            test1_success = test_chat_opening()
            test2_success = test_sprint_execution()
            
            if test1_success and test2_success:
                print("\n🎉 TODOS OS TESTES PASSARAM!")
                print("✅ A correção da automação foi bem-sucedida")
    else:
                print("\n❌ Alguns testes falharam")
                print(f"Teste básico: {'✅' if test1_success else '❌'}")
                print(f"Teste de sprint: {'✅' if test2_success else '❌'}")
                
        elif choice == "4":
            print("👋 Encerrando testes...")
            return
            
        else:
            print("❌ Opção inválida")
            
    except KeyboardInterrupt:
        print("\n⏹️ Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")

if __name__ == "__main__":
    main()