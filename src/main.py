#!/usr/bin/env python3
"""
Arquivo principal para executar o Agente Fiscal
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Verifica se as dependências estão instaladas"""
    try:
        import streamlit
        import crewai
        import pandas
        print("✅ Todas as dependências estão instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False

def check_ollama():
    """Verifica se o Ollama está rodando"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama está rodando")
            return True
        else:
            print("❌ Ollama não está respondendo")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar com Ollama: {e}")
        return False

def check_csv_files():
    """Verifica se os arquivos CSV existem"""
    base_path = Path(__file__).parent.parent
    csv_path = base_path / "knowledge"
    
    cabecalho_file = csv_path / "202401_NFs_Cabecalho.csv"
    itens_file = csv_path / "202401_NFs_Itens.csv"
    
    if cabecalho_file.exists() and itens_file.exists():
        print("✅ Arquivos CSV encontrados")
        return True
    else:
        print("❌ Arquivos CSV não encontrados")
        print(f"Procurando em: {csv_path}")
        return False

def install_requirements():
    """Instala as dependências do requirements.txt"""
    requirements_path = Path(__file__).parent.parent / "requirements.txt"
    if requirements_path.exists():
        print("📦 Instalando dependências...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)])
        return True
    else:
        print("❌ Arquivo requirements.txt não encontrado")
        return False

def run_streamlit():
    """Executa o Streamlit"""
    app_path = Path(__file__).parent / "app.py"
    if app_path.exists():
        print("🚀 Iniciando Streamlit...")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(app_path),
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    else:
        print("❌ Arquivo app.py não encontrado")

def main():
    """Função principal"""
    print("🤖 Agente Fiscal - Inicializando...")
    print("=" * 50)
    
    # Verificar dependências
    if not check_requirements():
        print("\n📦 Instalando dependências...")
        if not install_requirements():
            print("❌ Falha na instalação das dependências")
            return
        
        # Verificar novamente após instalação
        if not check_requirements():
            print("❌ Ainda há dependências faltando")
            return
    
    # Verificar Ollama
    if not check_ollama():
        print("\n⚠️  ATENÇÃO: Certifique-se de que o Ollama está rodando:")
        print("   1. Abra o terminal")
        print("   2. Execute: ollama serve")
        print("   3. Execute: ollama pull llama3.2:3b")
        return
    
    # Verificar arquivos CSV
    if not check_csv_files():
        print("\n⚠️  ATENÇÃO: Coloque os arquivos CSV na pasta 'knowledge/'")
        return
    
    print("\n✅ Todos os pré-requisitos atendidos!")
    print("🌐 Abrindo interface web...")
    print("-" * 50)
    
    # Executar Streamlit
    run_streamlit()

if __name__ == "__main__":
    main()