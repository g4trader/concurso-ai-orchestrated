#!/bin/bash

# Script de Instalação da Correção de Automação
# Corrige o problema de abertura de chats vs. edição de arquivos

echo "🔧 Instalando Correção de Automação do Cursor"
echo "=============================================="

# Verifica se estamos no diretório correto
if [ ! -f "fixed_cursor_automation.py" ]; then
    echo "❌ Execute este script no diretório playdevs/AUTOMATION/"
    exit 1
fi

# 1. Torna os scripts executáveis
echo "📝 Tornando scripts executáveis..."
chmod +x fixed_cursor_automation.py
chmod +x test_chat_fix.py

# 2. Verifica dependências Python
echo "🐍 Verificando dependências Python..."
python3 -c "import psutil, subprocess, json, os, signal, threading, pathlib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️ Instalando dependências Python..."
    pip3 install psutil
fi

# 3. Verifica se o Cursor está instalado
echo "🔍 Verificando instalação do Cursor..."
if [ -d "/Applications/Cursor.app" ]; then
    echo "✅ Cursor encontrado em /Applications/Cursor.app"
else
    echo "⚠️ Cursor não encontrado em /Applications/"
    echo "   Certifique-se de que o Cursor está instalado"
fi

# 4. Cria backup dos scripts originais
echo "💾 Criando backup dos scripts originais..."
if [ -f "cursor_automation.py" ]; then
    cp cursor_automation.py cursor_automation.py.backup
    echo "✅ Backup criado: cursor_automation.py.backup"
fi

if [ -f "advanced_cursor_automation.py" ]; then
    cp advanced_cursor_automation.py advanced_cursor_automation.py.backup
    echo "✅ Backup criado: advanced_cursor_automation.py.backup"
fi

# 5. Verifica configuração da Sprint 2
echo "📋 Verificando configuração da Sprint 2..."
if [ -f "sprint_2_config.json" ]; then
    echo "✅ Configuração da Sprint 2 encontrada"
else
    echo "❌ Configuração da Sprint 2 não encontrada"
    echo "   Certifique-se de que o arquivo sprint_2_config.json existe"
fi

# 6. Testa a correção
echo "🧪 Testando a correção..."
echo "   Execute: python3 test_chat_fix.py"
echo "   Ou execute: python3 fixed_cursor_automation.py"

echo ""
echo "🎉 Instalação da correção concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Execute: python3 test_chat_fix.py (para testar)"
echo "2. Execute: python3 fixed_cursor_automation.py (para usar)"
echo "3. Escolha a opção 1 para executar Sprint 2 corrigida"
echo ""
echo "🔧 O que foi corrigido:"
echo "- Problema de abertura de chats vs. edição de arquivos"
echo "- Melhor foco na interface do Cursor"
echo "- Tempos de espera otimizados"
echo "- Tratamento de erros melhorado"
echo ""
echo "✅ A automação agora deve abrir chats corretamente!"
