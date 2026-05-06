# Claude Web UI + DeepSeek

[![CI](https://github.com/BadAppleJuice2/claude-web/actions/workflows/ci.yml/badge.svg)](https://github.com/BadAppleJuice2/claude-web/actions/workflows/ci.yml)
[![Docker](https://github.com/BadAppleJuice2/claude-web/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/BadAppleJuice2/claude-web/actions/workflows/docker-publish.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 图形界面的 Claude Code，接入 DeepSeek 国内模型，无需科学上网，一键部署。

## ✨ 特性

- 🖥️ **可视化 Web 界面** - 类 ChatGPT 的交互体验
- 🇨🇳 **DeepSeek 国内模型** - 稳定、快速、性价比高
- 💻 **代码 Diff 对比** - 红绿高亮，一目了然
- 🖼️ **图片上传支持** - 多模态交互
- 💾 **会话历史管理** - 持久化存储对话记录
- 🌙 **暗黑模式** - 护眼主题
- 🐳 **Docker 支持** - 一键部署
- 📦 **Python SDK** - 程序化调用 DeepSeek API
- 🔄 **流式输出** - 打字机效果的实时响应

## 🚀 快速开始

### 方式一：一键脚本安装（推荐）

```bash
# 下载并运行安装脚本
curl -fsSL https://raw.githubusercontent.com/BadAppleJuice2/claude-web/main/install.sh | bash

# 配置 API Key（只需一次）
cd ~/claude-web-ui
./setup.sh

# 启动服务
./start.sh
```

访问 http://localhost:8765

---

### 方式二：Docker Compose（最简单）

```bash
# 1. 克隆仓库
git clone https://github.com/BadAppleJuice2/claude-web.git
cd claude-web

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 DEEPSEEK_API_KEY

# 3. 启动
docker-compose up -d
```

访问 http://localhost:8765

---

### 方式三：纯 Docker 命令

```bash
docker run -d \
  --name claude-web-ui \
  -p 8765:8765 \
  -e DEEPSEEK_API_KEY=sk-your-api-key \
  -e MODEL=deepseek-chat \
  ghcr.io/badapplejuice2/claude-web:latest
```

---

## 📦 Python SDK 使用

我们也提供了 Python SDK，方便你程序化调用 DeepSeek API：

```python
from deepseek_sdk import DeepSeekClient, Model

# 初始化客户端
client = DeepSeekClient(api_key="sk-your-key")

# 简单对话
response = client.chat("你好，请介绍一下 Python 装饰器")
print(response.content)

# 流式输出（打字机效果）
for token in client.chat("写一个快速排序", stream=True):
    print(token, end="", flush=True)

# 多轮对话
from deepseek_sdk import ChatSession

session = ChatSession(
    client,
    system_prompt="你是一位 Python 专家"
)

session.send("什么是生成器？")
session.send("能给个实际例子吗？")
```

更多示例见 [`examples/`](examples/) 目录。

---

## 🔧 配置说明

### 获取 DeepSeek API Key

1. 访问 https://platform.deepseek.com
2. 注册/登录账号
3. 创建 API Key（格式: `sk-...`）
4. 复制并配置到项目

### 环境变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `DEEPSEEK_API_KEY` | ✅ | - | DeepSeek API Key |
| `MODEL` | ❌ | `deepseek-chat` | 模型选择 |
| `PORT` | ❌ | `8765` | 服务端口 |
| `HOST` | ❌ | `0.0.0.0` | 监听地址 |

### 模型选择

| 模型 | 特点 | 适用场景 | 价格 |
|------|------|----------|------|
| `deepseek-chat` | 通用对话，速度快 | 日常编程、代码补全 | ¥1/百万Token |
| `deepseek-reasoner` | 推理能力强 | 复杂逻辑、数学问题 | ¥4/百万Token |

---

## 📁 项目结构

```
claude-web/
├── 📄 install.sh              # 一键安装脚本
├── 📄 deepseek_sdk.py         # Python SDK 封装
├── 📂 examples/               # DeepSeek API 调用示例
│   ├── basic_chat.py          #   基础对话
│   ├── streaming_chat.py      #   流式输出
│   ├── multi_turn_chat.py     #   多轮对话
│   └── code_assistant.py      #   代码助手
├── 🐳 Dockerfile              # Docker 镜像构建
├── 🐳 docker-compose.yml      # Docker Compose 配置
├── 🐳 docker-entrypoint.sh    # Docker 启动脚本
├── 📄 .env.example            # 环境变量模板
├── 📄 README.md               # 项目文档（本文件）
├── 📄 ARCHITECTURE.md         # 架构说明
├── 📄 CONTRIBUTING.md         # 贡献指南
├── 📄 LICENSE                 # MIT 许可证
└── 📂 .github/                # GitHub 配置
    ├── workflows/             #   CI/CD 自动化
    ├── ISSUE_TEMPLATE/        #   Issue 模板
    └── pull_request_template.md
```

---

## 🛠️ DeepSeek API 调用方法

### 基础调用

```python
import requests

API_KEY = "sk-your-key"
BASE_URL = "https://api.deepseek.com"

response = requests.post(
    f"{BASE_URL}/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "你好"}],
        "temperature": 0.7,
        "max_tokens": 2000
    }
)
print(response.json()["choices"][0]["message"]["content"])
```

### 流式调用

```python
response = requests.post(
    f"{BASE_URL}/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "你好"}],
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: ') and line[6:] != '[DONE]':
            import json
            chunk = json.loads(line[6:])
            print(chunk["choices"][0]["delta"].get("content", ""), end="", flush=True)
```

### 使用 SDK（推荐）

```python
from deepseek_sdk import DeepSeekClient

client = DeepSeekClient(api_key="sk-your-key")

# 普通对话
print(client.chat("你好").content)

# 流式输出
for token in client.chat("写一首诗", stream=True):
    print(token, end="", flush=True)
```

---

## 🐛 故障排查

### 端口被占用

```bash
# 更换端口启动
PORT=9000 ./start.sh
```

### 无法连接 DeepSeek

```bash
# 测试 API Key 是否有效
curl https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer sk-your-key"
```

### Docker 构建失败

```bash
# 清理缓存重新构建
docker-compose build --no-cache
docker-compose up -d
```

---

## 🤝 贡献

欢迎提交 Issue 和 PR！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

---

## 📄 许可证

[MIT License](LICENSE)

---

## 🙏 致谢

- [DeepSeek](https://deepseek.com) - 提供强大的 AI 模型
- [heng1234/claude-web](https://github.com/heng1234/claude-web) - 原始 Web UI 项目
- [Anthropic](https://anthropic.com) - Claude Code

---

⭐ 如果这个项目对你有帮助，请给我们一个 Star！
