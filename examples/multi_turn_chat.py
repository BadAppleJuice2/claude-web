#!/usr/bin/env python3
"""
DeepSeek API 多轮对话示例
维护对话上下文，实现连续交流
"""

import os
import requests
from typing import List, Dict

API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-api-key-here")
BASE_URL = "https://api.deepseek.com"


class ChatSession:
    """
    对话会话类 - 维护对话历史，支持多轮交流
    """

    def __init__(self, model: str = "deepseek-chat", system_prompt: str = None):
        self.model = model
        self.messages: List[Dict[str, str]] = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def send(self, message: str) -> str:
        """发送消息并获取回复"""
        self.messages.append({"role": "user", "content": message})

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": self.messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }

        response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        assistant_message = result["choices"][0]["message"]["content"]

        self.messages.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    def clear_history(self):
        """清空对话历史（保留系统提示词）"""
        system_msg = next((m for m in self.messages if m["role"] == "system"), None)
        self.messages = [system_msg] if system_msg else []


def main():
    print("🤖 DeepSeek 多轮对话示例\n")

    session = ChatSession(
        model="deepseek-chat",
        system_prompt="你是一位专业的 Python 编程导师，擅长用简单易懂的方式解释概念。"
    )

    conversations = [
        "什么是装饰器？",
        "能给个实际例子吗？",
        "这个例子中 @log 是怎么工作的？",
        "装饰器可以带参数吗？"
    ]

    for i, question in enumerate(conversations, 1):
        print(f"\n💬 第 {i} 轮对话:")
        print(f"👤 用户: {question}")
        answer = session.send(question)
        print(f"🤖 AI: {answer}")
        print("-" * 50)

    print(f"\n📊 对话历史记录数: {len(session.messages)}")


if __name__ == "__main__":
    main()
