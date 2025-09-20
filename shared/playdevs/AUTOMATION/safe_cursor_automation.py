#!/usr/bin/env python3
"""
Safe Cursor IDE Automation - Versão segura sem loops
Executa sprints de forma controlada e segura
"""

import subprocess
import time
import json
import os
import signal
import sys
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

class SafeCursorAutomation:
    """Automação segura do Cursor sem loops"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.cursor_process = None
        self.active_chats = {}
        self.completed_agents = set()
        self.running = False
    
    def _load_config(self, config_path: str) -> dict:
        """Carrega configuração"""
        default_config = {
            "cursor_app_name": "Cursor",
            "project_path": "/Users/lucianoterres/Documents/GitHub/concurso-ai-orchestrated",
            "wait_times": {
                "app_launch": 3.0,
                "chat_open": 2.0,
                "message_send": 1.0,
                "response_wait": 5.0
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
                        memory_usage=proc.info['memory_info'].rss / 1024 / 1024
                    )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None
    
    def launch_cursor(self) -> bool:
        """Lança o Cursor usando AppleScript (macOS)"""
        try:
            script = f'''
            tell application "{self.config["cursor_app_name"]}"
                activate
                delay 1
            end tell
            '''
            
            subprocess.run(['osascript', '-e', script], check=True, timeout=10)
            time.sleep(self.config["wait_times"]["app_launch"])
            
            self.cursor_process = self.find_cursor_process()
            if self.cursor_process:
                print(f"✅ Cursor lançado (PID: {self.cursor_process.pid})")
                return True
            else:
                print("❌ Cursor não foi encontrado após lançamento")
                return False
                
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"❌ Erro ao lançar Cursor: {e}")
            return False
    
    def execute_applescript(self, script: str) -> bool:
        """Executa script AppleScript com timeout"""
        try:
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True, check=True, timeout=10)
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"❌ Erro no AppleScript: {e}")
            return False
    
    def open_new_chat(self, chat_name: str) -> bool:
        """Abre novo chat usando AppleScript"""
        try:
            # Ativa o Cursor
            self.execute_applescript(f'tell application "{self.config["cursor_app_name"]}" to activate')
            time.sleep(1)
            
            # Abre novo chat (Cmd+L para abrir chat, não nova janela)
            script = '''
            tell application "System Events"
                keystroke "l" using command down
            end tell
            '''
            
            if self.execute_applescript(script):
                time.sleep(self.config["wait_times"]["chat_open"])
                
                # Salva referência do chat
                self.active_chats[chat_name] = {
                    "opened_at": time.time(),
                    "status": "active"
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
                key code 0 using command down
                key code 51
            end tell
            '''
            self.execute_applescript(script)
            time.sleep(0.5)
            
            # Digita o prompt (limitado para evitar problemas)
            short_prompt = prompt[:500] + "..." if len(prompt) > 500 else prompt
            escaped_prompt = short_prompt.replace('"', '\\"').replace('\n', '\\n')
            
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
    
    def check_dependencies(self, agent_config: dict) -> bool:
        """Verifica se as dependências do agente foram atendidas"""
        dependencies = agent_config.get('dependencies', [])
        
        for dep in dependencies:
            if dep not in self.completed_agents:
                print(f"⏸️ {agent_config['agent_type']} aguardando {dep}")
                return False
        
        return True
    
    def execute_agent_workflow(self, agent_config: dict) -> bool:
        """Executa workflow para um agente com verificação de dependências"""
        agent_name = agent_config['name']
        agent_type = agent_config['agent_type']
        
        print(f"\n🚀 Executando {agent_type} - {agent_config['story_id']}")
        
        # Verifica dependências
        if not self.check_dependencies(agent_config):
            return False
        
        # 1. Abre novo chat
        if not self.open_new_chat(agent_name):
            return False
        
        # 2. Envia prompt
        if not self.send_prompt(agent_config['prompt'], agent_name):
            return False
        
        # 3. Aguarda resposta (com timeout)
        print(f"⏳ Aguardando resposta de {agent_type}...")
        print(f"💡 Complete sua tarefa no chat '{agent_name}' e pressione Ctrl+C para continuar")
        
        try:
            # Aguarda input do usuário com timeout
            import select
            import sys
            
            if sys.stdin in select.select([sys.stdin], [], [], 30)[0]:
                input()  # Limpa o buffer
            else:
                print("⏰ Timeout - continuando para próximo agente")
                
        except KeyboardInterrupt:
            print(f"\n⏹️ Continuando para próximo agente...")
        except Exception:
            print("⏰ Continuando automaticamente...")
        
        # 4. Marca como concluído
        self.completed_agents.add(agent_name)
        self.active_chats[agent_name]["status"] = "completed"
        
        print(f"✅ {agent_type} concluído")
        return True
    
    def execute_sprint(self, sprint_number: int) -> bool:
        """Executa sprint completa de forma segura"""
        print(f"\n🎯 Executando Sprint {sprint_number}")
        
        # Carrega configuração da sprint
        sprint_config = self._load_sprint_config(sprint_number)
        if not sprint_config:
            return False
        
        print(f"📋 Sprint: {sprint_config.get('objective', 'N/A')}")
        print(f"👥 Agentes: {len(sprint_config['chats'])}")
        
        self.running = True
        
        try:
            # Executa cada agente em ordem
            for i, agent_config in enumerate(sprint_config["chats"], 1):
                if not self.running:
                    break
                    
                print(f"\n{'='*50}")
                print(f"📊 Progresso: {i}/{len(sprint_config['chats'])}")
                print(f"{'='*50}")
                
                if not self.execute_agent_workflow(agent_config):
                    print(f"⏸️ {agent_config['agent_type']} pulado (dependências não atendidas)")
                    continue
            
            if self.running:
                print(f"\n🎉 Sprint {sprint_number} executada com sucesso!")
                print(f"✅ Agentes concluídos: {len(self.completed_agents)}")
                return True
            else:
                print(f"\n⏹️ Sprint {sprint_number} interrompida")
                return False
            
        except KeyboardInterrupt:
            print(f"\n⏹️ Sprint {sprint_number} interrompida pelo usuário")
            self.running = False
            return False
        except Exception as e:
            print(f"\n❌ Erro na Sprint {sprint_number}: {e}")
            self.running = False
            return False
    
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
    
    def stop(self):
        """Para a execução"""
        self.running = False
        print("⏹️ Parando automação...")
    
    def cleanup(self):
        """Limpa recursos"""
        print("\n🧹 Limpando recursos...")
        self.active_chats.clear()
        self.completed_agents.clear()
        self.running = False
        print("✅ Limpeza concluída")

def signal_handler(signum, frame):
    """Handler para sinais de interrupção"""
    print("\n⏹️ Recebido sinal de interrupção")
    if 'automation' in globals():
        automation.stop()
    sys.exit(0)

def main():
    """Função principal"""
    global automation
    
    # Configura handlers de sinal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    automation = SafeCursorAutomation()
    
    try:
        print("🤖 Automação Segura do Cursor")
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
        
        # Executa Sprint 2
        print("\n🎯 Iniciando Sprint 2...")
        automation.execute_sprint(2)
    
    except KeyboardInterrupt:
        print("\n⏹️ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        automation.cleanup()

if __name__ == "__main__":
    main()


