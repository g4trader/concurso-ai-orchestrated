#!/bin/bash

# Script para executar Teste Rigoroso de UX
# Concurso AI - https://concurso-ai-orchestrated.vercel.app/

set -e

echo "🧪 Teste Rigoroso de UX - Concurso AI"
echo "======================================"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

error() {
    echo -e "${RED}❌${NC} $1"
}

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    error "Python 3 não está instalado!"
    echo "Instale Python 3 e tente novamente."
    exit 1
fi

success "Python 3 encontrado"

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    error "pip3 não está instalado!"
    echo "Instale pip3 e tente novamente."
    exit 1
fi

success "pip3 encontrado"

# Criar ambiente virtual (opcional)
if [ ! -d "venv_ux_test" ]; then
    log "Criando ambiente virtual..."
    python3 -m venv venv_ux_test
    success "Ambiente virtual criado"
fi

# Ativar ambiente virtual
log "Ativando ambiente virtual..."
source venv_ux_test/bin/activate
success "Ambiente virtual ativado"

# Instalar dependências
log "Instalando dependências..."
pip install -r requirements_ux_test.txt
success "Dependências instaladas"

# Verificar se Chrome está instalado
if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null; then
    warning "Chrome/Chromium não encontrado!"
    echo "Instale Google Chrome ou Chromium para executar os testes."
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt update && sudo apt install google-chrome-stable"
    echo ""
    echo "macOS:"
    echo "  brew install --cask google-chrome"
    echo ""
    echo "Windows:"
    echo "  Baixe do site oficial do Google Chrome"
    echo ""
    read -p "Pressione Enter para continuar mesmo assim..."
fi

# Executar testes
log "Iniciando testes de UX..."
echo ""
echo "🌐 URL: https://concurso-ai-orchestrated.vercel.app/"
echo "🔐 Credenciais: admin@concursoai.com / admin123"
echo ""

python3 test_ux_selenium.py

# Verificar se os relatórios foram gerados
if ls ux_test_report_*.json 1> /dev/null 2>&1; then
    success "Relatório JSON gerado"
fi

if ls ux_test_report_*.html 1> /dev/null 2>&1; then
    success "Relatório HTML gerado"
    
    # Abrir relatório HTML (se possível)
    if command -v xdg-open &> /dev/null; then
        log "Abrindo relatório HTML..."
        xdg-open ux_test_report_*.html
    elif command -v open &> /dev/null; then
        log "Abrindo relatório HTML..."
        open ux_test_report_*.html
    else
        warning "Não foi possível abrir o relatório automaticamente"
        echo "Abra manualmente o arquivo ux_test_report_*.html"
    fi
fi

echo ""
success "Testes de UX concluídos!"
echo ""
echo "📊 Relatórios gerados:"
ls -la ux_test_report_* 2>/dev/null || echo "Nenhum relatório encontrado"
echo ""
echo "🎯 Próximos passos:"
echo "1. Revise os relatórios gerados"
echo "2. Corrija os problemas identificados"
echo "3. Execute os testes novamente se necessário"
echo ""
echo "💡 Dicas:"
echo "- Os relatórios HTML são mais fáceis de visualizar"
echo "- Foque primeiro nos testes que falharam"
echo "- Testes com avisos podem indicar melhorias"
