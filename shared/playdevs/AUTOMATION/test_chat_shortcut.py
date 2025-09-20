#!/usr/bin/env python3
"""
Teste Específico de Atalho de Chat
Verifica se Cmd+L abre nova aba de chat corretamente
"""

import subprocess
import time

def test_chat_shortcut():
    """Testa o atalho Cmd+L para abrir nova aba de chat"""
    print("🧪 Teste de Atalho de Chat - Cmd+L")
    print("=" * 40)
    
    try:
        # 1. Ativa o Cursor
        print("🔍 Ativando Cursor...")
        script = 'tell application "Cursor" to activate'
        subprocess.run(['osascript', '-e', script], check=True)
        time.sleep(2)
        
        # 2. Testa Cmd+L
        print("⌨️ Executando Cmd+L...")
        script = '''
        tell application "System Events"
            keystroke "l" using command down
        end tell
        '''
        
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Cmd+L executado com sucesso")
            print("👀 Verifique se uma nova aba de chat foi aberta")
            time.sleep(3)
            
            # 3. Testa se consegue digitar no chat
            print("📝 Testando digitação no chat...")
            script = '''
            tell application "System Events"
                keystroke "Teste de atalho Cmd+L funcionando!"
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Digitação funcionou")
                print("🎉 Teste de atalho Cmd+L: PASSOU")
                return True
            else:
                print("❌ Falha na digitação")
                return False
        else:
            print("❌ Falha ao executar Cmd+L")
            print(f"Erro: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

def test_alternative_shortcuts():
    """Testa atalhos alternativos"""
    print("\n🔧 Testando Atalhos Alternativos")
    print("=" * 40)
    
    shortcuts = [
        ("Cmd+Shift+L", 'keystroke "l" using {command down, shift down}'),
        ("Cmd+K", 'keystroke "k" using command down'),
        ("Cmd+Shift+K", 'keystroke "k" using {command down, shift down}'),
        ("Cmd+N", 'keystroke "n" using command down'),
    ]
    
    for name, script_content in shortcuts:
        print(f"\n⌨️ Testando {name}...")
        
        try:
            # Ativa o Cursor
            subprocess.run(['osascript', '-e', 'tell application "Cursor" to activate'], 
                         check=True)
            time.sleep(1)
            
            # Executa atalho
            script = f'''
            tell application "System Events"
                {script_content}
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {name} executado com sucesso")
                time.sleep(2)
            else:
                print(f"❌ {name} falhou: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Erro com {name}: {e}")

def main():
    """Função principal"""
    print("🔧 Teste de Atalhos de Chat do Cursor")
    print("=" * 50)
    
    print("\n📋 Opções:")
    print("1. Testar Cmd+L (atalho principal)")
    print("2. Testar atalhos alternativos")
    print("3. Testar ambos")
    print("4. Sair")
    
    try:
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            success = test_chat_shortcut()
            if success:
                print("\n🎉 Cmd+L está funcionando corretamente!")
            else:
                print("\n❌ Cmd+L não está funcionando")
                
        elif choice == "2":
            test_alternative_shortcuts()
            
        elif choice == "3":
            success = test_chat_shortcut()
            test_alternative_shortcuts()
            
            if success:
                print("\n🎉 Cmd+L está funcionando corretamente!")
            else:
                print("\n❌ Cmd+L não está funcionando - testando alternativas...")
                
        elif choice == "4":
            print("👋 Encerrando testes...")
            return
            
        else:
            print("❌ Opção inválida")
            
    except KeyboardInterrupt:
        print("\n⏹️ Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")

if __name__ == "__main__":
    main()
