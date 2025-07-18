#!/usr/bin/env python3
"""
Script de inicialização do Bot Free Fire UP System
Inicia a API Flask e o Bot Telegram automaticamente
"""

import os
import sys
import time
import signal
import subprocess
import threading
from pathlib import Path

class SystemManager:
    def __init__(self):
        self.api_process = None
        self.bot_process = None
        self.running = True
        
    def start_api(self):
        """Inicia a API Flask"""
        print("🚀 Iniciando API Flask...")
        try:
            self.api_process = subprocess.Popen(
                [sys.executable, "src/main.py"],
                cwd=Path(__file__).parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ API Flask iniciada (PID: {})".format(self.api_process.pid))
            return True
        except Exception as e:
            print(f"❌ Erro ao iniciar API: {e}")
            return False
    
    def start_bot(self):
        """Inicia o Bot Telegram"""
        print("🤖 Iniciando Bot Telegram...")
        try:
            self.bot_process = subprocess.Popen(
                [sys.executable, "telegram_bot.py"],
                cwd=Path(__file__).parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Bot Telegram iniciado (PID: {})".format(self.bot_process.pid))
            return True
        except Exception as e:
            print(f"❌ Erro ao iniciar Bot: {e}")
            return False
    
    def check_api_health(self):
        """Verifica se a API está respondendo"""
        try:
            import requests
            response = requests.get("http://localhost:5001/api/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def wait_for_api(self, timeout=30):
        """Aguarda a API ficar disponível"""
        print("⏳ Aguardando API ficar disponível...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.check_api_health():
                print("✅ API está respondendo!")
                return True
            time.sleep(1)
        
        print("❌ Timeout: API não respondeu em {} segundos".format(timeout))
        return False
    
    def monitor_processes(self):
        """Monitora os processos em execução"""
        while self.running:
            try:
                # Verificar API
                if self.api_process and self.api_process.poll() is not None:
                    print("⚠️ API Flask parou inesperadamente")
                    self.running = False
                    break
                
                # Verificar Bot
                if self.bot_process and self.bot_process.poll() is not None:
                    print("⚠️ Bot Telegram parou inesperadamente")
                    self.running = False
                    break
                
                time.sleep(5)
            except KeyboardInterrupt:
                break
    
    def stop_all(self):
        """Para todos os processos"""
        print("\n🛑 Parando sistema...")
        self.running = False
        
        if self.bot_process:
            print("⏹️ Parando Bot Telegram...")
            self.bot_process.terminate()
            try:
                self.bot_process.wait(timeout=5)
                print("✅ Bot Telegram parado")
            except subprocess.TimeoutExpired:
                self.bot_process.kill()
                print("🔪 Bot Telegram forçado a parar")
        
        if self.api_process:
            print("⏹️ Parando API Flask...")
            self.api_process.terminate()
            try:
                self.api_process.wait(timeout=5)
                print("✅ API Flask parada")
            except subprocess.TimeoutExpired:
                self.api_process.kill()
                print("🔪 API Flask forçada a parar")
    
    def signal_handler(self, signum, frame):
        """Handler para sinais do sistema"""
        print(f"\n📡 Sinal recebido: {signum}")
        self.stop_all()
        sys.exit(0)
    
    def start_system(self):
        """Inicia o sistema completo"""
        print("🎮 Bot Free Fire UP System")
        print("=" * 50)
        
        # Configurar handlers de sinal
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Verificar dependências
        try:
            import requests
            import telegram
            import flask
            import cryptography
        except ImportError as e:
            print(f"❌ Dependência faltando: {e}")
            print("💡 Execute: pip install -r requirements.txt")
            return False
        
        # Iniciar API
        if not self.start_api():
            return False
        
        # Aguardar API ficar disponível
        if not self.wait_for_api():
            self.stop_all()
            return False
        
        # Iniciar Bot
        if not self.start_bot():
            self.stop_all()
            return False
        
        print("\n🎉 Sistema iniciado com sucesso!")
        print("📊 API Flask: http://localhost:5001")
        print("🤖 Bot Telegram: Ativo e aguardando comandos")
        print("\n💡 Comandos disponíveis no Telegram:")
        print("   /start - Instruções")
        print("   /add <token> - Adicionar conta")
        print("   /status - Ver status das contas")
        print("   /list - Listar contas")
        print("\n⌨️ Pressione Ctrl+C para parar o sistema")
        
        # Monitorar processos
        monitor_thread = threading.Thread(target=self.monitor_processes)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        try:
            # Aguardar indefinidamente
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all()
        
        return True

def main():
    """Função principal"""
    manager = SystemManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "test":
            # Executar testes
            print("🧪 Executando testes...")
            result = subprocess.run([sys.executable, "test_bot_api.py"])
            sys.exit(result.returncode)
        
        elif command == "api-only":
            # Apenas API
            print("🚀 Iniciando apenas a API...")
            if manager.start_api():
                manager.wait_for_api()
                print("✅ API rodando em http://localhost:5001")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    manager.stop_all()
            sys.exit(0)
        
        elif command == "help":
            print("🎮 Bot Free Fire UP System - Comandos")
            print("=" * 40)
            print("python start_system.py          - Iniciar sistema completo")
            print("python start_system.py test     - Executar testes")
            print("python start_system.py api-only - Apenas API Flask")
            print("python start_system.py help     - Esta ajuda")
            sys.exit(0)
    
    # Iniciar sistema completo
    success = manager.start_system()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

