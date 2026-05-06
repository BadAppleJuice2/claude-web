#!/usr/bin/env python3
"""
日志分析器
自动分析服务器日志，识别错误模式和异常情况

使用场景:
- 服务器故障排查
- 日志监控告警
- 性能问题分析
"""

import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from deepseek_sdk import DeepSeekClient


def parse_log_file(filepath: str, max_lines: int = 500) -> list:
    """解析日志文件，提取错误行"""
    errors = []
    warnings = []

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f):
            if i >= max_lines:
                break

            line = line.strip()
            if not line:
                continue

            # 简单的错误检测模式
            if any(keyword in line.lower() for keyword in ['error', 'exception', 'fatal']):
                errors.append(line)
            elif any(keyword in line.lower() for keyword in ['warning', 'warn']):
                warnings.append(line)

    return errors, warnings


def analyze_logs(errors: list, warnings: list) -> str:
    """使用AI分析日志"""
    client = DeepSeekClient()

    # 统计错误类型
    error_types = Counter()
    for error in errors:
        # 提取错误类型（简化处理）
        match = re.search(r'(\w+Error|Exception)', error)
        if match:
            error_types[match.group(1)] += 1

    system_prompt = """你是一位系统运维专家。请分析以下日志内容，提供：
1. 问题的根本原因分析
2. 紧急程度评估（高/中/低）
3. 具体的修复建议
4. 预防措施"""

    # 构建分析内容
    content = f"""错误统计:
{dict(error_types)}

错误日志样例({len(errors)}条):
"""
    for i, error in enumerate(errors[:10], 1):
        content += f"{i}. {error[:200]}\n"

    if warnings:
        content += f"\n警告日志样例({len(warnings)}条):\n"
        for i, warning in enumerate(warnings[:5], 1):
            content += f"{i}. {warning[:200]}\n"

    response = client.chat(
        message=content,
        system_prompt=system_prompt,
        temperature=0.3,
        max_tokens=2000
    )

    return response.content


def main():
    import argparse

    parser = argparse.ArgumentParser(description='日志分析器')
    parser.add_argument('logfile', help='日志文件路径')
    parser.add_argument('-n', '--lines', type=int, default=500, help='分析的最大行数')

    args = parser.parse_args()

    if not os.path.exists(args.logfile):
        print(f"错误: 文件不存在 {args.logfile}")
        return

    print(f"📁 正在分析日志: {args.logfile}\n")

    # 解析日志
    errors, warnings = parse_log_file(args.logfile, args.lines)

    print(f"📊 发现 {len(errors)} 个错误, {len(warnings)} 个警告\n")

    if not errors and not warnings:
        print("✅ 日志看起来很健康！")
        return

    # AI分析
    print("🤖 正在进行智能分析...\n")
    analysis = analyze_logs(errors, warnings)

    print("=" * 60)
    print("📋 日志分析报告")
    print("=" * 60)
    print(analysis)


if __name__ == "__main__":
    main()
