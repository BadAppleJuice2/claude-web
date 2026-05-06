#!/bin/bash
# Claude Web UI + DeepSeek 一键安装脚本
# 支持: macOS, Linux, Windows(WSL/Git Bash)

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[✓]${NC} $1"; }
print_error() { echo -e "${RED}[✗]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[!]${NC} $1"; }

command_exists() { command -v "$1" >/dev/null 2>&1; }

detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then OS="linux";
    elif [[ "$OSTYPE" == "darwin"* ]]; then OS="macos";
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then OS="windows";
    else OS="unknown"; fi
    print_info "检测到操作系统: $OS"
}

install_nodejs() {
    print_info "检查 Node.js..."
    if command_exists node; then
        NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
        if [ "$NODE_VERSION" -ge 18 ]; then
            print_success "Node.js 已安装: $(node --version)"
            return
        fi
    fi
    print_warn "Node.js 未安装或版本过低，开始安装..."
    if [ "$OS" == "macos" ]; then
        command_exists brew && brew install node || { print_error "请先安装 Homebrew: https://brew.sh"; exit 1; }
    elif [ "$OS" == "linux" ]; then
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
        sudo apt-get install -y nodejs
    else
        print_error "请手动安装 Node.js 18+: https://nodejs.org"; exit 1
    fi
    print_success "Node.js 安装完成: $(node --version)"
}

install_claude_code() {
    print_info "安装 Claude Code CLI..."
    if command_exists claude; then
        print_success "Claude Code 已安装: $(claude --version)"
        return
    fi
    npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com
    print_success "Claude Code 安装完成"
}

check_python() {
    print_info "检查 Python..."
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1)
        if [ "$PYTHON_VERSION" -ge 3 ]; then
            print_success "Python 已安装: $(python3 --version)"
            return
        fi
    fi
    print_error "Python 3.8+ 未安装"; exit 1
}

clone_project() {
    print_info "下载 Claude Web UI..."
    INSTALL_DIR="${HOME}/claude-web-ui"
    if [ -d "$INSTALL_DIR" ]; then
        print_warn "目录已存在，更新代码..."
        cd "$INSTALL_DIR" && git pull
    else
        git clone https://github.com/heng1234/claude-web.git "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi
    print_success "项目下载完成: $INSTALL_DIR"
}

install_python_deps() {
    print_info "安装 Python 依赖..."
    [ ! -d ".venv" ] && python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt -q
    print_success "Python 依赖安装完成"
}

fix_server_config() {
    print_info "配置服务器监听地址..."
    if grep -q "host = os.environ.get" server.py; then
        print_success "配置已修改"; return
    fi
    sed -i 's/uvicorn.run(app, host="127.0.0.1", port=port)/host = os.environ.get("HOST", "0.0.0.0")\n    uvicorn.run(app, host=host, port=port)/' server.py
    print_success "服务器配置完成"
}

create_scripts() {
    print_info "创建辅助脚本..."

    cat > start.sh << 'STARTEOF'
#!/bin/bash
set -e
GREEN='\033[0;32m'; BLUE='\033[0;34m'; NC='\033[0m'
echo -e "${BLUE}正在启动 Claude Web UI...${NC}"
cd "$(dirname "$0")"
[ ! -d ".venv" ] && { echo "错误: 虚拟环境不存在，请先运行 install.sh"; exit 1; }
source .venv/bin/activate
[ ! -f "$HOME/.claude/settings.json" ] && { echo "警告: 请先运行 ./setup.sh 配置 API Key"; exit 1; }
PORT=${PORT:-8765}; HOST=${HOST:-0.0.0.0}
echo ""
echo -e "${GREEN}✓ 服务启动成功!${NC}"
echo ""
echo "  访问地址: http://localhost:$PORT"
echo "  按 Ctrl+C 停止服务"
echo ""
python server.py
STARTEOF
    chmod +x start.sh

    cat > setup.sh << 'SETUPEOF'
#!/bin/bash
set -e
echo ""
echo "=========================================="
echo "  Claude Web UI + DeepSeek 配置向导"
echo "=========================================="
echo ""
read -p "请输入你的 DeepSeek API Key (sk-...): " API_KEY
[[ ! $API_KEY =~ ^sk- ]] && { echo "错误: API Key 格式不正确，应以 sk- 开头"; exit 1; }
mkdir -p "$HOME/.claude"
cat > "$HOME/.claude/settings.json" << JSONEOF
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "$API_KEY",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_MODEL": "deepseek-chat",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-chat",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-chat",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-chat",
    "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-chat",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "32000"
  }
}
JSONEOF
echo ""
echo "✓ 配置完成!"
echo "  配置文件: $HOME/.claude/settings.json"
echo ""
echo "现在可以运行: ./start.sh"
SETUPEOF
    chmod +x setup.sh

    print_success "辅助脚本创建完成"
}

main() {
    echo ""
    echo "=========================================="
    echo "  Claude Web UI + DeepSeek 一键安装"
    echo "  https://github.com/BadAppleJuice2/claude-web"
    echo "=========================================="
    echo ""

    detect_os
    install_nodejs
    install_claude_code
    check_python
    clone_project
    install_python_deps
    fix_server_config
    create_scripts

    echo ""
    echo "=========================================="
    echo "  🎉 安装完成!"
    echo "=========================================="
    echo ""
    echo "  安装目录: ${HOME}/claude-web-ui"
    echo ""
    echo "  下一步:"
    echo "    1. cd ${HOME}/claude-web-ui"
    echo "    2. ./setup.sh    # 配置 DeepSeek API Key"
    echo "    3. ./start.sh    # 启动服务"
    echo ""
    echo "  获取 API Key: https://platform.deepseek.com"
    echo ""
}

main "$@"
