#!/bin/bash
set -e

echo "=========================================="
echo "  Claude Web UI + DeepSeek (Docker)"
echo "=========================================="

if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "错误: 请设置 DEEPSEEK_API_KEY 环境变量"
    echo "示例: docker run -e DEEPSEEK_API_KEY=sk-xxx -p 8765:8765 claude-web-ui"
    exit 1
fi

mkdir -p /root/.claude
cat > /root/.claude/settings.json << EOF
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "$DEEPSEEK_API_KEY",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_MODEL": "${MODEL:-deepseek-chat}",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "${MODEL:-deepseek-chat}",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "${MODEL:-deepseek-chat}",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "${MODEL:-deepseek-chat}",
    "CLAUDE_CODE_SUBAGENT_MODEL": "${MODEL:-deepseek-chat}",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "32000"
  }
}
EOF

echo "✓ 配置完成"
cd /app && source .venv/bin/activate

PORT=${PORT:-8765}
HOST=${HOST:-0.0.0.0}

echo "启动服务: http://localhost:$PORT"
python server.py
