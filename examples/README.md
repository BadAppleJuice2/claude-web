# DeepSeek API 调用示例

本目录包含 DeepSeek API 的各种调用示例，帮助你快速上手。

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API Key
export DEEPSEEK_API_KEY="sk-your-api-key"

# 3. 运行示例
python basic_chat.py
```

## 示例列表

| 文件 | 功能 | 适用场景 |
|------|------|----------|
| `basic_chat.py` | 单轮对话 | 简单问答 |
| `streaming_chat.py` | 实时流式输出 | 长文本生成 |
| `multi_turn_chat.py` | 上下文对话 | 连续交流 |
| `code_assistant.py` | 编程辅助 | 代码生成/解释/审查 |

## API 参考

- 官方文档: https://platform.deepseek.com/api-docs
- 模型价格: https://platform.deepseek.com/pricing
