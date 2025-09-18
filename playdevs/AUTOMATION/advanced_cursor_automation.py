#!/usr/bin/env python3
"""
Advanced Cursor IDE Automation
Usa APIs do sistema operacional para controle mais preciso
"""

import subprocess
import time
import json
import os
import signal
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
import psutil

@dataclass
class ProcessInfo:
    """Informações sobre processo do Cursor"""
    pid: int
    name: str
    status: str
    memory_usage: float

class AdvancedCursorAutomation:
    """Automação avançada do Cursor usando APIs do sistema"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.cursor_process = None
        self.active_chats = {}
        self.monitoring = False
        self.monitor_thread = None
    
    def _load_config(self, config_path: str) -> dict:
        """Carrega configuração"""
        default_config = {
            "cursor_app_name": "Cursor",
            "cursor_bundle_id": "com.todesktop.230313mzl4w4u92",
            "project_path": "/Users/lucianoterres/Documents/GitHub/concurso-ai-orchestrated",
            "wait_times": {
                "app_launch": 5.0,
                "chat_open": 2.0,
                "message_send": 1.0,
                "response_wait": 10.0
            },
            "automation_scripts": {
                "open_chat": "tell application \"Cursor\" to activate",
                "send_message": "tell application \"System Events\" to keystroke \"{message}\"",
                "press_enter": "tell application \"System Events\" to key code 36"
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def find_cursor_process(self) -> Optional[ProcessInfo]:
        """Encontra processo do Cursor"""
        for proc in psutil.process_iter(['pid', 'name', 'status', 'memory_info']):
            try:
                if self.config["cursor_app_name"].lower() in proc.info['name'].lower():
                    return ProcessInfo(
                        pid=proc.info['pid'],
                        name=proc.info['name'],
                        status=proc.info['status'],
                        memory_usage=proc.info['memory_info'].rss / 1024 / 1024  # MB
                    )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None
    
    def launch_cursor(self) -> bool:
        """Lança o Cursor usando AppleScript (macOS)"""
        try:
            # Comando para abrir o Cursor
            script = f'''
            tell application "{self.config["cursor_app_name"]}"
                activate
                delay 2
            end tell
            '''
            
            subprocess.run(['osascript', '-e', script], check=True)
            time.sleep(self.config["wait_times"]["app_launch"])
            
            # Verifica se o processo foi criado
            self.cursor_process = self.find_cursor_process()
            if self.cursor_process:
                print(f"✅ Cursor lançado (PID: {self.cursor_process.pid})")
                return True
            else:
                print("❌ Cursor não foi encontrado após lançamento")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao lançar Cursor: {e}")
            return False
    
    def execute_applescript(self, script: str) -> bool:
        """Executa script AppleScript"""
        try:
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro no AppleScript: {e}")
            return False
    
    def open_new_chat(self, chat_name: str) -> bool:
        """Abre novo chat usando AppleScript"""
        try:
            # Ativa o Cursor
            self.execute_applescript(f'tell application "{self.config["cursor_app_name"]}" to activate')
            time.sleep(1)
            
            # Abre novo chat (Cmd+Shift+N)
            script = '''
            tell application "System Events"
                keystroke "n" using {command down, shift down}
            end tell
            '''
            
            if self.execute_applescript(script):
                time.sleep(self.config["wait_times"]["chat_open"])
                
                # Salva referência do chat
                self.active_chats[chat_name] = {
                    "opened_at": time.time(),
                    "status": "active",
                    "pid": self.cursor_process.pid if self.cursor_process else None
                }
                
                print(f"✅ Chat '{chat_name}' aberto")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Erro ao abrir chat '{chat_name}': {e}")
            return False
    
    def send_prompt(self, prompt: str, chat_name: str = None) -> bool:
        """Envia prompt usando AppleScript"""
        try:
            # Ativa o Cursor
            self.execute_applescript(f'tell application "{self.config["cursor_app_name"]}" to activate')
            time.sleep(0.5)
            
            # Limpa o campo de texto
            script = '''
            tell application "System Events"
                key code 0 using command down  -- Cmd+A
                key code 51  -- Delete
            end tell
            '''
            self.execute_applescript(script)
            time.sleep(0.5)
            
            # Digita o prompt
            # Escapa caracteres especiais para AppleScript
            escaped_prompt = prompt.replace('"', '\\"').replace('\n', '\\n')
            
            script = f'''
            tell application "System Events"
                keystroke "{escaped_prompt}"
            end tell
            '''
            
            if self.execute_applescript(script):
                time.sleep(1)
                
                # Envia a mensagem (Cmd+Enter)
                send_script = '''
                tell application "System Events"
                    key code 36 using command down
                end tell
                '''
                
                if self.execute_applescript(send_script):
                    time.sleep(self.config["wait_times"]["message_send"])
                    print(f"✅ Prompt enviado para '{chat_name or 'chat ativo'}'")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erro ao enviar prompt: {e}")
            return False
    
    def monitor_cursor_status(self):
        """Monitora status do Cursor em thread separada"""
        while self.monitoring:
            try:
                if self.cursor_process:
                    # Verifica se o processo ainda existe
                    if not psutil.pid_exists(self.cursor_process.pid):
                        print("⚠️ Processo do Cursor foi encerrado")
                        self.cursor_process = None
                        break
                    
                    # Atualiza informações do processo
                    try:
                        proc = psutil.Process(self.cursor_process.pid)
                        self.cursor_process.memory_usage = proc.memory_info().rss / 1024 / 1024
                        self.cursor_process.status = proc.status()
                    except psutil.NoSuchProcess:
                        self.cursor_process = None
                        break
                
                time.sleep(5)  # Verifica a cada 5 segundos
                
            except Exception as e:
                print(f"⚠️ Erro no monitoramento: {e}")
                time.sleep(5)
    
    def start_monitoring(self):
        """Inicia monitoramento do Cursor"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self.monitor_cursor_status)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            print("🔍 Monitoramento iniciado")
    
    def stop_monitoring(self):
        """Para monitoramento do Cursor"""
        if self.monitoring:
            self.monitoring = False
            if self.monitor_thread:
                self.monitor_thread.join(timeout=2)
            print("⏹️ Monitoramento parado")
    
    def execute_agent_workflow(self, chat_config: dict) -> bool:
        """Executa workflow para um agente"""
        print(f"\n🚀 Executando {chat_config['agent_type']} - {chat_config['story_id']}")
        
        # 1. Abre novo chat
        if not self.open_new_chat(chat_config['name']):
            return False
        
        # 2. Envia prompt
        if not self.send_prompt(chat_config['prompt'], chat_config['name']):
            return False
        
        # 3. Aguarda resposta
        print(f"⏳ Aguardando resposta de {chat_config['agent_type']}...")
        time.sleep(self.config["wait_times"]["response_wait"])
        
        # 4. Atualiza status
        self.active_chats[chat_config['name']]["status"] = "completed"
        
        print(f"✅ {chat_config['agent_type']} concluído")
        return True
    
    def execute_sprint(self, sprint_number: int) -> bool:
        """Executa sprint completa"""
        print(f"\n🎯 Executando Sprint {sprint_number}")
        
        # Carrega configuração da sprint
        sprint_config = self._load_sprint_config(sprint_number)
        if not sprint_config:
            return False
        
        # Inicia monitoramento
        self.start_monitoring()
        
        try:
            # Executa cada agente
            for chat_config in sprint_config["chats"]:
                if not self.execute_agent_workflow(chat_config):
                    print(f"❌ Falha em {chat_config['agent_type']}")
                    return False
            
            print(f"✅ Sprint {sprint_number} executada com sucesso")
            return True
            
        finally:
            self.stop_monitoring()
    
    def _load_sprint_config(self, sprint_number: int) -> Optional[dict]:
        """Carrega configuração da sprint"""
        config_file = f"sprint_{sprint_number}_config.json"
        config_path = Path(self.config["project_path"]) / "playdevs" / "AUTOMATION" / config_file
        
        if not config_path.exists():
            print(f"❌ Configuração não encontrada: {config_path}")
            return None
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Erro ao carregar configuração: {e}")
            return None
    
    def get_cursor_info(self) -> dict:
        """Retorna informações do Cursor"""
        if self.cursor_process:
            return {
                "pid": self.cursor_process.pid,
                "name": self.cursor_process.name,
                "status": self.cursor_process.status,
                "memory_mb": round(self.cursor_process.memory_usage, 2)
            }
        return {"status": "not_running"}
    
    def cleanup(self):
        """Limpa recursos"""
        print("\n🧹 Limpando recursos...")
        self.stop_monitoring()
        self.active_chats.clear()
        print("✅ Limpeza concluída")

def main():
    """Função principal"""
    automation = AdvancedCursorAutomation()
    
    try:
        print("🤖 Automação Avançada do Cursor")
        print("=" * 40)
        
        # Verifica se o Cursor está rodando
        cursor_info = automation.get_cursor_info()
        if cursor_info["status"] == "not_running":
            print("🚀 Lançando Cursor...")
            if not automation.launch_cursor():
                return
        else:
            print(f"✅ Cursor já está rodando (PID: {cursor_info['pid']})")
            automation.cursor_process = automation.find_cursor_process()
        
        # Menu de opções
        while True:
            print("\n📋 Opções:")
            print("1. Executar Sprint 2")
            print("2. Executar Sprint 3")
            print("3. Executar Sprint 4")
            print("4. Teste manual")
            print("5. Status do Cursor")
            print("6. Sair")
            
            choice = input("\nEscolha uma opção: ").strip()
            
            if choice == "1":
                automation.execute_sprint(2)
            elif choice == "2":
                automation.execute_sprint(3)
            elif choice == "3":
                automation.execute_sprint(4)
            elif choice == "4":
                # Teste manual
                automation.open_new_chat("Teste")
                automation.send_prompt("Este é um teste de automação avançada!")
            elif choice == "5":
                info = automation.get_cursor_info()
                print(f"📊 Status do Cursor: {info}")
            elif choice == "6":
                break
            else:
                print("❌ Opção inválida")
    
    except KeyboardInterrupt:
        print("\n⏹️ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        automation.cleanup()

if __name__ == "__main__":
    main()
