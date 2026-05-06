#!/usr/bin/env python3
"""
DeepSeek API 基础调用示例
最简单的对话调用方式
"""

import os
import requests

API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-api-key-here")
BASE_URL = "https://api.deepseek.com"


def chat_completion(message: str, model: str = "deepseek-chat") -> str:
    """
    发送单条对话请求

    Args:
        message: 用户输入的消息
        model: 模型名称 (deepseek-chat 或 deepseek-reasoner)

    Returns:
        AI 的回复内容
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
    response.raise_for_status()

    result = response.json()
    return result["choices"][0]["message"]["content"]


def main():
    print("🤖 DeepSeek 基础对话示例\n")

    questions = [
        "你好，请介绍一下自己",
        "Python 中如何实现快速排序？",
        "讲一个程序员笑话"
    ]

    for question in questions:
        print(f"👤 用户: {question}")
        answer = chat_completion(question)
        print(f"🤖 AI: {answer}\n")
        print("-" * 50)


if __name__ == "__main__":
    main()
