#!/usr/bin/env python3
"""
DeepSeek API 代码助手示例
针对编程场景的优化调用：代码生成、解释、审查
"""

import os
import requests

API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-api-key-here")
BASE_URL = "https://api.deepseek.com"

CODE_SYSTEM_PROMPT = """你是一位资深的全栈开发工程师，擅长：
1. 编写清晰、高效、可维护的代码
2. 提供详细的代码注释和文档
3. 解释代码的设计思路和最佳实践
4. 识别潜在的问题并给出改进建议

回复格式：先给出完整代码方案，然后解释关键部分，最后提供使用示例。"""


def code_assistant(prompt: str, language: str = "python") -> str:
    """代码助手 - 针对编程任务优化"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": CODE_SYSTEM_PROMPT},
            {"role": "user", "content": f"请使用 {language} 编写代码：\n\n{prompt}"}
        ],
        "temperature": 0.3,  # 代码任务使用较低温度
        "max_tokens": 4000
    }

    response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def explain_code(code: str, language: str = "python") -> str:
    """解释代码功能和工作原理"""
    prompt = f"请详细解释以下 {language} 代码的工作原理：\n\n```{language}\n{code}\n```"
    return code_assistant(prompt, language)


def review_code(code: str, language: str = "python") -> str:
    """代码审查 - 找出问题和改进建议"""
    prompt = f"请审查以下 {language} 代码，找出潜在问题、安全风险和改进建议：\n\n```{language}\n{code}\n```"
    return code_assistant(prompt, language)


def main():
    print("🤖 DeepSeek 代码助手示例\n")

    # 示例 1: 生成代码
    print("=" * 60)
    print("示例 1: 生成代码")
    print("=" * 60)
    task = "创建一个带缓存功能的 HTTP 请求客户端，支持自动重试和错误处理"
    print(f"\n📝 任务: {task}\n")
    print(code_assistant(task, "python"))

    # 示例 2: 解释代码
    print("\n" + "=" * 60)
    print("示例 2: 解释代码")
    print("=" * 60)
    sample_code = '''
@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''
    print(f"\n📝 代码:\n{sample_code}\n")
    print(explain_code(sample_code, "python"))

    # 示例 3: 代码审查
    print("\n" + "=" * 60)
    print("示例 3: 代码审查")
    print("=" * 60)
    buggy_code = '''
def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute(query)
    return result.fetchone()
'''
    print(f"\n📝 待审查代码:\n{buggy_code}\n")
    print(review_code(buggy_code, "python"))


if __name__ == "__main__":
    main()
