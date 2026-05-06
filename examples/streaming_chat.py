#!/usr/bin/env python3
"""
DeepSeek API 流式输出示例
实现打字机效果的实时输出
"""

import os
import json
import requests

API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-api-key-here")
BASE_URL = "https://api.deepseek.com"


def stream_chat(message: str, model: str = "deepseek-chat"):
    """
    流式对话 - 实时返回内容（打字机效果）

    Args:
        message: 用户输入
        model: 模型名称

    Yields:
        每个 token 的内容片段
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
        "stream": True,
        "temperature": 0.7
    }

    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=data,
        stream=True
    )
    response.raise_for_status()

    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                json_str = line[6:]
                if json_str == '[DONE]':
                    break
                try:
                    chunk = json.loads(json_str)
                    if 'choices' in chunk and chunk['choices']:
                        delta = chunk['choices'][0].get('delta', {})
                        if 'content' in delta:
                            yield delta['content']
                except json.JSONDecodeError:
                    continue


def main():
    print("🤖 DeepSeek 流式输出示例\n")

    question = "用 Python 写一个斐波那契数列生成器，并解释原理"
    print(f"👤 用户: {question}\n")
    print("🤖 AI: ", end="", flush=True)

    full_response = ""
    for token in stream_chat(question):
        print(token, end="", flush=True)
        full_response += token

    print(f"\n\n✅ 完整响应已接收，总字数: {len(full_response)}")


if __name__ == "__main__":
    main()
