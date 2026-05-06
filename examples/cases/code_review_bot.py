#!/usr/bin/env python3
"""
智能代码审查机器人
自动分析代码变更，生成审查报告

使用场景:
- Git 提交前自动检查
- CI/CD 流水线集成
- 代码审查辅助
"""

import os
import subprocess
import sys
from pathlib import Path

# 添加父目录到路径，导入SDK
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from deepseek_sdk import DeepSeekClient


def get_git_diff():
    """获取当前git变更的代码"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        print("错误: 无法获取git diff，请确保在git仓库中")
        return None


def review_code(code_diff: str) -> str:
    """
    使用DeepSeek审查代码

    Args:
        code_diff: git diff输出的代码变更

    Returns:
        审查报告
    """
    client = DeepSeekClient()

    system_prompt = """你是一位资深的代码审查专家。请审查以下代码变更，关注：
1. 潜在的bug和安全问题
2. 代码风格和最佳实践
3. 性能优化建议
4. 可维护性问题

请以结构化的方式输出审查结果：
- 🔴 严重问题（必须修复）
- 🟡 建议改进（推荐修复）
- 🟢 良好实践（值得表扬）"""

    prompt = f"请审查以下代码变更:\n\n```diff\n{code_diff[:8000]}\n```"

    response = client.chat(
        message=prompt,
        system_prompt=system_prompt,
        temperature=0.3,
        max_tokens=2000
    )

    return response.content


def main():
    print("🔍 智能代码审查机器人\n")

    # 获取代码变更
    diff = get_git_diff()
    if not diff:
        print("没有检测到代码变更")
        return

    if len(diff) > 10000:
        print(f"⚠️  变更内容较多({len(diff)}字符)，只审查前8000字符")

    print("🤖 正在分析代码...\n")

    # 生成审查报告
    report = review_code(diff)

    print("=" * 60)
    print("📋 代码审查报告")
    print("=" * 60)
    print(report)
    print("=" * 60)

    # 询问是否继续提交
    response = input("\n是否继续提交? (y/n): ")
    if response.lower() != 'y':
        print("❌ 已取消提交")
        sys.exit(1)
    else:
        print("✅ 继续提交")


if __name__ == "__main__":
    main()
