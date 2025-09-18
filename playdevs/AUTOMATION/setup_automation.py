#!/usr/bin/env python3
"""
Setup Script para Automação do Cursor
Instala dependências e configura o ambiente de automação
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Instala as dependências necessárias"""
    requirements = [
        "pyautogui",
        "pillow",
        "opencv-python",
        "keyboard",
        "psutil"
    ]
    
    print("📦 Instalando dependências...")
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} instalado com sucesso")
        except subprocess.CalledProcessError:
            print(f"❌ Erro ao instalar {package}")
            return False
    
    return True

def create_config_file():
    """Cria arquivo de configuração padrão"""
    config = {
        "cursor_shortcuts": {
            "new_chat": "cmd+shift+n",
            "focus_chat": "cmd+1",
            "send_message": "cmd+enter",
            "close_chat": "cmd+w"
        },
        "wait_times": {
            "chat_open": 2.0,
            "message_send": 1.0,
            "response_wait": 5.0,
            "ui_load": 1.5
        },
        "screen_resolution": [1920, 1080],
        "project_path": str(Path.cwd().parent)
    }
    
    config_path = Path(__file__).parent / "automation_config.json"
    
    try:
        import json
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Arquivo de configuração criado: {config_path}")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar configuração: {e}")
        return False

def create_launcher_script():
    """Cria script de lançamento"""
    launcher_content = '''#!/usr/bin/env python3
"""
Launcher para Automação do Cursor
"""

import sys
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.append(str(Path(__file__).parent))

from cursor_automation import CursorAutomation

def main():
    automation = CursorAutomation()
    
    print("🤖 Automação do Cursor - Concurso-AI")
    print("=" * 50)
    print("1. Executar Sprint 2")
    print("2. Executar Sprint 3")
    print("3. Executar Sprint 4")
    print("4. Teste manual")
    print("5. Sair")
    
    choice = input("\\nEscolha uma opção: ")
    
    try:
        if choice == "1":
            automation.execute_sprint(2)
        elif choice == "2":
            automation.execute_sprint(3)
        elif choice == "3":
            automation.execute_sprint(4)
        elif choice == "4":
            # Teste manual
            automation.open_cursor()
            automation.open_new_chat("Teste")
            automation.send_prompt("Olá, este é um teste de automação!")
        elif choice == "5":
            print("👋 Até logo!")
        else:
            print("❌ Opção inválida")
    except KeyboardInterrupt:
        print("\\n⏹️ Interrompido pelo usuário")
    except Exception as e:
        print(f"\\n❌ Erro: {e}")
    finally:
        automation.cleanup()

if __name__ == "__main__":
    main()
'''
    
    launcher_path = Path(__file__).parent / "launcher.py"
    
    try:
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
        
        # Torna o arquivo executável
        os.chmod(launcher_path, 0o755)
        print(f"✅ Script de lançamento criado: {launcher_path}")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar launcher: {e}")
        return False

def create_readme():
    """Cria README com instruções"""
    readme_content = '''# 🤖 Automação do Cursor IDE

Este diretório contém scripts para automatizar a execução de sprints no Cursor IDE.

## 🚀 Instalação

1. Execute o script de setup:
```bash
python setup_automation.py
```

2. Execute o launcher:
```bash
python launcher.py
```

## 📋 Funcionalidades

- ✅ Abertura automática do Cursor IDE
- ✅ Criação de chats para cada agente
- ✅ Envio automático de prompts
- ✅ Monitoramento de status
- ✅ Execução de sprints completas

## ⚙️ Configuração

Edite o arquivo `automation_config.json` para ajustar:
- Atalhos do teclado
- Tempos de espera
- Resolução da tela
- Caminho do projeto

## 🎯 Uso

### Execução Manual
```python
from cursor_automation import CursorAutomation

automation = CursorAutomation()
automation.open_cursor()
automation.open_new_chat("Meu Chat")
automation.send_prompt("Seu prompt aqui")
```

### Execução de Sprint
```python
automation.execute_sprint(2)  # Executa Sprint 2
```

## 🔧 Dependências

- pyautogui
- pillow
- opencv-python
- keyboard
- psutil

## ⚠️ Limitações

- Funciona apenas no macOS (ajustar atalhos para Windows/Linux)
- Requer que o Cursor esteja instalado
- Coordenadas da tela podem precisar de ajuste
- Funciona melhor em resolução 1920x1080

## 🛠️ Troubleshooting

1. **Cursor não abre**: Verifique se está instalado e no PATH
2. **Chats não abrem**: Ajuste os atalhos no config
3. **Prompts não enviam**: Verifique as coordenadas da tela
4. **Erro de permissão**: Execute com sudo (não recomendado)

## 📝 Logs

Os logs são exibidos no console. Para salvar em arquivo:
```bash
python launcher.py > automation.log 2>&1
```
'''
    
    readme_path = Path(__file__).parent / "README.md"
    
    try:
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        print(f"✅ README criado: {readme_path}")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar README: {e}")
        return False

def main():
    """Função principal de setup"""
    print("🚀 Setup da Automação do Cursor")
    print("=" * 40)
    
    # Verifica se está no diretório correto
    if not Path(__file__).parent.name == "AUTOMATION":
        print("❌ Execute este script no diretório AUTOMATION")
        return
    
    # Instala dependências
    if not install_requirements():
        print("❌ Falha na instalação de dependências")
        return
    
    # Cria arquivos de configuração
    if not create_config_file():
        print("❌ Falha na criação da configuração")
        return
    
    # Cria script de lançamento
    if not create_launcher_script():
        print("❌ Falha na criação do launcher")
        return
    
    # Cria README
    if not create_readme():
        print("❌ Falha na criação do README")
        return
    
    print("\n✅ Setup concluído com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Execute: python launcher.py")
    print("2. Escolha a sprint para executar")
    print("3. Monitore a execução no console")
    print("\n⚠️ Importante:")
    print("- Mantenha o Cursor visível durante a execução")
    print("- Não mova o mouse durante a automação")
    print("- Use Ctrl+C para interromper se necessário")

if __name__ == "__main__":
    main()
