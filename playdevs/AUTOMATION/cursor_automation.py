#!/usr/bin/env python3
"""
Cursor IDE Automation Script
Automatiza a abertura de chats e execução de scripts no Cursor IDE
"""

import pyautogui
import time
import subprocess
import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ChatConfig:
    """Configuração para um chat específico"""
    name: str
    prompt: str
    agent_type: str
    story_id: str
    dependencies: List[str] = None

@dataclass
class AutomationConfig:
    """Configuração geral da automação"""
    cursor_shortcuts: Dict[str, str]
    wait_times: Dict[str, float]
    screen_resolution: tuple
    project_path: str

class CursorAutomation:
    """Classe principal para automação do Cursor IDE"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.active_chats = {}
        self.setup_pyautogui()
    
    def _load_config(self, config_path: str) -> AutomationConfig:
        """Carrega configuração do arquivo JSON"""
        default_config = {
            "cursor_shortcuts": {
                "new_chat": "cmd+shift+n",  # macOS
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
            "screen_resolution": (1920, 1080),
            "project_path": "/Users/lucianoterres/Documents/GitHub/concurso-ai-orchestrated"
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return AutomationConfig(**default_config)
    
    def setup_pyautogui(self):
        """Configura PyAutoGUI para automação"""
        pyautogui.FAILSAFE = True  # Move mouse para canto superior esquerdo para parar
        pyautogui.PAUSE = 0.5  # Pausa entre comandos
        
        # Configura resolução da tela
        screen_width, screen_height = pyautogui.size()
        print(f"Resolução da tela detectada: {screen_width}x{screen_height}")
    
    def open_cursor(self) -> bool:
        """Abre o Cursor IDE"""
        try:
            # Tenta abrir o Cursor
            subprocess.run(["open", "-a", "Cursor"], check=True)
            time.sleep(self.config.wait_times["ui_load"])
            print("✅ Cursor IDE aberto com sucesso")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erro ao abrir Cursor IDE")
            return False
    
    def open_new_chat(self, chat_name: str) -> bool:
        """Abre um novo chat no Cursor"""
        try:
            # Atalho para novo chat (Cmd+L para nova aba de chat no Cursor)
            pyautogui.hotkey('cmd', 'l')
            time.sleep(self.config.wait_times["chat_open"])
            
            # Salva referência do chat
            self.active_chats[chat_name] = {
                "opened_at": time.time(),
                "status": "active"
            }
            
            print(f"✅ Chat '{chat_name}' aberto com sucesso")
            return True
        except Exception as e:
            print(f"❌ Erro ao abrir chat '{chat_name}': {e}")
            return False
    
    def send_prompt(self, prompt: str, chat_name: str = None) -> bool:
        """Envia um prompt para o chat ativo"""
        try:
            # Se não especificado, usa o último chat aberto
            if not chat_name:
                chat_name = list(self.active_chats.keys())[-1] if self.active_chats else None
            
            if not chat_name:
                print("❌ Nenhum chat ativo encontrado")
                return False
            
            # Seleciona o chat
            pyautogui.click(100, 100)  # Ajustar coordenadas conforme necessário
            time.sleep(0.5)
            
            # Digita o prompt
            pyautogui.write(prompt)
            time.sleep(1)
            
            # Envia a mensagem
            pyautogui.hotkey('cmd', 'enter')
            time.sleep(self.config.wait_times["message_send"])
            
            print(f"✅ Prompt enviado para chat '{chat_name}'")
            return True
        except Exception as e:
            print(f"❌ Erro ao enviar prompt: {e}")
            return False
    
    def wait_for_response(self, timeout: int = 30) -> bool:
        """Aguarda resposta do agente"""
        print(f"⏳ Aguardando resposta (timeout: {timeout}s)...")
        time.sleep(timeout)
        return True
    
    def execute_agent_workflow(self, chat_config: ChatConfig) -> bool:
        """Executa workflow completo para um agente"""
        print(f"\n🚀 Iniciando workflow para {chat_config.agent_type} - {chat_config.story_id}")
        
        # 1. Abre novo chat
        if not self.open_new_chat(chat_config.name):
            return False
        
        # 2. Envia prompt
        if not self.send_prompt(chat_config.prompt, chat_config.name):
            return False
        
        # 3. Aguarda resposta
        self.wait_for_response()
        
        # 4. Atualiza status
        self.active_chats[chat_config.name]["status"] = "completed"
        
        print(f"✅ Workflow concluído para {chat_config.agent_type}")
        return True
    
    def execute_sprint(self, sprint_number: int) -> bool:
        """Executa uma sprint completa"""
        print(f"\n🎯 Executando Sprint {sprint_number}")
        
        # Carrega configuração da sprint
        sprint_config = self._load_sprint_config(sprint_number)
        
        if not sprint_config:
            print(f"❌ Configuração da Sprint {sprint_number} não encontrada")
            return False
        
        # Executa cada agente da sprint
        for chat_config in sprint_config:
            if not self.execute_agent_workflow(chat_config):
                print(f"❌ Falha no workflow de {chat_config.agent_type}")
                return False
        
        print(f"✅ Sprint {sprint_number} executada com sucesso")
        return True
    
    def _load_sprint_config(self, sprint_number: int) -> List[ChatConfig]:
        """Carrega configuração de uma sprint específica"""
        config_file = f"sprint_{sprint_number}_config.json"
        config_path = Path(self.config.project_path) / "playdevs" / "AUTOMATION" / config_file
        
        if not config_path.exists():
            print(f"❌ Arquivo de configuração não encontrado: {config_path}")
            return None
        
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
                return [ChatConfig(**chat) for chat in data["chats"]]
        except Exception as e:
            print(f"❌ Erro ao carregar configuração: {e}")
            return None
    
    def monitor_chats(self) -> Dict[str, str]:
        """Monitora status dos chats ativos"""
        return {name: chat["status"] for name, chat in self.active_chats.items()}
    
    def close_chat(self, chat_name: str) -> bool:
        """Fecha um chat específico"""
        try:
            # Seleciona o chat
            # Implementar lógica para selecionar chat específico
            
            # Fecha o chat
            pyautogui.hotkey('cmd', 'w')
            time.sleep(1)
            
            # Remove da lista de chats ativos
            if chat_name in self.active_chats:
                del self.active_chats[chat_name]
            
            print(f"✅ Chat '{chat_name}' fechado")
            return True
        except Exception as e:
            print(f"❌ Erro ao fechar chat '{chat_name}': {e}")
            return False
    
    def cleanup(self):
        """Limpa recursos e fecha chats"""
        print("\n🧹 Limpando recursos...")
        
        for chat_name in list(self.active_chats.keys()):
            self.close_chat(chat_name)
        
        print("✅ Limpeza concluída")

def main():
    """Função principal para demonstração"""
    automation = CursorAutomation()
    
    try:
        # Abre o Cursor
        if not automation.open_cursor():
            return
        
        # Exemplo: Executa Sprint 2
        automation.execute_sprint(2)
        
        # Monitora status
        print("\n📊 Status dos chats:")
        for name, status in automation.monitor_chats().items():
            print(f"  {name}: {status}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    finally:
        automation.cleanup()

if __name__ == "__main__":
    main()
