# DeepSeek API 参考文档

> 本文档整理自 [DeepSeek 官方 API 文档](https://api-docs.deepseek.com/zh-cn/)，方便离线查阅。

---

## 目录

- [快速开始](#快速开始)
- [模型与价格](#模型与价格)
- [API 调用示例](#api-调用示例)
- [Anthropic API 兼容](#anthropic-api-兼容)
- [错误码](#错误码)
- [限速说明](#限速说明)

---

## 快速开始

### 基础信息

| 参数 | 值 |
|------|-----|
| **base_url (OpenAI)** | `https://api.deepseek.com` |
| **base_url (Anthropic)** | `https://api.deepseek.com/anthropic` |
| **api_key** | 从 [平台](https://platform.deepseek.com/api_keys) 申请 |

### 模型名称

| 模型名 | 说明 | 状态 |
|--------|------|------|
| `deepseek-v4-pro` | 专业版模型（推荐） | ✅ 最新 |
| `deepseek-v4-flash` | 轻量版模型 | ✅ 最新 |
| `deepseek-chat` | 通用对话模型 | ⚠️ 2026/07/24 弃用 |
| `deepseek-reasoner` | 推理模型 | ⚠️ 2026/07/24 弃用 |

> **注意**：`deepseek-chat` 和 `deepseek-reasoner` 将于 2026/07/24 弃用，请迁移到 `deepseek-v4-flash` 和 `deepseek-v4-pro`。

---

## 模型与价格

### 价格表（每百万 Token）

| 模型 | 输入（缓存命中） | 输入（缓存未命中） | 输出 |
|------|-----------------|-------------------|------|
| `deepseek-v4-flash` (原 chat) | ¥0.2 | ¥2 | ¥3 |
| `deepseek-v4-pro` (原 reasoner) | - | - | - |

### 模型能力对比

| 功能 | deepseek-v4-flash | deepseek-v4-pro |
|------|-------------------|-----------------|
| 上下文长度 | 128K | 128K |
| 输出长度 | 默认 4K，最大 8K | 默认 32K，最大 64K |
| JSON 输出 | ✅ | ✅ |
| Tool Calls | ✅ | ✅ |
| 对话前缀续写 | ✅ | ✅ |
| FIM 补全 | ✅ | ❌ |

### 扣费规则

```
扣减费用 = token 消耗量 × 模型单价
```

- 费用直接从充值余额或赠送余额中扣减
- 优先扣减赠送余额
- 建议定期检查 [账户用量](https://platform.deepseek.com/usage)

---

## API 调用示例

### cURL

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-v4-pro",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ],
    "thinking": {"type": "enabled"},
    "reasoning_effort": "high",
    "stream": false
  }'
```

### Python (OpenAI SDK)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

print(response.choices[0].message.content)
```

### Node.js

```javascript
import OpenAI from "openai";

const openai = new OpenAI({
    baseURL: 'https://api.deepseek.com',
    apiKey: process.env.DEEPSEEK_API_KEY,
});

async function main() {
    const completion = await openai.chat.completions.create({
        messages: [{ role: "system", content: "You are a helpful assistant." }],
        model: "deepseek-v4-pro",
        thinking: {"type": "enabled"},
        reasoning_effort: "high",
        stream: false,
    });
    console.log(completion.choices[0].message.content);
}

main();
```

---

## Anthropic API 兼容

DeepSeek API 支持 Anthropic API 格式，可以直接用于 Claude Code 等工具。

### 配置 Claude Code 使用 DeepSeek

```bash
# 1. 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 2. 配置环境变量
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=${DEEPSEEK_API_KEY}
export API_TIMEOUT_MS=600000  # 10分钟超时
export ANTHROPIC_MODEL=deepseek-chat
export ANTHROPIC_SMALL_FAST_MODEL=deepseek-chat
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1

# 3. 进入项目目录使用
cd my-project
claude
```

### Python (Anthropic SDK)

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="deepseek-chat",
    max_tokens=1000,
    system="You are a helpful assistant.",
    messages=[{
        "role": "user",
        "content": [{"type": "text", "text": "Hi, how are you?"}]
    }]
)

print(message.content)
```

### Anthropic API 兼容性

#### 支持的字段

| 字段 | 支持状态 |
|------|----------|
| model | 使用 DeepSeek 模型名 |
| max_tokens | ✅ 完全支持 |
| stream | ✅ 完全支持 |
| system | ✅ 完全支持 |
| temperature | ✅ 支持 [0.0 ~ 2.0] |
| thinking | ✅ 支持 |
| stop_sequences | ✅ 完全支持 |
| tools | ✅ 完全支持 |
| tool_choice | ✅ 支持 |

#### 不支持的字段

| 字段 | 说明 |
|------|------|
| anthropic-beta | 忽略 |
| anthropic-version | 忽略 |
| top_k | 忽略 |
| cache_control | 忽略 |
| image/document 类型 | 不支持 |

---

## 错误码

| 状态码 | 错误类型 | 说明 |
|--------|----------|------|
| 400 | Bad Request | 请求格式错误 |
| 401 | Unauthorized | API Key 无效 |
| 429 | Rate Limit | 请求过于频繁 |
| 500 | Server Error | 服务器内部错误 |
| 503 | Service Unavailable | 服务暂时不可用 |

---

## 限速说明

- 默认限速根据账户等级有所不同
- 建议实现指数退避重试机制
- 大量调用前请联系 DeepSeek 申请提升限额

---

## Token 用量计算

Token 是模型处理文本的最小单位，大约：

- 1 个汉字 ≈ 1-2 个 Token
- 1 个英文单词 ≈ 1 个 Token
- 1 个标点符号 ≈ 1 个 Token

计费基于输入 + 输出的总 Token 数。

---

## 相关链接

- [DeepSeek 平台](https://platform.deepseek.com)
- [官方 API 文档](https://api-docs.deepseek.com/zh-cn/)
- [价格页面](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)

---

*本文档最后更新：2025-01-06*
