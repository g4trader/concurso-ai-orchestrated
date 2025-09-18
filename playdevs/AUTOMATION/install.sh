#!/bin/bash

# Script de instalação para Automação do Cursor
# Instala dependências e configura o ambiente

echo "🚀 Instalação da Automação do Cursor"
echo "===================================="

# Verifica se Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale Python 3 primeiro."
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Verifica se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instale pip3 primeiro."
    exit 1
fi

echo "✅ pip3 encontrado"

# Cria ambiente virtual (opcional)
read -p "Deseja criar um ambiente virtual? (y/n): " create_venv
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv cursor_automation_env
    source cursor_automation_env/bin/activate
    echo "✅ Ambiente virtual criado e ativado"
fi

# Instala dependências
echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso"
else
    echo "❌ Erro na instalação das dependências"
    exit 1
fi

# Verifica se o Cursor está instalado
if [ -d "/Applications/Cursor.app" ]; then
    echo "✅ Cursor IDE encontrado em /Applications/Cursor.app"
else
    echo "⚠️ Cursor IDE não encontrado em /Applications/"
    echo "   Certifique-se de que o Cursor está instalado"
fi

# Configura permissões
echo "🔐 Configurando permissões..."

# macOS: Permissões para acessibilidade
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📱 Configurando permissões do macOS..."
    echo "   Você precisará conceder permissões de acessibilidade para:"
    echo "   - Terminal (ou seu editor de código)"
    echo "   - Python"
    echo ""
    echo "   Vá para: Preferências do Sistema > Segurança e Privacidade > Privacidade > Acessibilidade"
    echo "   Adicione o Terminal e Python à lista"
fi

# Torna scripts executáveis
chmod +x *.py
echo "✅ Scripts tornados executáveis"

# Cria arquivo de configuração padrão
echo "⚙️ Criando configuração padrão..."
python3 setup_automation.py

if [ $? -eq 0 ]; then
    echo "✅ Configuração criada com sucesso"
else
    echo "❌ Erro na criação da configuração"
fi

echo ""
echo "🎉 Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Conceda permissões de acessibilidade (macOS)"
echo "2. Execute: python3 launcher.py"
echo "3. Ou execute: python3 advanced_cursor_automation.py"
echo ""
echo "📚 Documentação:"
echo "- README.md - Instruções detalhadas"
echo "- automation_config.json - Configurações"
echo "- sprint_*_config.json - Configurações das sprints"
echo ""
echo "⚠️ Importante:"
echo "- Mantenha o Cursor visível durante a automação"
echo "- Use Ctrl+C para interromper se necessário"
echo "- Teste primeiro com o modo manual"
