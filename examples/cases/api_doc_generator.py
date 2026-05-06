#!/usr/bin/env python3
"""
API文档生成器
从Python代码自动生成API文档

使用场景:
- 自动生成项目文档
- 代码文档化
- API文档维护
"""

import ast
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from deepseek_sdk import DeepSeekClient


def extract_code_info(filepath: str) -> dict:
    """从Python文件提取代码结构信息"""
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return {"error": f"语法错误: {e}"}

    info = {
        "classes": [],
        "functions": [],
        "docstrings": []
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_info = {
                "name": node.name,
                "docstring": ast.get_docstring(node),
                "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            }
            info["classes"].append(class_info)

        elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
            func_info = {
                "name": node.name,
                "docstring": ast.get_docstring(node),
                "args": [arg.arg for arg in node.args.args]
            }
            info["functions"].append(func_info)

    return info


def generate_documentation(code_info: dict, source_code: str) -> str:
    """使用AI生成文档"""
    client = DeepSeekClient()

    system_prompt = """你是一位技术文档专家。请根据代码信息生成清晰、专业的API文档。

文档应包含:
1. 模块概述
2. 类说明（如有）
3. 函数/方法说明（参数、返回值、示例）
4. 使用示例

使用Markdown格式，包含代码高亮。"""

    content = f"""请为以下代码生成文档:

代码结构:
- 类: {len(code_info.get('classes', []))} 个
- 函数: {len(code_info.get('functions', []))} 个

详细信息:
{code_info}

源代码样例(前2000字符):
```python
{source_code[:2000]}
```
"""

    response = client.chat(
        message=content,
        system_prompt=system_prompt,
        temperature=0.3,
        max_tokens=2500
    )

    return response.content


def main():
    import argparse

    parser = argparse.ArgumentParser(description='API文档生成器')
    parser.add_argument('source', help='Python源文件路径')
    parser.add_argument('-o', '--output', help='输出文档路径')

    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"错误: 文件不存在 {args.source}")
        return

    print(f"📁 正在分析: {args.source}\n")

    # 提取代码信息
    code_info = extract_code_info(args.source)

    if "error" in code_info:
        print(f"❌ {code_info['error']}")
        return

    print(f"✅ 发现 {len(code_info['classes'])} 个类, {len(code_info['functions'])} 个函数\n")

    # 读取源代码
    with open(args.source, 'r') as f:
        source_code = f.read()

    # 生成文档
    print("🤖 正在生成文档...\n")
    documentation = generate_documentation(code_info, source_code)

    # 输出
    if args.output:
        with open(args.output, 'w') as f:
            f.write(documentation)
        print(f"✅ 文档已保存: {args.output}")
    else:
        print("=" * 60)
        print("📋 生成的文档")
        print("=" * 60)
        print(documentation)


if __name__ == "__main__":
    main()
